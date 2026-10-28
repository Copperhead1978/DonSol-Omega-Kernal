#!/usr/bin/env python3
"""Check this instruction mirror's local integrity; never grade model efficacy."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit


def validate(root: Path) -> list[str]:
    errors: list[str] = []

    def require(condition: bool, message: str) -> None:
        if not condition:
            errors.append(message)

    manifest_path = root / "manifest.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return [f"Cannot read manifest: {exc}"]

    require(manifest.get("schema_version") == 1, "Unsupported manifest schema")
    edition = manifest.get("edition")
    require(edition == "2026.10.28", "Unexpected repository edition")
    try:
        require((root / "VERSION").read_text().strip() == edition, "VERSION differs from manifest")
    except OSError:
        errors.append("Missing VERSION")

    def checked_path(relative: str) -> Path | None:
        if not isinstance(relative, str) or not relative:
            errors.append("Manifest contains an invalid path")
            return None
        path = (root / relative).resolve()
        if not path.is_relative_to(root.resolve()):
            errors.append(f"Path leaves repository: {relative}")
            return None
        require(path.is_file(), f"Missing file: {relative}")
        return path if path.is_file() else None

    components = manifest.get("components", [])
    require(bool(components), "No component versions declared")
    require(len({c["id"] for c in components}) == len(components), "Duplicate component ID")
    for component in components:
        require(bool(component.get("version")), f"Missing version: {component.get('id')}")
        checked_path(component.get("path", ""))

    exports = manifest.get("source_exports", [])
    require(len(exports) == 4, "Expected four complete recovered text exports")
    require(len({e["path"] for e in exports}) == len(exports), "Duplicate source export")
    for export in exports:
        path = checked_path(export.get("path", ""))
        if path:
            data = path.read_bytes()
            require(hashlib.sha256(data).hexdigest() == export.get("sha256"),
                    f"Source hash changed: {export['path']}")
            require(len(data) == export.get("size_bytes"), f"Source size changed: {export['path']}")

    current = checked_path(manifest.get("instructions", {}).get("full", ""))
    compact = checked_path(manifest.get("instructions", {}).get("compact", ""))
    light = checked_path(manifest.get("instructions", {}).get("light", ""))
    if current and compact and light:
        ctext = compact.read_text(encoding="utf-8")
        require(len(ctext) <= 4000, f"Compact boot is {len(ctext)} characters; ceiling is 4000")
        for path in (current, compact, light):
            text = path.read_text(encoding="utf-8")
            for token in ("MIRRORPULSE", "ANDREWPULSE", "SOLVIAN", "CUTGLYPH", "FIELDSMITH", "BRIDGENODE",
                          "UNKNOWN", "L0", "L1", "L2", "L3", "L4", "[T]", "[V]", "[I]", "[P]", "[F]"):
                require(token in text, f"Missing {token} in {path.relative_to(root)}")

    profile = manifest.get("tag_profiles", {}).get("current-v9.1", {})
    require(profile.get("V") == "verified_by_named_traceable_source", "Current V profile drift")
    require(profile.get("F") == "falsified", "Current F profile drift")
    coverage = manifest.get("coverage", {})
    require(coverage.get("complete_october_transcript") == "not_recovered", "Transcript coverage overclaim")
    require(coverage.get("runtime_implementation") == "not_supplied", "Runtime status overclaim")

    conflict_path = checked_path("docs/versions-and-conflicts.md")
    if conflict_path:
        conflict_text = conflict_path.read_text(encoding="utf-8")
        for cid in manifest.get("open_conflicts", []):
            require(cid in conflict_text, f"Missing declared conflict: {cid}")
    require(len(manifest.get("open_conflicts", [])) == 13, "Conflict register coverage changed")

    for relative in manifest.get("removed_baseline_paths", []):
        require(not (root / relative).exists(), f"Obsolete active file remains: {relative}")

    public_files = [p for p in root.rglob("*") if p.is_file()
                    and ".git" not in p.relative_to(root).parts
                    and "__pycache__" not in p.relative_to(root).parts]
    for path in public_files:
        relative = path.relative_to(root)
        require(path.suffix.lower() not in {".pdf", ".mhtml"}, f"Obsolete binary material remains: {relative}")
        if path.suffix in {".md", ".txt", ".json"}:
            text = path.read_text(encoding="utf-8")
            for marker in ("libfile_", "sediment://", "sandbox:/", "/workspace/scratch/", "BEGIN PRIVATE KEY"):
                require(marker not in text, f"Private/source transport marker in public text: {relative}")
            if "sources" not in relative.parts:
                require(not re.search(r"\+(?:280|764|147)%|\+∞%", text),
                        f"Obsolete numerical performance claim in current text: {relative}")

    # Historical source exports may contain old reference syntax and context.
    # Validate local links in authored current documents without rewriting sources.
    for path in root.rglob("*.md"):
        if any(part in {".git", "sources"} for part in path.relative_to(root).parts):
            continue
        text = path.read_text(encoding="utf-8")
        for target in re.findall(r"\[[^\]\n]*\]\(([^)\n]+)\)", text):
            target = target.strip().strip("<>")
            split = urlsplit(target)
            if split.scheme or split.netloc or not split.path:
                continue
            linked = (path.parent / unquote(split.path)).resolve()
            require(linked.is_relative_to(root.resolve()), f"Link leaves repository: {path.name}: {target}")
            require(linked.exists(), f"Broken local link: {path.relative_to(root)} -> {target}")

    return errors


if __name__ == "__main__":
    repository = Path(__file__).resolve().parents[1]
    problems = validate(repository)
    if problems:
        for problem in problems:
            print(f"FAIL: {problem}", file=sys.stderr)
        sys.exit(1)
    print("PASS: versions, source export hashes/sizes, local links, instruction limits, profiles, coverage, and conflicts")
    print("Scope: local repository integrity only; no model, scientific, external-link, or playback validation")
