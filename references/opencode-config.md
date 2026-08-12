# opencode: Configuration

> Source: https://opencode.ai/docs/config

OpenCode can be configured using JSON or JSONC (JSON with Comments) config files.

## Configuration Locations

Configuration files are **merged together, not replaced**. Settings from all config locations are combined, with later configs overriding earlier ones only for conflicting keys.

### Precedence Order (later overrides earlier)

1. **Remote config** - From `.well-known/opencode` (organizational defaults)
2. **Global config** - `~/.config/opencode/opencode.json` (user preferences)
3. **Custom config** - `OPENCODE_CONFIG` env var (custom overrides)
4. **Project config** - `opencode.json` in project root (project-specific settings)
5. **`.opencode` directories** - agents, commands, plugins
6. **Inline config** - `OPENCODE_CONFIG_CONTENT` env var (runtime overrides)
7. **Managed config files** - `/Library/Application Support/opencode/` on macOS (admin-controlled)
8. **macOS managed preferences** - `.mobileconfig` via MDM (highest priority, not user-overridable)

### Directory Naming

The `.opencode` and `~/.config/opencode` directories use **plural names** for subdirectories:
- `agents/`
- `commands/`
- `modes/`
- `plugins/`
- `skills/`
- `tools/`
- `themes/`

Singular names (e.g., `agent/`) are supported for backwards compatibility.

## Config File Locations

### Global Config

`~/.config/opencode/opencode.json` - User-wide server/runtime preferences (providers, models, permissions)

For TUI-specific settings: `~/.config/opencode/tui.json`

### Project Config

`opencode.json` in project root - Highest precedence among standard config files

For project TUI settings: `tui.json` alongside it

When OpenCode starts, it looks for config in the current directory, then traverses up to the nearest Git directory.

### Custom Path

Use `OPENCODE_CONFIG` environment variable:

```bash
export OPENCODE_CONFIG=/path/to/my/custom-config.json
opencode run "Hello world"
```

### Custom Directory

Use `OPENCODE_CONFIG_DIR` environment variable for agents, commands, modes, and plugins:

```bash
export OPENCODE_CONFIG_DIR=/path/to/my/config-directory
opencode run "Hello world"
```

## Config Schema

