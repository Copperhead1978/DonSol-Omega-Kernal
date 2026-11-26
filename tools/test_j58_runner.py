"""Actual local-file effects, duplicate refusal and crash/recovery; no production effects."""
import copy
import hashlib
import os
import subprocess
import sys
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from j58_preflight import canonical_bytes, scope_sha256
from j58_runner import FixturePermit, run_fixture
from test_omega_preflight import REGISTRY, valid_packet


class RunnerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.p = valid_packet()
        self.p.update(schema_version=2, FLIGHT_REGIME="TURBOJET", j58={"lenses": [], "reference_authors": [], "input_artifacts": [], "baseline": None, "transition": None},
                      action={"kind": "local_write", "target": "output/result.txt", "content": "Synthetic fixture output\n"},
                      recovery_plan="Resume the reserved local fixture; never overwrite conflicting bytes.",
                      authorization={"granted": True, "action_kind": "local_write", "target": "output/result.txt", "basis": "Synthetic test fixture"})

    def permit(self, p=None):
        p = p or self.p
        return FixturePermit(p["action"]["target"], scope_sha256(p), 4096, "Synthetic host test grant")

    def run_job(self, **kw):
        return run_fixture(self.p, REGISTRY, self.root, permit=self.permit(), **kw)

    def test_real_artifact_readback_and_duplicate_refusal(self):
        first = self.run_job()
        self.assertEqual(first["outcome"], "COMPLETED")
        target = self.root / self.p["action"]["target"]
        self.assertEqual(target.read_text(), self.p["action"]["content"])
        self.assertEqual(first["receipt"]["sha256"], hashlib.sha256(target.read_bytes()).hexdigest())
        before = target.stat().st_mtime_ns
        second = self.run_job()
        self.assertEqual(second["outcome"], "DUPLICATE_REFUSED")
        self.assertEqual(target.stat().st_mtime_ns, before)

    def test_packet_authorization_does_not_supply_host_permit(self):
        result = run_fixture(self.p, REGISTRY, self.root)
        self.assertEqual(result["outcome"], "REFUSED_HOLD")
        self.assertFalse((self.root / "output").exists())

    def test_wrong_permit_scope_target_budget_and_plan_hold(self):
        for permit in (FixturePermit("other", scope_sha256(self.p), 4096, "host"), FixturePermit(self.p["action"]["target"], "0" * 64, 4096, "host"), FixturePermit(self.p["action"]["target"], scope_sha256(self.p), 1, "host")):
            self.assertEqual(run_fixture(self.p, REGISTRY, self.root, permit=permit)["outcome"], "REFUSED_HOLD")
        self.p["phase"] = "plan"
        self.assertEqual(self.run_job()["outcome"], "REFUSED_HOLD")

    def test_changed_scope_and_preexisting_or_tampered_artifacts_are_never_overwritten(self):
        self.assertEqual(self.run_job()["outcome"], "COMPLETED")
        self.p["action"]["content"] = "Changed"
        self.assertEqual(self.run_job()["outcome"], "REFUSED_HOLD")
        target = self.root / self.p["action"]["target"]
        self.p["action"]["content"] = "Synthetic fixture output\n"
        target.write_text("external change")
        self.assertEqual(self.run_job()["outcome"], "REFUSED_HOLD")
        self.assertEqual(target.read_text(), "external change")

    def test_preexisting_artifact_without_a_reservation_is_refused(self):
        target = self.root / self.p["action"]["target"]
        target.parent.mkdir()
        target.write_text(self.p["action"]["content"])
        self.assertEqual(self.run_job()["outcome"], "REFUSED_HOLD")
        self.assertEqual(target.read_text(), self.p["action"]["content"])

    def test_different_job_cannot_reuse_reserved_target(self):
        self.assertEqual(self.run_job()["outcome"], "COMPLETED")
        self.p["job_id"] = "OTHER-JOB"
        self.assertEqual(self.run_job()["outcome"], "REFUSED_HOLD")

    def test_crash_after_reservation_and_after_publish_resume_without_rewrite(self):
        for stage in ("reserved", "published"):
            with self.subTest(stage=stage), tempfile.TemporaryDirectory() as root:
                def crash(observed):
                    if observed == stage:
                        raise RuntimeError("injected interruption")
                with self.assertRaises(RuntimeError):
                    run_fixture(self.p, REGISTRY, root, permit=self.permit(), fault_hook=crash)
                target = Path(root) / self.p["action"]["target"]
                before = target.stat().st_mtime_ns if target.exists() else None
                result = run_fixture(self.p, REGISTRY, root, permit=self.permit())
                self.assertEqual(result["outcome"], "COMPLETED")
                self.assertEqual(result["receipt"]["recovered"], stage == "published")
                if before is not None:
                    self.assertEqual(before, target.stat().st_mtime_ns)

    def test_process_death_after_publish_recovers_durable_reservation(self):
        import json
        pfile = self.root / "packet.json"
        pfile.write_bytes(canonical_bytes(self.p))
        script = "import json,os,sys; from pathlib import Path; from j58_runner import *; from test_omega_preflight import REGISTRY; p=json.loads(Path(sys.argv[1]).read_text()); run_fixture(p,REGISTRY,sys.argv[2],permit=FixturePermit(p['action']['target'],__import__('j58_preflight').scope_sha256(p),4096,'test'),fault_hook=lambda stage: os._exit(23) if stage=='published' else None)"
        child = subprocess.run([sys.executable, "-c", script, str(pfile), str(self.root)], cwd=Path(__file__).resolve().parent, capture_output=True)
        self.assertEqual(child.returncode, 23, child.stderr.decode())
        target = self.root / self.p["action"]["target"]
        before = target.stat().st_mtime_ns
        self.assertEqual(self.run_job()["outcome"], "COMPLETED")
        self.assertEqual(target.stat().st_mtime_ns, before)

    def test_simultaneous_duplicate_deliveries_have_one_writer(self):
        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(lambda _: self.run_job(), range(2)))
        self.assertCountEqual([r["outcome"] for r in results], ["COMPLETED", "DUPLICATE_REFUSED"])
        self.assertEqual(sum(r.get("effect_written", False) for r in results), 1)

    def test_stale_evidence_holds_only_affected_job(self):
        self.assertEqual(self.run_job()["outcome"], "COMPLETED")
        target = self.root / self.p["action"]["target"]
        original = target.read_bytes()
        self.p["job_id"] = "OTHER"
        self.p["action"]["target"] = "other.txt"
        self.p["authorization"]["target"] = "other.txt"
        self.p["j58"]["input_artifacts"] = [{"path": "absent", "sha256": "0" * 64}]
        self.assertEqual(self.run_job()["outcome"], "REFUSED_HOLD")
        self.assertEqual(target.read_bytes(), original)
        self.assertFalse((self.root / "other.txt").exists())

    def test_target_escape_and_symlink_parent_hold(self):
        with tempfile.TemporaryDirectory() as outside:
            (self.root / "output").symlink_to(outside, target_is_directory=True)
            self.assertEqual(self.run_job()["outcome"], "REFUSED_HOLD")
            self.assertFalse((Path(outside) / "result.txt").exists())


if __name__ == "__main__":
    unittest.main()
