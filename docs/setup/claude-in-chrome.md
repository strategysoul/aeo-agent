# Connect Claude in Chrome

Last checked: 2026-10-17, against [Use Claude Code with Chrome](https://code.claude.com/docs/en/chrome) and [Getting started with Claude in Chrome](https://support.claude.com/en/articles/12012173-getting-started-with-claude-in-chrome).

## What it adds

Claude in Chrome lets the agent use your own browser, with the sites you are already logged into.

| Step | What it provides |
|---|---|
| AI visibility | reads answers from AI tools you are logged into (for example ChatGPT, Perplexity, Gemini) when no API key or AI-visibility source is set up |
| Research | reads pages that need JavaScript to show their content |
| Search Console | one-off reads of your Search Console reports if no connector is set up |

Answers read this way reflect your logged-in account, which may be personalised. Reports label them with the source `chrome:<site>`.

## Plan needed

A Claude **Pro, Max, Team or Enterprise** plan. The extension is free. On Team and Enterprise, an admin can turn it off or limit which sites it can use. Plans: [claude.com/pricing](https://claude.com/pricing).

## Install the extension

1. Use Google Chrome. Claude Code also supports Microsoft Edge and detects other Chromium browsers (Brave, Arc, Vivaldi, Opera); Anthropic's support page lists Chrome only for the extension itself.
2. Install [Claude in Chrome](https://chromewebstore.google.com/detail/claude/fcoeoabgfenejglbffodgkkbkcdhcgfn) from the Chrome Web Store.
3. Sign in with the same Claude account and organization you use in the desktop app or Claude Code.
4. Pin the extension and grant the permissions it asks for.

## Connect it

### Claude desktop and Cowork

1. Open **Settings → Connectors**, select **Claude in Chrome**, click **Configure** and turn it on.
2. It is off by default in each conversation. Turn it on from the Connectors menu in the conversation where you run the AEO agent.
3. Cowork also has its own built-in browser. To have Cowork use Chrome, set **Settings → Cowork → Preferred browser**.

### Claude Code

1. Sign in with `/login`. Chrome integration does not work when Claude Code uses an API key or a token from `claude setup-token`.
2. Start Claude Code with:

   ```bash
   claude --chrome
   ```

3. To connect every time without the flag, run `/chrome` and choose **Enabled by default**. This loads the browser tools into every session, which uses more context.
4. Not available in WSL, or through Amazon Bedrock, Google Cloud or Microsoft Foundry.

## Before the visibility step

Log in to the AI tools you want checked (ChatGPT, Perplexity, Gemini, and so on) in the same Chrome profile. The agent does not log in for you, and it pauses if it meets a login page or a CAPTCHA.

## Check it worked

- Claude Code: `/chrome` shows "Status: Enabled" and "Extension: Installed".
- Then run `/aeo-agent:aeo <your-domain> setup`. The Claude in Chrome row should show `available`.

## Common errors

| What you see | Cause | Fix |
|---|---|---|
| "Browser extension is not connected" | extension not running, or signed in to a different Claude account or organization | Check that the extension and Claude use the same account and organization (`/status` shows the organization in Claude Code). Restart Chrome and Claude, then run `/chrome` → Reconnect extension. |
| Extension shows "Not detected" | extension missing or disabled | Install or enable it at `chrome://extensions`. On the first install, restart Chrome so it picks up the connection settings. |
| "Receiving end does not exist" | the extension went idle during a long session | Run `/chrome` → Reconnect extension. |
| "No tab available" | Claude acted before a tab was ready | Ask Claude to open a new tab and try again. |
| Browser stops responding | a pop-up dialog on the page is blocking it | Close the dialog yourself, then tell Claude to continue. |
| Windows: named pipe error (`EADDRINUSE`) | another Claude Code session is using Chrome | Close other sessions and restart Claude Code. |
