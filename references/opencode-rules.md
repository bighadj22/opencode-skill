# opencode: Rules and Instructions

> Source: https://opencode.ai/docs/rules

Rules provide custom instructions to OpenCode through `AGENTS.md` files and other instruction sources, customizing LLM behavior for specific projects and workflows.

## AGENTS.md Overview

`AGENTS.md` is similar to Cursor's rules file. It contains instructions included in the LLM's context to customize behavior for your specific project. This file should be committed to Git and shared across your team.

## Initialize with /init

Create or improve `AGENTS.md` using the `/init` command in OpenCode TUI:

```
/init
```

The `/init` command:
- Scans important files in your repository
- May ask targeted questions when information isn't obvious from the codebase
- Creates or updates `AGENTS.md` with concise, project-specific guidance

**Focus areas:**
- Build, lint, and test commands
- Command order and verification steps when they matter
- Architecture and repository structure not obvious from filenames
- Project-specific conventions, setup quirks, and operational gotchas
- References to existing instruction sources like Cursor or Copilot rules

**If `AGENTS.md` already exists**, `/init` improves it in place instead of replacing it.

## AGENTS.md Example

**AGENTS.md:**
```markdown
# SST v3 Monorepo Project

This is an SST v3 monorepo with TypeScript. The project uses bun workspaces for package management.

## Project Structure

- `packages/` - Contains all workspace packages (functions, core, web, etc.)
- `infra/` - Infrastructure definitions split by service (storage.ts, api.ts, web.ts)
- `sst.config.ts` - Main SST configuration with dynamic imports

## Code Standards

- Use TypeScript with strict mode enabled
- Shared code goes in `packages/core/` with proper exports configuration
- Functions go in `packages/functions/`
- Infrastructure should be split into logical files in `infra/`

## Monorepo Conventions

- Import shared modules using workspace names: `@my-app/core/example`
```

Project-specific instructions are shared across your team when committed to version control.

## File Locations

OpenCode supports multiple instruction file locations, each serving different purposes.

### Project Rules

**Location:** `AGENTS.md` in your project root

**Scope:** Project-specific rules that apply only when working in this directory or its subdirectories.

**Use for:** Team-wide conventions, project architecture, build/test commands, deployment procedures.

**Committed to Git:** Yes - share across team.

### Global Rules

**Location:** `~/.config/opencode/AGENTS.md`

**Scope:** Applied across all OpenCode sessions on your machine.

**Use for:** Personal preferences, coding style, workflow habits.

**Committed to Git:** No - personal configuration.

### Claude Code Compatibility

OpenCode supports Claude Code file conventions as fallbacks for migration:

**Project rules:** `CLAUDE.md` in project directory (used if no `AGENTS.md` exists)  
**Global rules:** `~/.claude/CLAUDE.md` (used if no `~/.config/opencode/AGENTS.md` exists)  
**Skills:** `~/.claude/skills/` - see [Agent Skills](https://opencode.ai/docs/skills/) for details

**Disable Claude Code compatibility:**

```bash
export OPENCODE_DISABLE_CLAUDE_CODE=1         # Disable all .claude support
export OPENCODE_DISABLE_CLAUDE_CODE_PROMPT=1  # Disable only ~/.claude/CLAUDE.md
export OPENCODE_DISABLE_CLAUDE_CODE_SKILLS=1  # Disable only .claude/skills
```

## File Precedence

OpenCode looks for rule files in this order:

1. **Local files** - Traverse up from current directory (`AGENTS.md`, `CLAUDE.md`)
2. **Global file** - `~/.config/opencode/AGENTS.md`
3. **Claude Code file** - `~/.claude/CLAUDE.md` (unless disabled)

**The first matching file wins in each category.** If you have both `AGENTS.md` and `CLAUDE.md`, only `AGENTS.md` is used. Similarly, `~/.config/opencode/AGENTS.md` takes precedence over `~/.claude/CLAUDE.md`.

## Custom Instructions Array

Specify additional instruction files in `opencode.json` to reuse existing documentation and rules:

**opencode.json:**
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

**Benefits:**
- Reuse existing project documentation
- Avoid duplicating rules into AGENTS.md
- Support glob patterns for flexible file matching
- Combine multiple instruction sources

**Global config:** `~/.config/opencode/opencode.json`

### Remote Instructions

Load instructions from remote URLs:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "instructions": [
    "https://raw.githubusercontent.com/my-org/shared-rules/main/style.md"
  ]
}
```

Remote instructions are fetched with a 5-second timeout. All instruction files combine with your `AGENTS.md` files.

## Referencing External Files

Two approaches for including external files in instructions:

### Using opencode.json (Recommended)

Use the `instructions` field with glob patterns:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "instructions": [
    "docs/development-standards.md",
    "test/testing-guidelines.md",
    "packages/*/AGENTS.md"
  ]
}
```

