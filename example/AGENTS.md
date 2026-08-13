# Tech News Daily Digest

This project is an OpenCode agent team that turns the current Hacker News top
stories into a source-grounded daily Markdown digest. The default `coordinator`
agent delegates all pipeline work to `scout`, `researcher`, `summarizer`,
`curator`, and `publisher` in that order. Run the team with `/run-digest` or ask
the coordinator for a daily digest.

## Commands

- `npm --prefix .opencode install` - Install the OpenCode plugin dependency
- `python3 -m pip install -r .opencode/requirements.txt` - Install Python tool dependencies
- `python3 -m py_compile .opencode/tools/fetch_hn.py .opencode/tools/scrape_articles.py` - Check Python syntax
- `opencode` - Start the OpenCode TUI with the coordinator
- `opencode run "/run-digest"` - Run the digest command non-interactively when provider credentials are configured

## Repo Map

| Path | What it is |
|---|---|
| `opencode.json` | Project OpenCode configuration and coordinator |
| `.opencode/agents/` | Five pipeline subagents |
| `.opencode/skills/` | Source-research and digest-formatting guidance |
| `.opencode/tools/` | Python API/scraping tools and TypeScript wrappers |
| `.opencode/workspace/data/` | Raw Hacker News API handoff |
| `.opencode/workspace/research/` | Scraped article-content handoff |
| `.opencode/workspace/briefs/` | Structured summaries handoff |
| `.opencode/workspace/drafts/` | Curated Markdown draft |
| `.opencode/workspace/reports/` | Reserved for future audits |
| `output/` | Published daily digest Markdown files |

## Pipeline Rules

- The scout uses only the free Hacker News Firebase API; no API key is needed.
- The researcher uses `requests` and `BeautifulSoup` through `scrape_articles`.
- Every handoff is a file under `.opencode/workspace/`; agents must return the exact path.
- Summaries must contain only facts supported by the scraped article content.
- Failed fetches remain explicitly marked as unavailable; agents must not invent replacements.
- The publisher copies validated digest content to `output/` and does not deploy externally.
- Generated workspace artifacts are ignored by `.opencode/.gitignore`; `.gitkeep` files preserve the directory layout.

## Tooling Conventions

- Run Python helpers from the repository root, for example `python3 .opencode/tools/fetch_hn.py` (defaults to 10) or `python3 .opencode/tools/fetch_hn.py 10`.
- Python tools emit structured JSON to stdout and errors to stderr.
- TypeScript wrappers are loaded by OpenCode from `.opencode/tools/` and invoke the Python scripts.
- All agents are pinned to `opencode/deepseek-v4-flash-free`.
- Keep an explicit `model: opencode/deepseek-v4-flash-free` in every agent file and in the coordinator configuration; do not rely on inheritance by accident.
- All agents use low temperatures between `0.2` and `0.3`.
