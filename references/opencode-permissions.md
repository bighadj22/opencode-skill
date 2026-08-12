# opencode: Permissions

> Source: https://opencode.ai/docs/permissions

OpenCode uses the `permission` config to decide whether a given action should run automatically, prompt you, or be blocked.

## Permission Actions

Each permission rule resolves to one of:
- `"allow"` - Run without approval
- `"ask"` - Prompt for approval
- `"deny"` - Block the action

## Available Permissions

OpenCode permissions are keyed by tool name, plus safety guards:

| Permission Key | Maps To Tools | Supports Patterns |
|----------------|---------------|-------------------|
| `read` | `read` | Yes (file paths) |
| `edit` | `write`, `edit`, `apply_patch` | Yes (file paths) |
| `glob` | `glob` | Yes (glob patterns) |
| `grep` | `grep` | Yes (regex patterns) |
| `list` | `list` | No |
| `bash` | `bash` | Yes (command patterns) |
| `task` | `task` | Yes (subagent types) |
| `skill` | `skill` | Yes (skill names) |
| `lsp` | `lsp` | No |
| `question` | `question` | No |
| `webfetch` | `webfetch` | Yes (URLs) |
| `websearch` | `websearch` | Yes (queries) |
| `external_directory` | Any tool touching paths outside worktree | Yes (path patterns) |
| `doom_loop` | Recovery when tool repeats 3 times | No |
| `todowrite` | `todowrite`, `todoread` | No |

Permissions marked "Supports Patterns" can use object syntax for granular control.

## Configuration

### Simple (Shorthand)

Set all permissions at once:

```json
{
  "permission": "allow"
}
```

Or configure specific tools:

```json
{
  "permission": {
    "*": "ask",
    "bash": "allow",
    "edit": "deny"
  }
}
```

The `*` wildcard sets a default for all unspecified permissions.

### Granular (Object Syntax)

For permissions that support patterns, use an object to apply different actions based on input:

```json
{
  "permission": {
    "bash": {
      "*": "ask",
      "git *": "allow",
      "npm *": "allow",
      "rm *": "deny",
      "grep *": "allow"
    },
    "edit": {
      "*": "deny",
      "packages/web/src/content/docs/*.mdx": "allow"
    }
  }
}
```

**Rules are evaluated by pattern match, with the last matching rule winning.** A common pattern is to put the catch-all `*` rule first, followed by more specific rules.

## Pattern Matching

Permission patterns use simple wildcard matching:
- `*` - Matches zero or more of any character
- `?` - Matches exactly one character
- All other characters match literally

### Examples

**Bash patterns:**
```json
{
  "bash": {
    "*": "ask",           // Default: ask for all commands
    "git *": "allow",     // Allow all git commands
    "git push *": "deny", // But deny git push
    "grep *": "allow",    // Allow grep with any args
    "npm install": "deny" // Deny npm install without args
  }
}
```

**File path patterns:**
```json
{
  "edit": {
    "*": "deny",                              // Deny all edits by default
    "src/**/*.ts": "allow",                   // Allow TypeScript in src
    "packages/*/src/**": "allow",             // Allow edits in package sources
    "*.md": "ask",                            // Ask before editing markdown
    "*.env": "deny",                          // Always deny .env files
    "packages/web/src/content/docs/*.mdx": "allow"
  }
}
```

**Skill patterns:**
```json
{
  "skill": {
    "*": "allow",
    "internal-*": "deny",       // Deny all skills starting with "internal-"
    "experimental-*": "ask"     // Ask before loading experimental skills
  }
}
```

## Home Directory Expansion

You can use `~` or `$HOME` at the start of a pattern to reference your home directory:

```json
{
  "external_directory": {
    "~/projects/*": "allow",
    "$HOME/documents/**": "allow"
  }
}
```

- `~/projects/*` → `/Users/username/projects/*`
- `$HOME/projects/*` → `/Users/username/projects/*`
- `~` → `/Users/username`

## External Directory Access

Use `external_directory` to allow tool calls that touch paths outside the working directory where OpenCode was started. This applies to any tool that takes a path as input (e.g., `read`, `edit`, `glob`, `grep`, and many `bash` commands).

**Important:** Home expansion (like `~/...`) only affects how a pattern is written. It does not make an external path part of the current workspace, so paths outside the working directory must still be allowed via `external_directory`.

```json
{
  "permission": {
    "external_directory": {
      "~/projects/personal/**": "allow"
    }
  }
}
```

Any directory allowed here **inherits the same defaults as the current workspace**. Since `read` defaults to `allow`, reads are also allowed for entries under `external_directory` unless overridden.

### Layering Permissions

Add explicit rules when a tool should be restricted in external paths:

```json
{
  "permission": {
    "external_directory": {
      "~/projects/personal/**": "allow"  // Allow access to this directory
    },
    "edit": {
      "~/projects/personal/**": "deny"   // But deny edits there
    }
  }
}
```

This allows reading from `~/projects/personal/` but blocks modifications.

## Default Permissions

If you don't specify anything, OpenCode starts from permissive defaults:

