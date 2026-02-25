# Copilot CLI Skills

A collection of reusable skills for the [GitHub Copilot CLI](https://docs.github.com/en/copilot/github-copilot-in-the-cli) agent. Each skill teaches Copilot a specialized workflow — from brainstorming features to building Excel dashboards — so it handles complex tasks consistently and well.

Skills are Markdown files that shape how Copilot approaches a problem. Drop one into your skills directory and the agent picks it up automatically. No plugins, no config, no build step.

## Included Skills

| Skill | What it does |
| --- | --- |
| **[brainstorming](brainstorming/)** | Turns ideas into designs through collaborative dialogue. Explores requirements, proposes approaches, and validates incrementally before any code is written. |
| **[excel-toolkit](excel-toolkit/)** | Reads, edits, analyzes, and creates Excel files (.xlsx, .csv, .tsv). Supports formulas, charts, and dashboard layouts. Includes Python helper scripts. |
| **[frontend-development](frontend-development/)** | Builds production-ready React/Vue/Svelte components with accessibility-first implementation, focus management, and design system compliance. |
| **[powerpoint-toolkit](powerpoint-toolkit/)** | Builds, edits, analyzes, and improves PowerPoint presentations. Handles design patterns, text extraction, and quality feedback. Includes Python helper scripts. |
| **[writing-plans](writing-plans/)** | Creates bite-sized implementation plans with exact file paths, test strategies, and commit instructions for each task. |
| **[writing-skills](writing-skills/)** | A meta-skill for creating new skills using TDD principles (RED → GREEN → REFACTOR) with subagent-based baseline testing. Includes reference docs on prompt engineering. |

## Installation

Skills can be installed in either of two locations:

- **`~/.copilot/skills/`** — user-level skills available across all your projects
- **`.agent/skills/`** — project-level skills checked in alongside your code (relative to your project root)

Copy any skill folder into your preferred skills directory:

```bash
# Install a single skill (user-level)
cp -r brainstorming ~/.copilot/skills/

# Install all skills (user-level)
cp -r brainstorming excel-toolkit frontend-development \
      powerpoint-toolkit writing-plans writing-skills \
      ~/.copilot/skills/

# Install a single skill (project-level)
cp -r brainstorming .agent/skills/

# Install all skills (project-level)
cp -r brainstorming excel-toolkit frontend-development \
      powerpoint-toolkit writing-plans writing-skills \
      .agent/skills/
```

Create the directory first if it doesn't exist:

```bash
# User-level
mkdir -p ~/.copilot/skills

# Project-level
mkdir -p .agent/skills
```

The toolkit skills (excel-toolkit, powerpoint-toolkit) include Python scripts that install their own dependencies on first use. Python 3 is required.

## Skill Structure

Every skill is a folder with a `SKILL.md` file at its root. That's the only required file.

```
my-skill/
├── SKILL.md              # Defines the skill (required)
├── scripts/              # Helper scripts the agent can run
│   ├── setup_deps.py
│   └── analyze.py
└── references/           # Additional context docs
    └── patterns.md
```

### SKILL.md Format

The file starts with YAML frontmatter that tells Copilot when to activate the skill, followed by Markdown instructions that define behavior:

```markdown
---
name: my-skill
description: Use when the user asks to do X, Y, or Z
---

# My Skill

## Overview

What this skill does and how it approaches the problem.

## The Process

Step-by-step instructions for the agent to follow.
```

- **`name`** — Identifier for the skill.
- **`description`** — Trigger conditions. Be specific about when this skill should activate.
- **Body** — The actual instructions. Write these as if you're onboarding a capable but context-free engineer.

### Optional Files

- **`scripts/`** — Python, Node, or shell scripts the agent can execute. Useful for tasks that need libraries (e.g., openpyxl for Excel, python-pptx for PowerPoint).
- **`references/`** — Supplementary docs the agent can consult. Design patterns, API references, style guides.

## Creating Your Own Skills

1. **Create a folder** in `~/.copilot/skills/` (user-level) or `.agent/skills/` (project-level) with your skill name.
2. **Write a `SKILL.md`** with frontmatter (`name`, `description`) and instructions.
3. **Test it** by asking Copilot to do something that matches your description trigger.
4. **Iterate** — refine the instructions based on where the agent goes off track.

Tips:
- The `description` field controls activation. Make it specific: list the exact scenarios where this skill should kick in.
- Write instructions in imperative mood: "Ask the user…", "Generate a file…", "Run the script…".
- Break complex workflows into numbered steps. Agents follow ordered lists well.
- Add constraints and guardrails for things the agent tends to get wrong.
- Use the [writing-skills](writing-skills/) skill itself to create and test new skills with a TDD workflow.

## Contributing

PRs welcome. If you've built a skill that solves a real workflow problem, open a pull request.

Keep skills focused — one skill, one job. If a skill tries to do everything, it does nothing well.

## License

[MIT](LICENSE)
