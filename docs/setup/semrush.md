# Connect Semrush

Last checked: 2026-10-17, against [Semrush MCP](https://developer.semrush.com/api/basics/semrush-mcp/) and [API unit balance](https://developer.semrush.com/api/basics/api-units-balance/).

## What it adds

The same kind of data as Ahrefs. You need only one of Ahrefs, Semrush or DataForSEO.

| Step | What Semrush provides |
|---|---|
| Keyword discovery and scoring | search volume, keyword difficulty, intent, related and question keywords |
| Google results | top results for a keyword with SERP features, used to find competitors and AI Overviews |
| Competitor keywords | organic competitors and the keywords they rank for |
| Technical health | Site Audit results (read-only) |

## Plan needed

The MCP server is free to connect, but every query uses **API units** from your Semrush subscription. Plans that include API units, according to Semrush on the date above:

- **Included (50,000 API units, refreshed on renewal):** Semrush One Starter, Semrush One Pro+, SEO Classic Pro, SEO Classic Guru
- **With an API units package (2M, 5M, 10M or 20M units):** SEO Classic Business, Semrush One Advanced
- **Trends API** (traffic and market data) is a separate subscription. The AEO agent does not need it.

Most reports charge per line returned; Domain Organic Search Keywords costs 10 units per line. The agent spends at most 10% of your remaining units per site per run by default (`budget` in `config.yaml`).

Current prices: [semrush.com/prices](https://www.semrush.com/prices/).

## Connect it

The server is at `https://mcp.semrush.com/v2/mcp` (streamable HTTP, OAuth by default).

### Claude desktop and Cowork

1. Open **Customize → Connect your apps** (or **Connectors**).
2. Search for **Semrush** and click **Connect**.
3. Sign in to Semrush and approve access.
4. Semrush now appears under Connectors. Turn it on in the conversation where you run the AEO agent.

### Claude Code

1. In your terminal:

   ```bash
   claude mcp add semrush https://mcp.semrush.com/v2/mcp -t http
   ```

   Add `--scope user` to use it in every project.
2. Start Claude Code, run `/mcp`, select Semrush and choose **Authenticate**.
3. Complete the Semrush login in the browser.

### Optional: let the agent read your unit balance

Semrush MCP has no tool for the remaining unit balance. If you set your API key as an environment variable, the agent reads the balance with Semrush's free balance call before and after each run, and budgets exactly:

1. Find your key in Semrush under **Subscription info → API units**.
2. Set it as `SEMRUSH_API_KEY` in your shell profile, or in a `.env` file outside any shared folder. Never paste it into chat.

Without the key, read the balance yourself at **My Profile → Subscription info → Summary** and put it in `config.yaml` → `capabilities.sources.semrush.units_left`, or set `budget.hard_cap_units`.

## Check it worked

Run `/aeo-agent:aeo <your-domain> setup`. The Semrush row should show `available`, with units left if the API key is set.

## Common errors

| What you see | Cause | Fix |
|---|---|---|
| `redirect URI … is not allowed` | Semrush has not allowed your client's OAuth redirect | Contact Semrush support with the client name and the redirect URI shown. |
| Error 400 during sign-in | stale login cookies | Clear Semrush cookies in your browser and start the sign-in again. |
| Not redirected to the Semrush login | the client could not open the browser | Open the URL the client shows by hand. |
| Tools missing | sign-in not finished, or no API access on your plan | Finish authentication; check your plan includes API units. |
| Queries fail or return nothing | no API units left, or the report needs another API (for example Trends) | Check **Subscription info → Summary**. The agent falls back to the next source. |
| Lists stop at the number of lines asked for | expected | The agent pages through or marks the list as incomplete. |
