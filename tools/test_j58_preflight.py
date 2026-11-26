"""Behavioral acceptance checks against pinned draft-2 requirements, using synthetic local bytes."""
import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from omega_preflight import assess
from j58_preflight import canonical_bytes, load_json, scope_sha256
from test_omega_preflight import REGISTRY, valid_packet


class J58Tests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.packet = valid_packet()
        self.packet.update(schema_version=2, FLIGHT_REGIME="TURBOJET", j58={
            "lenses": [], "reference_authors": [], "input_artifacts": [], "baseline": None, "transition": None})
        self.source = self.file("source.txt", b"Synthetic source measurement: 2")
        self.proof = self.file("proof.txt", b"Separate synthetic test: 1 + 1 = 2")
        self.dependency = self.file("dependency.txt", b"Synthetic dependency review")
        self.audit = self.file("audit.txt", b"Synthetic auditor boundary")
        self.chair = self.file("chair.txt", b"Synthetic chair boundary")
        self.packet["j58"]["input_artifacts"] = [self.source, self.proof, self.dependency]

    def file(self, name, data):
        if isinstance(data, dict):
            data = canonical_bytes(data)
        (self.root / name).write_bytes(data)
        return {"path": name, "sha256": hashlib.sha256(data).hexdigest()}

    def baseline(self, packet=None, **changes):
        p = packet or self.packet
        value = {"schema_version": 1, "record_type": "TURBOJET_BASELINE", "baseline_id": "synthetic-baseline",
                 "job_id": p["job_id"], "FLIGHT_REGIME": "TURBOJET", "scope_sha256": scope_sha256(p),
                 "claim_checks": [{"claim_id": "measurement", "source": self.source, "independent_proof": self.proof,
                                   "dependency_check": self.dependency, "checked_by": "synthetic fixture",
                                   "checked_at": "2026-11-26T12:00:00Z", "result": "passed"}],
                 "recheck_on": ["Source, dependencies or job scope change; externally observe any freshness trigger"],
                 "result": "passed"}
        value.update(changes)
        p["j58"]["baseline"] = self.file("baseline.json", value)
        return value

    def boundary(self, packet=None, **changes):
        p = packet or self.packet
        value = {"schema_version": 1, "record_type": "INLET_SPIKE_LOCK", "job_id": p["job_id"],
                 "scope_sha256": scope_sha256(p), "baseline_sha256": p["j58"]["baseline"]["sha256"],
                 "factual_claim_ids": ["measurement"], "hypothesis_claim_ids": [],
                 "auditor_filing": self.audit, "chair_filing": self.chair, "result": "passed"}
        value.update(changes)
        p["j58"]["transition"] = self.file("boundary.json", value)
        return value

    def inspect(self, packet=None):
        return assess(packet or self.packet, REGISTRY, self.root)

    def held(self, packet=None):
        self.assertEqual(self.inspect(packet)["status"], "HOLD")

    def test_legacy_packet_preserves_behavior_and_rejects_reserved_fields(self):
        p = valid_packet()
        self.assertEqual(assess(p, REGISTRY)["status"], "CHECKS_PASSED")
        for key in ("FLIGHT_REGIME", "j58"):
            changed = dict(p, **{key: None})
            self.assertEqual(assess(changed, REGISTRY)["status"], "HOLD")

    def test_explicit_root_and_regime_are_required(self):
        self.assertEqual(assess(self.packet, REGISTRY)["status"], "HOLD")
        for regime in (None, "UNKNOWN", [], True):
            self.packet["FLIGHT_REGIME"] = regime
            self.held()

    def test_schema_is_closed_and_lenses_are_checked(self):
        for change in ({"extra": 1}, {"lenses": ["UNKNOWN"]}, {"lenses": ["ATHENS", "ATHENS"]}, {"lenses": "ATHENS"}):
            p = copy.deepcopy(self.packet)
            p["j58"].update(change)
            self.held(p)
        p = copy.deepcopy(self.packet)
        del p["j58"]["baseline"]
        self.held(p)

    def test_transition_and_cruise_require_actual_prerequisites_even_in_plan(self):
        for regime in ("INLET_SPIKE", "TURBORAMJET"):
            p = copy.deepcopy(self.packet)
            p.update(phase="plan", FLIGHT_REGIME=regime)
            self.held(p)
        self.packet["FLIGHT_REGIME"] = "INLET_SPIKE"
        self.baseline()
        self.assertEqual(self.inspect()["status"], "CHECKS_PASSED")
        self.packet["FLIGHT_REGIME"] = "TURBORAMJET"
        self.held()
        self.boundary()
        self.assertEqual(self.inspect()["status"], "CHECKS_PASSED")

    def test_all_references_have_real_bytes_and_optional_records_are_checked(self):
        for change in ({"path": "missing"}, {"sha256": "0" * 64}, {"sync_id": ""}, {"extra": 1}):
            p = copy.deepcopy(self.packet)
            p["j58"]["input_artifacts"][0].update(change)
            self.held(p)
        self.packet["j58"]["baseline"] = self.file("bad.json", b"[]")
        self.held()

    def test_traversal_absolute_windows_and_symlink_escape_hold(self):
        for path in ("../source.txt", "/tmp/source.txt", "x/../source.txt", "C:\\source.txt", "\\\\server\\share"):
            p = copy.deepcopy(self.packet)
            p["j58"]["input_artifacts"][0]["path"] = path
            self.held(p)
        with tempfile.TemporaryDirectory() as outside:
            q = Path(outside) / "external"
            q.write_bytes(b"x")
            (self.root / "escape").symlink_to(q)
            self.packet["j58"]["input_artifacts"] = [{"path": "escape", "sha256": hashlib.sha256(b"x").hexdigest()}]
            self.held()

    def test_duplicate_paths_and_aliases_hold(self):
        p = copy.deepcopy(self.packet)
        p["j58"]["input_artifacts"].append(dict(self.source))
        self.held(p)
        (self.root / "alias").symlink_to(self.root / "source.txt")
        self.packet["j58"]["input_artifacts"].append(dict(self.source, path="alias"))
        self.held()

    def test_duplicate_keys_nonfinite_numbers_and_non_json_values_reject(self):
        for text in ('{"x":1,"x":2}', '{"x": NaN}', '{"x": Infinity}', '{"x": 1e999}'):
            with self.assertRaises(ValueError):
                load_json(text)
        for value in (float("nan"), float("inf"), {1, 2}):
            p = copy.deepcopy(self.packet)
            p["unused"] = value
            self.held(p)
        self.packet["j58"]["input_artifacts"] = [self.file("source.json", b'{"x":1,"x":2}')]
        self.held()

    def test_scope_matches_named_profile_and_preserves_array_order(self):
        p = self.packet
        value = {key: p[key] for key in ("job_id", "goal", "capability_ids", "action", "claims", "decision_inputs", "acceptance_criteria", "verification_plan")}
        value.update(recovery_plan=None, input_artifacts=p["j58"]["input_artifacts"], reference_authors=[])
        expected = hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()).hexdigest()
        self.assertEqual(scope_sha256(p), expected)
        p["j58"]["input_artifacts"].reverse()
        self.assertNotEqual(scope_sha256(p), expected)

    def test_scope_changes_hold_existing_evidence_but_phase_auth_and_tools_recheck(self):
        self.packet["FLIGHT_REGIME"] = "TURBORAMJET"
        self.baseline()
        self.boundary()
        for key, value in (("goal", "changed"), ("acceptance_criteria", ["changed"]), ("verification_plan", "changed")):
            p = copy.deepcopy(self.packet)
            p[key] = value
            self.held(p)
        p = copy.deepcopy(self.packet)
        p["environment"]["tools"]["local_execution"]["available"] = False
        self.held(p)
        self.packet["phase"] = "plan"
        self.assertEqual(self.inspect()["status"], "PLAN_ONLY")

    def test_changed_source_bytes_and_changed_claim_support_hold(self):
        self.packet["FLIGHT_REGIME"] = "INLET_SPIKE"
        self.baseline()
        (self.root / "source.txt").write_bytes(b"Changed measurement")
        self.held()

    def test_baseline_job_scope_result_and_extra_fields_hold(self):
        self.packet["FLIGHT_REGIME"] = "INLET_SPIKE"
        for change in ({"job_id": "other"}, {"scope_sha256": "0" * 64}, {"result": "hold"}, {"extra": 1}, {"schema_version": True}):
            self.baseline(**change)
            self.held()

    def test_missing_duplicate_extra_and_held_claim_checks_hold(self):
        self.packet["FLIGHT_REGIME"] = "INLET_SPIKE"
        original = self.baseline()["claim_checks"][0]
        for checks in ([], [original, original], [dict(original, claim_id="other")], [dict(original, result="hold")]):
            self.baseline(claim_checks=checks)
            self.held()

    def test_proof_membership_and_identical_bytes_hold(self):
        self.packet["FLIGHT_REGIME"] = "INLET_SPIKE"
        check = self.baseline()["claim_checks"][0]
        check["independent_proof"] = self.file("same-proof", (self.root / "source.txt").read_bytes())
        self.packet["j58"]["input_artifacts"].append(check["independent_proof"])
        self.baseline(claim_checks=[check])
        self.held()
        check["independent_proof"] = self.file("unlisted", b"Another proof")
        self.baseline(claim_checks=[check])
        self.held()

    def test_bad_timestamps_hold(self):
        self.packet["FLIGHT_REGIME"] = "INLET_SPIKE"
        for stamp in ("2026-11-26", "2026-11-26T12:00:00", "2026-99-26T12:00:00Z", "2026-11-26T12:00Z"):
            check = self.baseline()["claim_checks"][0]
            check["checked_at"] = stamp
            self.baseline(claim_checks=[check])
            self.held()

    def test_dependency_closure_requires_checked_factual_support(self):
        self.packet["claims"].append({"id": "derived", "tag": "I", "state": "active", "basis": "Synthetic inference", "depends_on": ["measurement"]})
        self.packet["decision_inputs"] = ["derived"]
        self.packet["FLIGHT_REGIME"] = "TURBORAMJET"
        self.baseline()
        self.boundary(factual_claim_ids=["measurement", "derived"])
        self.assertEqual(self.inspect()["status"], "CHECKS_PASSED")
        for tag, state in (("UNKNOWN", "active"), ("P", "active"), ("F", "active"), ("T", "dirty")):
            p = copy.deepcopy(self.packet)
            p["claims"][0].update(tag=tag, state=state)
            self.held(p)
        p = copy.deepcopy(self.packet)
        p["claims"][0]["depends_on"] = ["derived"]
        self.held(p)

    def test_boundary_bindings_partitions_and_distinct_filings_hold(self):
        self.packet["FLIGHT_REGIME"] = "TURBORAMJET"
        self.baseline()
        for change in ({"job_id": "other"}, {"scope_sha256": "0" * 64}, {"baseline_sha256": "0" * 64},
                       {"result": "hold"}, {"factual_claim_ids": []}, {"hypothesis_claim_ids": ["measurement"]},
                       {"chair_filing": self.audit}, {"extra": 1}):
            self.boundary(**change)
            self.held()

    def test_author_membership_uniqueness_and_lens_scope(self):
        author = {"author_id": "AUTHOR", "sources": [self.source]}
        self.packet["j58"]["reference_authors"] = [author]
        self.packet["j58"]["lenses"] = ["BENCH_PROOF"]
        self.assertEqual(self.inspect()["status"], "CHECKS_PASSED")
        for authors in ([author, author], [{"author_id": "bad-id", "sources": [self.source]}],
                        [{"author_id": "AUTHOR", "sources": []}], [{"author_id": "AUTHOR", "sources": [self.audit]}]):
            p = copy.deepcopy(self.packet)
            p["j58"]["reference_authors"] = authors
            self.held(p)

    def test_base_authorization_and_tools_cannot_be_bypassed_by_cruise(self):
        self.packet["action"] = {"kind": "local_write", "target": "artifact.txt"}
        self.packet["recovery_plan"] = "Synthetic fixture recovery"
        self.packet["FLIGHT_REGIME"] = "TURBORAMJET"
        self.baseline()
        self.boundary()
        self.held()
        self.packet["authorization"] = {"granted": True, "action_kind": "local_write", "target": "artifact.txt", "basis": "Synthetic fixture only"}
        self.assertEqual(self.inspect()["status"], "CHECKS_PASSED")
        self.assertIn("authenticate", " ".join(self.inspect()["warnings"]))

    def test_base_and_overlay_blockers_are_combined(self):
        self.packet["action"] = {"kind": "local_write", "target": "file"}
        self.packet["FLIGHT_REGIME"] = "BAD"
        result = self.inspect()
        self.assertTrue(any("authorization" in x for x in result["blockers"]))
        self.assertTrue(any("FLIGHT_REGIME" in x for x in result["blockers"]))

    def test_scope_binds_action_claim_dependency_recovery_and_source_order(self):
        self.packet["FLIGHT_REGIME"] = "TURBORAMJET"
        self.baseline()
        self.boundary()
        for mutate in (lambda p: p["action"].update(target="different"),
                       lambda p: p["claims"][0].update(basis="different source assertion"),
                       lambda p: p.update(recovery_plan="changed recovery"),
                       lambda p: p["j58"]["input_artifacts"].reverse()):
            p = copy.deepcopy(self.packet)
            mutate(p)
            self.held(p)


if __name__ == "__main__":
    unittest.main()
