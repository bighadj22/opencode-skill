---
name: agent-team-setup
description: Scaffold a complete team of AI agents in any opencode project — coordinator, subagents, skills, custom tools, workspace, and config. Use when the user wants to automate a multi-step workflow, create an agent pipeline, or set up opencode agents.
license: Apache-2.0
compatibility: opencode
metadata:
  author: Bilal Mansouri
  version: "1.0.0"
  category: opencode-setup
---

# Agent Team Setup

Create a complete, production-ready opencode agent team for any project. This skill
scaffolds the full `.opencode/` directory: coordinator agent, subagents, skills, tools,
workspace, and the root `opencode.json` + `AGENTS.md` files.

## When to Use

- User wants to automate a multi-step workflow (research → plan → write → publish, etc.)
- User asks to "set up agents" or "create an agent pipeline"
- User wants opencode subagents that work together on a task
- User wants to replicate a working agent-team pattern in a new project

## Prerequisites

- The target project must already have opencode installed (`opencode` CLI available)
- The project should be a git repo (agents can commit/push)
- Python 3 must be installed (tools use Python scripts)

---

## Phase 0: Model & Provider Setup

Before planning the team, decide which LLM model the agents will use. This skill
defaults to **Cloudflare Workers AI** so the user needs **no OpenAI or Anthropic API
keys** to get started.

### 0.1 Default: Cloudflare Workers AI

The default model for all agents is:

```
cloudflare-workers-ai/@cf/zai-org/glm-5.2
```

This routes LLM inference through **Cloudflare's Workers AI Gateway** using the
GLM-5.2 model hosted on Cloudflare's edge. No external API keys are required.

**When to use the default:**
- The user does not specify a model or provider
- The user wants a free, no-API-key setup

**What to tell the user when using the default:**

> "Your agents will use Cloudflare Workers AI (`@cf/zai-org/glm-5.2`) as the LLM.
> No OpenAI or Anthropic API keys are needed. If you want to use a different
> provider, let me know and I'll switch the model."

### 0.2 Alternative: Custom Provider

If the user explicitly asks for a different provider/model, use that instead. Common
alternatives:

| Provider | Model ID example | When the user asks |
|---|---|---|
| Anthropic | `anthropic/claude-sonnet-4-5` | "Use Claude" / "Use Anthropic" |
| OpenAI | `openai/gpt-4o` | "Use OpenAI" / "Use GPT-4" |
| OpenCode Zen | (via `/connect`) | "Use opencode connect" / "Use my existing provider" |
| Google | `google/gemini-2.0-flash` | "Use Gemini" / "Use Google" |

If the user says "use opencode connect" or "use my existing provider", tell them to
run `/connect` in the OpenCode TUI to configure their provider, then use the model
they connected to. In this case, omit the `model` field from agent frontmatter so
agents inherit the global default.

### 0.3 Decision table

| Situation | What to do |
|---|---|
| User says nothing about model | Use `cloudflare-workers-ai/@cf/zai-org/glm-5.2` for all agents |
| User says "use Cloudflare" | Same as above |
| User names a specific model (e.g. "use Claude") | Use that model ID |
| User says "use opencode connect" / "use my provider" | Omit `model` field; agents inherit global config |
| User wants different models per agent | Assign per agent in frontmatter |

### 0.4 How the model appears in agent files

Every subagent `.md` file gets a `model:` field in its YAML frontmatter:

```yaml
model: cloudflare-workers-ai/@cf/zai-org/glm-5.2
```

If using a custom provider, replace the value with the user's chosen model ID. If
the user wants agents to inherit the global model, omit the `model` line entirely.

---

## Phase 1: Plan the Team

Before writing any files, gather the information below. Ask the user if anything is
unclear — do NOT guess.

### 1.1 What is the pipeline?

Ask: "What are the steps this agent team should perform from start to finish?"

Example answer: "Research a topic → write a blog post → generate images → publish it"

