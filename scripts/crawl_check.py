"""Crawl a site politely and report technical facts that matter for search and AI answers, as JSON.

Standard library only. Reads robots.txt (with AI crawler access per bot), sitemaps, llms.txt, and up to
--max-pages HTML pages. Never logs in, never submits forms, and only fetches the given domain.

    python crawl_check.py --domain example.com --out technical/raw/2026-10-17/crawl.json
    python crawl_check.py --domain example.com --urls priority.txt --max-pages 50 --bot-check
"""

import argparse
import gzip
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import urllib.robotparser
import xml.etree.ElementTree as ET
from collections import Counter
from datetime import datetime, timezone
from html.parser import HTMLParser

USER_AGENT = "AEO-Agent/0.1 (site check; +https://github.com/strategysoul/aeo-agent)"

# Checked against each operator's docs on 2026-10-17. kind: search = decides whether the site can appear in
# that engine's answers; user = fetches a page when a person asks (may ignore robots.txt); training = model training.
BOTS = {
    "Googlebot": "search",
    "Bingbot": "search",
    "OAI-SearchBot": "search",
    "PerplexityBot": "search",
    "Claude-SearchBot": "search",
    "ChatGPT-User": "user",
    "Perplexity-User": "user",
    "Claude-User": "user",
    "GPTBot": "training",
    "ClaudeBot": "training",
    "Google-Extended": "training",  # also Gemini grounding; does not affect Google Search
}

TIMEOUT = 20
THIN_TEXT_CHARS = 500  # visible text below this on an HTML page suggests content that needs JavaScript


class _Recorder(urllib.request.HTTPRedirectHandler):
    def __init__(self):
        self.chain = []

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        self.chain.append({"status": code, "to": newurl})
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def fetch(url, user_agent=USER_AGENT):
    """GET a URL. Returns {status, url, redirects, headers, body} and never raises for HTTP or network errors."""
    rec = _Recorder()
    opener = urllib.request.build_opener(rec)
    req = urllib.request.Request(url, headers={"User-Agent": user_agent, "Accept-Encoding": "gzip"})
    try:
        with opener.open(req, timeout=TIMEOUT) as resp:
            raw = resp.read(5_000_000)
            if resp.headers.get("Content-Encoding") == "gzip" or url.endswith(".gz"):
                raw = gzip.decompress(raw)
            return {"status": resp.status, "url": resp.url, "redirects": rec.chain,
                    "headers": {k.lower(): v for k, v in resp.headers.items()},
                    "body": raw.decode(resp.headers.get_content_charset() or "utf-8", "replace")}
    except urllib.error.HTTPError as e:
        return {"status": e.code, "url": url, "redirects": rec.chain,
                "headers": {k.lower(): v for k, v in (e.headers or {}).items()}, "body": ""}
    except Exception as e:
        return {"status": None, "url": url, "redirects": rec.chain, "headers": {}, "body": "",
                "error": f"{type(e).__name__}: {e}"[:200]}


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title, self.description, self.robots, self.canonical = None, None, [], None
        self.h1, self.hreflang, self.jsonld_types, self.scripts = [], [], [], 0
        self.lang = None
        self._in, self._buf, self._skip, self.text_chars = None, [], 0, 0

    def handle_starttag(self, tag, attrs):
        a = {k: (v or "") for k, v in attrs}
        if tag == "html":
            self.lang = a.get("lang") or None
        elif tag == "title":
            self._in, self._buf = "title", []
        elif tag == "h1":
            self._in, self._buf = "h1", []
        elif tag == "meta":
            name = a.get("name", "").lower()
            if name == "description":
                self.description = a.get("content", "").strip()
            elif name in ("robots", "googlebot"):
                self.robots += [d.strip().lower() for d in a.get("content", "").split(",") if d.strip()]
        elif tag == "link":
            rel = a.get("rel", "").lower().split()
            if "canonical" in rel:
                self.canonical = a.get("href")
            if "alternate" in rel and a.get("hreflang"):
                self.hreflang.append({"lang": a["hreflang"], "href": a.get("href")})
        elif tag == "script":
            self.scripts += 1
            self._skip += 1
            if a.get("type", "").lower() == "application/ld+json":
                self._in, self._buf = "jsonld", []
        elif tag in ("style", "noscript", "template"):
            self._skip += 1

    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript", "template"):
            self._skip = max(0, self._skip - 1)
        if tag == "title" and self._in == "title":
            self.title = " ".join("".join(self._buf).split())
            self._in = None
        elif tag == "h1" and self._in == "h1":
            self.h1.append(" ".join("".join(self._buf).split()))
            self._in = None
        elif tag == "script" and self._in == "jsonld":
            self.jsonld_types += _jsonld_types("".join(self._buf))
            self._in = None

    def handle_data(self, data):
        if self._in:
            self._buf.append(data)
        if not self._skip and self._in != "title":
            self.text_chars += len(data.strip())


