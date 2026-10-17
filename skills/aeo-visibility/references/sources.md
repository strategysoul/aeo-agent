# AI-answer sources, tried in this order

Pick a source per engine: for each engine, use the first source that is `available` and covers it. Different engines can use different sources in the same run. Record the source on every row.

| Engine | 1st | 2nd | 3rd | 4th |
|---|---|---|---|---|
| Google AI Overviews | Brand Radar | Nimble (Google AI agent, if listed) | DataForSEO Google results (`ai_overview` item) | Chrome (google.com) |
| Google AI Mode | Brand Radar | Nimble (`google_ai_mirror_prod_data` or similar) | — | Chrome (google.com, AI Mode) |
| ChatGPT | Brand Radar | `ask_engines.py` openai | Nimble (ChatGPT agent, if listed) | Chrome (chatgpt.com) |
| Perplexity | Brand Radar | `ask_engines.py` perplexity | — | Chrome (perplexity.ai) |
| Gemini | Brand Radar | `ask_engines.py` gemini | — | Chrome (gemini.google.com) |
| Claude | Brand Radar custom prompts | `ask_engines.py` anthropic | — | Chrome (claude.ai) |
| Copilot | Brand Radar | — | — | Chrome (copilot.microsoft.com) |

If no source covers an engine, skip it and list it under "Not measured" in the output. Only when no engine at all can be measured, use the last resort below.

## What each source measures

| Source | `method` | Notes to carry into the report |
|---|---|---|
| Brand Radar | `measured` | Ahrefs' own prompt sample; AI chatbot data refreshes about monthly, AI Overviews every few days. Custom prompts are your questions on your chosen schedule. |
| Nimble | `measured` | Captures the public answer page for the query. |
| DataForSEO Google results | `measured` | The AI Overview shown for that keyword and location at call time. |
| `ask_engines.py` | `measured` | API answers with web search on. They can differ from what the consumer apps show; the model used is in `model_used`. |
| Chrome session | `measured` | The user's logged-in account; answers can be personalised by memory and history. |
| Web search stand-in | `inferred` | Not an AI answer. Only shows which domains rank for the question. Label it "weak stand-in". |

## Brand Radar

Through the Ahrefs connector, tool groups `brand-radar-simple` (domain and URL reports) and `brand-radar-entities` (entity reports). Read each tool's schema before calling.

- For each engine it covers: mentions, citations, share of voice and impressions for the brand and the top 5 competitors from `research/competitors.csv`, filtered to the topics' keywords where the tool allows it.
- Cited pages and domains for the brand's topics.
- If the user tracks custom prompts in Brand Radar, read their latest answers instead of asking again. Do not create or change tracked prompts: that changes the user's Ahrefs settings. Suggest which prompts from `prompts.csv` to add, and let the user add them.
- Claude custom prompts cost 8 checks each (Ahrefs help center, 2026-10-17).
- Brand Radar calls use Ahrefs API units: budget them as in rules.md.

## Nimble

Through the Nimble connector (`nimble_*` tools). Use the agent tool to list available web search agents, and use only agents whose description says they return a named AI engine's answer and sources (for example Google AI Mode). Record the agent name in `source` (`nimble:<agent>`). Nimble web search agents cost $1 per 1,000 pages (Nimble blog, 2026-10-17); count one page per question.

## `ask_engines.py`

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/ask_engines.py" \
  --prompts "<site>/prompts.csv" --engines openai,perplexity \
  --country <countries[0]> --max-calls <budget> \
  --out "<site>/visibility/raw/<date>/api-answers.jsonl"
```

- Only engines whose key is `available` or `untested` in `config.yaml`.
- For each engine with `engines.<engine>.model` in `config.yaml`, add `--model <engine>=<model>`.
- `--max-calls` is `budget.engine_calls_per_run` (default 100) across all engines. Pass only active prompts (filter `prompts.csv` to `active = yes` into a temporary file in the run's raw folder).
- The script appends; each line has `prompt_id`, `engine`, `model_used`, `text`, `citations`, `error`.
- Rows with an `error` are not scored. If every row for an engine failed, set that engine's source status to `error` in `config.yaml` with the first error message.
- Rough cost per question, from provider pricing on 2026-10-17: Perplexity `sonar` about $0.005–0.012 request fee plus tokens; Anthropic web search $0.01 per search plus tokens; Gemini $0.014 per search query after 5,000 free a month; OpenAI web search has a per-call tool fee on its pricing page. Say in the output which engines were asked and how many calls were made.

## Chrome session

Use only when the user is present (interactive run) or has said scheduled runs may use Chrome.

- At most `budget.chrome_prompts_per_engine` questions per engine per run (default 20). Pick the questions from the highest-scoring topics first.
- Open a new chat for every question. Paste the question exactly as written in `prompts.csv`. Wait for the answer to finish, then read the answer text and every cited link.
- Do not log in. If a login page, paywall or CAPTCHA appears, stop for that engine and tell the user. Never try to solve a CAPTCHA.
- Do not change any settings in the AI tool (memory, personalisation, model choice).
- Save each answer to `visibility/raw/<date>/chrome-<engine>-<prompt_id>.md` with the URL of the chat and the time.

## Last resort: web search stand-in

Run each question through web search, record the top 10 domains, and score only `cited` (is the site's domain among them) and `competitors_mentioned` (competitor domains among them). Leave `mentioned`, `position`, `accuracy` and `sentiment` empty. `source: web_search`, `method: inferred`.
