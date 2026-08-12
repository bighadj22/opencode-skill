# opencode: Commands

> Source: https://opencode.ai/docs/commands

Custom commands transform named prompt templates into executable slash commands, enabling consistent, repeatable workflows for common development tasks.

## What Are Commands?

Commands are reusable prompt templates that execute when you type `/command-name` in the OpenCode TUI. They supplement built-in commands like `/init`, `/undo`, `/redo`, `/share`, and `/help`.

## Creating Commands

### Markdown Files (Recommended)

Place markdown files in the `commands/` directory. The filename becomes the command name.

**Global commands:** `~/.config/opencode/commands/`  
**Project commands:** `.opencode/commands/`

**.opencode/commands/test.md:**
```markdown
---
description: Run tests with coverage
agent: build
model: anthropic/claude-3-5-sonnet-20241022
---

Run the full test suite with coverage report and show any failures.
Focus on the failing tests and suggest fixes.
```

Usage: `/test`

### JSON Configuration

Define commands in `opencode.json`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "command": {
    "test": {
      "template": "Run the full test suite with coverage report and show any failures.\nFocus on the failing tests and suggest fixes.",
      "description": "Run tests with coverage",
      "agent": "build",
      "model": "anthropic/claude-3-5-sonnet-20241022"
    }
  }
}
```

## Prompt Features

Commands support several special syntax features for dynamic prompts.

### Arguments

Use `$ARGUMENTS` to pass arguments to commands:

**.opencode/commands/component.md:**
```markdown
---
description: Create a new component
---

Create a new React component named $ARGUMENTS with TypeScript support.
Include proper typing and basic structure.
```

Usage: `/component Button`

**Positional parameters** allow accessing individual arguments:
- `$1` - First argument
- `$2` - Second argument
- `$3` - Third argument
- And so on...

**.opencode/commands/create-file.md:**
```markdown
---
description: Create a new file with content
---

Create a file named $1 in the directory $2
with the following content: $3
```

Usage: `/create-file config.json src "{ \"key\": \"value\" }"`

This replaces:
- `$1` with `config.json`
- `$2` with `src`
- `$3` with `{ "key": "value" }`

### Shell Output Injection

Use `!`command`` to inject bash command output into your prompt:

**.opencode/commands/analyze-coverage.md:**
```markdown
---
description: Analyze test coverage
---

Here are the current test results:
!`npm test`

Based on these results, suggest improvements to increase coverage.
```

Commands run in your project's root directory and their output becomes part of the prompt.

**Example with git:**

**.opencode/commands/review-changes.md:**
```markdown
---
description: Review recent changes
---

Recent git commits:
!`git log --oneline -10`

Review these changes and suggest any improvements.
```

### File References

Include file content using `@filename`:

**.opencode/commands/review-component.md:**
```markdown
---
description: Review component
---

Review the component in @src/components/Button.tsx.
Check for performance issues and suggest improvements.
```

The file content gets included in the prompt automatically.

## Configuration Options

### template (required)

The prompt sent to the LLM when the command is executed.

```json
{
  "command": {
    "test": {
      "template": "Run the full test suite with coverage report and show any failures.\nFocus on the failing tests and suggest fixes."
    }
  }
}
```

### description

Brief description displayed in the TUI when typing the command.

```json
{
  "command": {
    "test": {
      "description": "Run tests with coverage"
    }
  }
}
```

### agent

Specify which agent should execute this command. If the agent is a subagent, the command triggers a subagent invocation by default (controlled by `subtask` option).

```json
{
  "command": {
    "review": {
      "agent": "plan"
    }
  }
}
```

Optional. If not specified, uses your current agent.

### subtask

Boolean flag to force the command to trigger a subagent invocation. Useful when you want the command to run in a separate context without polluting your primary conversation. Forces the agent to act as a subagent even if `mode` is set to `primary` in the agent configuration.

```json
{
  "command": {
    "analyze": {
      "subtask": true
    }
  }
}
```

Optional.

### model

Override the default model for this specific command.

```json
{
  "command": {
    "analyze": {
      "model": "anthropic/claude-3-5-sonnet-20241022"
    }
  }
}
```

Optional.

## Built-in Commands

OpenCode includes built-in commands: `/init`, `/undo`, `/redo`, `/share`, `/help`. See [TUI documentation](https://opencode.ai/docs/tui#commands) for details.

**Custom commands can override built-in commands.** If you define a custom command with the same name as a built-in command, your custom version takes precedence.

## Command Examples

### Test Runner with Coverage

**.opencode/commands/test.md:**
```markdown
---
description: Run tests with coverage report
agent: build
---

