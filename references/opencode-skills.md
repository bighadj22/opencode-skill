# opencode: Agent Skills

> Source: https://opencode.ai/docs/skills

Agent skills let OpenCode discover reusable instructions from your repo or home directory. Skills are loaded on-demand via the native `skill` tool—agents see available skills and can load the full content when needed.

## File Locations

Create one folder per skill name and put a `SKILL.md` inside it. OpenCode searches these locations:

**Project config:**
- `.opencode/skills/<name>/SKILL.md`

**Global config:**
- `~/.config/opencode/skills/<name>/SKILL.md`

**Claude-compatible paths:**
- `.claude/skills/<name>/SKILL.md` (project)
- `~/.claude/skills/<name>/SKILL.md` (global)

**Agent-compatible paths:**
- `.agents/skills/<name>/SKILL.md` (project)
- `~/.agents/skills/<name>/SKILL.md` (global)

## Discovery Mechanism

For project-local paths, OpenCode walks up from your current working directory until it reaches the git worktree. It loads any matching `skills/*/SKILL.md` in `.opencode/` and any matching `.claude/skills/*/SKILL.md` or `.agents/skills/*/SKILL.md` along the way.

Global definitions are also loaded from `~/.config/opencode/skills/*/SKILL.md`, `~/.claude/skills/*/SKILL.md`, and `~/.agents/skills/*/SKILL.md`.

## Frontmatter Format

Each `SKILL.md` must start with YAML frontmatter. Only these fields are recognized:

### Required Fields

- **name** (required) - Skill identifier
- **description** (required) - Brief description (1-1024 characters)

### Optional Fields

- **license** - License information
- **compatibility** - Compatibility flag (e.g., "opencode")
- **metadata** - String-to-string map of additional metadata

**Unknown frontmatter fields are ignored.**

## Naming Rules

The `name` field must:
- Be 1–64 characters
- Be lowercase alphanumeric with single hyphen separators
- Not start or end with `-`
- Not contain consecutive `--`
- Match the directory name that contains `SKILL.md`

**Regex equivalent:** `^[a-z0-9]+(-[a-z0-9]+)*$`

## Length Rules

`description` must be 1-1024 characters. Keep it specific enough for the agent to choose correctly.

## Example Skill

Create `.opencode/skills/git-release/SKILL.md`:

```markdown
---
name: git-release
description: Create consistent releases and changelogs
license: MIT
compatibility: opencode
metadata:
  audience: maintainers
  workflow: github
---

## What I do

- Draft release notes from merged PRs
- Propose a version bump
- Provide a copy-pasteable `gh release create` command

## When to use me

Use this when you are preparing a tagged release.
Ask clarifying questions if the target versioning scheme is unclear.
```

## How Skills Appear to Agents

OpenCode lists available skills in the `skill` tool description. Each entry includes the skill name and description:

```xml
<available_skills>
  <skill>
    <name>git-release</name>
    <description>Create consistent releases and changelogs</description>
  </skill>
</available_skills>
```

The agent loads a skill by calling the tool:

```javascript
skill({ name: "git-release" })
```

## Permissions

Control which skills agents can access using pattern-based permissions in `opencode.json`:

```json
{
  "permission": {
    "skill": {
      "*": "allow",
      "pr-review": "allow",
      "internal-*": "deny",
      "experimental-*": "ask"
    }
  }
}
```

### Permission Actions

| Action | Behavior |
|--------|----------|
| `allow` | Skill loads immediately |
| `deny` | Skill hidden from agent, access rejected |
| `ask` | User prompted for approval before loading |

Patterns support wildcards: `internal-*` matches `internal-docs`, `internal-tools`, etc.

## Per-Agent Permission Overrides

Give specific agents different permissions than the global defaults.

### For Custom Agents (in agent frontmatter)

```markdown
---
permission:
  skill:
    "documents-*": "allow"
---
```

### For Built-in Agents (in opencode.json)

```json
{
  "agent": {
    "plan": {
      "permission": {
        "skill": {
          "internal-*": "allow"
        }
      }
    }
  }
}
```

## Disabling the Skill Tool

Completely disable skills for agents that shouldn't use them.

### For Custom Agents

```markdown
---
tools:
  skill: false
---
```

### For Built-in Agents

```json
{
  "agent": {
    "plan": {
      "tools": {
        "skill": false
      }
    }
  }
}
```

When disabled, the `<available_skills>` section is omitted entirely.

## Troubleshooting

If a skill does not show up:

1. **Verify** `SKILL.md` is spelled in all caps
2. **Check** that frontmatter includes `name` and `description`
3. **Ensure** skill names are unique across all locations
4. **Check permissions** - skills with `deny` are hidden from agents

## Best Practices

### When to Create a Skill

Create a skill when:
- An agent needs domain-specific knowledge (e.g., writing style guide, SEO rules)
- A workflow has reusable steps that could be documented separately
- A capability spans multiple agents (e.g., R2 upload used by multiple agents)

### Skill vs Agent

| Use a **skill** when... | Use an **agent** when... |
|-------------------------|--------------------------|
| Knowledge needs to be loaded on demand | Work needs to be delegated automatically |
| The knowledge spans multiple agents | The task is a distinct pipeline step |
| It's reference material, not executable work | It needs its own permissions/model |
| It's a style guide, checklist, or template | It saves files to the workspace |

### Linking Skills to Agents

Mention skills by name in agent instructions:
> "Follow the writing rules in the writer-arabic skill."

The coordinator or agent can load the skill using the skill tool when needed.

## Example Skills

### Style Guide Skill

`.opencode/skills/code-style/SKILL.md`:

```markdown
---
name: code-style
description: Project coding style and conventions
---

## Naming Conventions

- Use camelCase for variables and functions
- Use PascalCase for classes and components
- Use UPPER_CASE for constants
- Prefix private methods with underscore

## Code Structure

- Keep functions under 50 lines
- Max 3 levels of nesting
- One component per file
- Group related functions together

## Documentation

- JSDoc for all public functions
- Inline comments for complex logic
- README for each module
```

### API Integration Skill

`.opencode/skills/api-patterns/SKILL.md`:

```markdown
---
name: api-patterns
description: Standard patterns for API integration
---

## Error Handling

Always wrap API calls in try-catch:

```typescript
try {
  const response = await fetch(url)
  if (!response.ok) throw new Error(response.statusText)
  return await response.json()
} catch (error) {
  logger.error('API call failed', { url, error })
  throw error
}
```

## Retry Logic

Use exponential backoff for retries:
- First retry: 1s delay
- Second retry: 2s delay
- Third retry: 4s delay
- Max 3 retries

## Rate Limiting

Respect rate limits:
- Check X-RateLimit headers
- Back off when limits are hit
- Cache responses when possible
```
