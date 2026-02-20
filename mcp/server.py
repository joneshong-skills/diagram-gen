#!/usr/bin/env python3
"""diagram-gen MCP Server — Mermaid diagram rendering as MCP tools.

Dual transport: stdio (Claude Code) + streamable-http (Pulso Gateway / any client).

Usage:
  python server.py                              # stdio (default, for Claude Code)
  python server.py --transport streamable-http  # HTTP on port 8850
  python server.py --transport sse --port 9000  # SSE on custom port
"""

import argparse
import os
import subprocess
import tempfile
from pathlib import Path

from mcp.server import FastMCP

SKILL_DIR = Path(__file__).resolve().parent.parent
RENDER_SCRIPT = SKILL_DIR / "scripts" / "render.mjs"
NODE_BIN = "node"
SKILL_NAME = "diagram-gen"


def _get_default_port() -> int:
    """Read port from shared registry, fallback to 8850."""
    registry = SKILL_DIR.parent / "_shared" / "mcp-ports.json"
    try:
        import json
        data = json.loads(registry.read_text())
        return data["ports"].get(SKILL_NAME, 8850)
    except (FileNotFoundError, KeyError, json.JSONDecodeError):
        return 8850


DEFAULT_PORT = _get_default_port()

mcp = FastMCP(
    "diagram-gen",
    host="127.0.0.1",
    port=DEFAULT_PORT,
    streamable_http_path="/mcp",
)


def _run_render(args: list[str], timeout: int = 30) -> subprocess.CompletedProcess:
    """Run render.mjs with given arguments."""
    return subprocess.run(
        [NODE_BIN, str(RENDER_SCRIPT)] + args,
        capture_output=True,
        text=True,
        timeout=timeout,
        cwd=str(SKILL_DIR),
    )


@mcp.tool()
def render_mermaid(
    mermaid_code: str,
    output_path: str,
    theme: str = "github-light",
    transparent: bool = False,
) -> str:
    """Render Mermaid diagram code to SVG file.

    Args:
        mermaid_code: Mermaid diagram source code
        output_path: Output SVG file path (absolute)
        theme: Theme name (e.g. github-light, tokyo-night, dracula). Use list_themes to see all.
        transparent: Use transparent background
    """
    with tempfile.NamedTemporaryFile(mode="w", suffix=".mmd", delete=False) as f:
        f.write(mermaid_code)
        input_path = f.name

    try:
        cmd_args = ["--input", input_path, "--output", output_path, "--theme", theme]
        if transparent:
            cmd_args.append("--transparent")

        result = _run_render(cmd_args)

        if result.returncode != 0:
            return f"Error rendering diagram:\n{result.stderr}"

        return f"SVG diagram saved to {output_path}"
    finally:
        os.unlink(input_path)


@mcp.tool()
def render_ascii(mermaid_code: str) -> str:
    """Render Mermaid diagram code to ASCII art.

    Args:
        mermaid_code: Mermaid diagram source code
    """
    with tempfile.NamedTemporaryFile(mode="w", suffix=".mmd", delete=False) as f:
        f.write(mermaid_code)
        input_path = f.name

    try:
        result = _run_render(["--input", input_path, "--format", "ascii"])

        if result.returncode != 0:
            return f"Error rendering ASCII:\n{result.stderr}"

        return result.stdout
    finally:
        os.unlink(input_path)


@mcp.tool()
def list_themes() -> str:
    """List all available Mermaid rendering themes."""
    result = _run_render(["--list-themes"])

    if result.returncode != 0:
        return f"Error listing themes:\n{result.stderr}"

    return result.stdout


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="diagram-gen MCP Server")
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse", "streamable-http"],
        default="stdio",
        help="Transport protocol (default: stdio)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=DEFAULT_PORT,
        help=f"Port for HTTP transports (default: {DEFAULT_PORT})",
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host for HTTP transports (default: 127.0.0.1)",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    mcp.settings.host = args.host
    mcp.settings.port = args.port
    mcp.run(transport=args.transport)
