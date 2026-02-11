[English](README.md) | [繁體中文](README.zh.md)

# diagram-gen

Professional diagram generation for Claude Code. Produce Mermaid diagrams with auto-layout, semantic colors, and SVG rendering via beautiful-mermaid.

## Features

- **Mermaid-first** — Auto-layout, native GitHub/Obsidian rendering
- **SVG rendering** — 15 themes via beautiful-mermaid (zero headless browser)
- **ASCII output** — Terminal-friendly diagrams
- **Syntax error prevention** — 5 critical rules that prevent the most common Mermaid parsing errors
- **Semantic colors** — Map colors to meaning (input=green, decision=yellow, error=red)
- **12 diagram patterns** — Flowchart, sequence, state, class, ER, mindmap, Gantt, architecture, and more

## Installation

```bash
git clone https://github.com/joneshong-skills/diagram-gen.git ~/.claude/skills/diagram-gen
```

The skill activates automatically when you ask Claude Code to create diagrams, generate flowcharts, visualize workflows, or render Mermaid.

## Quick Start

### Mermaid Code Block (default)

Ask Claude Code to create a diagram — it will output a ` ```mermaid ` code block that renders natively in GitHub and Obsidian.

### SVG File

```bash
RENDER="node ~/.claude/skills/diagram-gen/scripts/render.mjs"

# Render with theme
$RENDER --input diagram.mmd --output diagram.svg --theme tokyo-night

# List available themes
$RENDER --list-themes
```

### ASCII (Terminal)

```bash
$RENDER --input diagram.mmd --format ascii
```

## Supported Diagram Types

| Type | Mermaid Syntax | Best For |
|------|---------------|----------|
| Flowchart | `flowchart TB/LR` | Processes, workflows, decisions |
| Sequence | `sequenceDiagram` | API calls, message flows |
| State | `stateDiagram-v2` | State machines, lifecycles |
| Class | `classDiagram` | Object models, architecture |
| ER | `erDiagram` | Database schemas |
| Mindmap | `mindmap` | Hierarchy, brainstorming |
| Gantt | `gantt` | Timelines, project planning |

## Acknowledgements

Inspired by community Claude Code diagram skills:
- [axtonliu/axton-obsidian-visual-skills](https://github.com/axtonliu/axton-obsidian-visual-skills) — Syntax error prevention rules
- [sickn33/Pretty-mermaid-skills](https://github.com/sickn33/Pretty-mermaid-skills) — beautiful-mermaid rendering
- [rnjn/cc-excalidraw-skill](https://github.com/rnjn/cc-excalidraw-skill) — Color system best practices
- [GBSOSS/ai-drawio](https://github.com/GBSOSS/ai-drawio) — Diagram pattern catalog

## License

MIT