**Server/runtime config:** [`opencode.ai/config.json`](https://opencode.ai/config.json)  
**TUI config:** [`opencode.ai/tui.json`](https://opencode.ai/tui.json)

Your editor should validate and autocomplete based on the schema.

## Major Configuration Options

### $schema

```json
{
  "$schema": "https://opencode.ai/config.json"
}
```

### Models

Configure providers and models:

```json
{
  "provider": {},
  "model": "anthropic/claude-sonnet-4-5",
  "small_model": "anthropic/claude-haiku-4-5"
}
```

`small_model` is used for lightweight tasks like title generation. Defaults to a cheaper model if available.

**Provider options:**

```json
{
  "provider": {
    "anthropic": {
      "options": {
        "timeout": 600000,
        "chunkTimeout": 30000,
        "setCacheKey": true
      }
    }
  }
}
```

- `timeout` - Request timeout in milliseconds (default: 300000). Set to `false` to disable.
- `chunkTimeout` - Timeout between streamed response chunks
- `setCacheKey` - Ensure cache key is always set

Model ID format: `provider/model-id` (e.g., `anthropic/claude-sonnet-4-5`)

### Agents

Configure specialized agents:

```json
{
  "agent": {
    "code-reviewer": {
      "description": "Reviews code for best practices and potential issues",
      "model": "anthropic/claude-sonnet-4-5",
      "prompt": "You are a code reviewer. Focus on security, performance, and maintainability.",
      "permission": {
        "edit": "deny",
        "bash": "deny"
      }
    }
  }
}
```

Agents can also be defined in markdown files in `~/.config/opencode/agents/` or `.opencode/agents/`.

### Default Agent

Set which primary agent is used by default:

```json
{
  "default_agent": "plan"
}
```

Must be a primary agent (not a subagent).

### Subagent Depth

Control nested subagent invocations:

```json
{
  "subagent_depth": 2
}
```

- `0` - Prevent all subagent launches
- `1` - Default; primary agents can launch subagents, but those cannot launch more
- `2+` - Allow additional nesting levels

### Permissions

Control which actions require approval:

```json
{
  "permission": {
    "edit": "deny",
    "bash": "ask"
  }
}
```

Actions: `"allow"`, `"ask"`, `"deny"`

**Available permission keys:**
- `read` - Reading files
- `edit` - File modifications (write, edit, apply_patch)
- `glob` - File globbing
- `grep` - Content search
- `list` - Directory listing
- `bash` - Shell commands
- `task` - Spawning subagents
- `external_directory` - Access outside project worktree
- `todowrite` - Todo management
- `webfetch` - Fetching URLs
- `websearch` - Web search
- `lsp` - LSP queries
- `skill` - Loading skills
- `question` - Asking user questions
- `doom_loop` - Recovery when stuck

**Pattern-based permissions:**

```json
{
  "permission": {
    "bash": {
      "*": "ask",
      "git *": "allow",
      "npm *": "allow",
      "rm *": "deny"
    },
    "edit": {
      "*": "deny",
      "packages/web/src/content/docs/*.mdx": "allow"
    }
  }
}
```

**Home directory expansion:**

```json
{
  "permission": {
    "external_directory": {
      "~/projects/personal/**": "allow"
    }
  }
}
```

Use `~` or `$HOME` at the start of patterns.

### Tools (deprecated)

Legacy field. Use `permission` instead.

```json
{
  "tools": {
    "write": false,
    "bash": false
  }
}
```

### Commands

Configure custom commands for repetitive tasks:

```json
{
  "command": {
    "test": {
      "template": "Run the full test suite with coverage report and show any failures.\nFocus on the failing tests and suggest fixes.",
      "description": "Run tests with coverage",
      "agent": "build",
      "model": "anthropic/claude-haiku-4-5"
    },
    "component": {
      "template": "Create a new React component named $ARGUMENTS with TypeScript support.\nInclude proper typing and basic structure.",
      "description": "Create a new component"
    }
  }
}
```

Commands can also be defined in markdown files in `~/.config/opencode/commands/` or `.opencode/commands/`.

### Instructions

Configure instruction files for the model:

```json
{
  "instructions": [
    "CONTRIBUTING.md",
    "docs/guidelines.md",
    ".cursor/rules/*.md"
  ]
}
```

Takes array of paths and glob patterns to instruction files.

### MCP Servers

Configure Model Context Protocol servers:

```json
{
  "mcp": {
    "my-mcp-server": {
      "type": "local",
      "command": ["npx", "-y", "my-mcp-command"],
      "enabled": true,
      "environment": {
        "MY_ENV_VAR": "value"
      }
    },
    "remote-mcp": {
      "type": "remote",
      "url": "https://my-mcp-server.com",
      "enabled": true,
      "headers": {
        "Authorization": "Bearer MY_API_KEY"
      }
    }
  }
}
```

### Server

Configure server settings for `opencode serve` and `opencode web`:

```json
{
  "server": {
    "port": 4096,
    "hostname": "0.0.0.0",
    "mdns": true,
    "mdnsDomain": "myproject.local",
    "cors": ["http://localhost:5173"]
  }
}
```

### Shell

Configure shell for interactive terminal:

```json
{
  "shell": "pwsh"
}
```

If not specified, OpenCode auto-discovers a sensible default.

### Sharing

Configure the share feature:

```json
{
  "share": "manual"
}
```

Options:
- `"manual"` - Allow manual sharing via commands (default)
- `"auto"` - Automatically share new conversations
- `"disabled"` - Disable sharing entirely

### Snapshot

Enable/disable file change tracking:

```json
{
  "snapshot": false
}
```

Disabling snapshots means changes cannot be rolled back through the UI. Useful for large repositories.

### Autoupdate

Control automatic updates:

```json
{
  "autoupdate": false
}
```

Or set to `"notify"` to be notified without auto-downloading.

### Formatters

Enable and configure code formatters:

```json
{
  "formatter": true
}
```

Or configure specific formatters:

```json
{
  "formatter": {
    "prettier": {
      "disabled": true
    },
    "custom-prettier": {
      "command": ["npx", "prettier", "--write", "$FILE"],
      "environment": {
        "NODE_ENV": "development"
      },
      "extensions": [".js", ".ts", ".jsx", ".tsx"]
    }
  }
}
```

### LSP Servers

Enable and configure LSP servers:

```json
{
  "lsp": true
}
```

Or configure specific servers:

```json
{
  "lsp": {
    "typescript": {
      "disabled": true
    }
  }
}
```

### Compaction

Control context compaction behavior:

```json
{
  "compaction": {
    "auto": true,
    "prune": false,
    "reserved": 10000
  }
}
```

- `auto` - Automatically compact when context is full (default: `true`)
- `prune` - Remove old tool outputs to save tokens (default: `false`)
- `reserved` - Token buffer for compaction

### Watcher

Configure file watcher ignore patterns:

```json
{
  "watcher": {
    "ignore": ["node_modules/**", "dist/**", ".git/**"]
  }
}
```

### Image Attachments

Configure image attachment limits:

```json
{
  "attachment": {
    "image": {
      "auto_resize": true,
      "max_width": 2000,
      "max_height": 2000,
      "max_base64_bytes": 5242880
    }
  }
}
```

### Policies (Experimental)

Control OpenCode actions on configured resources:

```json
{
  "experimental": {
    "policies": [
      {
        "effect": "deny",
        "action": "provider.use",
        "resource": "openai"
      }
    ]
  }
}
```

### Plugins

Load plugins from npm:

```json
{
  "plugin": [
    "opencode-helicone-session",
    "@my-org/custom-plugin"
  ]
}
```

Plugins can also be placed in `.opencode/plugins/` or `~/.config/opencode/plugins/`.

### Enabled/Disabled Providers

Control which providers are loaded:

```json
{
  "enabled_providers": ["anthropic", "openai"],
  "disabled_providers": ["gemini"]
}
```

`disabled_providers` takes priority over `enabled_providers`.

## TUI Configuration

Use a dedicated `tui.json` file for TUI-specific settings:

```json
{
  "$schema": "https://opencode.ai/tui.json",
  "theme": "tokyonight",
  "scroll_speed": 3,
  "scroll_acceleration": {
    "enabled": true
  },
  "diff_style": "auto",
  "cursor": {
    "style": "block",
    "blinking": true
  },
  "mouse": true,
  "attention": {
    "enabled": true,
    "notifications": true,
    "sound": true,
    "volume": 0.4
  },
  "keybinds": {
    "command_list": "ctrl+p"
  }
}
```

Use `OPENCODE_TUI_CONFIG` to point to a custom TUI config file.

## Variable Substitution

### Environment Variables

Use `{env:VARIABLE_NAME}`:

```json
{
  "model": "{env:OPENCODE_MODEL}",
  "provider": {
    "anthropic": {
      "options": {
        "apiKey": "{env:ANTHROPIC_API_KEY}"
      }
    }
  }
}
```

### File Contents

Use `{file:path/to/file}`:

```json
{
  "instructions": ["./custom-instructions.md"],
  "provider": {
    "openai": {
      "options": {
        "apiKey": "{file:~/.secrets/openai-key}"
      }
    }
  }
}
```

Paths can be relative to config file directory or absolute (`/` or `~`).

## Provider-Specific Options

### Amazon Bedrock

```json
{
  "provider": {
    "amazon-bedrock": {
      "options": {
        "region": "us-east-1",
        "profile": "my-aws-profile",
        "endpoint": "https://bedrock-runtime.us-east-1.vpce-xxxxx.amazonaws.com"
      }
    }
  }
}
```

## Managed Settings (Enterprise)

### File-based Managed Config

Drop an `opencode.json` or `opencode.jsonc` in:
- **macOS:** `/Library/Application Support/opencode/`
- **Linux:** `/etc/opencode/`
- **Windows:** `%ProgramData%\opencode`

These require admin/root access, so users cannot modify them.

### macOS Managed Preferences

OpenCode reads managed preferences from `ai.opencode.managed` preference domain via `.mobileconfig` files deployed through MDM.

**Example .mobileconfig:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>PayloadContent</key>
  <array>
    <dict>
      <key>PayloadType</key>
      <string>ai.opencode.managed</string>
      <key>PayloadIdentifier</key>
      <string>com.example.opencode.config</string>
      <key>PayloadUUID</key>
      <string>GENERATE-YOUR-OWN-UUID</string>
      <key>PayloadVersion</key>
      <integer>1</integer>
      <key>share</key>
      <string>disabled</string>
      <key>permission</key>
      <dict>
        <key>*</key>
        <string>ask</string>
        <key>bash</key>
        <dict>
          <key>*</key>
          <string>ask</string>
          <key>rm -rf *</key>
          <string>deny</string>
        </dict>
      </dict>
    </dict>
  </array>
</dict>
</plist>
```

Verify with:
```bash
opencode debug config
```
