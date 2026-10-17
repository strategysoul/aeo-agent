# Connect Ahrefs

Last checked: 2026-10-17, against [Ahrefs MCP docs](https://docs.ahrefs.com/mcp/docs/introduction) and the [Ahrefs help center](https://help.ahrefs.com/en/articles/13913559-getting-started-with-ahrefs-mcp).

## What it adds

Measured data in place of estimates:

| Step | What Ahrefs provides |
|---|---|
| Keyword discovery and scoring | search volume, keyword difficulty, related terms, search suggestions |
| Google results | the top results for a keyword, used to find competitors |
| Competitor keywords | organic competitors and the keywords they rank for |
| Technical health | Site Audit issues and health score, if you have a Site Audit project |
| AI visibility | brand mentions and citations in AI answers, with the Brand Radar add-on |

Without Ahrefs (or Semrush or DataForSEO), keyword volumes are estimated from Google results and autocomplete and labelled "inferred".

## Plan needed

Ahrefs MCP works on **Lite and higher** plans. Each plan has a monthly allowance of API units and a cap on rows per request. Figures from the Ahrefs help center on the date above:

| Plan | API units per month | Rows per request |
|---|---|---|
| Lite | 200,000 | 100 |
| Standard | 800,000 | 250 |
| Advanced | 2,000,000 | 500 |
| Enterprise | custom | unlimited |

- Each call costs at least 50 units. Larger requests cost more.
- Units are shared with Ahrefs Connect and direct API use.
- Keys created through the OAuth flow default to 200,000 units per month. A workspace admin can change this in the API keys report.
- AI-answer data needs the **Brand Radar** add-on, bought separately.

Current prices: [ahrefs.com/pricing](https://ahrefs.com/pricing).

The AEO agent spends at most 10% of your remaining units per site per run by default. Change this in the site's `config.yaml` under `budget`.

## Connect it

Ahrefs runs a remote MCP server at `https://api.ahrefs.com/mcp/mcp`. Local MCP setup is no longer supported, and the old `@ahrefs/mcp` npm package does not work with MCP keys.

### Claude desktop and Cowork

1. Open **Customize → Connectors** and click **+**.
2. Search for **Ahrefs** in the list of connectors and open its card.
3. Click **Connect**.
4. Choose your Ahrefs workspace and account.
5. In the consent window, click **Allow**.
6. Ahrefs now appears in your connectors list. Turn it on for the conversation where you run the AEO agent.

### Claude Code

1. In your terminal:

   ```bash
   claude mcp add ahrefs https://api.ahrefs.com/mcp/mcp -t http
   ```

   Add `--scope user` to use it in every project.
2. Start Claude Code and run `/mcp`.
3. Choose the Ahrefs server and start authentication.
4. Sign in to Ahrefs in the browser, choose a workspace and approve access.
5. Run `/mcp` again and check that Ahrefs shows as connected.

### Claude desktop, with an MCP key instead of the connector

1. In Ahrefs, open **Account settings → API keys** and click **Generate MCP key**.
2. In Claude desktop, open **Settings → Developer → Edit config**.
3. Add an Ahrefs entry under `mcpServers` in `claude_desktop_config.json`, following the format on the [Ahrefs Claude desktop page](https://docs.ahrefs.com/mcp/docs/claude-desktop-web), with your MCP key in place of the placeholder.
4. Save and restart Claude desktop.

Do not paste the key into chat, into this repo, or into any site folder.

## Check it worked

Run `/aeo-agent:aeo <your-domain> setup`. The Ahrefs row should show `available` with your plan, units left and row limit.

## Common errors

| What you see | Cause | Fix |
|---|---|---|
| 401 authentication error | key expired, subscription inactive, or the wrong kind of key | Regenerate the key. Renew the subscription. API keys and MCP keys are not interchangeable: use an MCP key for the MCP server. |
| `insufficient plan` or a report not available | the report needs a higher plan or an add-on (for example Brand Radar) | The agent falls back to the next source and labels the data. Upgrade only if you need that report. |
| A list comes back with exactly 100 (or 250, 500) rows | the plan's row cap | Expected. The agent pages through or marks the list as incomplete. |
| Units run out mid-month | monthly allowance used | Check **Account settings → Limits and usage**. Lower `budget.share_of_remaining` in `config.yaml`, or wait for the reset. |
| Competitor list empty for a new site | Ahrefs has little data on the domain yet | Expected for new sites. The agent takes competitors from Google results for its starting keywords instead. |

## Note on scripts

Ahrefs does not allow its MCP endpoint to be called from custom scripts or standalone HTTP clients. The AEO agent only calls Ahrefs through Claude's connector. For programmatic access, Ahrefs points to its public API.