**Benefits:**
- Automatic file discovery with globs
- Ideal for monorepos
- Maintainable at scale
- Files always loaded at session start

### Manual Instructions in AGENTS.md

Teach OpenCode to load files on-demand:

**AGENTS.md:**
```markdown
# TypeScript Project Rules

## External File Loading

CRITICAL: When you encounter a file reference (e.g., @rules/general.md), use your Read tool to load it on a need-to-know basis. They're relevant to the SPECIFIC task at hand.

Instructions:

- Do NOT preemptively load all references - use lazy loading based on actual need
- When loaded, treat content as mandatory instructions that override defaults
- Follow references recursively when needed

## Development Guidelines

For TypeScript code style and best practices: @docs/typescript-guidelines.md
For React component architecture and hooks patterns: @docs/react-patterns.md
For REST API design and error handling: @docs/api-standards.md
For testing strategies and coverage requirements: @test/testing-guidelines.md

## General Guidelines

Read the following file immediately as it's relevant to all workflows: @rules/general-guidelines.md.
```

**This approach allows:**
- Modular, reusable rule files
- Sharing rules across projects via symlinks or git submodules
- Keeping AGENTS.md concise while referencing detailed guidelines
- Loading files only when needed for specific tasks

**For monorepos or shared standards**, `opencode.json` with glob patterns is more maintainable.

## Instructions vs Skills vs Commands

Understanding when to use each:

| Use **AGENTS.md/Instructions** when... | Use a **Skill** when... | Use a **Command** when... |
|----------------------------------------|-------------------------|---------------------------|
| Always-on project context needed | Knowledge loaded on-demand | Triggering a specific workflow |
| Architectural rules apply to all work | Domain expertise for specific tasks | Repeating the same prompt template |
| Build/test commands must be known | Reference material that's optional | Automating multi-step processes |
| Team-wide conventions | Guidance spans multiple agents | Slash command convenience wanted |

## Example AGENTS.md Files

### Full-Stack Web Application

```markdown
# E-Commerce Platform

Full-stack Next.js 14 app with TypeScript, Prisma, and Tailwind CSS.

## Development

- `npm run dev` - Start dev server (localhost:3000)
- `npm run db:push` - Push schema changes to database
- `npm test` - Run Jest + React Testing Library tests
- `npm run lint` - ESLint + Prettier check

## Architecture

- `app/` - Next.js 14 App Router pages and layouts
- `components/` - Reusable React components
- `lib/` - Utilities, database client, API helpers
- `prisma/` - Database schema and migrations
- `public/` - Static assets

## Conventions

- Use Server Components by default
- Client Components only when needed (use 'use client' directive)
- API routes in `app/api/` using Route Handlers
- All database queries through `lib/db.ts` client
- Tailwind for styling, no CSS modules
- Zod for runtime validation

## Database

- PostgreSQL via Supabase
- Prisma schema: `prisma/schema.prisma`
- After schema changes: `npm run db:push`, then restart dev server
- Seed data: `npm run db:seed`

## Deployment

- Vercel deployment on push to `main`
- Environment variables required: DATABASE_URL, NEXT_PUBLIC_API_URL
- Preview deployments on all PRs
```

