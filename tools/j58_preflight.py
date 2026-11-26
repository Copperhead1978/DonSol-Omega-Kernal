"""J58 draft-2 local record/byte checks. No network, source truth or authentication."""
from __future__ import annotations

import hashlib
import json
import math
import re
from datetime import datetime
from pathlib import Path, PureWindowsPath

LENSES = {"ATHENS", "FIRST_PRINCIPLES", "BENCH_PROOF", "ENDURANCE_FIXTURE", "JUNG_PSYCHOLOGY"}
SCOPE_FIELDS = ("job_id", "goal", "capability_ids", "action", "claims", "decision_inputs", "acceptance_criteria", "verification_plan")


def _fail(message):
    raise ValueError(message)


def _object_pairs(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            _fail(f"Duplicate JSON key: {key}")
        out[key] = value
    return out


def load_json(data):
    value = json.loads(data, object_pairs_hook=_object_pairs,
                       parse_constant=lambda value: _fail(f"Non-finite JSON number: {value}"))
    _finite(value)
    return value


def canonical_bytes(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def scope_sha256(packet):
    """The exact named serialization profile in the pinned draft-2 specification."""
    value = {k: packet[k] for k in SCOPE_FIELDS}
    value["recovery_plan"] = packet.get("recovery_plan")
    value["input_artifacts"] = packet["j58"]["input_artifacts"]
    value["reference_authors"] = packet["j58"]["reference_authors"]
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def _shape(value, required, optional=()):
    if not isinstance(value, dict) or set(value) - set(required) - set(optional) or set(required) - set(value):
        _fail(f"Malformed closed record; required keys: {', '.join(required)}")


def _text(value):
    if not isinstance(value, str) or not value.strip():
        _fail("Expected nonempty text")


def _digest(value):
    if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value):
        _fail("Expected lowercase SHA-256")


def _texts(value, nonempty=False, unique=False):
    if not isinstance(value, list) or (nonempty and not value):
        _fail("Expected a list of text values")
    for item in value:
        _text(item)
    if unique and len(set(value)) != len(value):
        _fail("Duplicate list item")


def _stamp(value):
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}[Tt]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:[Zz]|[+-]\d{2}:\d{2})", value):
        _fail("checked_at must be a timezone-aware RFC3339 timestamp")
    parsed = datetime.fromisoformat(value.upper().replace("Z", "+00:00"))
    if parsed.utcoffset() is None:
        _fail("Timestamp has no timezone")


def _finite(value):
    if value is not None and type(value) not in (dict, list, str, int, float, bool):
        _fail("Value is not a JSON data type")
    if isinstance(value, float) and not math.isfinite(value):
        _fail("Non-finite number in input record")
    if isinstance(value, dict):
        for key, child in value.items():
            if not isinstance(key, str):
                _fail("JSON object keys must be strings")
            _finite(child)
    elif isinstance(value, list):
        for child in value:
            _finite(child)


def bounded_path(root, relative):
    _text(relative)
    path = Path(relative)
    win = PureWindowsPath(relative)
    if path.is_absolute() or win.is_absolute() or win.drive or ".." in path.parts or "\\" in relative:
        _fail(f"Path must be relative without traversal: {relative}")
    resolved = (root / path).resolve()
    if not resolved.is_relative_to(root):
        _fail(f"Path escapes workspace: {relative}")
    return resolved


class Evidence:
    def __init__(self, root):
        if root is None:
            _fail("Version 2 requires an explicit workspace root")
        self.root = Path(root).resolve(strict=True)
        if not self.root.is_dir():
            _fail("Workspace root is not a directory")
        self.inputs = {}
        self.input_paths = set()

    def read(self, ref):
        _shape(ref, ("path", "sha256"), ("sync_id",))
        _digest(ref["sha256"])
        if "sync_id" in ref:
            _text(ref["sync_id"])
        path = bounded_path(self.root, ref["path"])
        if not path.is_file():
            _fail(f"Missing evidence file: {ref['path']}")
        data = path.read_bytes()
        if hashlib.sha256(data).hexdigest() != ref["sha256"]:
            _fail(f"Evidence byte digest mismatch: {ref['path']}")
        if path.suffix.lower() == ".json":
            load_json(data)
        return path, data

    def record(self, ref):
        return load_json(self.read(ref)[1])

    def add_inputs(self, refs):
        if not isinstance(refs, list):
            _fail("input_artifacts must be a list")
        for ref in refs:
            path, data = self.read(ref)
            if ref["path"] in self.inputs or path in self.input_paths:
                _fail(f"Duplicate or aliased input path: {ref['path']}")
            self.inputs[ref["path"]] = (ref["sha256"], data)
            self.input_paths.add(path)

    def member(self, ref):
        _, data = self.read(ref)
        if ref["path"] not in self.inputs or self.inputs[ref["path"]][0] != ref["sha256"]:
            _fail(f"Evidence reference absent from declared inputs: {ref['path']}")
        return data


