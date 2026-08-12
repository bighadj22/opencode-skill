# opencode: MCP Servers

> Source: https://opencode.ai/docs/mcp-servers

You can add external tools to OpenCode using the Model Context Protocol (MCP). OpenCode supports both local and remote MCP servers. Once added, MCP tools are automatically available to the LLM alongside built-in tools.

## Important Caveats

**MCP servers add to your context.** This can quickly add up if you have a lot of tools, so be careful with which MCP servers you enable.

Certain MCP servers, like the GitHub MCP server, tend to add many tokens and can easily exceed the context limit.

## Configuration

Define MCP servers in your OpenCode config under `mcp`. Add each MCP with a unique name:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "name-of-mcp-server": {
      // ...
      "enabled": true
    },
    "name-of-other-mcp-server": {
      // ...
    }
  }
}
```

You can disable a server by setting `enabled` to `false`. This is useful for temporarily disabling without removing the configuration.

## Overriding Remote Defaults

Organizations can provide default MCP servers via their `.well-known/opencode` endpoint. These servers may be disabled by default, allowing users to opt-in.

To enable a specific server from your organization's remote config:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "jira": {
      "type": "remote",
      "url": "https://jira.example.com/mcp",
      "enabled": true
    }
  }
}
```

Your local config values override the remote defaults. See [config precedence](https://opencode.ai/docs/config#precedence-order) for more details.

## Local MCP Servers

Add local MCP servers using `type: "local"`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "my-local-mcp-server": {
      "type": "local",
      "command": ["npx", "-y", "my-mcp-command"],
      "enabled": true,
      "environment": {
        "MY_ENV_VAR": "my_env_var_value"
      }
    }
  }
}
```

The `command` is how the local MCP server is started. You can also pass in environment variables.

### Example: MCP Everything

Here's how to add the test [`@modelcontextprotocol/server-everything`](https://www.npmjs.com/package/@modelcontextprotocol/server-everything) MCP server:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "mcp_everything": {
      "type": "local",
      "command": ["npx", "-y", "@modelcontextprotocol/server-everything"]
    }
  }
}
```

To use it, add `use the mcp_everything tool` to your prompts:

```
use the mcp_everything tool to add the number 3 and 4
```

### Local MCP Options

| Option | Type | Required | Description |
|--------|------|----------|-------------|
| `type` | String | Y | Must be `"local"` |
| `command` | Array | Y | Command and arguments to run the MCP server |
| `cwd` | String | | Working directory for the MCP server process. Relative paths resolve from the workspace. |
| `environment` | Object | | Environment variables to set when running the server |
| `enabled` | Boolean | | Enable or disable the MCP server on startup |
| `timeout` | Number | | Timeout in ms for fetching tools from the MCP server. Defaults to 5000 (5 seconds) |

## Remote MCP Servers

Add remote MCP servers by setting `type` to `"remote"`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "my-remote-mcp": {
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

The `url` is the URL of the remote MCP server. With the `headers` option you can pass in a list of headers.

### Remote MCP Options

| Option | Type | Required | Description |
|--------|------|----------|-------------|
| `type` | String | Y | Must be `"remote"` |
| `url` | String | Y | URL of the remote MCP server |
| `enabled` | Boolean | | Enable or disable the MCP server on startup |
| `headers` | Object | | Headers to send with the request |
| `oauth` | Object | | OAuth authentication configuration |
| `timeout` | Number | | Timeout in ms for fetching tools from the MCP server. Defaults to 5000 (5 seconds) |

## OAuth Authentication

OpenCode automatically handles OAuth authentication for remote MCP servers. When a server requires authentication, OpenCode will:

1. Detect the 401 response and initiate the OAuth flow
2. Use Dynamic Client Registration (RFC 7591) if supported by the server
3. Store tokens securely for future requests

### Automatic OAuth

For most OAuth-enabled MCP servers, no special configuration is needed:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "my-oauth-server": {
      "type": "remote",
      "url": "https://mcp.example.com/mcp"
    }
  }
}
```

If the server requires authentication, OpenCode will prompt you to authenticate when you first try to use it. You can also manually trigger the flow with `opencode mcp auth <server-name>`.

### Pre-registered OAuth

If you have client credentials from the MCP server provider:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "my-oauth-server": {
      "type": "remote",
      "url": "https://mcp.example.com/mcp",
      "oauth": {
        "clientId": "{env:MY_MCP_CLIENT_ID}",
        "clientSecret": "{env:MY_MCP_CLIENT_SECRET}",
        "scope": "tools:read tools:execute"
      }
    }
  }
}
```

### OAuth Commands

Authenticate with a specific MCP server:

```bash
opencode mcp auth my-oauth-server
```

List all MCP servers and their auth status:

```bash
opencode mcp list
```

Remove stored credentials:

```bash
opencode mcp logout my-oauth-server
```

The `mcp auth` command will open your browser for authorization. After you authorize, OpenCode will store the tokens securely in `~/.local/share/opencode/mcp-auth.json`.

### Disabling OAuth

