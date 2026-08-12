# {{PROJECT_NAME}}

{{PROJECT_DESCRIPTION}}

The default agent here is the **coordinator**: it runs the {{PIPELINE_NAME}} pipeline ({{AGENT_LIST}). For routine code work, switch to the build agent.

## Repo map

| Path | What it is |
|---|---|
| `{{SOURCE_DIR}}/` | {{SOURCE_DESCRIPTION}} |
| `.opencode/agents/` | Pipeline subagents ({{AGENT_LIST}}) |
| `.opencode/skills/` | Project skills: {{SKILL_LIST}} |
| `.opencode/tools/` | Custom tools: {{TOOL_LIST}} |
| `.opencode/workspace/` | Pipeline artifacts: {{WORKSPACE_DIRS}} |

## {{DOMAIN_RULES_HEADER}}

- {{RULE_1}}
- {{RULE_2}}
- {{RULE_3}}

## Deploy

`{{BUILD_COMMAND}}` → `{{OUTPUT_DIR}}` ({{HOSTING_PLATFORM}}). Push to `main` auto-deploys.

## Tooling conventions

- Python helpers: `python3 .opencode/tools/*.py` (run from repo root).
- Commit style: short imperative, e.g. `feat: description`.