def _closure(packet):
    by_id = {c["id"]: c for c in packet["claims"]}
    seen, pending = set(), list(packet["decision_inputs"])
    while pending:
        key = pending.pop()
        if key in seen:
            continue
        seen.add(key)
        claim = by_id[key]
        if claim["state"] != "active" or claim["tag"] not in {"T", "V", "I"}:
            _fail(f"Unsettled decision closure: {key}")
        pending.extend(claim["depends_on"])
    for key in seen:
        if by_id[key]["tag"] != "I":
            continue
        support, todo = set(), list(by_id[key]["depends_on"])
        while todo:
            parent = todo.pop()
            if parent in support:
                continue
            support.add(parent)
            todo.extend(by_id[parent]["depends_on"])
        if not any(by_id[p]["tag"] in {"T", "V"} for p in support):
            _fail(f"Inference has no factual support: {key}")
    return by_id, seen


def _baseline(value, packet, scope, evidence, must_pass):
    _shape(value, ("schema_version", "record_type", "baseline_id", "job_id", "FLIGHT_REGIME", "scope_sha256", "claim_checks", "recheck_on", "result"))
    if type(value["schema_version"]) is not int or value["schema_version"] != 1 or value["record_type"] != "TURBOJET_BASELINE" or value["FLIGHT_REGIME"] != "TURBOJET":
        _fail("Invalid baseline type/version/regime")
    _text(value["baseline_id"])
    _digest(value["scope_sha256"])
    _texts(value["recheck_on"], nonempty=True)
    if value["job_id"] != packet["job_id"] or value["scope_sha256"] != scope:
        _fail("Baseline job/scope mismatch")
    if value["result"] not in ("passed", "hold") or (must_pass and value["result"] != "passed"):
        _fail("Baseline is not passed")
    checks = value["claim_checks"]
    if not isinstance(checks, list):
        _fail("claim_checks must be a list")
    ids = []
    for check in checks:
        _shape(check, ("claim_id", "source", "independent_proof", "dependency_check", "checked_by", "checked_at", "result"))
        _text(check["claim_id"])
        _text(check["checked_by"])
        _stamp(check["checked_at"])
        source = evidence.member(check["source"])
        proof = evidence.member(check["independent_proof"])
        evidence.member(check["dependency_check"])
        if source == proof:
            _fail("Source and independent proof have identical bytes")
        if check["result"] not in ("passed", "hold") or (must_pass and check["result"] != "passed"):
            _fail("Claim check is not passed")
        ids.append(check["claim_id"])
    if len(ids) != len(set(ids)):
        _fail("Duplicate baseline claim check")
    if must_pass:
        by_id, closure = _closure(packet)
        expected = {key for key in closure if by_id[key]["tag"] in {"T", "V"}}
        if set(ids) != expected:
            _fail("Baseline claim checks must cover exactly the factual decision closure")


