# opencode: Agents

> Source: https://opencode.ai/docs/agents

Agents are specialized AI assistants that can be configured for specific tasks and workflows in OpenCode. They allow you to create focused tools with custom prompts, models, and tool access.

## Agent Types

### Primary Agents

Primary agents are the main assistants you interact with directly. You can cycle through them using the Tab key or your configured `switch_agent` keybind.

**Built-in primary agents:**
- **Build** - Default agent with all tools enabled for full development work
- **Plan** - Restricted agent for planning and analysis (file edits and bash set to "ask")
- **Compaction** - Hidden system agent for context compaction
- **Title** - Hidden system agent for session title generation
- **Summary** - Hidden system agent for session summaries

### Subagents

Subagents are specialized assistants that primary agents can invoke for specific tasks. You can also manually invoke them by @ mentioning them.

**Built-in subagents:**
- **General** - General-purpose agent for researching complex questions and executing multi-step tasks (full tool access except todo)
- **Explore** - Fast, read-only agent for exploring codebases
- **Scout** - Read-only agent for external docs and dependency research

## Configuration

Agents can be configured in two ways:

### JSON Configuration

In `opencode.json`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "agent": {
    "code-reviewer": {
      "description": "Reviews code for best practices and potential issues",
      "mode": "subagent",
      "model": "anthropic/claude-sonnet-4-20250514",
      "prompt": "You are a code reviewer. Focus on security, performance, and maintainability.",
      "permission": {
        "edit": "deny"
      }
    }
  }
}
```

### Markdown Configuration

Create files in `~/.config/opencode/agents/` or `.opencode/agents/`:

**~/.config/opencode/agents/review.md:**
```markdown
---
description: Reviews code for quality and best practices
mode: subagent
model: anthropic/claude-sonnet-4-20250514
temperature: 0.1
permission:
  edit: deny
  bash: deny
---

You are in code review mode. Focus on:

- Code quality and best practices
- Potential bugs and edge cases
- Performance implications
- Security considerations

Provide constructive feedback without making direct changes.
```

The markdown filename becomes the agent name (e.g., `review.md` creates a `review` agent).

## Configuration Options

### description (required)

Brief description of what the agent does and when to use it.

```json
{
  "agent": {
    "review": {
      "description": "Reviews code for best practices and potential issues"
    }
  }
}
```

### mode

Controls how the agent can be used. Options:
- `"primary"` - Main assistant for direct interaction
- `"subagent"` - Specialized assistant invoked by primary agents
- `"all"` - Can be used as both (default if not specified)

```json
{
  "agent": {
    "review": {
      "mode": "subagent"
    }
  }
}
```

### model

Override the model for this agent. If not specified:
- Primary agents use the globally configured model
- Subagents use the model of the primary agent that invoked them

Model ID format: `provider/model-id` (e.g., `anthropic/claude-haiku-4-20250514`)

```json
{
  "agent": {
    "plan": {
      "model": "anthropic/claude-haiku-4-20250514"
    }
  }
}
```

### temperature

Control randomness and creativity of responses (0.0-1.0):
- **0.0-0.2**: Very focused and deterministic (code analysis, planning)
- **0.3-0.5**: Balanced with some creativity (general development)
- **0.6-1.0**: More creative and varied (brainstorming, exploration)

If not specified, OpenCode uses model-specific defaults (typically 0, or 0.55 for Qwen models).

```json
{
  "agent": {
    "analyze": {
      "temperature": 0.1
    },
    "brainstorm": {
      "temperature": 0.7
    }
  }
}
```

### steps (max_steps)

Maximum number of agentic iterations before forcing text-only response. Useful for cost control.

```json
{
  "agent": {
    "quick-thinker": {
      "description": "Fast reasoning with limited iterations",
      "steps": 5
    }
  }
}
```

Default is unlimited. Legacy `maxSteps` field is deprecated.

### prompt

Path to custom system prompt file (relative to config file location).

```json
{
  "agent": {
    "review": {
      "prompt": "{file:./prompts/code-review.txt}"
    }
  }
}
```

### disable

Set to `true` to disable the agent.

```json
{
  "agent": {
    "review": {
      "disable": true
    }
  }
}
```

### hidden

Hide a subagent from `@` autocomplete menu. Only applies to `mode: subagent` agents. Hidden agents can still be invoked by the model via the Task tool if permissions allow.

```json
{
  "agent": {
    "internal-helper": {
      "mode": "subagent",
      "hidden": true
    }
  }
}
```

### color

Customize visual appearance in the UI. Use hex color or theme color name.

```json
{
  "agent": {
    "creative": {
      "color": "#ff6b6b"
    },
    "code-reviewer": {
      "color": "accent"
    }
  }
}
```

Theme colors: `primary`, `secondary`, `accent`, `success`, `warning`, `error`, `info`

### top_p

Alternative to temperature for controlling response diversity (0.0-1.0).

```json
{
  "agent": {
    "brainstorm": {
      "top_p": 0.9
    }
  }
}
```

### permission

Control what actions an agent can take. Each permission can be:
- `"allow"` - Run without approval
- `"ask"` - Prompt for approval
- `"deny"` - Block the action

**Available permission keys:**
- `read` - Reading files
- `edit` - File modifications (write, edit, apply_patch)
- `glob` - File pattern matching
- `grep` - Content search
- `list` - Directory listing
- `bash` - Shell commands
- `task` - Task tool (spawning subagents)
- `external_directory` - Access outside project worktree
- `todowrite` - Todo list management
- `webfetch` - Fetching web content
- `websearch` - Web search
- `lsp` - LSP server interactions
- `skill` - Loading skills
- `question` - Asking user questions
- `doom_loop` - Recovery when agent appears stuck

**Simple permissions:**

```json
{
  "agent": {
    "build": {
      "permission": {
        "edit": "ask",
        "bash": "allow"
      }
    }
  }
}
```

**Pattern-based permissions (for bash, edit, etc.):**

```json
{
  "agent": {
    "build": {
      "permission": {
        "bash": {
          "*": "ask",
          "git status *": "allow",
          "git diff": "allow",
          "grep *": "allow"
        },
        "edit": {
          "*": "deny",
          "src/content/**": "allow"
        }
      }
    }
  }
}
```

Pattern rules:
- `*` matches zero or more characters
- `?` matches exactly one character
- Last matching rule wins
- Put `*` wildcard first, then specific rules

**Task permissions (controlling subagent invocation):**

```json
{
  "agent": {
    "orchestrator": {
      "permission": {
        "task": {
          "*": "deny",
          "orchestrator-*": "allow",
          "code-reviewer": "ask"
        }
      }
    }
  }
}
```

When set to `deny`, the subagent is removed from the Task tool description entirely.

**Markdown agent permissions:**

```markdown
---
description: Code review without edits
mode: subagent
permission:
  edit: deny
  bash:
    "*": ask
    "git diff": allow
    "git log*": allow
    "grep *": allow
  webfetch: deny
