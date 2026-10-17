# Contributing

Thanks for helping. Issues and pull requests are welcome at [github.com/strategysoul/aeo-agent](https://github.com/strategysoul/aeo-agent).

## Before you open a pull request

Run the same checks as CI:

```bash
claude plugin validate --strict .
```

```bash
python -m pytest scripts/tests
```

```bash
python scripts/check_site.py examples/example-site/northpine-running.example
```

```bash
python scripts/scan_repo.py
```

The scripts and tests use only the Python standard library; pytest is optional (`python -m unittest discover -s scripts/tests` works too).

## What to keep in mind

- **Check provider docs, not memory.** Setup guides, recipes and crawler facts must match the provider's current documentation. Update the "Last checked" date and link the page you checked.
- **Formats are a contract.** If you change a file format in a skill, update `scripts/check_site.py` and the example site in the same pull request.
- **Every data point says where it came from** (`source`, `method`, `record_date`, `run_id`). New steps must follow `skills/aeo/references/rules.md`.
- **The agent recommends; it does not act.** No skill may change a site, CMS, DNS, CDN or tool settings, post anything, sign up for anything or contact anyone.
- **Nothing site-specific in skills.** Industries, countries and wording come from the site's profile and research, not from the skill text.
- **No real data in examples or tests.** Use `.example` domains and made-up businesses. Never commit keys, `.env` files or real site folders.
- **Skill size.** Keep each `SKILL.md` under about 3,000 words; move detail into `references/`. Refer to plugin files with `${CLAUDE_PLUGIN_ROOT}`.
- **Plain writing.** Short sentences, descriptive headings, no slogans.

## Adding a data source

1. A capability test in `skills/aeo-setup/references/capability-tests.md` (cheapest call; what to record).
2. A recipe for each step that uses it, and its place in the fallback order.
3. A setup guide in `docs/setup/` with the same sections as the others.
4. A row in `docs/data-sources.md` and `docs/costs.md`.

## Releases

Bump `version` in `.claude-plugin/plugin.json`, then tag `vX.Y.Z`. CI builds `aeo-agent.plugin` and attaches it to the GitHub release.
