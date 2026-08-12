# Agent Team Setup Skill

A reusable opencode skill that scaffolds a complete team of AI agents in any project.

## What It Does

When you load this skill and ask it to "set up an agent team for [your project]", it will:

1. **Plan** the pipeline (agents, handoffs, tools)
2. **Scaffold** the `.opencode/` directory structure
3. **Generate** the `opencode.json` coordinator config
4. **Create** subagent `.md` files with proper permissions
5. **Create** skill `.md` files for domain knowledge
6. **Create** custom tool `.py` + `.ts` pairs
7. **Create** the `AGENTS.md` project instructions file
8. **Test** the pipeline end-to-end

## How to Use

1. Copy this skill to your opencode skills directory:
   ```bash
   cp -r /Users/bilalmansouri/agent-team-setup-skill ~/.agents/skills/agent-team-setup
   ```

2. In any project, load the skill and describe your pipeline:
   ```
   @skill agent-team-setup

   Set up an agent team for my SaaS marketing blog:
   research trending topics → write SEO articles → generate social media images → publish to WordPress
   ```

3. The skill will scaffold everything and walk you through any decisions.

## What's Inside

```
agent-team-setup-skill/
  SKILL.md              # The full skill instructions (loaded by opencode)
  templates/
    opencode.json       # Coordinator config template
    AGENTS.md            # Project instructions template
    agent.md             # Subagent definition template
    skill.md             # Skill definition template
    tool.py              # Python script template
    tool.ts              # TypeScript wrapper template
    package.json         # .opencode/ package.json
    gitignore            # .opencode/.gitignore
    requirements.txt     # Python deps template
```

## Patterns Extracted From

This skill was distilled from a production Arabic AI-news blog (characterailab.com) that uses:
- 7 subagents (scout, planner, writer, illustrator, editor, publisher, optimizer)
- 9 skills (research, brief, writing, SEO, publishing, images, schema, R2 upload, ranking)
- 8 custom tools (search, transcript, NLP, image gen, schema, rank tracker, internal linker, competitor analyzer)
- A coordinator that orchestrates the full pipeline sequentially
- File-based handoffs through `.opencode/workspace/` directories

The same patterns work for any domain — content creation, software development, data
analysis, customer support, etc.
