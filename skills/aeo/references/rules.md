# Rules every AEO agent step follows

## Where data comes from

Every data point written to a file carries four fields:

| Field | Values |
|---|---|
| `source` | the tool or URL it came from, e.g. `ahrefs`, `gsc`, `chrome:chatgpt.com`, `https://…` |
| `method` | `measured` (the tool reports it), `estimated` (a tool's model, e.g. keyword volume), `inferred` (the agent worked it out) |
| `record_date` | ISO date the value was collected |
| `run_id` | `<YYYY-MM-DD>-<step>-<4 random hex chars>`, the same for every row from one run |

In CSV files these are columns. In Markdown, put them in a line under the claim or in a table column.

Reports say plainly when a weaker source was used, e.g. "Keyword volumes are inferred from autocomplete because no SEO data source is connected."

## Choosing a source

1. Read `capabilities.sources` in `config.yaml`.
2. Use the first source in the step's fallback order whose status is `available`.
3. If a call fails, record the error in `capabilities.sources.<name>.last_error`, set its status to `error`, and try the next source. Do not retry the same call more than once.
4. If a response returns exactly the plan's row limit, assume it was cut off: page through (if the tool supports offsets) or note that the list is incomplete.
5. MCP connector calls only happen inside Claude. Scripts in `scripts/` call AI-engine APIs only. Some providers, Ahrefs among them, do not allow their MCP endpoint to be called from scripts.

## Budget

- Before a step that uses paid units, read `units_left` for the source. It is in the source's own `unit` (API units, or US dollars for DataForSEO).
- Per site per run, spend at most `budget.share_of_remaining` × `units_left` (default 10%), and never more than `budget.hard_cap_units` if it is set.
- Estimate the cost before each batch of calls. If the batch would go over budget, shrink it (fewer keywords, fewer rows) and say what was cut.
- After each run, append to `state.json` → `runs`: `{run_id, step, source, units_spent, started_at, finished_at}`.

## Approvals

The research brief and the priority topics need a person's approval. Scheduled or non-interactive runs never pass an unapproved gate. When the approved content changes (its hash in `state.json` no longer matches), ask again.

## Snapshots and history

Raw responses go under dated folders (`research/raw/<date>/`, `visibility/<date>.csv`) and are never overwritten. New runs add to earlier files; `*history.csv` files are append-only.

## Evidence

Every factual claim about the market, a competitor or an AI answer needs a URL and a date. If something was looked for and not found, write "not found". If it is a guess, label it "inferred".

## What the agent never does

- Change the site, its CMS, DNS, CDN, or settings in any tool. It recommends; people make changes.
- Write keys, tokens or personal data into site folders, logs or reports. Check whether a key is set; never print its value.
- Carry text from one site's folder into another site's files.

## Writing style for files and reports

Plain language. Descriptive headings that say what the section shows. Short sentences. No slogans, no hype, no emoji. Numbers with units and dates.
