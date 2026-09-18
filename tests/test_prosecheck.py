import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("prosecheck", ROOT / "plugins/author-voice/skills/author-voice/scripts/prosecheck.py")
pc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pc)


class PreservationTests(unittest.TestCase):
    def test_clean_style_edit(self):
        before = "Furthermore, latency fell from 12 ms to 9 ms [3]."
        after = "Latency fell from 12 ms to 9 ms [3]."
        self.assertEqual(pc.compare(before, after)["protected_differences"], {})

    def test_values_units_and_citations(self):
        for before, after, kind in [
            ("12 ms", "13 ms", "numbers"),
            ("12 ms", "12 s", "quantities"),
            ("−12", "12", "numbers"),
            ("p = 0.05", "p = 0.5", "numbers"),
            ("[2–4]", "[2–5]", "citations"),
            ("[@smith2024]", "[@jones2024]", "citations"),
            (r"\citep{smith}", r"\citep{jones}", "citations"),
            ("(Smith, 2024)", "(Jones, 2024)", "citations"),
        ]:
            with self.subTest(before=before):
                self.assertIn(kind, pc.compare(before, after)["protected_differences"])

    def test_duplicate_values_are_not_discarded(self):
        self.assertIn("numbers", pc.compare("n=30 and m=30", "n=30")["protected_differences"])

    def test_literal_blocks(self):
        examples = [
            ("```python\nx = 'old'\n```\n", "code_fences"),
            ("~~~~\nold\n~~~\n~~~~\n", "code_fences"),
            ("`old`", "inline_code"),
            ("$old$", "math"),
            (r"\(old\)", "math"),
            (r"\begin{equation}old\end{equation}", "math"),
            ('“old”', "quotations"),
            ("> old", "blockquotes"),
            ("<!-- author-voice:keep -->old<!-- /author-voice:keep -->", "keep_blocks"),
            ("| old | other |", "table_rows"),
            ("# old", "headings"),
            ("[^a]: old", "reference_definitions"),
        ]
        for before, kind in examples:
            with self.subTest(kind=kind):
                self.assertIn(kind, pc.compare(before, before.replace("old", "new"))["protected_differences"])

    def test_links(self):
        result = pc.compare("[paper](https://example.org/one)", "[paper](https://example.org/two)")
        self.assertIn("link_targets", result["protected_differences"])

    def test_qualifiers_need_review(self):
        result = pc.compare("It may help, but is not causal.", "It helps.")
        self.assertEqual(result["status"], "review-required")
        self.assertTrue(result["review_notes"])

    def test_same_numbers_can_have_different_meaning(self):
        result = pc.compare("A scored 20 and B scored 30.", "B scored 20 and A scored 30.")
        self.assertTrue(result["semantic_review_required"])
        self.assertEqual(result["status"], "no-mechanical-differences-found")

    def test_explicit_lock(self):
        self.assertIn("explicit_locks", pc.compare("robust regression", "regression", ["robust regression"])["protected_differences"])
        with self.assertRaises(ValueError):
            pc.compare("original", "original", ["absent"])

    def test_linter_excludes_literal_content(self):
        text = '```\nFurthermore\n```\n"Moreover"\n\nFurthermore, it works.'
        candidates = pc.lint(text)["candidates"]
        self.assertEqual(len(candidates), 1)
        self.assertEqual(candidates[0]["line"], 6)

    def test_no_punctuation_or_technical_word_blacklist(self):
        self.assertEqual(pc.lint("Robust regression uses an M-estimator—see the proof.")["candidates"], [])

    def test_rejects_binary_formats(self):
        with self.assertRaises(ValueError):
            pc.read_text("paper.pdf")


if __name__ == "__main__":
    unittest.main()
