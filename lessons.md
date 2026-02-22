# Diagram Gen Lessons

### 2026-02-14 — Headless SVG render with explicit output path
- **Friction**: Need to ensure headless execution still writes file into requested directory with naming constraint.
- **Fix**: Generated Mermaid source file in target folder and rendered via `scripts/render.mjs` with absolute input/output paths.
- **Rule**: In headless mode, always use absolute paths for `--input` and `--output`, and create the target directory before rendering.
