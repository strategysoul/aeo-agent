# Connect Google Search Console

Last checked: 2026-10-17.

## What it adds

Search Console is Google's own record of how your site appears in Google Search. It is free.

| Step | What Search Console provides |
|---|---|
| Keyword discovery | the queries people already find you with, including ones no SEO tool lists |
| Tracking | your clicks, impressions, click-through rate and average position, measured by Google |
| Technical health | index status of pages, submitted sitemaps |

Without it, the agent checks your rankings itself in Google results, which is slower, covers fewer keywords and is labelled as a weaker source.

## What you need

- A Google account with access to the site's Search Console property. Free.
- If the site is not in Search Console yet, verify it first (below).

## 1. Verify the site (skip if you already see it in Search Console)

1. Go to [search.google.com/search-console](https://search.google.com/search-console) and add a property.
2. Choose **Domain** (covers every subdomain and both http and https; needs a DNS record) or **URL prefix** (one exact address; several ways to verify, such as an HTML file or meta tag).
3. Follow Google's verification steps: [Verify your site ownership](https://support.google.com/webmasters/answer/9008080).
4. New properties take a few days to collect data.

The AEO agent never changes DNS or your site. You add the verification record yourself.

## 2. Connect Search Console to Claude

Google does not publish an official Search Console MCP server (as of the date above). Every connector is third-party code that calls the [Search Console API](https://developers.google.com/webmaster-tools). Before you connect one:

- Check who runs it, whether the code is public, and when it was last updated.
- Prefer a read-only connector. The AEO agent only needs to list properties and read search analytics, plus URL inspection if available.
- You are giving it access to your Search Console data through Google sign-in. You can remove that access later at [myaccount.google.com/permissions](https://myaccount.google.com/permissions).

### Claude desktop and Cowork

1. Open **Customize → Connectors** (or **Settings → Connectors**) and choose to add a custom connector.
2. Paste the connector's server URL from its documentation.
3. Click **Add**, then sign in with the Google account that has access to the property.
4. Turn the connector on in the conversation where you run the AEO agent.

### Claude Code

1. In your terminal, add the connector's server URL:

   ```bash
   claude mcp add --transport http search-console <server-url>
   ```

   Add `--scope user` to use it in every project.
2. Start Claude Code, run `/mcp`, choose `search-console` and complete Google sign-in.

Self-hosted connectors that use your own Google Cloud OAuth credentials need extra steps: create a Google Cloud project, enable the Search Console API, and create OAuth credentials. Follow that connector's own guide.

### No connector: reading it in Chrome

If you have Claude in Chrome and are logged into Search Console, the agent can read the Performance report in your browser for one-off checks. This is slower, limited to what the page shows, and does not count as a connected source in the setup table.

## Check it worked

Run `/aeo-agent:aeo <your-domain> setup`. The Search Console row should show `available` and the property it matched, for example `sc-domain:example.com`.

## Common errors

| What you see | Cause | Fix |
|---|---|---|
| `no property for this domain` | the Google account you signed in with has no access to this site, or the property uses a different address (`www.`, `http://`) | Sign in with the account that owns the property, or ask the owner to add you as a user in Search Console → Settings → Users and permissions. |
| Data is empty | property was added recently | Wait a few days. Search Console does not backfill data from before the property was added. |
| Recent days missing | Search Console data lags by about two days | Expected. The agent reports the latest available date. |
| Permission or 403 errors | you have restricted access, or the connector's sign-in expired | Ask for full access on the property, or reconnect the connector. |