### 1.2 Identify the agents

Break the pipeline into 3-7 distinct roles. Each role becomes one subagent.

| Role type | When to use |
|---|---|
| Scout / Researcher | Gathers raw data from external sources |
| Planner / Analyst | Turns raw data into a structured plan |
| Creator / Writer | Produces the main output (article, code, document) |
| Specialist (image, SEO, test, etc.) | Does one specific task that needs special tools |
| Editor / Reviewer | Validates, formats, and polishes the output |
| Publisher / Deployer | Ships the output to production |
| Optimizer / Monitor | Post-publication maintenance and auditing |

### 1.3 Map the handoffs

For each agent, determine:
- **Input**: What does it receive? (topic, file path, URL, previous agent's output)
- **Output**: What does it produce? (file in workspace, URL, structured data)
- **Handoff mechanism**: Files in `.opencode/workspace/` (recommended) or inline in the task prompt

### 1.4 Identify custom tools

Does the pipeline need capabilities beyond what opencode + web search provides?

Common tool needs:
- Web scraping / search
- File analysis (NLP, keyword extraction)
- External API calls (image generation, translation, etc.)
- Platform-specific actions (deploy, upload, etc.)

Each tool = one Python script + one TypeScript wrapper.

### 1.5 Choose the model

**Default:** `cloudflare-workers-ai/@cf/zai-org/glm-5.2` (Cloudflare Workers AI — no
API keys needed). Use this for all agents unless the user asks for something else
(see Phase 0).

All agents can share the same model, or you can assign cheaper models to simple tasks
and smarter models to complex ones. If the user wants different models per agent, set
the `model:` field in each agent's frontmatter accordingly.

### 1.6 Set temperatures

| Temperature | Use for |
|---|---|
| 0.1-0.2 | Deployment, publishing, validation (deterministic) |
| 0.3 | Research, planning, editing (focused) |
| 0.5-0.7 | Creative writing, brainstorming (expressive) |

---

## Phase 2: Scaffold the Directory Structure

Create the following in the target project root:

```
.opencode/
  agents/          # One .md file per subagent
  skills/          # One subfolder per skill, each with SKILL.md
  tools/           # Pairs of .py + .ts files per custom tool
  workspace/       # Runtime artifacts (create subdirs as needed)
    research/      # Scout output
    briefs/        # Planner output
    drafts/        # Writer output
    reports/       # Audit/optimizer output
    data/          # Shared data files
  package.json     # @opencode-ai/plugin dependency
  requirements.txt # Python dependencies for tools
  .gitignore       # Ignore node_modules, etc.
```

### 2.1 Create `.opencode/package.json`

```json
{
  "dependencies": {
    "@opencode-ai/plugin": "latest"
  }
}
```

Then run `cd .opencode && npm install` (or let opencode handle it).

### 2.2 Create `.opencode/.gitignore`

```
node_modules
package-lock.json
bun.lock
```

### 2.3 Create workspace directories

```bash
mkdir -p .opencode/workspace/{research,briefs,drafts,reports,data}
```

Add a `.gitkeep` to each if the project is git-tracked and you want the structure
committed but empty.

---

## Phase 3: Create the Coordinator

The coordinator is the **primary** agent — the one the user talks to first. It does
NOT do work itself; it delegates to subagents in order.

### 3.1 Add to `opencode.json`

```json
{
  "$schema": "https://opencode.ai/config.json",
  "default_agent": "coordinator",
  "instructions": ["AGENTS.md"],
  "agent": {
    "coordinator": {
      "description": "Master orchestrator for the [PROJECT NAME] pipeline. Routes tasks to sub-agents in order.",
      "mode": "primary",
      "temperature": 0.2,
      "prompt": "You are the coordinator of [PROJECT DESCRIPTION].\n\nWhen the user gives you [INPUT TYPE], run the pipeline in order. At each step use the task tool with the matching subagent type and pass the [INPUT] (and any intermediate file paths) in your prompt. Do NOT do the agent's work yourself — delegate.\n\n1. Spawn the [AGENT_1] subagent with [INPUT]. It saves [OUTPUT_1] to [PATH_1] and returns a summary.\n2. Spawn the [AGENT_2] subagent with [OUTPUT_1_PATH]. It saves [OUTPUT_2] to [PATH_2].\n3. Continue for each agent in the pipeline...\n\nReport progress to the user after every step. If an agent fails or returns an error, stop and report the error to the user — never skip a step to work around a failure.\n\nIf the user asks for routine work unrelated to the pipeline, handle it directly or tell them what to do.",
      "permission": {
        "task": {
          "*": "deny",
          "[agent-1-name]": "allow",
          "[agent-2-name]": "allow",
          "[agent-3-name]": "allow"
        }
      }
    }
  }
}
```

Key rules for the coordinator prompt:
- List each step explicitly with the agent name and what it receives
- Say "do NOT do the agent's work yourself — delegate"
- Say "stop and report errors — never skip a step"
- Say "report progress after every step"
- Include a fallback instruction for non-pipeline tasks

### 3.2 Add MCP servers (optional)

If the project uses a framework with an MCP server (e.g. Astro docs), add it:

```json
{
  "mcp": {
    "mcp-server-name": {
      "type": "remote",
      "url": "https://mcp.example.com/mcp",
      "enabled": true
    }
  }
}
```

---

## Phase 4: Create Subagents

Each subagent is a `.md` file in `.opencode/agents/`. The filename must match the
agent's `name` field.

### 4.1 Agent file template

```markdown
---
name: [agent-name]
description: [One sentence: what this agent does, when to use it]
mode: subagent
model: [model-id]
temperature: [0.1-0.7]
permission:
  edit:
    "*": ask
    "[allowed-write-paths]": allow
  bash:
    "*": allow
    "[allowed-commands]": allow
---
# [Agent Display Name]

[One line: what project/context this agent serves]

## Mission

[One sentence: the core job of this agent]

## Input

- [What the agent receives: file path, topic, URL, etc.]

## Steps

1. [First action]
2. [Second action]
3. [Third action]
...

## Output

[What the agent produces and where it saves it]

## Rules

- [Boundary: what the agent must NOT do]
- [Quality: what the agent must ensure]
- [Scope: what the agent should stay within]
```

### 4.2 Permission patterns

| Permission | Pattern | Meaning |
|---|---|---|
| `edit: {"*": ask}` | Default | Ask before editing anything |
| `edit: {".opencode/workspace/research/**": allow}` | Scoped | Auto-allow writes to specific dirs |
| `edit: {"src/content/**": allow}` | Code dirs | Auto-allow writes to source files |
| `bash: {"*": allow}` | All bash | Allow any shell command |
| `bash: {"python3 .opencode/tools/*.py *": allow}` | Scoped | Allow only tool scripts |
| `bash: {"git *": allow}` | Git | Allow git operations |

### 4.3 Key principles for agent design

1. **Single responsibility**: Each agent does ONE thing well. Don't make an agent that
   both researches AND writes.
2. **Clear handoffs**: Agent A's output is Agent B's input. Use files in
   `.opencode/workspace/` as the handoff mechanism — the coordinator passes file paths.
3. **No overlap**: Don't have two agents that do the same thing.
4. **Explicit rules**: State what the agent must NOT do (e.g., "do not write the article,
   do not touch src/content/").
5. **Realistic permissions**: Only give write access to the directories the agent needs.

---

## Phase 5: Create Skills

Skills are knowledge documents — "how to" guides that agents (or the user) load for
context on a specific domain.

### 5.1 When to create a skill

Create a skill when:
- An agent needs domain-specific knowledge (e.g., writing style guide, SEO rules)
- A workflow has reusable steps that could be documented separately
- A capability spans multiple agents (e.g., R2 upload used by illustrator AND editor)

### 5.2 Skill file template

Create `.opencode/skills/[skill-name]/SKILL.md`:

```markdown
---
name: [skill-name]
description: [One sentence: what this skill teaches, when to use it]
---

# [Skill Display Name]

[Context: what project/domain this applies to]

## [Section: Key concept or workflow]

[Content: steps, rules, templates, examples]

## [Section: Another concept]

[Content]
```

### 5.3 Skill vs Agent: when to use which

| Use an **agent** when... | Use a **skill** when... |
|---|---|
| Work needs to be delegated automatically | Knowledge needs to be loaded on demand |
| The task is a distinct pipeline step | The knowledge spans multiple agents |
| It needs its own permissions/model | It's reference material, not executable work |
| It saves files to the workspace | It's a style guide, checklist, or template |

### 5.4 Linking skills to agents

Mention skills by name in agent instructions:
> "Follow the writing rules in the writer-style skill."

The coordinator or agent can load the skill using the skill tool when needed.

---

## Phase 6: Create Custom Tools

Tools are executable scripts wrapped as callable opencode tools. Each tool = one
Python script + one TypeScript wrapper.

### 6.1 Tool file structure

```
.opencode/tools/
  tool_name.py     # The actual logic
  tool_name.ts     # The opencode wrapper
```

### 6.2 Python script template

```python
#!/usr/bin/env python3
"""
[Tool description]
Usage: python3 tool_name.py <args>
"""
import sys
import json

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 tool_name.py <args>", file=sys.stderr)
        sys.exit(1)
    
    arg = sys.argv[1]
    # ... do the work ...
    result = {"arg": arg, "status": "ok"}
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
```

### 6.3 TypeScript wrapper template

```typescript
import { tool } from "@opencode-ai/plugin"
import path from "path"

export default tool({
  description: "[Tool description for the LLM]",
  args: {
    argName: tool.schema.string().describe("[arg description]"),
  },
  async execute(args, context) {
    const script = path.join(context.worktree, ".opencode/tools/tool_name.py")
    const result = await Bun.$`python3 ${script} ${args.argName}`.text()
    return result.trim()
  },
})
```

### 6.4 Tool design principles

1. **Python does the work**: All logic in `.py` file. The `.ts` file just calls it.
2. **JSON output**: Python scripts print JSON to stdout for structured results.
3. **Error handling**: Print errors to stderr, exit with code 1.
4. **No API keys in code**: Read from environment variables (`os.environ.get('KEY')`).
5. **One tool per file**: Don't combine multiple tools into one script.
6. **Idempotent**: Running the same tool twice should give the same result.

### 6.5 Python dependencies

List all Python package requirements in `.opencode/tools/requirements.txt`:

```
requests>=2.31.0
beautifulsoup4>=4.12.0
```

Install with: `pip3 install -r .opencode/tools/requirements.txt`

---

## Phase 7: Create AGENTS.md

The `AGENTS.md` file at the project root is the project-level instruction file. It
gives every agent (and the user's main session) context about the project.

### 7.1 Initialize with /init

You can create or update `AGENTS.md` automatically:

```
/init
```

The `/init` command scans your repository, may ask clarifying questions, and generates
concise project-specific guidance covering:
- Build, lint, and test commands
- Command order and verification steps
- Architecture and repository structure
- Project-specific conventions and operational gotchas

If `AGENTS.md` already exists, `/init` improves it in place instead of replacing it.

### 7.2 Template

```markdown
# [Project Name]

[One paragraph: what the project is, what the default agent does, and how to use it.]

## Commands

- `[build command]` - Build the project
- `[test command]` - Run tests
- `[lint command]` - Lint and format code
- `[deploy command]` - Deploy to production

## Repo map

| Path | What it is |
|---|---|
| `[source dir]/` | [What lives here] |
| `.opencode/agents/` | Pipeline subagents ([list names]) |
| `.opencode/skills/` | Project skills ([list names]) |
| `.opencode/tools/` | Custom tools ([list names]) |
| `.opencode/workspace/` | Pipeline artifacts: research/, briefs/, drafts/, reports/ |

## [Domain rules]

- [Rule 1: e.g., frontmatter schema constraints]
- [Rule 2: e.g., naming conventions]
- [Rule 3: e.g., what sources are allowed/banned]

## Deploy

`[build command]` → `[output dir]` ([hosting platform]). Push to `main` auto-deploys.

## Tooling conventions

- Python helpers: `python3 .opencode/tools/*.py` (run from repo root).
- Commit style: short imperative, e.g. `feat: description`.
```

### 7.3 Custom Instructions Array

For larger projects, use `opencode.json` to reference additional instruction files:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "instructions": [
    "CONTRIBUTING.md",
    "docs/guidelines.md",
    ".cursor/rules/*.md"
  ]
}
```

This avoids duplicating existing documentation into AGENTS.md. Supports glob patterns
for monorepos: `packages/*/AGENTS.md`

---

## Phase 8: Create Custom Commands (Optional)

Commands are reusable prompt templates that execute when you type `/command-name` in
the OpenCode TUI. They're useful for repetitive workflows in your agent pipeline.

### 8.1 When to Create Commands

Create commands for tasks your team runs frequently:
- Running the full pipeline on a topic
- Testing and reviewing output
- Analyzing recent changes
- Generating reports
- Deploying to production

### 8.2 Command File Template

Create markdown files in `.opencode/commands/`:

**.opencode/commands/run-pipeline.md:**
```markdown
---
description: Run the full content pipeline
agent: coordinator
---

Run the complete pipeline for topic: $ARGUMENTS

Execute each agent in sequence:
1. Scout research
2. Planner brief
3. Writer draft
4. Editor review
5. Publisher deploy

Report progress after each step.
```

Usage: `/run-pipeline "AI trends 2024"`

### 8.3 Command Features

**Arguments:** Use `$ARGUMENTS` or `$1`, `$2`, `$3` for positional parameters

**Shell output:** Use !```command``` to inject bash output:
```markdown
Recent changes:
!`git log --oneline -10`
```

**File references:** Use `@filename` to include file content:
```markdown
Review the component in @src/components/Button.tsx
```

### 8.4 Example Commands for Agent Teams

**.opencode/commands/status.md:**
```markdown
---
description: Check pipeline status
---

Check workspace status:
!`ls -la .opencode/workspace/*/`

Report which stages are complete and what's next.
```

**.opencode/commands/test-output.md:**
```markdown
---
description: Test and validate output
agent: editor
---

Review all output files:
!`find .opencode/workspace/final -type f`

Validate each file meets quality standards.
```

---

## Phase 9: Verify and Test

## Phase 9: Verify and Test

### 9.1 Verify structure

Check that all files exist:
```
opencode.json
AGENTS.md
.opencode/agents/[name].md (one per subagent)
.opencode/skills/[name]/SKILL.md (one per skill)
.opencode/tools/[name].py + [name].ts (one pair per tool)
.opencode/workspace/[subdir]/ (runtime dirs)
.opencode/package.json
.opencode/requirements.txt (if tools have Python deps)
```

### 9.2 Test the pipeline

1. Run `opencode` in the project directory.
2. Give the coordinator a test input.
3. Watch each subagent get spawned in order.
4. Check that workspace files are created at each step.
5. Verify the final output is correct.

### 9.3 Common issues

| Issue | Fix |
|---|---|
| Agent not found | Check `name` in agent .md matches the task subagent_type |
| Permission denied | Check the coordinator's `permission.task` whitelist |
| Tool not callable | Run `cd .opencode && npm install` for plugin deps |
| Python script fails | Check `requirements.txt` installed, check Python path |
| Model not found | Verify the model ID is valid for the opencode instance |

---

## Reference: Complete Example

Here is the full pattern from a working production setup (a content publishing pipeline):

### Pipeline
```
User → coordinator → scout → planner → writer → illustrator → editor → publisher
                                                                     ↓
                                                              Optimizer (on demand)
```

### opencode.json
```json
{
  "$schema": "https://opencode.ai/config.json",
  "default_agent": "coordinator",
  "model": "cloudflare-workers-ai/@cf/zai-org/glm-5.2",
  "instructions": ["AGENTS.md"],
  "mcp": {
    "docs-server": {
      "type": "remote",
      "url": "https://mcp.docs.example.com/mcp",
      "enabled": true
    }
  },
  "agent": {
    "coordinator": {
      "description": "Master orchestrator for the content pipeline.",
      "mode": "primary",
      "temperature": 0.2,
      "prompt": "You are the coordinator...\n\n1. Spawn scout...\n2. Spawn planner...\n3. Spawn writer...\n4. Spawn illustrator...\n5. Spawn editor...\n6. Spawn publisher...\n\nReport progress after every step. If an agent fails, stop and report.",
      "permission": {
        "task": {
          "*": "deny",
          "scout": "allow",
          "planner": "allow",
          "writer": "allow",
          "illustrator": "allow",
          "editor": "allow",
          "publisher": "allow",
          "optimizer": "allow"
        }
      }
    }
  }
}
```

### Agent file (scout.md)
```markdown
---
name: scout
description: Researches topics and saves a research brief.
mode: subagent
model: cloudflare-workers-ai/@cf/zai-org/glm-5.2
temperature: 0.3
permission:
  edit:
    "*": ask
    ".opencode/workspace/research/**": allow
    ".opencode/workspace/data/**": allow
  bash:
    "*": allow
    "python3 .opencode/tools/*.py *": allow
---
# Scout

## Mission
Turn a raw topic into a dated, sourced research file.

## Steps
1. Run `python3 .opencode/tools/search_web.py "<topic>"` to gather sources.
2. Extract hard facts: dates, names, numbers, quotes.
3. Save to `.opencode/workspace/research/{slug}.md`.

## Rules
- Research only. Do not write the article.
- Never invent facts. If missing, write "unavailable".
```

### Tool (search_web.ts)
```typescript
import { tool } from "@opencode-ai/plugin"
import path from "path"

export default tool({
  description: "Search the web for information.",
  args: {
    query: tool.schema.string().describe("Search query"),
  },
  async execute(args, context) {
    const script = path.join(context.worktree, ".opencode/tools/search_web.py")
    const result = await Bun.$`python3 ${script} ${args.query}`.text()
    return result.trim()
  },
})
```

### Skill (research-workflow/SKILL.md)
```markdown
---
name: research-workflow
description: Research workflow — web search, source grading, fact recording.
---

# Research Workflow

## Search
- `python3 .opencode/tools/search_web.py "<query>"`

## Grading sources
- Tier A: official statements
- Tier B: established outlets
- Tier C: blogs, forums — leads only

## Recording facts
Only write facts with a source. Note: what, when, who, URL.
```

---

## Checklist: Complete Agent Team Setup

- [ ] Model: Default to `cloudflare-workers-ai/@cf/zai-org/glm-5.2` unless user specifies otherwise
- [ ] Plan: pipeline steps, agents, handoffs, tools, model, temperatures
- [ ] Create `.opencode/` directory structure
- [ ] Create `.opencode/package.json` and run `npm install`
- [ ] Create `.opencode/.gitignore`
- [ ] Create workspace subdirectories
- [ ] Create `opencode.json` with coordinator (and provider/model if using Cloudflare default)
- [ ] Create `AGENTS.md` with project context (or run `/init`)
- [ ] Create one `.md` per subagent in `.opencode/agents/` (with Cloudflare model in frontmatter)
- [ ] Create one `SKILL.md` per skill in `.opencode/skills/[name]/`
- [ ] Create `.py` + `.ts` pairs per tool in `.opencode/tools/`
- [ ] Create `requirements.txt` for Python deps
- [ ] Create custom commands in `.opencode/commands/` (optional)
- [ ] Test the pipeline end-to-end
- [ ] Fix any issues from testing

---

## References

This skill includes comprehensive references extracted from the official opencode documentation. Use these when you need detailed information about specific opencode features while building agent teams.

- **[opencode-agents.md](references/opencode-agents.md)** - Complete agent configuration guide: agent types (primary/subagent), all configuration options (mode, model, temperature, steps, prompt, permissions, tools), built-in agents, per-agent permissions, task permissions for controlling subagent invocation, and navigation between agent sessions.

- **[opencode-skills.md](references/opencode-skills.md)** - Skill system documentation: file locations (.opencode/skills, .claude/skills, .agents/skills), frontmatter format, naming rules, discovery mechanism, permissions, per-agent overrides, and when to use skills vs agents.

- **[opencode-tools.md](references/opencode-tools.md)** - Custom tool creation guide: tool structure (TypeScript wrappers + Python scripts), tool() helper API, arguments with Zod/tool.schema, context object (agent, sessionID, messageID, directory, worktree), using Bun.$ for shell commands, Python tool patterns, and complete examples.

- **[opencode-commands.md](references/opencode-commands.md)** - Custom commands system: command creation (markdown files and JSON config), prompt features ($ARGUMENTS, positional parameters, shell output injection with !`command`, file references with @filename), configuration options (template, description, agent, subtask, model), built-in commands, and command examples for agent teams.

- **[opencode-rules.md](references/opencode-rules.md)** - Rules and instructions guide: AGENTS.md purpose and best practices, /init command for automatic generation, file locations and precedence (project, global, Claude Code compatibility), custom instructions array in opencode.json with glob patterns, remote URL support, referencing external files, and integration with agent teams.

- **[opencode-config.md](references/opencode-config.md)** - Complete opencode.json schema: all configuration locations and precedence order, config file format (JSON/JSONC), major options (models, agents, default_agent, subagent_depth, permissions, tools, commands, instructions, mcp, server, shell, sharing, snapshot, autoupdate, formatters, lsp, compaction, watcher, image attachments, policies, plugins, enabled/disabled providers), variable substitution ({env:VAR}, {file:path}), TUI configuration (tui.json), and managed settings for enterprise.

- **[opencode-permissions.md](references/opencode-permissions.md)** - Permission system guide: permission actions (allow/ask/deny), all available permissions (read, edit, glob, grep, list, bash, task, skill, lsp, question, webfetch, websearch, external_directory, doom_loop, todowrite), pattern matching rules (wildcards, home directory expansion), granular object syntax for path/command patterns, auto mode (--auto flag), per-agent permission overrides, task permissions for controlling subagent spawning, and common permission patterns.

- **[opencode-mcp.md](references/opencode-mcp.md)** - MCP server integration: local MCP servers (type, command, cwd, environment, timeout), remote MCP servers (type, url, headers, oauth, timeout), OAuth authentication (automatic/pre-registered/commands), managing MCP tools globally and per-agent, glob patterns for tool control, example MCP servers (Sentry, Context7, Grep by Vercel), and best practices.

- **[opencode-builtin-tools.md](references/opencode-builtin-tools.md)** - Built-in tools reference: all built-in tools (bash, edit, write, read, grep, glob, list, lsp, apply_patch, skill, todowrite, webfetch, websearch, question), special permissions (external_directory, doom_loop), tool internals (ripgrep, .gitignore, .ignore patterns), pattern support for each tool, default permissions, and tool management by agent.

When building agent teams, consult these references for:
- Detailed agent configuration options beyond the templates in this skill
- Advanced permission patterns for fine-grained control
- Complete MCP server setup including OAuth flows
- Custom tool API details and advanced patterns
- Full opencode.json schema and all available config options
- Commands system for creating reusable workflows
- AGENTS.md best practices and the /init command