def _jsonld_types(text):
    try:
        data = json.loads(text)
    except ValueError:
        return ["(invalid JSON-LD)"]
    found, stack = [], [data]
    while stack:
        node = stack.pop()
        if isinstance(node, list):
            stack += node
        elif isinstance(node, dict):
            t = node.get("@type")
            found += t if isinstance(t, list) else ([t] if t else [])
            stack += [v for v in node.values() if isinstance(v, (list, dict))]
    return found


def parse_page(html):
    p = PageParser()
    p.feed(html)
    return {"title": p.title, "description": p.description, "meta_robots": p.robots, "canonical": p.canonical,
            "h1": p.h1, "lang": p.lang, "hreflang": p.hreflang, "jsonld_types": sorted(set(p.jsonld_types)),
            "scripts": p.scripts, "text_chars": p.text_chars}


def robots_access(robots_txt, base):
    """Per bot: whether it may fetch the home page."""
    rp = urllib.robotparser.RobotFileParser()
    rp.parse(robots_txt.splitlines())
    return {bot: {"kind": kind, "allowed": rp.can_fetch(bot, base + "/")} for bot, kind in BOTS.items()}, rp


def sitemap_urls(start, limit, fetcher=fetch):
    """Follow sitemap indexes. Returns (page_urls, sitemaps_read, errors)."""
    todo, seen, pages, errors = list(start), set(), [], []
    while todo and len(pages) < limit and len(seen) < 50:
        sm = todo.pop(0)
        if sm in seen:
            continue
        seen.add(sm)
        r = fetcher(sm)
        if r["status"] != 200:
            errors.append({"sitemap": sm, "status": r["status"]})
            continue
        try:
            root = ET.fromstring(r["body"].encode())
        except ET.ParseError:
            errors.append({"sitemap": sm, "status": "invalid XML"})
            continue
        for el in root.iter():
            if el.tag.endswith("}loc") or el.tag == "loc":
                loc = (el.text or "").strip()
                (todo if root.tag.endswith("sitemapindex") else pages).append(loc)
    return pages[:limit], sorted(seen), errors


def page_issues(page, domain):
    out = []
    s = page["status"]
    if s is None or s >= 400:
        return [{"type": "http_error", "severity": "error", "detail": str(s or page.get("error"))}]
    if len(page["redirects"]) > 1:
        out.append({"type": "redirect_chain", "severity": "warning", "detail": f"{len(page['redirects'])} hops"})
    if "html" not in page.get("content_type", "html"):
        return out
    if not page["title"]:
        out.append({"type": "missing_title", "severity": "error", "detail": ""})
    elif len(page["title"]) > 65:
        out.append({"type": "long_title", "severity": "notice", "detail": f"{len(page['title'])} chars"})
    if not page["description"]:
        out.append({"type": "missing_description", "severity": "notice", "detail": ""})
    if len(page["h1"]) != 1:
        out.append({"type": "h1_count", "severity": "warning", "detail": f"{len(page['h1'])} h1 tags"})
    if not page["canonical"]:
        out.append({"type": "missing_canonical", "severity": "warning", "detail": ""})
    else:
        canon = urllib.parse.urljoin(page["final_url"], page["canonical"])
        if canon.rstrip("/") != page["final_url"].rstrip("/"):
            out.append({"type": "canonical_elsewhere", "severity": "notice", "detail": canon})
    blocked = {"noindex", "none", "nosnippet"} & set(page["meta_robots"] + page.get("x_robots", []))
    if blocked:
        out.append({"type": "blocks_search_or_snippets", "severity": "error", "detail": ",".join(sorted(blocked))})
    if any(d.startswith("max-snippet:0") for d in page["meta_robots"]):
        out.append({"type": "blocks_search_or_snippets", "severity": "error", "detail": "max-snippet:0"})
    if page["text_chars"] < THIN_TEXT_CHARS and page["scripts"] >= 3:
        out.append({"type": "possibly_js_only", "severity": "warning",
                    "detail": f"{page['text_chars']} chars of text without JavaScript, {page['scripts']} scripts"})
    if not on_site(page["final_url"], domain):
        out.append({"type": "redirects_off_site", "severity": "warning",
                    "detail": urllib.parse.urlparse(page["final_url"]).hostname or ""})
    return out