If you want to disable automatic OAuth for a server (e.g., for servers that use API keys instead):

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "my-api-key-server": {
      "type": "remote",
      "url": "https://mcp.example.com/mcp",
      "oauth": false,
      "headers": {
        "Authorization": "Bearer {env:MY_API_KEY}"
      }
    }
  }
}
```

### OAuth Options

| Option | Type | Description |
|--------|------|-------------|
| `oauth` | Object\|false | OAuth config object, or `false` to disable OAuth auto-detection |
| `clientId` | String | OAuth client ID. If not provided, dynamic client registration will be attempted |
| `clientSecret` | String | OAuth client secret, if required by the authorization server |
| `scope` | String | OAuth scopes to request during authorization |

### Debugging OAuth

If a remote MCP server is failing to authenticate:

```bash
# View auth status for all OAuth-capable servers
opencode mcp auth list

# Debug connection and OAuth flow for a specific server
opencode mcp debug my-oauth-server
```

The `mcp debug` command shows the current auth status, tests HTTP connectivity, and attempts the OAuth discovery flow.

## Managing MCP Tools

MCPs are available as tools in OpenCode, alongside built-in tools. You can manage them through permissions.

### Global Tool Control

Enable or disable MCP tools globally:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "my-mcp-foo": {
      "type": "local",
      "command": ["bun", "x", "my-mcp-command-foo"]
    },
    "my-mcp-bar": {
      "type": "local",
      "command": ["bun", "x", "my-mcp-command-bar"]
    }
  },
  "permission": {
    "my-mcp-foo": "deny"
  }
}
```

Use glob patterns to disable all matching MCPs:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "my-mcp-foo": {
      "type": "local",
      "command": ["bun", "x", "my-mcp-command-foo"]
    },
    "my-mcp-bar": {
      "type": "local",
      "command": ["bun", "x", "my-mcp-command-bar"]
    }
  },
  "permission": {
    "my-mcp*": "deny"
  }
}
```

### Per-Agent Tool Control

If you have many MCP servers, you may want to enable them per agent and disable them globally:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "my-mcp": {
      "type": "local",
      "command": ["bun", "x", "my-mcp-command"],
      "enabled": true
    }
  },
  "permission": {
    "my-mcp*": "deny"
  },
  "agent": {
    "my-agent": {
      "permission": {
        "my-mcp*": "allow"
      }
    }
  }
}
```

### Glob Patterns

The glob pattern uses simple regex globbing patterns:
- `*` matches zero or more of any character (e.g., `"my-mcp*"` matches `my-mcp_search`, `my-mcp_list`, etc.)
- `?` matches exactly one character
- All other characters match literally

MCP server tools are registered with server name as prefix, so to disable all tools for a server:

```json
{
  "permission": {
    "mymcpservername_*": "deny"
  }
}
```

## Example MCP Servers

### Sentry

Add the [Sentry MCP server](https://mcp.sentry.dev/) to interact with your Sentry projects and issues:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "sentry": {
      "type": "remote",
      "url": "https://mcp.sentry.dev/mcp",
      "oauth": {}
    }
  }
}
```

After adding the configuration, authenticate with Sentry:

```bash
opencode mcp auth sentry
```

This will open a browser window to complete the OAuth flow and connect OpenCode to your Sentry account.

Once authenticated, you can use Sentry tools in your prompts:

```
Show me the latest unresolved issues in my project. use sentry
```

### Context7

Add the [Context7 MCP server](https://github.com/upstash/context7) to search through docs:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "context7": {
      "type": "remote",
      "url": "https://mcp.context7.com/mcp"
    }
  }
}
```

If you have signed up for a free account, you can use your API key for higher rate limits:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "context7": {
      "type": "remote",
      "url": "https://mcp.context7.com/mcp",
      "headers": {
        "CONTEXT7_API_KEY": "{env:CONTEXT7_API_KEY}"
      }
    }
  }
}
```

Use in prompts:

```
Configure a Cloudflare Worker script to cache JSON API responses for five minutes. use context7
```

Alternatively, add to your [AGENTS.md](https://opencode.ai/docs/rules/):

```markdown
When you need to search docs, use `context7` tools.
```

### Grep by Vercel

Add the [Grep by Vercel](https://grep.app/) MCP server to search through code snippets on GitHub:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "gh_grep": {
      "type": "remote",
      "url": "https://mcp.grep.app"
    }
  }
}
```

Use in prompts:

```
What's the right way to set a custom domain in an SST Astro component? use the gh_grep tool
```

Or add to AGENTS.md:

```markdown
If you are unsure how to do something, use `gh_grep` to search code examples from GitHub.
```

## Best Practices

1. **Start with disabled** - Set `"enabled": false` initially and enable only when needed
2. **Use specific names** - Give MCP servers descriptive names (e.g., `github-issues` not `mcp1`)
3. **Document in AGENTS.md** - Tell agents when to use specific MCP servers
4. **Monitor context usage** - Large MCP servers can quickly fill context
5. **Scope to agents** - Enable MCP tools only for agents that need them
6. **Use environment variables** - Store API keys and secrets in env vars, not config files
7. **Test OAuth flows** - Use `opencode mcp debug` to verify authentication works
