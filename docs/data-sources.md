# Data sources and fallbacks

Each need has an order of sources. The agent uses the first one that is connected and working, falls back to the next on an error, and labels the result.

| Need | Sources, in order | Last resort |
|---|---|---|
| Keyword volume, difficulty, intent | Ahrefs → Semrush → DataForSEO | Demand bands from Search Console, autocomplete and "People also ask", labelled `inferred` |
| Google results for a keyword | Ahrefs → Semrush → DataForSEO | Chrome or web search |
| Competitor keywords | Ahrefs → Semrush → DataForSEO | Competitor page titles and headings |
| Competitor ads and their wording | Google Ads Transparency Center through Chrome → DataForSEO (if its docs list an endpoint) → web fetch | Not checked, said in the output. Keywords from ads are always `inferred`: the Center shows ads, not the keywords they target |
| Own rankings and clicks | Google Search Console → Ahrefs / Semrush | Rank checks in Google results |
| Technical health | Ahrefs Site Audit → Semrush Site Audit, plus always the agent's own crawl | Own crawl only |
| AI answers and citations | Brand Radar → Nimble → engine APIs (`ask_engines.py`) → Chrome | Web search as a weak stand-in, labelled as such |
| Market research | Web search and fetch → Firecrawl → Nimble | — |

The AI-answer order is chosen per engine; the full table is in [skills/aeo-visibility/references/sources.md](../skills/aeo-visibility/references/sources.md).

## What `method` means

| Value | Meaning | Example |
|---|---|---|
| `measured` | The tool or page reports it directly | Search Console clicks; an AI answer's citations |
| `estimated` | A provider's model | Keyword search volume |
| `inferred` | The agent worked it out | Demand band from autocomplete; a page that probably needs JavaScript |

## Limits the agent handles

- **Row caps.** A response with exactly the plan's row limit is treated as cut off: the agent pages through or marks the list incomplete.
- **Plan or add-on errors.** Recorded in `config.yaml`; that need moves to the next source.
- **No competitors for a new site.** Competitors come from Google results for the starting keywords instead.
- **Provider terms.** Some providers (Ahrefs among them) do not allow their MCP endpoint to be called from scripts. All MCP calls stay inside Claude; scripts only call AI-engine APIs and your own site.

## Setup guides

[Ahrefs](setup/ahrefs.md) · [Brand Radar](setup/brand-radar.md) · [Semrush](setup/semrush.md) · [DataForSEO](setup/dataforseo.md) · [Search Console](setup/google-search-console.md) · [AI-engine API keys](setup/ai-engine-api-keys.md) · [Nimble](setup/nimble.md) · [Claude in Chrome](setup/claude-in-chrome.md) · [Scheduling](setup/scheduling.md)

Firecrawl has no guide yet: set `FIRECRAWL_API_KEY` or connect its MCP server, and the research step uses it when web fetch fails.
