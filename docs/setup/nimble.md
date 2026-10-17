# Connect Nimble

Last checked: 2026-10-17, against the [Nimble MCP server docs](https://docs.nimbleway.com/integrations/mcp-server/mcp-server) and Nimble's [Google AI Mode guide](https://www.nimbleway.com/blog/scraping-google-ai-mode-for-llm-overviews-and-sources).

## What it adds

Nimble collects live web pages, including some AI answer pages, through its API.

| Step | What Nimble provides |
|---|---|
| AI visibility | answers and sources from Google AI Mode (and other AI answer pages where Nimble offers an agent for them), when Brand Radar does not cover the engine |
| Research | search, page extraction and crawling, for pages that block simple fetching |

What we could confirm: Nimble documents a web search agent for Google AI Mode that returns the answer text and its sources. We could not confirm agents for ChatGPT or Perplexity answers. The visibility step lists Nimble's agents at run time and uses only those that say they return a named AI engine's answer.

## Price

Nimble web search agents cost $1 per 1,000 pages, and new accounts start with 5,000 free pages (Nimble, on the date above). The agent counts one page per question. Current prices: [nimbleway.com/pricing](https://www.nimbleway.com/pricing).

## Connect it

Get an API key from your Nimble account. Set it as the environment variable `NIMBLE_API_KEY` (see [ai-engine-api-keys.md](ai-engine-api-keys.md#set-the-keys) for how).

The MCP server is at `https://mcp.nimbleway.com/mcp` and takes the key as `Authorization: Bearer <key>`.

### Claude Code

```bash
claude mcp add --transport http nimble-mcp-server https://mcp.nimbleway.com/mcp \
  --header "Authorization: Bearer ${NIMBLE_API_KEY}"
```

### Claude desktop

1. Open **Settings → Developer → Edit config**.
2. Add a `nimble` entry under `mcpServers` that runs `npx -y mcp-remote@latest https://mcp.nimbleway.com/mcp` with the header `Authorization: Bearer ${NIMBLE_API_KEY}` and your key in its `env` block, as shown on the [Nimble MCP page](https://docs.nimbleway.com/integrations/mcp-server/mcp-server). This needs Node.js.
3. Restart Claude desktop.

## Check it worked

Run `/aeo-agent:aeo <your-domain> setup`. Nimble shows `untested` until its first successful call, because setup does not spend pages on a test. After the first visibility or research run it shows `available`.

## Common errors

| What you see | Cause | Fix |
|---|---|---|
| 401 or unauthorized | key wrong, or `Bearer` typed into the key value | Store the raw key; the `Bearer ` prefix belongs in the header only. |
| No Nimble tools in Claude | connector not loaded | Restart the app after editing the config; check Node.js is installed for the desktop config. |
| No agent for an engine | Nimble has no agent for that AI engine | Expected. The agent uses the next source for that engine. |