def on_site(url, domain):
    host = urllib.parse.urlparse(url).hostname or ""
    return host == domain or host.endswith("." + domain)


def crawl(domain, max_pages, priority_urls, delay, bot_check, fetcher=fetch, sleep=time.sleep):
    base = f"https://{domain}"
    report = {"domain": domain, "checked_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
              "user_agent": USER_AGENT}

    r = fetcher(base + "/robots.txt")
    rp = None
    report["robots"] = {"status": r["status"]}
    if r["status"] == 200:
        report["robots"]["bots"], rp = robots_access(r["body"], base)
        report["robots"]["sitemaps"] = rp.site_maps() or []
    else:
        # Google's rule, followed by most crawlers: a 4xx robots.txt (except 429) means everything is allowed;
        # 429, 5xx or no answer means crawlers treat the whole site as blocked.
        allowed = r["status"] is not None and 400 <= r["status"] < 500 and r["status"] != 429
        report["robots"]["bots"] = {b: {"kind": k, "allowed": allowed} for b, k in BOTS.items()}
        report["robots"]["sitemaps"] = []

    r = fetcher(base + "/llms.txt")
    report["llms_txt"] = {"status": r["status"], "bytes": len(r["body"])}

    starts = report["robots"]["sitemaps"] or [base + "/sitemap.xml"]
    urls, read, errors = sitemap_urls(starts, max(max_pages * 5, 500), fetcher)
    report["sitemap"] = {"read": read, "errors": errors, "url_count": len(urls)}

    queue, seen = [], set()
    for u in [base + "/"] + list(priority_urls) + urls:
        u = urllib.parse.urljoin(base + "/", u.strip())
        if u and u not in seen and on_site(u, domain):
            seen.add(u)
            queue.append(u)
    pages = []
    for u in queue[:max_pages]:
        if rp and not rp.can_fetch(USER_AGENT, u):
            pages.append({"url": u, "status": None, "skipped": "disallowed for this checker in robots.txt",
                          "issues": []})
            continue
        r = fetcher(u)
        page = {"url": u, "final_url": r["url"], "status": r["status"], "redirects": r["redirects"],
                "content_type": r["headers"].get("content-type", ""),
                "x_robots": [d.strip().lower() for d in r["headers"].get("x-robots-tag", "").split(",") if d.strip()],
                "last_modified": r["headers"].get("last-modified")}
        if r.get("error"):
            page["error"] = r["error"]
        if r["status"] == 200 and "html" in page["content_type"]:
            page.update(parse_page(r["body"]))
        else:
            page.update({"title": None, "description": None, "meta_robots": [], "canonical": None, "h1": [],
                         "text_chars": 0, "scripts": 0})
        page["issues"] = page_issues(page, domain)
        pages.append(page)
        sleep(delay)

    titles = Counter(p["title"] for p in pages if p.get("title"))
    for p in pages:
        if p.get("title") and titles[p["title"]] > 1:
            p["issues"].append({"type": "duplicate_title", "severity": "warning", "detail": p["title"][:80]})
    report["pages"] = pages
    report["sitemap"]["not_in_sitemap"] = [p["url"] for p in pages if p["url"] not in set(urls)][:50]

    if bot_check:
        # Indicative only: a firewall that verifies bot IP addresses will treat this request differently.
        report["bot_fetch"] = {b: fetcher(base + "/", user_agent=b)["status"] for b, k in BOTS.items() if k != "training"}

    counts = Counter(i["severity"] for p in pages for i in p["issues"])
    report["summary"] = {"pages_checked": len(pages), "errors": counts["error"], "warnings": counts["warning"],
                         "notices": counts["notice"],
                         "search_bots_blocked": [b for b, v in report["robots"]["bots"].items()
                                                 if v["kind"] == "search" and not v["allowed"]]}
    return report


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--domain", required=True, help="domain without scheme, e.g. example.com")
    p.add_argument("--out", required=True, help="JSON file to write")
    p.add_argument("--max-pages", type=int, default=200)
    p.add_argument("--urls", help="text file of URLs to check first, one per line")
    p.add_argument("--delay", type=float, default=0.5, help="seconds between page requests (default 0.5)")
    p.add_argument("--bot-check", action="store_true", help="also fetch the home page with each AI bot's user agent")
    a = p.parse_args(argv)

    domain = a.domain.lower().removeprefix("https://").removeprefix("http://").strip("/")
    priority = []
    if a.urls:
        with open(a.urls, encoding="utf-8") as f:
            priority = [line.strip() for line in f if line.strip()]
    report = crawl(domain, a.max_pages, priority, a.delay, a.bot_check)
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print(json.dumps(report["summary"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