def _transition(value, packet, scope, evidence, baseline_ref, must_pass):
    _shape(value, ("schema_version", "record_type", "job_id", "scope_sha256", "baseline_sha256", "factual_claim_ids", "hypothesis_claim_ids", "auditor_filing", "chair_filing", "result"))
    if type(value["schema_version"]) is not int or value["schema_version"] != 1 or value["record_type"] != "INLET_SPIKE_LOCK":
        _fail("Invalid transition type/version")
    _digest(value["scope_sha256"])
    _digest(value["baseline_sha256"])
    if not baseline_ref or value["job_id"] != packet["job_id"] or value["scope_sha256"] != scope or value["baseline_sha256"] != baseline_ref["sha256"]:
        _fail("Transition job/scope/baseline mismatch")
    for key in ("factual_claim_ids", "hypothesis_claim_ids"):
        _texts(value[key], unique=True)
    if value["result"] not in ("passed", "hold") or (must_pass and value["result"] != "passed"):
        _fail("Transition is not passed")
    audit_path, audit = evidence.read(value["auditor_filing"])
    chair_path, chair = evidence.read(value["chair_filing"])
    if audit_path == chair_path or audit == chair:
        _fail("Auditor and Chair filings must be distinct pinned files and bytes")
    if must_pass:
        by_id, closure = _closure(packet)
        if set(value["factual_claim_ids"]) != closure or set(value["hypothesis_claim_ids"]) != {c["id"] for c in packet["claims"] if c["tag"] == "P"} or set(value["hypothesis_claim_ids"]) & closure:
            _fail("Transition factual/hypothesis partitions do not match the packet")


def assess_v2(packet, registry, base_assess, workspace_root):
    normalized = dict(packet, schema_version=1)
    try:
        result = base_assess(normalized, registry)
    except (ValueError, TypeError, KeyError, AttributeError, RecursionError) as exc:
        result = {"status": "HOLD", "blockers": [f"Base record check failed: {exc}"], "warnings": [],
                  "scope": "Declared record checks only; no action executed, evidence authenticated, or permission granted."}
    try:
        _finite(packet)
        _finite(registry)
        if packet.get("FLIGHT_REGIME") not in ("TURBOJET", "INLET_SPIKE", "TURBORAMJET"):
            _fail("Missing or unknown FLIGHT_REGIME")
        extension = packet.get("j58")
        _shape(extension, ("lenses", "reference_authors", "input_artifacts", "baseline", "transition"))
        _texts(extension["lenses"], unique=True)
        if set(extension["lenses"]) - LENSES:
            _fail("Unknown lens ID")
        evidence = Evidence(workspace_root)
        evidence.add_inputs(extension["input_artifacts"])
        authors = extension["reference_authors"]
        if not isinstance(authors, list):
            _fail("reference_authors must be a list")
        author_ids = []
        for author in authors:
            _shape(author, ("author_id", "sources"))
            if not isinstance(author["author_id"], str) or not re.fullmatch(r"[A-Z][A-Z0-9_]*", author["author_id"]):
                _fail("Malformed author ID")
            if not isinstance(author["sources"], list) or not author["sources"]:
                _fail("A mounted author needs source references")
            for ref in author["sources"]:
                evidence.member(ref)
            author_ids.append(author["author_id"])
        if len(set(author_ids)) != len(author_ids):
            _fail("Duplicate author ID")
        scope = scope_sha256(packet)
        regime = packet["FLIGHT_REGIME"]
        baseline_ref, transition_ref = extension["baseline"], extension["transition"]
        if regime != "TURBOJET" and baseline_ref is None:
            _fail("Transition/cruise requires a baseline")
        if regime == "TURBORAMJET" and transition_ref is None:
            _fail("Cruise requires a transition boundary")
        baseline = None
        if baseline_ref is not None:
            baseline = evidence.record(baseline_ref)
            _baseline(baseline, packet, scope, evidence, regime != "TURBOJET" or baseline.get("result") == "passed")
        if transition_ref is not None:
            transition = evidence.record(transition_ref)
            if transition.get("result") == "passed" and (baseline is None or baseline.get("result") != "passed"):
                _fail("A passed boundary requires a passed baseline")
            _transition(transition, packet, scope, evidence, baseline_ref, regime == "TURBORAMJET" or transition.get("result") == "passed")
        result["scope_sha256"] = scope
        result["warnings"].append("Byte identity and record consistency do not authenticate reviewers, prove independence/truth, or observe task-specific freshness conditions.")
    except (ValueError, OSError, TypeError, KeyError, AttributeError, RecursionError, RuntimeError) as exc:
        result["blockers"].append(f"J58: {exc}")
    if result["blockers"]:
        result["status"] = "HOLD"
    return result