---
```

### tools (deprecated)

Legacy field for controlling tool access. Use `permission` instead.

`true` is equivalent to `{"*": "allow"}` permission  
`false` is equivalent to `{"*": "deny"}` permission

```json
{
  "agent": {
    "plan": {
      "tools": {
        "write": false,
        "bash": false,
        "mymcp_*": false
      }
    }
  }
}
```

### Additional Options

Any other options are passed directly to the provider as model options (e.g., OpenAI's reasoning models):

```json
{
  "agent": {
    "deep-thinker": {
      "model": "openai/gpt-5",
      "reasoningEffort": "high",
      "textVerbosity": "low"
    }
  }
}
```

## Usage

### Primary Agents

- Use Tab key to cycle through primary agents during a session
- Or use configured `switch_agent` keybind

### Subagents

Subagents can be invoked:
1. **Automatically** by primary agents based on descriptions
2. **Manually** by @ mentioning: `@general help me search for this function`
3. **Via Task tool** by primary agents (if permissions allow)

### Session Navigation

- `session_child_first` (default: <Leader>+Down) - Enter first child session from parent
- `session_child_cycle` (default: Right) - Cycle to next child session
- `session_child_cycle_reverse` (default: Left) - Cycle to previous child session
- `session_parent` (default: Up) - Return to parent session

## Creating Agents

Interactive command:

```bash
opencode agent create
```

This command will:
1. Ask where to save the agent (global or project-specific)
2. Request description of what the agent should do
3. Generate appropriate system prompt and identifier
4. Let you select permissions
5. Create a markdown file with the configuration

## Example Agents

### Documentation Agent

```markdown
---
description: Writes and maintains project documentation
mode: subagent
permission:
  bash: deny
---

You are a technical writer. Create clear, comprehensive documentation.

Focus on:

- Clear explanations
- Proper structure
- Code examples
- User-friendly language
```

### Security Auditor

```markdown
---
description: Performs security audits and identifies vulnerabilities
mode: subagent
permission:
  edit: deny
---

You are a security expert. Focus on identifying potential security issues.

Look for:

- Input validation vulnerabilities
- Authentication and authorization flaws
- Data exposure risks
- Dependency vulnerabilities
- Configuration security issues
```

## Global Configuration

### default_agent

Set which primary agent is used by default:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "default_agent": "plan"
}
```

Must be a primary agent (not a subagent). Applies to TUI, CLI, desktop app, and GitHub Action.

### subagent_depth

Control how deeply subagents can invoke other subagents:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "subagent_depth": 2
}
```

- `0` - Prevent all subagent launches
- `1` - Default; primary agents can launch subagents, but those subagents cannot launch more
- `2+` - Allow additional levels of nesting
