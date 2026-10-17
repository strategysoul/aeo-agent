# Add Ahrefs Brand Radar

Last checked: 2026-10-17, against [What is Brand Radar](https://help.ahrefs.com/en/articles/11064852-what-is-brand-radar-and-how-to-use-it) and the [Ahrefs MCP tool categories](https://docs.ahrefs.com/mcp/docs/tool-categories).

## What it adds

Brand Radar is Ahrefs' AI-visibility tool. It is the first choice for AI answers in the visibility step because it covers the most engines with search-volume context.

| AI platform | Covered |
|---|---|
| Google AI Overviews and AI Mode | yes |
| ChatGPT, Perplexity, Gemini, Copilot | yes |
| Grok | yes (data collection temporarily paused on the date above) |
| Claude | custom prompts only; each Claude check uses 8 checks |

It reports share of voice, mentions, citations and impressions for your brand and competitors, and the pages and domains AI answers cite. With **custom prompts** it also tracks answers to your own questions, from monthly to daily.

Data freshness: AI Overviews every few days; AI chatbots about once a month; custom prompts on the schedule you choose.

## Price

Brand Radar needs an Ahrefs plan (see [ahrefs.md](ahrefs.md)) plus the **Brand Radar AI** add-on. On the date above:

| Option | Price |
|---|---|
| One AI platform index | $199 a month |
| All platforms, with 2,500 custom prompt checks | $699 a month |
| Extra custom prompt checks | $50 (2,500), $100 (7,000) or $250 (25,000) a month |

Lite and higher plans also include a small number of tracked custom prompts. Brand Radar calls through MCP also use Ahrefs API units. Current prices: [ahrefs.com/brand-radar](https://ahrefs.com/brand-radar).

## Connect it

There is nothing extra to connect. Once the add-on is on your Ahrefs account, the Ahrefs connector exposes the `brand-radar-simple` and `brand-radar-entities` tool groups. Set up the Ahrefs connector first with [ahrefs.md](ahrefs.md).

The agent reads Brand Radar but does not change it. To track the questions from your site's `prompts.csv` as custom prompts, add them in Ahrefs yourself; the visibility step suggests which ones.

## Check it worked

Run `/aeo-agent:aeo <your-domain> setup`. The Brand Radar row should show `available, via: ahrefs`. If Ahrefs shows `available` but Brand Radar shows `missing`, the add-on is not on the account, or the subscription response did not list it.

## Common errors

| What you see | Cause | Fix |
|---|---|---|
| `insufficient plan` or add-on error on a Brand Radar call | add-on not bought, or a platform index not included | Check the add-on in Ahrefs. The agent falls back to the next source for that engine. |
| Numbers barely change week to week for ChatGPT or Gemini | chatbot data refreshes about monthly | Expected. Use custom prompts or API keys for weekly changes. |
| Claude data missing | Claude is covered by custom prompts only | Add custom prompts for Claude, or use an Anthropic API key. |
