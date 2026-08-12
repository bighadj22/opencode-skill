# opencode: Custom Tools

> Source: https://opencode.ai/docs/custom-tools

Custom tools are functions you create that the LLM can call during conversations. They work alongside opencode's built-in tools like `read`, `write`, and `bash`.

## Creating Tools

Tools are defined as TypeScript or JavaScript files. The tool definition can invoke scripts written in any language—TypeScript or JavaScript is only used for the tool definition itself.

### Location

Tools can be defined:
- **Locally:** `.opencode/tools/` directory in your project
- **Globally:** `~/.config/opencode/tools/`

### Basic Structure

The easiest way to create tools is using the `tool()` helper which provides type-safety and validation:

**.opencode/tools/database.ts:**
```typescript
import { tool } from "@opencode-ai/plugin"

export default tool({
  description: "Query the project database",
  args: {
    query: tool.schema.string().describe("SQL query to execute"),
  },
  async execute(args) {
    // Your database logic here
    return `Executed query: ${args.query}`
  },
})
```

**The filename becomes the tool name.** The above creates a `database` tool.

### Multiple Tools Per File

You can export multiple tools from a single file. Each export becomes a separate tool with the name `<filename>_<exportname>`:

**.opencode/tools/math.ts:**
```typescript
import { tool } from "@opencode-ai/plugin"

export const add = tool({
  description: "Add two numbers",
  args: {
    a: tool.schema.number().describe("First number"),
    b: tool.schema.number().describe("Second number"),
  },
  async execute(args) {
    return (args.a + args.b).toString()
  },
})

export const multiply = tool({
  description: "Multiply two numbers",
  args: {
    a: tool.schema.number().describe("First number"),
    b: tool.schema.number().describe("Second number"),
  },
  async execute(args) {
    return (args.a * args.b).toString()
  },
})
```

This creates two tools: `math_add` and `math_multiply`.

### Name Collisions

Custom tools are keyed by tool name. If a custom tool uses the same name as a built-in tool, the custom tool takes precedence.

Example replacing the built-in `bash` tool:

**.opencode/tools/bash.ts:**
```typescript
import { tool } from "@opencode-ai/plugin"

export default tool({
  description: "Restricted bash wrapper",
  args: {
    command: tool.schema.string(),
  },
  async execute(args) {
    return `blocked: ${args.command}`
  },
})
```

