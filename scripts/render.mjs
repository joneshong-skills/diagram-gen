#!/usr/bin/env node

/**
 * render.mjs — Render Mermaid diagrams to SVG or ASCII via beautiful-mermaid.
 * Auto-installs the dependency on first run.
 *
 * Usage:
 *   node render.mjs --input diagram.mmd --output diagram.svg --theme tokyo-night
 *   node render.mjs --input diagram.mmd --format ascii
 *   node render.mjs --list-themes
 */

import { execSync } from 'child_process';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';
import { readFileSync, writeFileSync, existsSync } from 'fs';

const __dirname = dirname(fileURLToPath(import.meta.url));
const skillRoot = join(__dirname, '..');

async function loadBeautifulMermaid() {
  try {
    return await import('beautiful-mermaid');
  } catch {}

  console.error('[diagram-gen] beautiful-mermaid not found. Installing...');
  try {
    execSync('npm install --no-fund --no-audit', {
      cwd: skillRoot,
      stdio: ['pipe', 'pipe', 'inherit'],
      timeout: 120_000,
    });
    console.error('[diagram-gen] Installed successfully.\n');
  } catch (e) {
    console.error(`[diagram-gen] Auto-install failed: ${e.message}`);
    console.error(`Manual fix: cd ${skillRoot} && npm install`);
    process.exit(1);
  }

  try {
    const pkgPath = join(skillRoot, 'node_modules', 'beautiful-mermaid', 'dist', 'index.js');
    return await import(pkgPath);
  } catch (e) {
    console.error(`[diagram-gen] Failed to load after install: ${e.message}`);
    process.exit(1);
  }
}

function parseArgs() {
  const args = process.argv.slice(2);
  const opts = {
    input: null,
    output: null,
    format: 'svg',
    theme: null,
    bg: '#FFFFFF',
    fg: '#27272A',
    font: 'Inter',
    transparent: false,
    useAscii: false,
    paddingX: 5,
    paddingY: 5,
    listThemes: false,
  };

  for (let i = 0; i < args.length; i++) {
    const key = args[i];
    const val = args[i + 1];

    switch (key) {
      case '--input': case '-i': opts.input = val; i++; break;
      case '--output': case '-o': opts.output = val; i++; break;
      case '--format': case '-f': opts.format = val; i++; break;
      case '--theme': case '-t': opts.theme = val; i++; break;
      case '--bg': opts.bg = val; i++; break;
      case '--fg': opts.fg = val; i++; break;
      case '--line': opts.line = val; i++; break;
      case '--accent': opts.accent = val; i++; break;
      case '--muted': opts.muted = val; i++; break;
      case '--surface': opts.surface = val; i++; break;
      case '--border': opts.border = val; i++; break;
      case '--font': opts.font = val; i++; break;
      case '--transparent': opts.transparent = true; break;
      case '--use-ascii': opts.useAscii = true; break;
      case '--padding-x': opts.paddingX = parseInt(val); i++; break;
      case '--padding-y': opts.paddingY = parseInt(val); i++; break;
      case '--list-themes': opts.listThemes = true; break;
      case '--help': case '-h':
        console.log(`diagram-gen render — Mermaid to SVG/ASCII

Usage:
  node render.mjs --input <file> [options]
  node render.mjs --list-themes

Options:
  -i, --input <file>     Input Mermaid file (.mmd) [required]
  -o, --output <file>    Output file (default: stdout)
  -f, --format <fmt>     svg | ascii (default: svg)
  -t, --theme <name>     Theme name (e.g. tokyo-night, dracula, github-dark)
      --bg <hex>         Background color (custom)
      --fg <hex>         Foreground color (custom)
      --font <name>      Font family (default: Inter)
      --transparent      Transparent background (SVG only)
      --use-ascii        Pure ASCII instead of Unicode box-drawing
      --list-themes      List all available themes`);
        process.exit(0);
    }
  }

  return opts;
}

async function main() {
  const opts = parseArgs();
  const { renderMermaid, renderMermaidAscii, THEMES } = await loadBeautifulMermaid();

  // List themes mode
  if (opts.listThemes) {
    const names = Object.keys(THEMES);
    console.log('Available themes:\n');
    names.forEach((name, i) => {
      console.log(`  ${String(i + 1).padStart(2)}. ${name}`);
    });
    console.log(`\nTotal: ${names.length} themes`);
    return;
  }

  // Require input
  if (!opts.input) {
    console.error('Error: --input is required. Use --help for usage.');
    process.exit(1);
  }

  if (!existsSync(opts.input)) {
    console.error(`Error: Input file not found: ${opts.input}`);
    process.exit(1);
  }

  const input = readFileSync(opts.input, 'utf8');

  if (opts.format === 'ascii') {
    const ascii = renderMermaidAscii(input, {
      useAscii: opts.useAscii,
      paddingX: opts.paddingX,
      paddingY: opts.paddingY,
    });
    if (opts.output) {
      writeFileSync(opts.output, ascii);
      console.error(`ASCII diagram saved to ${opts.output}`);
    } else {
      console.log(ascii);
    }
  } else {
    const theme = opts.theme ? THEMES[opts.theme] : undefined;
    const colors = theme || {
      bg: opts.bg,
      fg: opts.fg,
      ...(opts.line && { line: opts.line }),
      ...(opts.accent && { accent: opts.accent }),
      ...(opts.muted && { muted: opts.muted }),
      ...(opts.surface && { surface: opts.surface }),
      ...(opts.border && { border: opts.border }),
    };

    const svg = await renderMermaid(input, {
      ...colors,
      font: opts.font,
      transparent: opts.transparent,
    });

    if (opts.output) {
      writeFileSync(opts.output, svg);
      console.error(`SVG diagram saved to ${opts.output}`);
    } else {
      console.log(svg);
    }
  }
}

main().catch(e => {
  console.error('Error:', e.message);
  process.exit(1);
});
