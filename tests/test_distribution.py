import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class DistributionTests(unittest.TestCase):
    def test_archives_reproducible(self):
        builder = load("build")
        with tempfile.TemporaryDirectory() as directory:
            a, b = Path(directory) / "a.zip", Path(directory) / "b.zip"
            builder.archive(a, {"b.md": b"two", "a.md": b"one"})
            builder.archive(b, {"a.md": b"one", "b.md": b"two"})
            self.assertEqual(a.read_bytes(), b.read_bytes())
            with zipfile.ZipFile(a) as archive:
                self.assertEqual(archive.read("a.md"), b"one")

    def test_portable_core_is_complete_and_within_budget(self):
        builder = load("build")
        core = (ROOT / "plugins/author-voice/skills/author-voice/SKILL.md").read_text().split("---", 2)[2].strip().split("## Conditional resources", 1)[0].strip()
        for path, content in builder.generated().items():
            if path.endswith("instructions.md"):
                self.assertIn(core, content)
                self.assertLessEqual(len(content), 8000)
                self.assertNotIn("](references/", content)

    def test_missing_eval_responses_not_treated_as_success(self):
        evaluator = load("evaluate")
        cases = json.loads((ROOT / "evals/cases.json").read_text())
        with tempfile.TemporaryDirectory() as directory:
            report = evaluator.assess(cases, Path(directory))
            self.assertEqual(report["missing"], len(cases))
            self.assertIsNone(report["automatic_quality_grade"])

    def test_eval_surfaces_protected_change(self):
        evaluator = load("evaluate")
        cases = [{"id": "probe", "mode": "revise", "source": "Latency is 12 ms.", "locks": [], "review": ["Keep latency."]}]
        with tempfile.TemporaryDirectory() as directory:
            (Path(directory) / "probe.md").write_text("Latency is 9 ms.")
            result = evaluator.assess(cases, Path(directory))
            self.assertIn("numbers", result["cases"][0]["mechanical"]["protected_differences"])


if __name__ == "__main__":
    unittest.main()
