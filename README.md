# SKILL.md

A curated collection of high-quality skills for [Claude Code](https://docs.anthropic.com/en/docs/claude-code), built on the [Agent Skills](https://github.com/anthropics/agent-skills) open standard.

## What are Skills?

Skills are reusable instruction sets (defined in `SKILL.md` files) that extend Claude Code with specialized capabilities. They follow the [Agent Skills](https://github.com/anthropics/agent-skills) open standard, making them portable across compatible AI tools.

## Available Skills

| Skill | Description |
|-------|-------------|
| [explain-code](explain-code/) | Explain source code through structured text explanations and Excalidraw diagrams. Supports class diagrams, flow diagrams, ER diagrams, sequence diagrams, component diagrams, and more. |

## Installation

### Option 1: Copy into your project

```bash
git clone https://github.com/Badhansen/SKILL.md.git
cp -r SKILL.md/explain-code /path/to/your/project/.claude/skills/
```

### Option 2: Install globally

```bash
git clone https://github.com/Badhansen/SKILL.md.git
cp -r SKILL.md/explain-code ~/.claude/skills/
```

## Repo Structure

```
SKILL.md/
├── README.md
├── LICENSE
└── explain-code/
    ├── SKILL.md              # Skill definition
    ├── examples/             # Sample .excalidraw outputs
    │   ├── class-diagram-auth.excalidraw
    │   ├── er-diagram-blog.excalidraw
    │   └── flow-diagram-login.excalidraw
    ├── references/           # Diagram templates & code patterns
    │   ├── diagram-templates.md
    │   └── code-patterns.md
    └── scripts/              # Validation & generation utilities
        ├── generate_diagram.py
        ├── validate.sh
        └── validate_excalidraw.py
```

## Contributing

Contributions are welcome. Each skill should:

- Solve a real, recurring problem in software development
- Include a well-defined `SKILL.md` with clear instructions
- Provide examples and reference material where applicable
- Follow the [Agent Skills](https://github.com/anthropics/agent-skills) open standard

## License

[MIT](LICENSE)
