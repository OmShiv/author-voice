import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from test_distribution import ROOT, load


class SubmissionTests(unittest.TestCase):
    def test_release_rejects_unselected_publisher_and_wrong_tag(self):
        submission = load("prepare_submission")
        blockers = submission.release_blockers(ROOT, {}, "0.1.0", "v9.0.0")
        self.assertTrue(any("tag must equal" in item for item in blockers))
        self.assertTrue(any("publisher.repository" in item for item in blockers))
        self.assertTrue(any("Choose a license" in item for item in blockers))

    def test_reviewer_pack_preserves_input_and_does_not_claim_test_results(self):
        submission = load("prepare_submission")
        source = json.loads((ROOT / "evals/cases.json").read_text())
        cases = submission.reviewer_cases(source)
        self.assertEqual(sum(c["category"] == "positive" for c in cases), 5)
        self.assertEqual(sum(c["category"] == "negative" for c in cases), 3)
        for case in cases:
            original = next(c for c in source if c["id"] == case["id"])
            self.assertIn(original["source"], case["prompt"])
            self.assertEqual(case["expected_behavior"], original["review"])
            self.assertEqual(case["status"], "not_run")
            self.assertIsNone(case["actual_response"])

    def test_archive_gate_detects_tampering_missing_license_and_unsafe_path(self):
        submission, builder = load("prepare_submission"), load("build")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "dist").mkdir()
            (root / "LICENSE").write_text("Test license")
            sums = []
            for name in submission.ARCHIVES:
                path = root / "dist" / name
                builder.archive(path, {"LICENSE": b"Test license", "SKILL.md": b"body"})
                sums.append(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {name}\n")
            (root / "dist/SHA256SUMS").write_text("".join(sums))
            self.assertEqual(submission.check_archives(root), [])
            builder.archive(root / "dist" / submission.ARCHIVES[0], {"../escape": b"bad"})
            result = submission.check_archives(root)
            self.assertTrue(any("Checksum mismatch" in item for item in result))
            self.assertTrue(any("Unsafe archive path" in item for item in result))
            self.assertTrue(any("current LICENSE" in item for item in result))


if __name__ == "__main__":
    unittest.main()