Run the full test suite with coverage report and show any failures.
Focus on the failing tests and suggest fixes.
```

### Component Generator

**.opencode/commands/component.md:**
```markdown
---
description: Create a new React component
---

Create a new React component named $ARGUMENTS with:
- TypeScript support
- Proper prop typing
- Basic JSDoc comments
- Export statement

Place it in src/components/ directory.
```

### Code Review Command

**.opencode/commands/review.md:**
```markdown
---
description: Review recent changes
agent: plan
subtask: true
---

Review these recent git changes:
!`git diff --staged`

Check for:
- Code quality issues
- Potential bugs
- Security concerns
- Performance implications
- Missing tests
```

### Documentation Generator

**.opencode/commands/document.md:**
```markdown
---
description: Generate documentation for a file
---

Generate comprehensive documentation for @$ARGUMENTS including:
- Overview of the file's purpose
- Function/class descriptions
- Parameter documentation
- Return value documentation
- Usage examples
```

Usage: `/document src/utils/helpers.ts`

### Commit Helper

**.opencode/commands/commit.md:**
```markdown
---
description: Generate commit message from staged changes
---

Based on these staged changes:
!`git diff --staged`

Generate a conventional commit message that:
- Uses the conventional commit format (feat/fix/docs/etc.)
- Has a concise subject line (50 chars max)
- Includes a detailed body explaining the changes
- Mentions any breaking changes
```

### Performance Analyzer

**.opencode/commands/perf.md:**
```markdown
---
description: Analyze performance of current changes
agent: build
---

Current git diff:
!`git diff`

Analyze these changes for:
- Time complexity implications
- Memory usage patterns
- Potential bottlenecks
- Database query efficiency
- Network call optimization opportunities
```

## Best Practices

1. **Keep commands focused** - Each command should do one thing well
2. **Use descriptive names** - Command names should clearly indicate their purpose
3. **Document arguments** - If using `$ARGUMENTS` or positional parameters, document expected format
4. **Choose appropriate agents** - Use `plan` for analysis, `build` for implementation
5. **Use subtask wisely** - Set `subtask: true` for commands that should run in isolation
6. **Combine features** - Mix shell output, file references, and arguments for powerful workflows
7. **Test commands** - Run commands with different inputs to verify behavior
8. **Share with team** - Commit project commands to version control for team consistency

## Common Patterns

### Multi-step Workflow Commands

```markdown
---
description: Full feature workflow
agent: build
---

1. Analyze the current codebase structure: !`tree -L 2 src/`
2. Create feature implementation for $ARGUMENTS
3. Generate tests for the new feature
4. Update documentation
5. Run tests: !`npm test`
```

### Context-Aware Commands

```markdown
---
description: Smart refactoring based on context
---

Current file structure:
!`ls -la src/components/`

Recent changes:
!`git log --oneline -5`

Refactor @$1 following these patterns and ensuring compatibility with recent changes.
```

### CI/CD Integration Commands

```markdown
---
description: Pre-deployment checklist
---

Run all pre-deployment checks:

1. Tests: !`npm test`
2. Linting: !`npm run lint`
3. Build: !`npm run build`
4. Type check: !`tsc --noEmit`

Report any failures and suggest fixes.
```

## Directory Structure for Commands

```
project/
  .opencode/
    commands/
      test.md
      component.md
      review.md
      commit.md
      deploy.md
```

Or globally:

```
~/.config/opencode/
  commands/
    format.md
    analyze.md
    document.md
```

## Integration with Agent Teams

Commands work seamlessly with agent teams. The coordinator can instruct team members to use specific commands:

**In coordinator prompt:**
```
When the user provides a feature request:
1. Run /analyze to understand requirements
2. Run /component <name> to scaffold
3. Run /test to verify
4. Run /review to check quality
```

This enables standardized, repeatable workflows across your agent team.

