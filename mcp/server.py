#!/usr/bin/env python3
"""diagram-gen MCP Server — Mermaid diagram rendering as MCP tools.

Wraps the existing render.mjs script, exposing it as MCP tools
that Claude Code or Agent SDK can call programmatically.
"""

import asyncio
import json
import os
import subprocess
import tempfile
from pathlib import Path

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

# Paths
SKILL_DIR = Path(__file__).resolve().parent.parent
RENDER_SCRIPT = SKILL_DIR / "scripts" / "render.mjs"
NODE_BIN = "node"

server = Server("diagram-gen")


def _run_render(args: list[str], timeout: int = 30) -> subprocess.CompletedProcess:
    """Run render.mjs with given arguments."""
    return subprocess.run(
        [NODE_BIN, str(RENDER_SCRIPT)] + args,
        capture_output=True,
        text=True,
        timeout=timeout,
        cwd=str(SKILL_DIR),
    )


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="render_mermaid",
            description="Render Mermaid diagram code to SVG file",
            inputSchema={
                "type": "object",
                "properties": {
                    "mermaid_code": {
                        "type": "string",
                        "description": "Mermaid diagram source code",
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Output SVG file path (absolute)",
                    },
                    "theme": {
                        "type": "string",
                        "description": "Theme name (e.g. github-light, tokyo-night, dracula). Use list_themes to see all.",
                        "default": "github-light",
                    },
                    "transparent": {
                        "type": "boolean",
                        "description": "Use transparent background",
                        "default": False,
                    },
                },
                "required": ["mermaid_code", "output_path"],
            },
        ),
        Tool(
            name="render_ascii",
            description="Render Mermaid diagram code to ASCII art",
            inputSchema={
                "type": "object",
                "properties": {
                    "mermaid_code": {
                        "type": "string",
                        "description": "Mermaid diagram source code",
                    },
                },
                "required": ["mermaid_code"],
            },
        ),
        Tool(
            name="list_themes",
            description="List all available Mermaid rendering themes",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "render_mermaid":
        return await _handle_render_mermaid(arguments)
    elif name == "render_ascii":
        return await _handle_render_ascii(arguments)
    elif name == "list_themes":
        return await _handle_list_themes()
    else:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]


async def _handle_render_mermaid(args: dict) -> list[TextContent]:
    mermaid_code = args["mermaid_code"]
    output_path = args["output_path"]
    theme = args.get("theme", "github-light")
    transparent = args.get("transparent", False)

    # Write mermaid code to temp file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".mmd", delete=False) as f:
        f.write(mermaid_code)
        input_path = f.name

    try:
        cmd_args = [
            "--input", input_path,
            "--output", output_path,
            "--theme", theme,
        ]
        if transparent:
            cmd_args.append("--transparent")

        result = _run_render(cmd_args)

        if result.returncode != 0:
            return [TextContent(
                type="text",
                text=f"Error rendering diagram:\n{result.stderr}",
            )]

        return [TextContent(
            type="text",
            text=f"SVG diagram saved to {output_path}",
        )]
    finally:
        os.unlink(input_path)


async def _handle_render_ascii(args: dict) -> list[TextContent]:
    mermaid_code = args["mermaid_code"]

    with tempfile.NamedTemporaryFile(mode="w", suffix=".mmd", delete=False) as f:
        f.write(mermaid_code)
        input_path = f.name

    try:
        result = _run_render(["--input", input_path, "--format", "ascii"])

        if result.returncode != 0:
            return [TextContent(
                type="text",
                text=f"Error rendering ASCII:\n{result.stderr}",
            )]

        return [TextContent(type="text", text=result.stdout)]
    finally:
        os.unlink(input_path)


async def _handle_list_themes() -> list[TextContent]:
    result = _run_render(["--list-themes"])

    if result.returncode != 0:
        return [TextContent(
            type="text",
            text=f"Error listing themes:\n{result.stderr}",
        )]

    return [TextContent(type="text", text=result.stdout)]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


if __name__ == "__main__":
    asyncio.run(main())
