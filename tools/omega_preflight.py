#!/usr/bin/env python3
"""Inspect a declared job packet. No execution, network, authorization or truth oracle."""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path


def assess(packet: object, registry: object) -> dict:
    blockers: list[str] = []
    warnings: list[str] = []

    def finish() -> dict:
        return {
            "status": "HOLD" if blockers else "PLAN_ONLY" if phase == "plan" else "CHECKS_PASSED",
            "blockers": blockers,
            "warnings": warnings,
            "scope": "Declared record checks only; no action executed, evidence authenticated, or permission granted.",
        }

    phase = None
    if not isinstance(packet, dict) or not isinstance(registry, dict):
        blockers.append("Packet and capability registry must be JSON objects.")
        return finish()
    phase = packet.get("phase")
    if packet.get("schema_version") != 1 or registry.get("schema_version") != 1:
        blockers.append("Unsupported packet or registry schema.")
    if not isinstance(phase, str) or phase not in {"plan", "execute"}:
        blockers.append("Phase must be plan or execute.")
    for field in ("job_id", "goal", "verification_plan"):
        if not isinstance(packet.get(field), str) or not packet[field].strip():
            blockers.append(f"Missing nonempty {field}.")
    criteria = packet.get("acceptance_criteria")
    if not isinstance(criteria, list) or not criteria or any(not isinstance(x, str) or not x.strip() for x in criteria):
        blockers.append("Acceptance criteria must be a nonempty list of nonempty strings.")

    def prerequisite(message: str) -> None:
        (warnings if phase == "plan" else blockers).append(message)

    caps = registry.get("capabilities")
    if not isinstance(caps, list) or any(not isinstance(c, dict) or not isinstance(c.get("id"), str) for c in caps):
        blockers.append("Malformed capability registry.")
        return finish()
    indexed = {c["id"]: c for c in caps}
    if len(indexed) != len(caps):
        blockers.append("Duplicate capability IDs in registry.")
    selected = packet.get("capability_ids")
    if not isinstance(selected, list) or not selected or any(not isinstance(x, str) for x in selected):
        blockers.append("Select at least one capability ID.")
        selected = []
    environment = packet.get("environment")
    if not isinstance(environment, dict):
        environment = {}
    try:
        observed = datetime.fromisoformat(environment.get("observed_at", "").replace("Z", "+00:00"))
        if observed.utcoffset() is None:
            raise ValueError("timezone required")
    except (ValueError, TypeError, AttributeError):
        prerequisite("Record a timezone-aware environment observation time; refresh changeable state before acting.")
    tools = environment.get("tools")
    if not isinstance(tools, dict):
        tools = {}
    for cid in sorted(set(selected)):
        capability = indexed.get(cid)
        if not capability:
            blockers.append(f"Unknown capability: {cid}")
            continue
        status = capability.get("status")
        if not isinstance(status, str) or status not in {"documented", "implemented_local"}:
            prerequisite(f"Capability is not supplied for execution: {cid}")
        elif capability["status"] == "documented":
            warnings.append(f"{cid} is a documented method, not an installed executor.")
        required = capability.get("required_tools")
        if not isinstance(required, list) or any(not isinstance(t, str) for t in required):
            blockers.append(f"Malformed tool requirements: {cid}")
            continue
        for tool in required:
            observation = tools.get(tool)
            if not isinstance(observation, dict) or observation.get("available") is not True or not isinstance(observation.get("basis"), str) or not observation["basis"].strip():
                prerequisite(f"Missing observed tool binding: {tool} (for {cid})")

    action = packet.get("action")
    if not isinstance(action, dict):
        action = {}
    kind = action.get("kind")
    target = action.get("target")
    if not isinstance(kind, str) or kind not in {"read", "local_write", "external_write"} or not isinstance(target, str) or not target.strip():
        blockers.append("Action needs a supported kind and explicit target.")
    if isinstance(kind, str) and kind in {"local_write", "external_write"}:
        auth = packet.get("authorization")
        if not isinstance(auth, dict) or auth.get("granted") is not True or auth.get("action_kind") != kind or auth.get("target") != target or not isinstance(auth.get("basis"), str) or not auth["basis"].strip():
            prerequisite("No matching recorded authorization for this action and target; reuse existing authorization when it covers them.")
        if not isinstance(packet.get("recovery_plan"), str) or not packet["recovery_plan"].strip():
            prerequisite("Record a recovery plan for the write action, including irreversible limits where applicable.")

    claims = packet.get("claims")
    inputs = packet.get("decision_inputs")
    if not isinstance(claims, list) or any(not isinstance(c, dict) or not isinstance(c.get("id"), str) or not c["id"] for c in claims):
        blockers.append("Claims must be a list of records with nonempty IDs.")
        return finish()
    if not isinstance(inputs, list) or any(not isinstance(i, str) for i in inputs):
        blockers.append("Decision inputs must be a list of claim IDs.")
        return finish()
    by_id = {c["id"]: c for c in claims}
    if len(by_id) != len(claims):
        blockers.append("Duplicate claim IDs.")
    malformed = False
    for claim in claims:
        cid = claim["id"]
        tag, state = claim.get("tag"), claim.get("state")
        if not isinstance(tag, str) or tag not in {"T", "V", "I", "P", "F", "UNKNOWN"} or not isinstance(state, str) or state not in {"active", "dirty", "quarantined"}:
            blockers.append(f"Invalid current-v9.1 tag or record state: {cid}")
        parents = claim.get("depends_on")
        if not isinstance(parents, list) or any(not isinstance(x, str) for x in parents):
            blockers.append(f"Invalid dependency list: {cid}")
            malformed = True
            continue
        for parent in parents:
            if parent not in by_id:
                blockers.append(f"Missing dependency: {cid} -> {parent}")
        if isinstance(tag, str) and tag in {"T", "V", "I"} and (not isinstance(claim.get("basis"), str) or not claim["basis"].strip()):
            blockers.append(f"Claim lacks a recorded basis: {cid}")
        if claim.get("tag") == "I" and not parents:
            blockers.append(f"Inference lacks declared supporting claims: {cid}")
    if malformed:
        return finish()

    # Inspect explicit local ancestry only. This is not the unresolved v8.1
    # T-scale arithmetic, DIRTY propagation rule, or a persistent cascade service.
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(cid: str) -> None:
        if cid in visiting:
            blockers.append(f"Dependency cycle at {cid}")
            return
        if cid in visited or cid not in by_id:
            return
        visiting.add(cid)
        for parent in by_id[cid]["depends_on"]:
            visit(parent)
        visiting.remove(cid)
        visited.add(cid)

    for cid in by_id:
        visit(cid)
    pending = list(inputs)
    checked: set[str] = set()
    while pending:
        cid = pending.pop()
        if cid in checked:
            continue
        checked.add(cid)
        claim = by_id.get(cid)
        if claim is None:
            blockers.append(f"Missing decision input: {cid}")
            continue
        tag = claim.get("tag")
        if not isinstance(tag, str) or tag not in {"T", "V", "I"} or claim.get("state") != "active":
            prerequisite(f"Unsettled decision input or ancestor: {cid}")
        pending.extend(claim["depends_on"])
    warnings.append("Tool inventory, claim tags, sources and authorization are caller declarations; their truth and current validity require separate checks.")
    return finish()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packet", type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    try:
        result = assess(json.loads(args.packet.read_text(encoding="utf-8")),
                        json.loads((root / "capabilities.json").read_text(encoding="utf-8")))
    except (OSError, ValueError, RecursionError) as exc:
        print(json.dumps({"status": "HOLD", "blockers": [f"Cannot inspect packet: {exc}"]}, indent=2))
        return 1
    print(json.dumps(result, indent=2))
    return int(result["status"] == "HOLD")


if __name__ == "__main__":
    raise SystemExit(main())
