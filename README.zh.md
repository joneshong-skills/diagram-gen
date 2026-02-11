[English](README.md) | [繁體中文](README.zh.md)

# diagram-gen

Claude Code 的專業圖表生成工具。使用 Mermaid 語法自動排版，搭配語義化配色和 beautiful-mermaid SVG 渲染。

## 功能特色

- **Mermaid 優先** — 自動排版，GitHub/Obsidian 原生渲染
- **SVG 渲染** — 透過 beautiful-mermaid 提供 15 種主題（零 headless browser）
- **ASCII 輸出** — 終端機友好的文字圖表
- **語法錯誤預防** — 5 條關鍵規則，防止最常見的 Mermaid 解析錯誤
- **語義化配色** — 依照意義上色（輸入=綠、決策=黃、錯誤=紅）
- **12 種圖表模式** — 流程圖、序列圖、狀態圖、類別圖、ER 圖、心智圖、甘特圖、架構圖等

## 安裝

```bash
git clone https://github.com/joneshong-skills/diagram-gen.git ~/.claude/skills/diagram-gen
```

當您要求 Claude Code 建立圖表、產生流程圖、視覺化工作流程或渲染 Mermaid 時，技能會自動啟動。

## 快速開始

### Mermaid 程式碼區塊（預設）

直接請 Claude Code 建立圖表，會輸出 ` ```mermaid ` 程式碼區塊，在 GitHub 和 Obsidian 中原生渲染。

### SVG 檔案

```bash
RENDER="node ~/.claude/skills/diagram-gen/scripts/render.mjs"

# 使用主題渲染
$RENDER --input diagram.mmd --output diagram.svg --theme tokyo-night

# 列出可用主題
$RENDER --list-themes
```

### ASCII（終端機）

```bash
$RENDER --input diagram.mmd --format ascii
```

## 支援的圖表類型

| 類型 | Mermaid 語法 | 適用場景 |
|------|-------------|---------|
| 流程圖 | `flowchart TB/LR` | 流程、工作流程、決策 |
| 序列圖 | `sequenceDiagram` | API 呼叫、訊息流 |
| 狀態圖 | `stateDiagram-v2` | 狀態機、生命週期 |
| 類別圖 | `classDiagram` | 物件模型、架構 |
| ER 圖 | `erDiagram` | 資料庫結構 |
| 心智圖 | `mindmap` | 階層結構、腦力激盪 |
| 甘特圖 | `gantt` | 時間軸、專案規劃 |

## 致謝

靈感來自社群 Claude Code 圖表技能：
- [axtonliu/axton-obsidian-visual-skills](https://github.com/axtonliu/axton-obsidian-visual-skills) — 語法錯誤預防規則
- [sickn33/Pretty-mermaid-skills](https://github.com/sickn33/Pretty-mermaid-skills) — beautiful-mermaid 渲染
- [rnjn/cc-excalidraw-skill](https://github.com/rnjn/cc-excalidraw-skill) — 配色系統最佳實踐
- [GBSOSS/ai-drawio](https://github.com/GBSOSS/ai-drawio) — 圖表模式目錄

## 授權

MIT
