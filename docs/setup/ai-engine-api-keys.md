# Add AI-engine API keys (OpenAI, Perplexity, Gemini, Anthropic)

Last checked: 2026-10-17, against each provider's web search documentation: [OpenAI](https://developers.openai.com/api/docs/guides/tools-web-search), [Perplexity](https://docs.perplexity.ai/getting-started/models), [Gemini](https://ai.google.dev/gemini-api/docs/google-search), [Anthropic](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool).

## What they add

With a key, `scripts/ask_engines.py` asks that engine your questions with web search turned on and saves the answer and the pages it cited. The visibility step then scores each answer. The same questions every week give a repeatable trend.

| Key | Engine asked | Default model |
|---|---|---|
| `OPENAI_API_KEY` | OpenAI (ChatGPT's models) | `gpt-5.5` |
| `PERPLEXITY_API_KEY` | Perplexity Sonar | `sonar` |
| `GEMINI_API_KEY` | Google Gemini with Google Search | `gemini-3.8-flash` |
| `ANTHROPIC_API_KEY` | Claude with web search | `claude-opus-5-5` |

API answers can differ from what people see in the ChatGPT, Perplexity, Gemini or Claude apps, but they are the most repeatable measurement you can run yourself. One key is enough for the Recommended setup level; all four are part of the Full level.

## Cost

You pay each provider for what the script uses. Rates on the date above:

| Engine | Search fee | Plus |
|---|---|---|
| Perplexity `sonar` | $5–12 per 1,000 requests, depending on search context size | $1 per million input and output tokens |
| Anthropic | $10 per 1,000 searches (one question can trigger several, capped at 5 by the script) | standard token prices |
| Gemini | 5,000 search queries a month free, then $14 per 1,000 | standard token prices |
| OpenAI | a per-call web search tool fee, see the [pricing page](https://openai.com/api/pricing/) | standard token prices |

The agent asks at most `budget.engine_calls_per_run` questions per site per run (default 100), across all engines. Set a monthly spending limit in each provider's console as well.

## Get the keys

- **OpenAI:** [platform.openai.com/api-keys](https://platform.openai.com/api-keys). API billing is separate from a ChatGPT subscription.
- **Perplexity:** the API section of your Perplexity account settings. API credit is separate from Perplexity Pro.
- **Gemini:** [aistudio.google.com/apikey](https://aistudio.google.com/apikey).
- **Anthropic:** the API keys page of the [Claude Console](https://platform.claude.com/). API billing is separate from a Claude subscription.

Create a key used only for this agent, so you can see its spending and revoke it on its own.

## Set the keys

The keys must be environment variables where Claude runs commands. Never paste a key into chat, into a site folder, or into this repo.

**macOS or Linux** — add to `~/.zshrc` or `~/.bashrc`, then open a new terminal:

```bash
export OPENAI_API_KEY="..."
```

**Windows** — in PowerShell, then open a new terminal:

```powershell
setx OPENAI_API_KEY "..."
```

**Claude Code (CLI or the desktop app's Code tab):** start Claude Code from a terminal where the variables are set. Alternatively, put them under `env` in your user settings file `~/.claude/settings.json`. Never put them in a project's `.claude/settings.json`, which is often committed to git.

**Claude desktop chat and Cowork:** the script needs the variables in the environment where commands run. If they are not available there, the agent falls back to Brand Radar, Nimble or your Chrome session for AI answers.

The script itself needs only Python 3.9 or later; it uses no extra packages.

## Check it worked

```bash
python scripts/ask_engines.py --check
```

This makes free calls (listing models) for OpenAI, Gemini and Anthropic, and checks that the Perplexity key is set. It prints `available`, `missing`, `untested` or `error` for each engine. `/aeo-agent:aeo <your-domain> setup` runs the same check and shows the result in the setup table.

## Common errors

| What you see | Cause | Fix |
|---|---|---|
| `missing` although you set the key | the terminal or app was started before the key was set | Open a new terminal, or restart the app. |
| `HTTP 401` | wrong or revoked key | Create a new key and set it again. |
| `HTTP 429` | rate limit or no credit | The script retries once. Add credit or lower `budget.engine_calls_per_run`. |
| `HTTP 400` naming a model | the default model was retired or renamed | Run with `--model engine=<current model>`; the visibility step passes this through when `config.yaml` has `engines.<engine>.model`. |
| `model declined to answer` (Anthropic) | the model refused the question | The row is skipped; reword the question in `prompts.csv` if it keeps happening. |
| Perplexity shows `untested` | there is no free check call | Normal; the first real run confirms the key. |
