"""Tests for crawl_check.py against a fake site in memory. No network."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
import crawl_check as cc  # noqa: E402

GOOD = """<!doctype html><html lang="en"><head>
<title>Trail shoes for wide feet | Example Shoes</title>
<meta name="description" content="Wide trail shoes.">
<link rel="canonical" href="https://example-shoes.example/wide">
<link rel="alternate" hreflang="de" href="https://example-shoes.example/de/wide">
<script type="application/ld+json">{"@context":"https://schema.org","@graph":[{"@type":"Product"},{"@type":["FAQPage"]}]}</script>
</head><body><h1>Trail shoes for wide feet</h1><p>{text}</p></body></html>""".replace("{text}", "Fits wide feet. " * 60)

JS_ONLY = """<html><head><title>App</title><link rel="canonical" href="/app"></head>
<body><div id="root"></div><script src="a.js"></script><script src="b.js"></script><script src="c.js"></script></body></html>"""

NOINDEX = """<html><head><title>Hidden</title><meta name="robots" content="noindex, follow"></head><body><h1>x</h1></body></html>"""

ROBOTS = """User-agent: *
Allow: /

User-agent: GPTBot
Disallow: /

User-agent: PerplexityBot
Disallow: /

Sitemap: https://example-shoes.example/sitemap_index.xml
"""

INDEX = """<?xml version="1.0"?><sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
<sitemap><loc>https://example-shoes.example/pages.xml</loc></sitemap></sitemapindex>"""

PAGES = """<?xml version="1.0"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
<url><loc>https://example-shoes.example/wide</loc></url>
<url><loc>https://example-shoes.example/app</loc></url>
<url><loc>https://example-shoes.example/hidden</loc></url>
<url><loc>https://example-shoes.example/gone</loc></url>
<url><loc>https://other.example/off-site</loc></url>
</urlset>"""

BASE = "https://example-shoes.example"


def resp(status, body="", url=None, ctype="text/html; charset=utf-8", redirects=()):
    return {"status": status, "url": url, "redirects": list(redirects), "headers": {"content-type": ctype}, "body": body}


SITE = {
    BASE + "/robots.txt": resp(200, ROBOTS, ctype="text/plain"),
    BASE + "/llms.txt": resp(404),
    BASE + "/sitemap_index.xml": resp(200, INDEX, ctype="application/xml"),
    BASE + "/pages.xml": resp(200, PAGES, ctype="application/xml"),
    BASE + "/": resp(200, GOOD.replace("/wide", "/").replace("Trail shoes for wide feet |", "Home |"),redirects=[{"status": 301, "to": "x"}, {"status": 301, "to": "y"}]),
    BASE + "/wide": resp(200, GOOD),
    BASE + "/app": resp(200, JS_ONLY),
    BASE + "/hidden": resp(200, NOINDEX),
    BASE + "/gone": resp(404, ""),
}


def fake_fetch(url, user_agent=cc.USER_AGENT):
    r = dict(SITE.get(url, resp(404)))
    r["url"] = r["url"] or url
    if user_agent == "OAI-SearchBot" and url == BASE + "/":
        r["status"] = 403
    return r


class ParseTests(unittest.TestCase):
    def test_parse_page(self):
        p = cc.parse_page(GOOD)
        self.assertEqual(p["title"], "Trail shoes for wide feet | Example Shoes")
        self.assertEqual(p["h1"], ["Trail shoes for wide feet"])
        self.assertEqual(p["canonical"], "https://example-shoes.example/wide")
        self.assertEqual(p["lang"], "en")
        self.assertEqual(p["jsonld_types"], ["FAQPage", "Product"])
        self.assertEqual(p["hreflang"][0]["lang"], "de")
        self.assertGreater(p["text_chars"], 500)

    def test_invalid_jsonld(self):
        p = cc.parse_page('<script type="application/ld+json">{not json</script>')
        self.assertEqual(p["jsonld_types"], ["(invalid JSON-LD)"])

    def test_robots_access(self):
        bots, _ = cc.robots_access(ROBOTS, BASE)
        self.assertFalse(bots["GPTBot"]["allowed"])
        self.assertFalse(bots["PerplexityBot"]["allowed"])
        self.assertTrue(bots["OAI-SearchBot"]["allowed"])
        self.assertEqual(bots["PerplexityBot"]["kind"], "search")


class CrawlTests(unittest.TestCase):
    def setUp(self):
        self.report = cc.crawl("example-shoes.example", 20, [], 0, True, fetcher=fake_fetch, sleep=lambda s: None)
        self.pages = {p["url"]: p for p in self.report["pages"]}

    def issues(self, path):
        return {i["type"] for i in self.pages[BASE + path]["issues"]}

    def test_sitemap_index_followed_and_off_site_dropped(self):
        self.assertEqual(self.report["sitemap"]["url_count"], 5)
        self.assertNotIn("https://other.example/off-site", self.pages)
        self.assertEqual(len(self.pages), 5)

    def test_summary(self):
        s = self.report["summary"]
        self.assertEqual(s["search_bots_blocked"], ["PerplexityBot"])
        self.assertEqual(s["pages_checked"], 5)
        self.assertEqual(self.report["llms_txt"]["status"], 404)

    def test_issues(self):
        self.assertEqual(self.issues("/wide"), set())
        self.assertIn("possibly_js_only", self.issues("/app"))
        self.assertIn("blocks_search_or_snippets", self.issues("/hidden"))
        self.assertIn("missing_canonical", self.issues("/hidden"))
        self.assertEqual(self.issues("/gone"), {"http_error"})
        self.assertIn("redirect_chain", self.issues("/"))

    def test_bot_check(self):
        self.assertEqual(self.report["bot_fetch"]["OAI-SearchBot"], 403)
        self.assertNotIn("GPTBot", self.report["bot_fetch"])

    def test_robots_5xx_blocks_everything(self):
        def down(url, user_agent=cc.USER_AGENT):
            return resp(503) if url.endswith("robots.txt") else fake_fetch(url, user_agent)
        r = cc.crawl("example-shoes.example", 1, [], 0, False, fetcher=down, sleep=lambda s: None)
        self.assertIn("OAI-SearchBot", r["summary"]["search_bots_blocked"])

    def test_on_site(self):
        self.assertTrue(cc.on_site("https://www.example-shoes.example/x", "example-shoes.example"))
        self.assertFalse(cc.on_site("https://notexample-shoes.example/x", "example-shoes.example"))


if __name__ == "__main__":
    unittest.main()