- Most permissions default to `"allow"`
- `doom_loop` and `external_directory` default to `"ask"`
- `read` is `"allow"`, but `.env` files are denied by default:

```json
{
  "permission": {
    "read": {
      "*": "allow",
      "*.env": "deny",
      "*.env.*": "deny",
      "*.env.example": "allow"
    }
  }
}
```

## Auto Mode

Start OpenCode with `--auto` to automatically approve permission requests that are not explicitly denied:

```bash
opencode --auto
```

Or with `opencode run`:

```bash
opencode run --auto "Refactor this module"
```

**Explicit `"deny"` rules are still enforced.** Auto mode only changes requests that would otherwise ask for approval.

In the TUI:
- Open command palette and select "Enable auto-approve permissions" or "Disable auto-approve permissions"
- When auto mode is active, a muted `auto` indicator appears next to the current agent

## "Ask" Behavior

When OpenCode prompts for approval, the UI offers three outcomes:

1. **once** - Approve just this request
2. **always** - Approve future requests matching the suggested patterns (for the rest of the current OpenCode session)
3. **reject** - Deny the request

The set of patterns that `always` would approve is provided by the tool. For example, bash approvals typically whitelist a safe command prefix like `git status*`.

## Per-Agent Permissions

You can override permissions per agent. Agent permissions are merged with the global config, and **agent rules take precedence**.

### In opencode.json

```json
{
  "permission": {
    "bash": {
      "*": "ask",
      "git *": "allow",
      "git commit *": "deny",
      "git push *": "deny",
      "grep *": "allow"
    }
  },
  "agent": {
    "build": {
      "permission": {
        "bash": {
          "*": "ask",
          "git *": "allow",
          "git commit *": "ask",    // Override: allow asking for commit
          "git push *": "deny",
          "grep *": "allow"
        }
      }
    }
  }
}
```

### In Markdown Agents

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

Only analyze code and suggest changes.
```

## Command Pattern Matching

Use pattern matching for commands with arguments:

```json
{
  "bash": {
    "grep *": "allow",      // Allows "grep pattern file.txt"
    "grep": "deny"          // But denies just "grep" without args
  }
}
```

- `"grep *"` allows `grep pattern file.txt`
- `"grep"` alone would block it

Commands like `git status` work for default behavior but require explicit permission (like `"git status *"`) when arguments are passed.

## Task Permissions (Subagent Control)

Control which subagents an agent can invoke via the Task tool:

```json
{
  "agent": {
    "orchestrator": {
      "permission": {
        "task": {
          "*": "deny",                  // Deny all by default
          "orchestrator-*": "allow",    // Allow orchestrator-* subagents
          "code-reviewer": "ask"        // Ask before invoking code-reviewer
        }
      }
    }
  }
}
```

When set to `"deny"`, the subagent is removed from the Task tool description entirely, so the model won't attempt to invoke it.

**Rules are evaluated in order, and the last matching rule wins.** In the example above, `orchestrator-planner` matches both `*` (deny) and `orchestrator-*` (allow), but since `orchestrator-*` comes after `*`, the result is `allow`.

**Users can always invoke any subagent directly via the `@` autocomplete menu**, even if the agent's task permissions would deny it.

## Wildcard Patterns for Tools

Permission keys are matched as wildcard patterns against the underlying tool name. This works for built-ins, custom tools, and MCP tools:

```json
{
  "permission": {
    "mymcp_*": "deny",      // Deny every tool from an MCP server
    "mymcp_search": "ask"   // Ask for this specific tool
  }
}
```

## Common Permission Patterns

### Read-Only Agent

```json
{
  "agent": {
    "readonly": {
      "permission": {
        "edit": "deny",
        "bash": "deny",
        "todowrite": "deny"
      }
    }
  }
}
```

### Careful Build Agent

```json
{
  "agent": {
    "careful-build": {
      "permission": {
        "*": "ask",
        "read": "allow",
        "grep": "allow",
        "glob": "allow"
      }
    }
  }
}
```

### Git-Only Agent

```json
{
  "agent": {
    "git-helper": {
      "permission": {
        "bash": {
          "*": "deny",
          "git *": "allow",
          "git push *": "ask"
        },
        "edit": "deny"
      }
    }
  }
}
```

### Docs Writer

```json
{
  "agent": {
    "docs-writer": {
      "permission": {
        "edit": {
          "*": "deny",
          "docs/**/*.md": "allow",
          "README.md": "allow"
        },
        "bash": "deny"
      }
    }
  }
}
```

## Security Best Practices

1. **Start restrictive** - Use `"*": "ask"` or `"*": "deny"` as the base, then allow specific tools
2. **Deny dangerous commands** - Block `rm -rf`, `sudo`, `chmod`, destructive operations
3. **Protect secrets** - Deny reading `.env`, `*.key`, credential files
4. **Limit external access** - Use `external_directory` carefully
5. **Review agent permissions** - Each agent should have minimum necessary permissions
6. **Use auto mode carefully** - Only enable auto mode when you trust the agent's scope

## Debugging Permissions

To check resolved permissions:

```bash
opencode debug config
```

This shows the final merged configuration including all permission rules.
