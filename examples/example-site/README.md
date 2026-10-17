# Example site: Northpine Running (made up)

**Everything in this folder is fictional.** Northpine Running, its products, its competitors, the forums, review sites and regulators it mentions, and every number are invented for this example. All web addresses use the reserved `.example` domain, so none of them point at a real business.

The folder `northpine-running.example/` shows what the AEO agent writes for one site after its first two weekly runs. The files were written by hand to match the formats in the skills exactly; they are not the output of a live run. `scripts/check_site.py` checks them in CI, so if a skill changes a file format, this example must change with it.

## The story in the files

| Date | What ran | Where to look |
|---|---|---|
| 2026-10-05 | Setup: Search Console, DataForSEO and an OpenAI key connected, a Perplexity key set; no Ahrefs, Semrush, Chrome or Brand Radar. Setup level: Recommended. | `config.yaml` |
| 2026-10-05 | Profile and research. No research existed, so all seven questions were researched; the brief was approved. | `profile.md`, `research/` |
| 2026-10-06 | Keywords: 20 found, 2 dropped for fit 0, 5 topics; 4 approved. | `keywords/` |
| 2026-10-06 | First weekly run: technical check, 12 AI questions to ChatGPT and Perplexity, 10 actions, report. | `technical/`, `visibility/`, `actions.md` |
| 2026-10-07, 10-10 | Daily quick technical checks | `technical/history.csv` |
| 2026-10-13 | Second weekly run. One action confirmed (canonical tags), one marked done by the owner but its check failed, one dismissed by the owner. | `reports/latest.md` |

Things worth noticing:

- **A wrong AI answer traced to its source.** ChatGPT says Northpine "ships worldwide". The answer cites the shipping page, which still has an old line "We ship worldwide (coming 2025)" (`visibility/2026-10-13.csv`, action A003).
- **A blocked search bot.** robots.txt blocks Claude-SearchBot, which reduces visibility in Claude's search results; GPTBot is also blocked, which only affects training and is left as the owner's decision (`technical/latest.md`).
- **Weaker sources are labelled.** Volumes are DataForSEO estimates, the JavaScript-only page is "inferred" because Chrome is not connected, and the report lists the engines that were not measured.
- **Noise is called noise.** Mention rates went up 8–9 points, but with 12 answers per engine the report does not call it a trend.
- **Zero-volume questions are kept.** "what are good alternatives to ridgeline for wide feet" has no search volume but is in the scored list and in `prompts.csv`.

## Shortened for the example

- 12 AI questions instead of the usual 30–100; 20 keywords.
- Only the second week's per-answer file (`visibility/2026-10-13.csv`) is included; `history.csv` has both weeks.
- Raw folders hold a few sample files, not every response. `technical/raw/2026-10-13/crawl.json` shows 2 of 120 pages.

## Check it

```bash
python scripts/check_site.py examples/example-site/northpine-running.example
```
