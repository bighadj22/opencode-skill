# opencode: Built-in Tools

> Source: https://opencode.ai/docs/tools

Tools allow the LLM to perform actions in your codebase. OpenCode comes with a set of built-in tools that can be extended with [custom tools](https://opencode.ai/docs/custom-tools) or [MCP servers](https://opencode.ai/docs/mcp-servers).

By default, all tools are enabled and don't need permission to run. You can control tool behavior through [permissions](https://opencode.ai/docs/permissions).

## Configuration

Use the `permission` field to control tool behavior:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "permission": {
    "edit": "deny",
    "bash": "ask",
    "webfetch": "allow"
  }
}
```

Use wildcards to control multiple tools at once:

```json
{
  "permission": {
    "mymcp_*": "ask"  // All tools from an MCP server
  }
}
```

## Built-in Tools

### bash

Execute shell commands in your project environment.

```json
{
  "permission": {
    "bash": "allow"
  }
}
```

Allows the LLM to run terminal commands like `npm install`, `git status`, or any other shell command.

**Permission:** Can use pattern-based rules for specific commands.

```json
{
  "permission": {
    "bash": {
      "*": "ask",
      "git *": "allow",
      "npm install": "deny"
    }
  }
}
```

### edit

Modify existing files using exact string replacements.

```json
{
  "permission": {
    "edit": "allow"
  }
}
```

Performs precise edits to files by replacing exact text matches. This is the primary way the LLM modifies code.

**Permission:** Can use path-based patterns.

```json
{
  "permission": {
    "edit": {
      "*": "deny",
      "src/**/*.ts": "allow"
    }
  }
}
```

### write

Create new files or overwrite existing ones.

```json
{
  "permission": {
    "edit": "allow"  // write is controlled by edit permission
  }
}
```

Use this to allow the LLM to create new files. It will overwrite existing files if they already exist.

**Note:** The `write` tool is controlled by the `edit` permission, which covers all file modifications (`edit`, `write`, `apply_patch`).

**Permission:** Can use path-based patterns (via `edit` permission).

### read

Read file contents from your codebase.

```json
{
  "permission": {
    "read": "allow"
  }
}
```

Reads files and returns their contents. Supports reading specific line ranges for large files.

**Default:** Most files are allowed, but `.env` files are denied by default:

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

**Permission:** Can use path-based patterns.

### grep

Search file contents using regular expressions.

```json
{
  "permission": {
    "grep": "allow"
  }
}
```

Fast content search across your codebase. Supports full regex syntax and file pattern filtering.

Uses [ripgrep](https://github.com/BurntSushi/ripgrep) under the hood. By default, respects `.gitignore` patterns.

**Permission:** Can use pattern-based rules.

### glob

Find files by pattern matching.

```json
{
  "permission": {
    "glob": "allow"
  }
}
```

Search for files using glob patterns like `**/*.js` or `src/**/*.ts`. Returns matching file paths sorted by modification time.

Uses [ripgrep](https://github.com/BurntSushi/ripgrep) under the hood. By default, respects `.gitignore` patterns.

**Permission:** Can use pattern-based rules.

### list

List directory contents.

```json
{
  "permission": {
    "list": "allow"
  }
}
```

**Permission:** Simple allow/ask/deny only (no pattern-based rules).

### lsp (experimental)

Interact with your configured LSP servers to get code intelligence features like definitions, references, hover info, and call hierarchy.

**Only available when `OPENCODE_EXPERIMENTAL_LSP_TOOL=true` (or `OPENCODE_EXPERIMENTAL=true`).**

```json
{
  "permission": {
    "lsp": "allow"
  }
}
```

**Supported operations:**
- `goToDefinition`
- `findReferences`
- `hover`
- `documentSymbol`
- `workspaceSymbol`
- `goToImplementation`
- `prepareCallHierarchy`
- `incomingCalls`
- `outgoingCalls`

To configure which LSP servers are available, see [LSP Servers](https://opencode.ai/docs/lsp).

**Permission:** Simple allow/ask/deny only (no pattern-based rules).

### apply_patch

Apply patches to files.

```json
{
  "permission": {
    "edit": "allow"  // apply_patch is controlled by edit permission
  }
}
```

Applies patch files to your codebase. Useful for applying diffs and patches from various sources.

**Note:** When handling `tool.execute.before` or `tool.execute.after` hooks, check `input.tool === "apply_patch"` (not `"patch"`).

**Important:** `apply_patch` uses `output.args.patchText` instead of `output.args.filePath`. Paths are embedded in marker lines within `patchText` and are relative to the project root:
- `*** Add File: src/new-file.ts`
- `*** Update File: src/existing.ts`
- `*** Move to: src/renamed.ts`
- `*** Delete File: src/obsolete.ts`

The `apply_patch` tool is controlled by the `edit` permission, which covers all file modifications (`edit`, `write`, `apply_patch`).

**Permission:** Can use path-based patterns (via `edit` permission).

### skill

Load a [skill](https://opencode.ai/docs/skills) (a `SKILL.md` file) and return its content in the conversation.

```json
{
  "permission": {
    "skill": "allow"
  }
}
```

Skills are loaded on-demand when the agent needs domain-specific knowledge or workflow guidance.

**Permission:** Can use pattern-based rules for skill names.

```json
{
  "permission": {
    "skill": {
      "*": "allow",
      "internal-*": "deny",
      "experimental-*": "ask"
    }
  }
}
```

### todowrite

Manage todo lists during coding sessions.

```json
{
  "permission": {
    "todowrite": "allow"
  }
}
```

Creates and updates task lists to track progress during complex operations. The LLM uses this to organize multi-step tasks.

**This tool is disabled for subagents by default**, but you can enable it manually.

**Permission:** Simple allow/ask/deny only (no pattern-based rules).

### webfetch

Fetch web content.

```json
{
  "permission": {
    "webfetch": "allow"
  }
}
```

Allows the LLM to fetch and read web pages. Useful for looking up documentation or researching online resources.

**Permission:** Can use URL-based patterns.

```json
{
  "permission": {
    "webfetch": {
      "*": "ask",
      "https://docs.example.com/*": "allow"
    }
  }
}
```

### websearch

Search the web for information.

**Only available when using the OpenCode provider or when the `OPENCODE_ENABLE_EXA` environment variable is set to any truthy value (e.g., `true` or `1`).**

To enable when launching OpenCode:

```bash
OPENCODE_ENABLE_EXA=1 opencode
```

```json
{
  "permission": {
    "websearch": "allow"
  }
}
```

Performs web searches using Exa AI to find relevant information online. Useful for researching topics, finding current events, or gathering information beyond the training data cutoff.

**No API key is required** — the tool connects directly to Exa AI's hosted MCP service without authentication.

**Use `websearch` when you need to find information (discovery), and `webfetch` when you need to retrieve content from a specific URL (retrieval).**

**Permission:** Can use query-based patterns.

### question

Ask the user questions during execution.

```json
{
  "permission": {
    "question": "allow"
  }
}
```

Allows the LLM to ask the user questions during a task. Useful for:
- Gathering user preferences or requirements
- Clarifying ambiguous instructions
- Getting decisions on implementation choices
- Offering choices about what direction to take

Each question includes a header, the question text, and a list of options. Users can select from provided options or type a custom answer. When there are multiple questions, users can navigate between them before submitting all answers.

**Permission:** Simple allow/ask/deny only (no pattern-based rules).

## Special Permissions

These are not tools themselves, but permission keys that control special behaviors:

### external_directory

Triggered when a tool touches paths outside the project working directory.

```json
{
  "permission": {
    "external_directory": {
      "~/projects/personal/**": "allow"
    }
  }
}
```

Applies to any tool that takes a path as input (e.g., `read`, `edit`, `glob`, `grep`, and many `bash` commands).

**Default:** `"ask"`

### doom_loop

Triggered when the same tool call repeats 3 times with identical input.

```json
{
  "permission": {
    "doom_loop": "ask"
  }
}
```

Recovery prompts when an agent appears stuck in a loop.

**Default:** `"ask"`

## Tool Internals

Internally, tools like `grep` and `glob` use [ripgrep](https://github.com/BurntSushi/ripgrep) under the hood. By default, ripgrep respects `.gitignore` patterns, which means files and directories listed in your `.gitignore` will be excluded from searches and listings.

### Ignore Patterns

To include files that would normally be ignored, create a `.ignore` file in your project root. This file can explicitly allow certain paths:

```
!node_modules/
!dist/
!build/
```

For example, this `.ignore` file allows ripgrep to search within `node_modules/`, `dist/`, and `build/` directories even if they're listed in `.gitignore`.

## Tool Management by Agent

You can control which tools are available per agent:

```json
{
  "permission": {
    "*": "deny"  // Global default
  },
  "agent": {
    "readonly": {
      "permission": {
        "read": "allow",
        "grep": "allow",
        "glob": "allow"
      }
    },
    "builder": {
      "permission": {
        "*": "allow"  // All tools
      }
    }
  }
}
```

## Summary Table

| Tool | Purpose | Pattern Support | Default Permission |
|------|---------|-----------------|-------------------|
| `bash` | Execute shell commands | Yes (commands) | `allow` |
| `edit` | Modify files | Yes (paths) | `allow` |
| `write` | Create/overwrite files | Yes (via `edit`) | `allow` |
| `read` | Read files | Yes (paths) | `allow` (except `.env`) |
| `grep` | Search file contents | Yes (patterns) | `allow` |
| `glob` | Find files by pattern | Yes (patterns) | `allow` |
| `list` | List directory contents | No | `allow` |
| `lsp` | Code intelligence | No | `allow` |
| `apply_patch` | Apply patch files | Yes (via `edit`) | `allow` |
| `skill` | Load skill files | Yes (skill names) | `allow` |
| `todowrite` | Manage todo lists | No | `allow` |
| `webfetch` | Fetch web content | Yes (URLs) | `allow` |
| `websearch` | Search the web | Yes (queries) | `allow` |
| `question` | Ask user questions | No | `allow` |
| `external_directory` | Access outside worktree | Yes (paths) | `ask` |
| `doom_loop` | Recovery when stuck | No | `ask` |
