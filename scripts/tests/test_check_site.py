"""Tests for check_site.py, run against the made-up example site."""

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import check_site as cs  # noqa: E402

EXAMPLE = ROOT / "examples" / "example-site" / "northpine-running.example"


class CheckSiteTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.site = Path(self.tmp.name) / "site"
        shutil.copytree(EXAMPLE, self.site)

    def tearDown(self):
        self.tmp.cleanup()

    def test_example_site_passes(self):
        self.assertEqual(cs.check(EXAMPLE), [])

    def test_edited_brief_breaks_approval(self):
        with (self.site / "research" / "brief.md").open("a", encoding="utf-8") as f:
            f.write("\n- a new unapproved finding\n")
        self.assertTrue(any("research_brief" in p for p in cs.check(self.site)))

    def test_bad_method_and_missing_provenance(self):
        path = self.site / "research" / "competitors.csv"
        lines = path.read_text(encoding="utf-8").splitlines()
        lines[1] = lines[1].replace(",measured,", ",guessed,")
        lines[2] = lines[2].replace(",2026-10-05-research-3c4d", ",")
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        problems = cs.check(self.site)
        self.assertTrue(any("method 'guessed'" in p for p in problems))
        self.assertTrue(any("empty run_id" in p for p in problems))

    def test_secret_is_found(self):
        fake_key = "sk-" + "proj-" + "abcdefghijklmnopqrstuvwxyz123456"  # split so the repo scan does not flag this file
        (self.site / "notes.md").write_text(f"OPENAI_API_KEY={fake_key}\n", encoding="utf-8")
        self.assertTrue(any("looks like a key" in p for p in cs.check(self.site)))

    def test_missing_file_and_changed_columns(self):
        (self.site / "gaps.csv").unlink()
        path = self.site / "prompts.csv"
        path.write_text(path.read_text(encoding="utf-8").replace("prompt_id,prompt,", "id,prompt,", 1), encoding="utf-8")
        problems = cs.check(self.site)
        self.assertIn("missing gaps.csv", problems)
        self.assertTrue(any(p.startswith("prompts.csv: columns") for p in problems))


if __name__ == "__main__":
    unittest.main()