### Python Data Science Project

```markdown
# ML Pipeline Project

Python 3.11 project for training and deploying ML models.

## Setup

```bash
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
```

## Commands

- `python -m pytest` - Run all tests
- `python -m pytest -v` - Verbose test output
- `python scripts/train.py` - Train model
- `python scripts/evaluate.py` - Evaluate model performance
- `python -m black .` - Format code
- `python -m pylint src/` - Lint code

## Structure

- `src/` - Main package code
  - `data/` - Data loading and preprocessing
  - `models/` - Model definitions
  - `training/` - Training loops and utilities
  - `evaluation/` - Metrics and evaluation
- `notebooks/` - Jupyter notebooks for exploration
- `tests/` - Pytest test files
- `scripts/` - CLI scripts for training/evaluation

## Conventions

- Type hints required for all functions
- Docstrings follow Google style
- Use dataclasses for configuration
- All data paths relative to project root
- Use logging module, not print()
- pytest fixtures in `tests/conftest.py`

## Data

- Raw data: `data/raw/`
- Processed data: `data/processed/`
- Models saved to: `models/`
- Never commit data files or model checkpoints

## Dependencies

- PyTorch for models
- pandas for data manipulation
- scikit-learn for metrics
- Add new deps to `requirements.txt` with versions pinned
```

### Monorepo Configuration

```markdown
# Monorepo Project

Turborepo monorepo with multiple apps and shared packages.

## Workspace Structure

- `apps/web` - Next.js web application
- `apps/api` - Express API server
- `packages/ui` - Shared React component library
- `packages/config` - Shared ESLint, TypeScript configs
- `packages/utils` - Shared utility functions

## Commands

- `npm run dev` - Start all apps in dev mode
- `npm run build` - Build all packages and apps
- `npm test` - Run tests across all workspaces
- `npm run lint` - Lint all workspaces

## Conventions

- Import shared packages: `@repo/ui`, `@repo/utils`, etc.
- Add dependencies to correct package, not root
- Changes to `packages/*` require rebuilding dependent apps
- All packages use TypeScript strict mode

## Development Workflow

1. Make changes in relevant package/app
2. If changing `packages/*`, rebuild with `npm run build`
3. Test changes: `npm test`
4. Lint: `npm run lint`
5. Commit following conventional commits format
```

## Best Practices

1. **Be specific** - Provide concrete commands, not vague guidelines
2. **Include context** - Explain *why* a convention exists when it's not obvious
3. **Keep it current** - Update AGENTS.md as the project evolves
4. **Focus on non-obvious** - Don't document what's clear from code structure
5. **Use sections** - Organize with clear headers for easy scanning
6. **Document workflows** - Include step-by-step processes
7. **Reference external files** - Use `opencode.json` instructions array for detailed guides
8. **Test regularly** - Verify AGENTS.md actually helps agents understand the project

## Integration with Agent Teams

For agent teams, AGENTS.md provides shared project knowledge:

```markdown
# Agent Team Project

## Pipeline

This project uses a multi-agent pipeline:
1. Scout - Research (see .opencode/agents/scout.md)
2. Writer - Content creation (see .opencode/agents/writer.md)
3. Editor - Quality review (see .opencode/agents/editor.md)
4. Publisher - Deployment (see .opencode/agents/publisher.md)

## Workspace

Agents use `.opencode/workspace/` for handoffs:
- `research/` - Scout output
- `drafts/` - Writer output
- `final/` - Editor output

## Custom Tools

- `search_web.py` - Web search tool
- `upload_r2.py` - R2 upload tool

Run: `python3 .opencode/tools/<tool>.py <args>`

## Deployment

Publisher deploys to R2 bucket: `content-prod`
Deployment triggers Cloudflare cache purge
```

