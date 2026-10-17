"""Ask AI engines a list of questions with web search on, and save answers and cited URLs as JSON lines.

Standard library only. Keys come from environment variables and are never printed.

    python ask_engines.py --prompts prompts.csv --engines openai,perplexity --country US --out answers.jsonl
    python ask_engines.py --check            # free key check where the engine has one

prompts.csv needs the columns prompt_id and prompt. Other columns are ignored.
Scoring the answers (mention, position, accuracy, sentiment) happens in the aeo-visibility skill, not here.
"""

import argparse
import csv
import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

# Defaults checked against provider docs on 2026-10-17. Override with --model engine=model.
ENGINES = {
    "openai": {"env": "OPENAI_API_KEY", "model": "gpt-5.5"},
    "perplexity": {"env": "PERPLEXITY_API_KEY", "model": "sonar"},
    "gemini": {"env": "GEMINI_API_KEY", "model": "gemini-3.8-flash"},
    "anthropic": {"env": "ANTHROPIC_API_KEY", "model": "claude-opus-5-5"},
}

# Free calls that prove a key works. Perplexity has none we know of, so its key is only checked for presence.
CHECK_URLS = {
    "openai": "https://api.openai.com/v1/models",
    "gemini": "https://generativelanguage.googleapis.com/v1beta/models",
    "anthropic": "https://api.anthropic.com/v1/models",
}

TIMEOUT = 300


def headers(engine, key):
    if engine == "anthropic":
        return {
            "x-api-key": key,
            "anthropic-version": "2023-06-01",
            # Server-side fallback: if the model declines, the API retries on a fallback model.
            "anthropic-beta": "server-side-fallback-2026-07-01",
        }
    if engine == "gemini":
        return {"x-goog-api-key": key}
    return {"Authorization": f"Bearer {key}"}


def build_request(engine, model, prompt, country):
    """Return (url, body) for one question."""
    loc = {"type": "approximate", "country": country} if country else None
    if engine == "openai":
        tool = {"type": "web_search"}
        if loc:
            tool["user_location"] = loc
        return "https://api.openai.com/v1/responses", {"model": model, "input": prompt, "tools": [tool]}
    if engine == "perplexity":
        body = {"model": model, "messages": [{"role": "user", "content": prompt}]}
        if country:
            body["web_search_options"] = {"user_location": {"country": country}}
        return "https://api.perplexity.ai/v1/sonar", body
    if engine == "gemini":
        # ponytail: the Interactions API takes no location; answers are not localised for Gemini.
        return "https://generativelanguage.googleapis.com/v1beta/interactions", {
            "model": model,
            "input": prompt,
            "tools": [{"type": "google_search"}],
            "store": False,
        }
    if engine == "anthropic":
        tool = {"type": "web_search_20260318", "name": "web_search", "max_uses": 5}
        if loc:
            tool["user_location"] = loc
        return "https://api.anthropic.com/v1/messages", {
            "model": model,
            "max_tokens": 16000,
            "messages": [{"role": "user", "content": prompt}],
            "tools": [tool],
            "fallbacks": "default",
        }
    raise ValueError(f"unknown engine: {engine}")


def _dedupe(cites):
    seen, out = set(), []
    for c in cites:
        url = c.get("url")
        if url and url not in seen:
            seen.add(url)
            out.append({"url": url, "title": c.get("title") or ""})
    return out


def parse_response(engine, data):
    """Return {"text", "citations": [{"url", "title"}]} from a provider response."""
    texts, cites = [], []
    if engine == "openai":
        for item in data.get("output", []):
            if item.get("type") != "message":
                continue
            for part in item.get("content", []):
                if part.get("type") == "output_text":
                    texts.append(part.get("text", ""))
                    cites += [a for a in part.get("annotations", []) if a.get("type") == "url_citation"]
    elif engine == "perplexity":
        choices = data.get("choices") or [{}]
        texts.append(choices[0].get("message", {}).get("content", ""))
        cites = data.get("search_results") or [{"url": u} for u in data.get("citations", [])]
    elif engine == "gemini":
        if "steps" in data:  # Interactions API
            for step in data["steps"]:
                if step.get("type") != "model_output":
                    continue
                for part in step.get("content", []):
                    if "text" in part:
                        texts.append(part["text"])
                        cites += [a for a in part.get("annotations", []) if a.get("type") == "url_citation"]
        else:  # legacy generateContent
            cand = (data.get("candidates") or [{}])[0]
            texts += [p.get("text", "") for p in cand.get("content", {}).get("parts", [])]
            chunks = cand.get("groundingMetadata", {}).get("groundingChunks", [])
            cites = [{"url": c["web"].get("uri"), "title": c["web"].get("title")} for c in chunks if "web" in c]
    elif engine == "anthropic":
        for block in data.get("content", []):
            if block.get("type") == "text":
                texts.append(block.get("text", ""))
                cites += [c for c in block.get("citations") or [] if c.get("type") == "web_search_result_location"]
    return {"text": "".join(texts).strip(), "citations": _dedupe(cites)}


