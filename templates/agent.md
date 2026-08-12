---
name: {{AGENT_NAME}}
description: {{AGENT_DESCRIPTION}}
mode: subagent
model: cloudflare-workers-ai/@cf/zai-org/glm-5.2
temperature: {{TEMPERATURE}}
permission:
  edit:
    "*": ask
    "{{WRITE_PATHS}}": allow
  bash:
    "*": allow
    "{{BASH_PATTERNS}}": allow
---
# {{Agent Display Name}}

{{PROJECT_CONTEXT}}

## Mission

{{MISSION}}

## Input

- {{INPUT_DESCRIPTION}}

## Steps

1. {{STEP_1}}
2. {{STEP_2}}
3. {{STEP_3}}
4. {{STEP_4}}

## Output

{{OUTPUT_DESCRIPTION}}

## Rules

- {{RULE_1}}
- {{RULE_2}}
- {{RULE_3}}
