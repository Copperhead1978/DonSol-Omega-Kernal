"""Behavior checks for the local packet inspector, not model-performance tests."""

import copy
import json
import unittest
from pathlib import Path

from omega_preflight import assess

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = json.loads((ROOT / "capabilities.json").read_text())


def valid_packet():
    return {
        "schema_version": 1,
        "job_id": "TEST",
        "goal": "Review local evidence.",
        "phase": "execute",
        "capability_ids": ["local-preflight"],
        "environment": {"observed_at": "2026-10-28T17:00:00-04:00", "tools": {
            "local_execution": {"available": True, "basis": "Test fixture: local Python supplied."}}},
        "action": {"kind": "read", "target": "local test fixture"},
        "claims": [{"id": "measurement", "tag": "T", "state": "active", "basis": "Synthetic test record, not a real experiment.", "depends_on": []}],
        "decision_inputs": ["measurement"],
        "acceptance_criteria": ["Inspect the packet and report its limits."],
        "verification_plan": "Assert deterministic checker behavior only."
    }


class PreflightTests(unittest.TestCase):
    def run_packet(self, packet):
        return assess(packet, REGISTRY)

    def test_clear_packet_does_not_claim_execution(self):
        result = self.run_packet(valid_packet())
        self.assertEqual(result["status"], "CHECKS_PASSED")
        self.assertIn("no action executed", result["scope"])

    def test_unknown_and_proposed_capabilities_hold_execution(self):
        for capability in ("imaginary", "workflow-runner"):
            with self.subTest(capability=capability):
                packet = valid_packet()
                packet["capability_ids"] = [capability]
                self.assertEqual(self.run_packet(packet)["status"], "HOLD")

    def test_plan_can_describe_unsupplied_expansion(self):
        packet = valid_packet()
        packet.update(phase="plan", capability_ids=["workflow-runner"])
        result = self.run_packet(packet)
        self.assertEqual(result["status"], "PLAN_ONLY")
        self.assertTrue(any("not supplied" in w for w in result["warnings"]))

    def test_available_flag_needs_observation_basis(self):
        packet = valid_packet()
        del packet["environment"]["tools"]["local_execution"]["basis"]
        self.assertEqual(self.run_packet(packet)["status"], "HOLD")

    def test_environment_time_needs_timezone(self):
        packet = valid_packet()
        packet["environment"]["observed_at"] = "2026-10-28T17:00:00"
        self.assertEqual(self.run_packet(packet)["status"], "HOLD")

    def test_write_requires_matching_existing_authority(self):
        packet = valid_packet()
        packet["action"] = {"kind": "external_write", "target": "repo-A"}
        packet["recovery_plan"] = "Revert the commit."
        packet["authorization"] = {"granted": True, "action_kind": "external_write", "target": "repo-B", "basis": "Existing user request"}
        self.assertEqual(self.run_packet(packet)["status"], "HOLD")
        packet["authorization"]["target"] = "repo-A"
        self.assertEqual(self.run_packet(packet)["status"], "CHECKS_PASSED")

    def test_write_requires_recovery_record(self):
        packet = valid_packet()
        packet["action"] = {"kind": "local_write", "target": "example"}
        packet["authorization"] = {"granted": True, "action_kind": "local_write", "target": "example", "basis": "Test fixture"}
        self.assertEqual(self.run_packet(packet)["status"], "HOLD")

    def test_transitive_unsettled_ancestor_holds_decision(self):
        for tag, state in (("P", "active"), ("UNKNOWN", "active"), ("F", "active"), ("T", "dirty"), ("T", "quarantined")):
            with self.subTest(tag=tag, state=state):
                packet = valid_packet()
                packet["claims"][0].update(tag=tag, state=state)
                packet["claims"].append({"id": "derived", "tag": "I", "state": "active", "basis": "Derived test assertion", "depends_on": ["measurement"]})
                packet["decision_inputs"] = ["derived"]
                self.assertEqual(self.run_packet(packet)["status"], "HOLD")

    def test_unrelated_unknown_does_not_block_bounded_job(self):
        packet = valid_packet()
        packet["claims"].append({"id": "unrelated", "tag": "UNKNOWN", "state": "active", "basis": "", "depends_on": []})
        self.assertEqual(self.run_packet(packet)["status"], "CHECKS_PASSED")

    def test_missing_and_cyclic_dependencies_hold(self):
        for parents in (["absent"], ["measurement"]):
            packet = valid_packet()
            packet["claims"][0]["depends_on"] = parents
            self.assertEqual(self.run_packet(packet)["status"], "HOLD")

    def test_current_profile_and_inference_basis_are_required(self):
        for changes in ({"tag": "H"}, {"basis": ""}, {"tag": "I"}):
            packet = valid_packet()
            packet["claims"][0].update(changes)
            self.assertEqual(self.run_packet(packet)["status"], "HOLD")

    def test_missing_acceptance_and_verification_hold(self):
        for field in ("acceptance_criteria", "verification_plan"):
            packet = valid_packet()
            del packet[field]
            self.assertEqual(self.run_packet(packet)["status"], "HOLD")

    def test_malformed_and_duplicate_records_hold(self):
        packets = [None, [], {"schema_version": 1}]
        duplicate = valid_packet()
        duplicate["claims"].append(copy.deepcopy(duplicate["claims"][0]))
        packets.append(duplicate)
        for packet in packets:
            with self.subTest(packet=packet):
                self.assertEqual(self.run_packet(packet)["status"], "HOLD")

    def test_malformed_field_types_hold_without_running_anything(self):
        for field in ("phase", "action", "claims", "decision_inputs", "environment"):
            packet = valid_packet()
            packet[field] = None
            with self.subTest(field=field):
                self.assertEqual(self.run_packet(packet)["status"], "HOLD")
        for field in ("tag", "state", "depends_on"):
            packet = valid_packet()
            packet["claims"][0][field] = {}
            with self.subTest(claim_field=field):
                self.assertEqual(self.run_packet(packet)["status"], "HOLD")

    def test_registry_corruption_holds(self):
        register = copy.deepcopy(REGISTRY)
        register["capabilities"].append(copy.deepcopy(register["capabilities"][0]))
        self.assertEqual(assess(valid_packet(), register)["status"], "HOLD")
        register = copy.deepcopy(REGISTRY)
        next(c for c in register["capabilities"] if c["id"] == "local-preflight")["status"] = []
        self.assertEqual(assess(valid_packet(), register)["status"], "HOLD")


if __name__ == "__main__":
    unittest.main()
