"""Tests for ask_engines.py. No network, no keys. Run: python -m pytest scripts/tests (or python -m unittest discover scripts/tests)."""

import csv
import io
import json
import os
import sys
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest import mock

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))
import ask_engines as ae  # noqa: E402


def fixture(name):
    return json.loads((HERE / "fixtures" / f"{name}.json").read_text(encoding="utf-8"))


class ParseTests(unittest.TestCase):
    def test_openai(self):
        r = ae.parse_response("openai", fixture("openai"))
        self.assertIn("Example Trail Pro", r["text"])
        self.assertEqual([c["url"] for c in r["citations"]],
                         ["https://reviews.example.org/wide-trail-shoes", "https://example-shoes.example/trail-pro"])

    def test_perplexity_prefers_search_results(self):
        r = ae.parse_response("perplexity", fixture("perplexity"))
        self.assertEqual(r["citations"], [{"url": "https://forum.example.net/thread/123", "title": "Wide feet trail shoe thread"}])

    def test_perplexity_citations_only(self):
        data = fixture("perplexity")
        del data["search_results"]
        r = ae.parse_response("perplexity", data)
        self.assertEqual(r["citations"], [{"url": "https://forum.example.net/thread/123", "title": ""}])

    def test_gemini_interactions(self):
        r = ae.parse_response("gemini", fixture("gemini"))
        self.assertEqual(r["text"], "Sample Ridge and Example Trail Pro are common choices.")
        self.assertEqual(r["citations"][0]["url"], "https://sample-brand.example/ridge")

    def test_gemini_generate_content(self):
        r = ae.parse_response("gemini", fixture("gemini_generate_content"))
        self.assertEqual(r["text"], "Example Trail Pro fits wide feet.")
        self.assertEqual(len(r["citations"]), 1)

    def test_anthropic_joins_text_and_keeps_citations(self):
        r = ae.parse_response("anthropic", fixture("anthropic"))
        self.assertEqual(r["text"], "I'll search for that. The Example Trail Pro is a frequent pick.")
        self.assertEqual(r["citations"], [{"url": "https://reviews.example.org/wide-trail-shoes", "title": "Best wide trail shoes"}])

    def test_empty_responses_do_not_crash(self):
        for engine in ae.ENGINES:
            self.assertEqual(ae.parse_response(engine, {}), {"text": "", "citations": []})


class RequestTests(unittest.TestCase):
    def test_country_is_passed_where_supported(self):
        _, body = ae.build_request("openai", "m", "q", "GB")
        self.assertEqual(body["tools"][0]["user_location"]["country"], "GB")
        _, body = ae.build_request("perplexity", "m", "q", "GB")
        self.assertEqual(body["web_search_options"]["user_location"]["country"], "GB")
        _, body = ae.build_request("anthropic", "m", "q", "GB")
        self.assertEqual(body["tools"][0]["user_location"]["country"], "GB")

    def test_no_country(self):
        _, body = ae.build_request("openai", "m", "q", "")
        self.assertNotIn("user_location", body["tools"][0])

    def test_key_only_in_headers(self):
        url, body = ae.build_request("anthropic", "m", "q", "US")
        self.assertNotIn("secret", url + json.dumps(body))
        self.assertEqual(ae.headers("anthropic", "secret")["x-api-key"], "secret")
        self.assertEqual(ae.headers("openai", "secret")["Authorization"], "Bearer secret")


def write_prompts(dirpath, n):
    path = os.path.join(dirpath, "prompts.csv")
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["prompt_id", "prompt", "topic"])
        for i in range(n):
            w.writerow([f"p{i}", f"question {i}", "t"])
    return path


class RunTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.out = os.path.join(self.tmp.name, "answers.jsonl")

    def tearDown(self):
        self.tmp.cleanup()

    def records(self):
        with open(self.out, encoding="utf-8") as f:
            return [json.loads(line) for line in f]

    @mock.patch.dict(os.environ, {"OPENAI_API_KEY": "k"}, clear=True)
    def test_run_writes_records_and_skips_missing_keys(self):
        prompts = ae.read_prompts(write_prompts(self.tmp.name, 2))
        with mock.patch.object(ae, "http_json", return_value=fixture("openai")):
            n = ae.run(prompts, ["openai", "perplexity"], {}, "US", self.out, 10)
        self.assertEqual(n, 2)
        recs = self.records()
        self.assertEqual({r["engine"] for r in recs}, {"openai"})
        self.assertIsNone(recs[0]["error"])
        self.assertEqual(recs[0]["model_used"], "gpt-5.5")

    @mock.patch.dict(os.environ, {"OPENAI_API_KEY": "k", "ANTHROPIC_API_KEY": "k"}, clear=True)
    def test_max_calls_is_total_across_engines(self):
        prompts = ae.read_prompts(write_prompts(self.tmp.name, 3))
        with mock.patch.object(ae, "http_json", return_value=fixture("openai")):
            n = ae.run(prompts, ["openai", "anthropic"], {}, "", self.out, 4)
        self.assertEqual(n, 4)
        self.assertEqual(len(self.records()), 4)

    @mock.patch.dict(os.environ, {"OPENAI_API_KEY": "k"}, clear=True)
    def test_http_error_is_recorded_not_raised(self):
        prompts = ae.read_prompts(write_prompts(self.tmp.name, 1))
        err = urllib.error.HTTPError("u", 401, "Unauthorized", {}, io.BytesIO(b'{"error":"bad key"}'))
        with mock.patch.object(ae, "http_json", side_effect=err):
            ae.run(prompts, ["openai"], {}, "", self.out, 10)
        rec = self.records()[0]
        self.assertTrue(rec["error"].startswith("HTTP 401"))
        self.assertEqual(rec["citations"], [])

    @mock.patch.dict(os.environ, {"ANTHROPIC_API_KEY": "k"}, clear=True)
    def test_anthropic_pause_turn_is_continued(self):
        paused = {"stop_reason": "pause_turn", "content": [{"type": "text", "text": "Searching"}]}
        with mock.patch.object(ae, "http_json", side_effect=[paused, fixture("anthropic")]) as m:
            r = ae.ask("anthropic", "claude-opus-5-5", "q", "", "k")
        self.assertEqual(m.call_count, 2)
        self.assertEqual(m.call_args[0][1]["messages"][1], {"role": "assistant", "content": paused["content"]})
        self.assertIn("Example Trail Pro", r["text"])

    def test_anthropic_refusal_raises(self):
        with mock.patch.object(ae, "http_json", return_value={"stop_reason": "refusal", "content": []}):
            with self.assertRaises(RuntimeError):
                ae.ask("anthropic", "m", "q", "", "k")

    def test_retry_once_on_429(self):
        err = urllib.error.HTTPError("u", 429, "Too Many", {"retry-after": "0"}, io.BytesIO(b""))
        with mock.patch.object(ae, "http_json", side_effect=[err, {"ok": 1}]), mock.patch.object(ae.time, "sleep"):
            self.assertEqual(ae.call("u", {}, {}), {"ok": 1})

    def test_missing_columns(self):
        path = os.path.join(self.tmp.name, "bad.csv")
        Path(path).write_text("id,question\n1,x\n", encoding="utf-8")
        with self.assertRaises(SystemExit):
            ae.read_prompts(path)


class CheckTests(unittest.TestCase):
    @mock.patch.dict(os.environ, {"OPENAI_API_KEY": "k", "PERPLEXITY_API_KEY": "k", "GEMINI_API_KEY": "k"}, clear=True)
    def test_check_statuses(self):
        err = urllib.error.HTTPError("u", 403, "Forbidden", {}, io.BytesIO(b"denied"))
        with mock.patch.object(ae, "http_json", side_effect=[{}, err]):
            out = ae.check(["openai", "gemini", "perplexity", "anthropic"])
        self.assertEqual(out["openai"]["status"], "available")
        self.assertEqual(out["gemini"]["status"], "error")
        self.assertEqual(out["perplexity"]["status"], "untested")
        self.assertEqual(out["anthropic"]["status"], "missing")


if __name__ == "__main__":
    unittest.main()