def http_json(url, body, hdrs):
    """POST body (or GET when body is None) and return parsed JSON. Raises urllib.error.HTTPError."""
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json", **hdrs})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return json.loads(resp.read().decode())


def call(url, body, hdrs):
    """One call with a single retry on rate limits and server errors."""
    for attempt in range(2):
        try:
            return http_json(url, body, hdrs)
        except urllib.error.HTTPError as e:
            if attempt == 0 and (e.code == 429 or e.code >= 500):
                time.sleep(min(int(e.headers.get("retry-after") or 5), 30))
                continue
            raise


def ask(engine, model, prompt, country, key):
    url, body = build_request(engine, model, prompt, country)
    hdrs = headers(engine, key)
    data = call(url, body, hdrs)
    if engine == "anthropic":
        # A long search turn can pause; send the paused message back to let it finish.
        for _ in range(3):
            if data.get("stop_reason") != "pause_turn":
                break
            body["messages"] = body["messages"][:1] + [{"role": "assistant", "content": data["content"]}]
            data = call(url, body, hdrs)
        if data.get("stop_reason") == "refusal":
            raise RuntimeError("model declined to answer")
    result = parse_response(engine, data)
    result["usage"] = data.get("usage")
    # The model that actually answered; differs from the requested one after an Anthropic fallback.
    result["model_used"] = data.get("model") or model
    return result


def error_text(e):
    if isinstance(e, urllib.error.HTTPError):
        try:
            detail = e.read().decode()[:300]
        except Exception:
            detail = ""
        return f"HTTP {e.code}: {detail}"
    return f"{type(e).__name__}: {e}"[:300]


def check(engines):
    out = {}
    for engine in engines:
        key = os.environ.get(ENGINES[engine]["env"])
        if not key:
            out[engine] = {"status": "missing"}
        elif engine not in CHECK_URLS:
            out[engine] = {"status": "untested", "note": "key set; no free check call"}
        else:
            try:
                http_json(CHECK_URLS[engine], None, headers(engine, key))
                out[engine] = {"status": "available"}
            except Exception as e:
                out[engine] = {"status": "error", "last_error": error_text(e)}
    return out


def read_prompts(path):
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    missing = {"prompt_id", "prompt"} - set(rows[0] if rows else {})
    if missing:
        raise SystemExit(f"{path} is missing columns: {', '.join(sorted(missing))}")
    return rows


def run(prompts, engines, models, country, out_path, max_calls):
    calls = 0
    with open(out_path, "a", encoding="utf-8") as out:
        for engine in engines:
            key = os.environ.get(ENGINES[engine]["env"])
            if not key:
                print(f"skip {engine}: {ENGINES[engine]['env']} not set", file=sys.stderr)
                continue
            model = models.get(engine, ENGINES[engine]["model"])
            for row in prompts:
                if calls >= max_calls:
                    print(f"stopped at --max-calls {max_calls}", file=sys.stderr)
                    return calls
                rec = {
                    "prompt_id": row["prompt_id"],
                    "prompt": row["prompt"],
                    "engine": engine,
                    "model": model,
                    "country": country,
                    "asked_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                }
                try:
                    rec.update(ask(engine, model, row["prompt"], country, key))
                    rec["error"] = None
                except Exception as e:
                    rec.update({"text": "", "citations": [], "usage": None, "error": error_text(e)})
                out.write(json.dumps(rec, ensure_ascii=False) + "\n")
                out.flush()
                calls += 1
    return calls


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--prompts", help="CSV with prompt_id and prompt columns")
    p.add_argument("--engines", default=",".join(ENGINES), help="comma-separated: " + ",".join(ENGINES))
    p.add_argument("--model", action="append", default=[], metavar="ENGINE=MODEL", help="override a default model")
    p.add_argument("--country", default="", help="two-letter country code for localised search")
    p.add_argument("--out", help="JSON lines file to append to")
    p.add_argument("--max-calls", type=int, default=100, help="stop after this many calls in total (default 100)")
    p.add_argument("--check", action="store_true", help="check which keys work, using free calls only")
    a = p.parse_args(argv)

    engines = [e.strip() for e in a.engines.split(",") if e.strip()]
    unknown = [e for e in engines if e not in ENGINES]
    if unknown:
        p.error(f"unknown engine(s): {', '.join(unknown)}")

    if a.check:
        print(json.dumps(check(engines), indent=2))
        return 0
    if not a.prompts or not a.out:
        p.error("--prompts and --out are required unless --check is given")

    models = dict(m.split("=", 1) for m in a.model)
    n = run(read_prompts(a.prompts), engines, models, a.country.upper(), a.out, a.max_calls)
    print(json.dumps({"calls": n, "out": a.out}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
