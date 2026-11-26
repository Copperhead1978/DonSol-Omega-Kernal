"""Opt-in local artifact fixture gateway; no network, publishing or general tool execution."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sqlite3
import uuid
from dataclasses import dataclass
from pathlib import Path

if __package__:
    from .j58_preflight import bounded_path, canonical_bytes, load_json
    from .omega_preflight import assess
else:
    from j58_preflight import bounded_path, canonical_bytes, load_json
    from omega_preflight import assess

JOURNAL = ".omega-fixture.sqlite3"


@dataclass(frozen=True)
class FixturePermit:
    """Host-supplied scope/target/budget; never accepted from a job packet."""
    target: str
    scope_sha256: str
    max_bytes: int
    authority_ref: str


def _parent_fd(root, relative):
    """Open each write-directory component without following a symlink."""
    fd = os.open(root, os.O_RDONLY | os.O_DIRECTORY)
    try:
        for part in Path(relative).parts[:-1]:
            try:
                os.mkdir(part, dir_fd=fd)
            except FileExistsError:
                pass
            child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
            os.close(fd)
            fd = child
        return fd
    except BaseException:
        os.close(fd)
        raise


def _read(parent, name):
    fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=parent)
    with os.fdopen(fd, "rb") as stream:
        return stream.read()


def run_fixture(packet, registry, workspace_root, *, permit=None, fault_hook=None):
    """Recheck inputs, reserve once, publish without overwrite, then read back.

    Only the host can supply a FixturePermit. The caller must authenticate that
    host authority outside this local program. A packet's own authorization is
    still checked by preflight and can never supply this separate opt-in.
    """
    try:
        packet = load_json(canonical_bytes(packet))
    except (ValueError, TypeError, RecursionError) as exc:
        return {"outcome": "REFUSED_HOLD", "reason": f"Invalid JSON packet: {exc}"}
    inspection = assess(packet, registry, workspace_root)
    if inspection["status"] != "CHECKS_PASSED":
        return {"outcome": "REFUSED_HOLD", "inspection": inspection}
    db = None
    parent = None
    try:
        action = packet["action"]
        if packet["schema_version"] != 2 or packet["phase"] != "execute" or set(action) != {"kind", "target", "content"} or action["kind"] != "local_write" or not isinstance(action["content"], str):
            raise ValueError("Only a version-2 local_write text artifact fixture is implemented")
        if not isinstance(permit, FixturePermit) or not isinstance(permit.authority_ref, str) or not permit.authority_ref.strip() or type(permit.max_bytes) is not int or permit.max_bytes < 0:
            raise ValueError("A separate host FixturePermit with an explicit byte ceiling is required")
        if permit.target != action["target"] or permit.scope_sha256 != inspection["scope_sha256"]:
            raise ValueError("Host permit does not match this target and evidence/action scope")
        content = action["content"].encode("utf-8")
        if len(content) > permit.max_bytes:
            raise ValueError("Artifact exceeds the host byte ceiling")
        root = Path(workspace_root).resolve(strict=True)
        target = bounded_path(root, action["target"])
        relative = target.relative_to(root).as_posix()
        if relative == "." or relative.startswith(JOURNAL):
            raise ValueError("Artifact target is reserved for runner state")
        journal = root / JOURNAL
        if journal.is_symlink():
            raise ValueError("Runner journal cannot be a symlink")
        parent = _parent_fd(root, action["target"])
        name = Path(action["target"]).name
        digest = hashlib.sha256(content).hexdigest()
        db = sqlite3.connect(journal, timeout=30, isolation_level=None)
        db.execute("PRAGMA synchronous=FULL")
        db.execute("CREATE TABLE IF NOT EXISTS jobs (job_id TEXT PRIMARY KEY, scope TEXT NOT NULL, target TEXT UNIQUE NOT NULL, content_sha256 TEXT NOT NULL, state TEXT NOT NULL, receipt TEXT)")
        db.execute("BEGIN IMMEDIATE")
        row = db.execute("SELECT scope,target,content_sha256,state,receipt FROM jobs WHERE job_id=?", (packet["job_id"],)).fetchone()
        if row is None:
            try:
                os.stat(name, dir_fd=parent, follow_symlinks=False)
            except FileNotFoundError:
                pass
            else:
                raise ValueError("Refusing an existing artifact without this job's reservation")
            db.execute("INSERT INTO jobs VALUES (?,?,?,?,?,NULL)", (packet["job_id"], inspection["scope_sha256"], relative, digest, "reserved"))
        elif row[:3] != (inspection["scope_sha256"], relative, digest):
            raise ValueError("Job identity was already reserved for a different scope/target/content")
        db.commit()  # The reservation survives a crash before/after publication.
        if fault_hook:
            fault_hook("reserved")
        db.execute("BEGIN IMMEDIATE")  # Serialize all writers and recovery in this workspace journal.
        row = db.execute("SELECT scope,target,content_sha256,state,receipt FROM jobs WHERE job_id=?", (packet["job_id"],)).fetchone()
        try:
            existing = _read(parent, name)
        except FileNotFoundError:
            existing = None
        if row[3] == "completed":
            if existing != content:
                raise ValueError("Completed artifact is missing or changed; no overwrite permitted")
            db.commit()
            return {"outcome": "DUPLICATE_REFUSED", "receipt": json.loads(row[4]), "effect_written": False}
        recovered = existing is not None
        if recovered and existing != content:
            raise ValueError("Reserved artifact differs from expected bytes; no overwrite permitted")
        if not recovered:
            temporary = ".j58-" + uuid.uuid4().hex + ".tmp"
            fd = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=parent)
            try:
                with os.fdopen(fd, "wb") as stream:
                    stream.write(content)
                    stream.flush()
                    os.fsync(stream.fileno())
                os.link(temporary, name, src_dir_fd=parent, dst_dir_fd=parent, follow_symlinks=False)
                os.fsync(parent)
            finally:
                os.unlink(temporary, dir_fd=parent)
            if fault_hook:
                fault_hook("published")
        if _read(parent, name) != content:
            raise ValueError("Artifact readback mismatch")
        receipt = {"job_id": packet["job_id"], "scope_sha256": inspection["scope_sha256"], "target": relative,
                   "sha256": digest, "bytes": len(content), "readback_verified": True,
                   "recovered": recovered, "authority_ref": permit.authority_ref,
                   "scope": "One local artifact fixture; host authority and evidence meaning are external checks."}
        db.execute("UPDATE jobs SET state='completed',receipt=? WHERE job_id=?", (json.dumps(receipt, sort_keys=True), packet["job_id"]))
        db.commit()
        return {"outcome": "COMPLETED", "receipt": receipt, "effect_written": not recovered}
    except (OSError, ValueError, TypeError, KeyError, sqlite3.Error) as exc:
        if db is not None and db.in_transaction:
            db.rollback()
        return {"outcome": "REFUSED_HOLD", "reason": str(exc), "inspection": inspection}
    finally:
        if db is not None:
            db.close()
        if parent is not None:
            os.close(parent)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packet", type=Path)
    parser.add_argument("--workspace-root", type=Path, required=True)
    parser.add_argument("--allow-local-fixture-write", action="store_true", help="Host opt-in; does not authorize production tools")
    parser.add_argument("--max-bytes", type=int, help="Explicit local artifact byte ceiling")
    args = parser.parse_args()
    try:
        packet = load_json(args.packet.read_bytes())
        registry = load_json((Path(__file__).resolve().parents[1] / "capabilities.json").read_bytes())
        inspection = assess(packet, registry, args.workspace_root)
        permit = None
        if args.allow_local_fixture_write and args.max_bytes is not None and inspection["status"] == "CHECKS_PASSED":
            permit = FixturePermit(packet["action"]["target"], inspection["scope_sha256"], args.max_bytes, "Explicit CLI local-fixture opt-in")
        result = run_fixture(packet, registry, args.workspace_root, permit=permit)
    except (OSError, ValueError, TypeError, KeyError, RecursionError) as exc:
        result = {"outcome": "REFUSED_HOLD", "reason": str(exc)}
    print(json.dumps(result, indent=2))
    return 0 if result["outcome"] == "COMPLETED" else 4 if result["outcome"] == "DUPLICATE_REFUSED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
