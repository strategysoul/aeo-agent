"""Check that a site folder written by the AEO agent is complete and consistent.

    python check_site.py <path to site folder>

Checks: required files exist, CSV columns match the formats in the skills, every data row says where it came
from (source, method, record_date, run_id), approved files match the hashes in state.json, prompt ids are
unique, and nothing that looks like an API key is in the folder. Exits 1 if any problem is found.
"""

import csv
import hashlib
import json
import re
import sys
from pathlib import Path

PROV = ["source", "method", "record_date", "run_id"]
METHODS = {"measured", "estimated", "inferred"}

# Column lists copied from the skills. Keep in step when a skill changes a format.
COLUMNS = {
    "research/competitors.csv": "domain,name,type,keywords_in_top10,seed_keywords_checked,evidence_url,source,method,record_date,run_id",
    "keywords/raw.csv": "keyword,origin,volume,demand_band,difficulty,intent,ai_overview,paa,gsc_impressions,gsc_position,gsc_url,notes,source,method,record_date,run_id",
    "keywords/scored.csv": "keyword,origin,volume,demand_band,difficulty,intent,ai_overview,paa,gsc_impressions,gsc_position,gsc_url,notes,source,method,record_date,run_id,fit,fit_reason,intent_score,demand,ease,bonus,score",
    "prompts.csv": "prompt_id,prompt,topic,type,language,country,active,created,run_id",
    "visibility/history.csv": "record_date,engine,source,answers,mention_rate,citation_rate,avg_position,share_of_voice,accuracy_issues,negative,run_id",
    "visibility/cited_domains.csv": "record_date,domain,answers_citing,engines,topics,is_own_site,is_competitor,run_id",
    "technical/issues.csv": "issue_key,type,severity,url,detail,in_topic,source,first_seen,last_seen,status,run_id",
    "technical/history.csv": "record_date,source,mode,health_score,errors,warnings,notices,pages_checked,search_bots_blocked,run_id",
    "gaps.csv": "topic,primary_keyword,demand,page_url,page_ok,best_position,position_source,ai_answers,mentioned,cited,cited_instead,ranks_instead,gap,record_date,run_id",
    "reports/rankings.csv": "record_date,period_start,period_end,topic,clicks,impressions,avg_position,source,run_id",
}
ANSWER_COLUMNS = "prompt_id,topic,type,engine,source,model_used,mentioned,position,cited,cited_urls,accuracy,accuracy_notes,sentiment,competitors_mentioned,cited_domains,answer_file,method,record_date,run_id"

REQUIRED = ["config.yaml", "state.json", "decisions.md", "profile.md", "research/brief.md", "research/coverage.json",
            "keywords/topics.md", "actions.md", "reports/latest.md"] + list(COLUMNS)

SECRET = re.compile(r"(sk-[A-Za-z0-9_-]{20,}|sk-ant-[A-Za-z0-9_-]{10,}|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{30,}"
                    r"|(api[_-]?key|password|secret|token)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{16,})", re.I)
ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_csv(path, rel, expected, problems):
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames or []
        rows = list(reader)
    if header != expected.split(","):
        problems.append(f"{rel}: columns differ from the documented format")
        return rows
    for i, row in enumerate(rows, start=2):
        if None in row or any(v is None for v in row.values()):
            problems.append(f"{rel}:{i}: wrong number of fields")
            continue
        if "method" in row and row["method"] not in METHODS:
            problems.append(f"{rel}:{i}: method '{row['method']}' is not measured/estimated/inferred")
        for field in ("record_date", "created", "first_seen", "last_seen"):
            if field in row and not ISO_DATE.match(row[field]):
                problems.append(f"{rel}:{i}: {field} '{row[field]}' is not YYYY-MM-DD")
        for field in [p for p in PROV if p in row]:
            if not row[field].strip():
                problems.append(f"{rel}:{i}: empty {field}")
    if not rows:
        problems.append(f"{rel}: no rows")
    return rows


def check(site):
    site = Path(site)
    problems = []
    for rel in REQUIRED:
        if not (site / rel).is_file():
            problems.append(f"missing {rel}")

    for rel, cols in COLUMNS.items():
        if (site / rel).is_file():
            rows = check_csv(site / rel, rel, cols, problems)
            if rel == "prompts.csv" and rows and "prompt_id" in rows[0]:
                ids = [r["prompt_id"] for r in rows]
                if len(ids) != len(set(ids)):
                    problems.append("prompts.csv: duplicate prompt_id")

    answer_files = sorted((site / "visibility").glob("[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9].csv"))
    if not answer_files:
        problems.append("missing visibility/<date>.csv")
    for path in answer_files:
        check_csv(path, f"visibility/{path.name}", ANSWER_COLUMNS, problems)

    state_path = site / "state.json"
    if state_path.is_file():
        state = json.loads(state_path.read_text(encoding="utf-8"))
        gates = {"research_brief": ("research/brief.md", "brief_hash"),
                 "priority_topics": ("keywords/topics.md", "topics_hash")}
        for gate, (rel, key) in gates.items():
            a = state.get("approvals", {}).get(gate, {})
            if a.get("approved") and (site / rel).is_file() and a.get(key) != sha256(site / rel):
                problems.append(f"state.json: {gate} is approved but {rel} has changed since (hash mismatch)")

    for path in site.rglob("*"):
        if path.is_file() and path.suffix in {".md", ".csv", ".json", ".jsonl", ".yaml", ".txt"}:
            if SECRET.search(path.read_text(encoding="utf-8", errors="replace")):
                problems.append(f"{path.relative_to(site).as_posix()}: contains something that looks like a key or password")
    return problems


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1:
        print(__doc__.strip().splitlines()[2].strip(), file=sys.stderr)
        return 2
    problems = check(argv[0])
    for p in problems:
        print(p)
    print("OK" if not problems else f"{len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