**Prefer unique names unless you intentionally want to replace a built-in tool.** If you want to disable a built-in tool but not override it, use [permissions](https://opencode.ai/docs/permissions).

## Arguments

Use `tool.schema` (which is just [Zod](https://zod.dev/)) to define argument types:

```typescript
args: {
  query: tool.schema.string().describe("SQL query to execute")
}
```

You can also import Zod directly and return a plain object:

```typescript
import { z } from "zod"

export default {
  description: "Tool description",
  args: {
    param: z.string().describe("Parameter description"),
  },
  async execute(args, context) {
    // Tool implementation
    return "result"
  },
}
```

## Context

Tools receive context about the current session:

**.opencode/tools/project.ts:**
```typescript
import { tool } from "@opencode-ai/plugin"

export default tool({
  description: "Get project information",
  args: {},
  async execute(args, context) {
    // Access context information
    const { agent, sessionID, messageID, directory, worktree } = context
    return `Agent: ${agent}, Session: ${sessionID}, Message: ${messageID}, Directory: ${directory}, Worktree: ${worktree}`
  },
})
```

**Context Properties:**
- `agent` - Current agent name
- `sessionID` - Current session identifier
- `messageID` - Current message identifier
- `directory` - Session working directory
- `worktree` - Git worktree root

**Use `context.directory` for the session working directory. Use `context.worktree` for the git worktree root.**

## Writing Tools in Other Languages

You can write your tools in any language. Here's an example that adds two numbers using Python.

### Step 1: Create the Python Script

**.opencode/tools/add.py:**
```python
import sys

a = int(sys.argv[1])
b = int(sys.argv[2])
print(a + b)
```

### Step 2: Create the TypeScript Wrapper

**.opencode/tools/python-add.ts:**
```typescript
import { tool } from "@opencode-ai/plugin"
import path from "path"

export default tool({
  description: "Add two numbers using Python",
  args: {
    a: tool.schema.number().describe("First number"),
    b: tool.schema.number().describe("Second number"),
  },
  async execute(args, context) {
    const script = path.join(context.worktree, ".opencode/tools/add.py")
    const result = await Bun.$`python3 ${script} ${args.a} ${args.b}`.text()
    return result.trim()
  },
})
```

Here we use the [`Bun.$`](https://bun.com/docs/runtime/shell) utility to run the Python script.

## Tool Design Principles

When creating custom tools for agent teams:

1. **Python does the work** - All logic in `.py` file. The `.ts` file just calls it.
2. **JSON output** - Python scripts print JSON to stdout for structured results.
3. **Error handling** - Print errors to stderr, exit with code 1.
4. **No API keys in code** - Read from environment variables (`os.environ.get('KEY')`).
5. **One tool per file** - Don't combine multiple tools into one script.
6. **Idempotent** - Running the same tool twice should give the same result.

## Example: Python Tool with JSON Output

**.opencode/tools/search_web.py:**
```python
#!/usr/bin/env python3
"""
Web search tool
Usage: python3 search_web.py <query>
"""
import sys
import json
import os

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 search_web.py <query>", file=sys.stderr)
        sys.exit(1)
    
    query = sys.argv[1]
    
    # Fetch API key from environment
    api_key = os.environ.get('SEARCH_API_KEY')
    if not api_key:
        print("Error: SEARCH_API_KEY not set", file=sys.stderr)
        sys.exit(1)
    
    # ... do the search ...
    
    result = {
        "query": query,
        "results": [
            {"title": "Example 1", "url": "https://example.com/1"},
            {"title": "Example 2", "url": "https://example.com/2"}
        ],
        "status": "ok"
    }
    
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
```

**.opencode/tools/search_web.ts:**
```typescript
import { tool } from "@opencode-ai/plugin"
import path from "path"

export default tool({
  description: "Search the web and return results",
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

## Using Bun Shell

The `Bun.$` utility provides a convenient shell interface:

```typescript
// Simple command
const output = await Bun.$`ls -la`.text()

// With variables
const filename = "test.txt"
const content = await Bun.$`cat ${filename}`.text()

// With working directory
const result = await Bun.$`pwd`.cwd("/tmp").text()

// Capture stderr
try {
  await Bun.$`some-command`.text()
} catch (error) {
  console.error("Command failed:", error)
}
```

## Tool Management

### Installing Dependencies

For TypeScript tools, install dependencies in `.opencode/`:

**.opencode/package.json:**
```json
{
  "dependencies": {
    "@opencode-ai/plugin": "latest",
    "axios": "^1.6.0"
  }
}
```

Then run:
```bash
cd .opencode && npm install
```

For Python tools, list dependencies in `.opencode/tools/requirements.txt`:

**.opencode/tools/requirements.txt:**
```
requests>=2.31.0
beautifulsoup4>=4.12.0
```

Install with:
```bash
pip3 install -r .opencode/tools/requirements.txt
```

### Enabling/Disabling Tools

Control tool access through permissions in `opencode.json`:

```json
{
  "permission": {
    "my-custom-tool": "allow",
    "dangerous-tool": "deny",
    "sensitive-tool": "ask"
  }
}
```

Or disable globally and enable per agent:

```json
{
  "permission": {
    "my-tool": "deny"
  },
  "agent": {
    "builder": {
      "permission": {
        "my-tool": "allow"
      }
    }
  }
}
```

## Complete Example: DuckDuckGo Search Tool

**.opencode/tools/search_duckduckgo.py:**
```python
#!/usr/bin/env python3
import sys
import json
import requests

def search(query):
    url = "https://api.duckduckgo.com/"
    params = {
        "q": query,
        "format": "json",
        "no_html": 1
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        results = []
        for item in data.get("RelatedTopics", [])[:5]:
            if "Text" in item and "FirstURL" in item:
                results.append({
                    "title": item.get("Text", "")[:100],
                    "url": item.get("FirstURL", "")
                })
        
        return {
            "query": query,
            "results": results,
            "count": len(results)
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No query provided"}))
        sys.exit(1)
    
    result = search(sys.argv[1])
    print(json.dumps(result, ensure_ascii=False, indent=2))
```

**.opencode/tools/search_duckduckgo.ts:**
```typescript
import { tool } from "@opencode-ai/plugin"
import path from "path"

export default tool({
  description: "Search the web via DuckDuckGo and return top results",
  args: {
    query: tool.schema.string().describe("Search query"),
  },
  async execute(args, context) {
    const script = path.join(context.worktree, ".opencode/tools/search_duckduckgo.py")
    const result = await Bun.$`python3 ${script} ${args.query}`.text()
    return result.trim()
  },
})
```

## Advanced: Using with Agent Teams

When building agent teams, custom tools become powerful coordination mechanisms:

1. **Shared data tools** - Tools that read/write to `.opencode/workspace/data/`
2. **External API tools** - Tools that interact with third-party services
3. **Validation tools** - Tools that check work from other agents
4. **Notification tools** - Tools that alert users or other systems

**Example: Handoff verification tool:**

```typescript
import { tool } from "@opencode-ai/plugin"
import { readFileSync } from "fs"
import path from "path"

export default tool({
  description: "Verify that required handoff files exist",
  args: {
    files: tool.schema.array(tool.schema.string()).describe("List of file paths to check"),
  },
  async execute(args, context) {
    const missing = []
    for (const file of args.files) {
      const fullPath = path.join(context.worktree, file)
      try {
        readFileSync(fullPath)
      } catch {
        missing.push(file)
      }
    }
    
    if (missing.length > 0) {
      return `Missing files: ${missing.join(", ")}`
    }
    return "All handoff files present"
  },
})
```
