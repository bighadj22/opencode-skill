# Agent Team Setup Skill

![Agent Team Workflow](images/banner.png)

A reusable opencode skill that scaffolds a complete team of AI agents in any project.

## What It Does

This skill helps you create production-ready agent teams for automating multi-step workflows. When you load this skill and describe your pipeline, it will:

1. **Plan** the pipeline (agents, handoffs, tools)
2. **Scaffold** the `.opencode/` directory structure
3. **Generate** the `opencode.json` coordinator config
4. **Create** subagent `.md` files with proper permissions
5. **Create** skill `.md` files for domain knowledge
6. **Create** custom tool `.py` + `.ts` pairs
7. **Create** the `AGENTS.md` project instructions file (or use `/init`)
8. **Create** custom commands for repetitive workflows (optional)
9. **Test** the pipeline end-to-end

## Installation

### Option 1: Clone from GitHub (Recommended)

```bash
# For global installation (available in all projects)
git clone https://github.com/bighadj22/opencode-skill.git ~/.config/opencode/skills/agent-team-setup

# Or for .agents directory
git clone https://github.com/bighadj22/opencode-skill.git ~/.agents/skills/agent-team-setup
```

### Option 2: Manual Installation

1. Download or clone this repository
2. Copy the folder to your OpenCode skills directory:

```bash
# For global installation
cp -r agent-team-setup-skill ~/.config/opencode/skills/agent-team-setup

# Or for .agents directory
cp -r agent-team-setup-skill ~/.agents/skills/agent-team-setup
```

### Option 3: Project-Specific Installation

```bash
# Install for a specific project only
cd /path/to/your/project
mkdir -p .opencode/skills
git clone https://github.com/bighadj22/opencode-skill.git .opencode/skills/agent-team-setup
```

### Verify Installation

After installation, restart OpenCode and verify the skill is available:

```bash
opencode
# Then in OpenCode, type:
# "What skills do you have?" or "List available skills"
```

You should see `agent-team-setup` in the list of available skills.

## How to Use

### Usage

In any project, load the skill and describe your workflow:

```
@skill agent-team-setup

Set up an agent team for my SaaS marketing blog:
research trending topics → write SEO articles → generate social media images → publish to WordPress
```

The skill will guide you through the entire setup process and help you make decisions about:
- Agent roles and responsibilities
- Handoff mechanisms between agents
- Custom tools needed
- Model selection and temperature settings
- Permission configurations


## What's Inside

```
agent-team-setup-skill/
  SKILL.md              # The full skill instructions (loaded by opencode)
  README.md             # This file
  references/           # Comprehensive OpenCode documentation references
    opencode-agents.md
    opencode-skills.md
    opencode-tools.md
    opencode-commands.md
    opencode-rules.md
    opencode-config.md
    opencode-permissions.md
    opencode-mcp.md
    opencode-builtin-tools.md
  templates/
    opencode.json       # Coordinator config template
    AGENTS.md           # Project instructions template
    agent.md            # Subagent definition template
    skill.md            # Skill definition template
    tool.py             # Python script template
    tool.ts             # TypeScript wrapper template
    package.json        # .opencode/ package.json
    gitignore           # .opencode/.gitignore
    requirements.txt    # Python deps template
```

## Use Cases

This skill works for any multi-step automated workflow:

- **Content Creation**: Research → Write → Edit → Publish → Promote
- **Software Development**: Analyze → Design → Code → Test → Deploy
- **Data Analysis**: Collect → Clean → Analyze → Visualize → Report
- **Customer Support**: Triage → Investigate → Respond → Follow-up
- **Marketing**: Research → Plan → Create → Schedule → Track

## Features

- **Complete Setup**: Creates all necessary files and directories
- **Best Practices**: Follows OpenCode conventions and patterns
- **Comprehensive Documentation**: Includes 9 detailed reference files covering all OpenCode features
- **Flexible Architecture**: Adapts to any domain or workflow
- **Permission Control**: Proper security boundaries for each agent
- **Custom Tools**: Templates for Python + TypeScript tool integration
- **Skills System**: Knowledge documents for domain-specific guidance
- **Commands System**: Reusable prompt templates for common workflows
- **AGENTS.md Integration**: Project-level instructions with /init support

## License

MIT

