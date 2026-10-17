# Technical checks and what they mean

Facts below were checked against each operator's documentation on 2026-10-17. Re-check when writing a recommendation that depends on one.

## AI and search crawlers in robots.txt

| Token | Operator | Kind | What blocking it does | Docs |
|---|---|---|---|---|
| `Googlebot` | Google | search | Pages cannot be indexed, so they cannot appear in Google Search, AI Overviews or AI Mode. | [Google AI features](https://developers.google.com/search/docs/appearance/ai-features) |
| `Bingbot` | Microsoft | search | Pages drop out of Bing and the products that use its index. | |
| `OAI-SearchBot` | OpenAI | search | The site does not appear in ChatGPT search answers (it can still show as a navigational link). Changes take about 24 hours. | [OpenAI bots](https://developers.openai.com/api/docs/bots) |
| `PerplexityBot` | Perplexity | search | The site is not surfaced or linked in Perplexity results. Changes take up to 24 hours. | [Perplexity bots](https://docs.perplexity.ai/guides/bots) |
| `Claude-SearchBot` | Anthropic | search | The site appears less often in Claude's search results. | [Anthropic crawlers](https://support.claude.com/en/articles/8896518-does-anthropic-crawl-the-web) |
| `ChatGPT-User` | OpenAI | user | Fetches a page when a person asks; OpenAI says robots.txt rules may not apply. | OpenAI bots |
| `Perplexity-User` | Perplexity | user | Fetches a page when a person asks; generally ignores robots.txt. | Perplexity bots |
| `Claude-User` | Anthropic | user | Fetches a page when a person asks Claude; blocking it can reduce visibility in user-directed search. | Anthropic crawlers |
| `GPTBot` | OpenAI | training | Content is not used to train OpenAI's models. Does not control ChatGPT search. | OpenAI bots |
| `ClaudeBot` | Anthropic | training | Future content is excluded from Anthropic's training data. | Anthropic crawlers |
| `Google-Extended` | Google | training | Limits use for Gemini training and grounding. Google says it does not affect inclusion or ranking in Google Search. | [Google crawlers](https://developers.google.com/search/docs/crawling-indexing/google-common-crawlers) |

How to report:

- **A blocked `search` bot is an error.** It directly removes the site from that engine's answers. Recommend allowing it.
- **A blocked `user` bot is a warning.** Explain the trade-off; these bots may ignore robots.txt anyway.
- **A blocked `training` bot is information, not a fault.** It is a business decision. Say what it controls and do not recommend unblocking unless the user has said they want to be in training data. Note that `Google-Extended` also affects Gemini grounding.
- `robots.txt` answering 5xx or not at all: crawlers treat the whole site as blocked. Error.
- `bot_fetch` results (home page fetched with each bot's user-agent string) are indicative only: a firewall or CDN that checks bot IP addresses treats real bots differently. A 403 or a challenge page here is worth asking the hosting or CDN owner about, labelled `inferred`.

## Page-level issues from `crawl_check.py`

| Issue | Severity | Why it matters here |
|---|---|---|
| `http_error` | error | The page cannot rank or be cited. |
| `blocks_search_or_snippets` (`noindex`, `nosnippet`, `max-snippet:0`) | error if the page is in an approved topic, otherwise notice | Google requires a page to be indexed and snippet-eligible to be a supporting link in AI features. Some pages are meant to be hidden; check before calling it a fault. |
| `possibly_js_only` | warning | Very little text in the HTML before JavaScript runs. Some AI crawlers do not run JavaScript. Confirm with the rendered page (Chrome) before recommending a fix. |
| `missing_title`, `duplicate_title`, `h1_count`, `missing_canonical`, `canonical_elsewhere`, `redirect_chain`, `redirects_off_site`, `missing_description`, `long_title` | as set by the script | Standard SEO hygiene. Prioritise pages in approved topics. |

## llms.txt

`llms.txt` is a proposed format (llmstxt.org), not a standard. Google says sites do not need new machine-readable or AI text files, or special schema, to appear in AI Overviews or AI Mode. Report presence as information. Recommend creating one only as a low-effort, low-certainty action, and say that its effect is unproven.

## Structured data

Report the JSON-LD types found per page. Google says no special schema is needed for AI features, and structured data must match the visible text. Recommend schema only where it fits the page type (for example `Product` with price on product pages, `Organization` on the home page), as a normal SEO improvement, not as an AI requirement.

## Health score

- From Ahrefs or Semrush Site Audit: use their score as reported, with `source`.
- From the agent's own crawl: `100 × pages with no error ÷ pages checked`, labelled "own crawl". It is not comparable with Ahrefs or Semrush scores; keep separate series in `history.csv`.
