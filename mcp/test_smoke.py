#!/usr/bin/env python3
"""Smoke test for diagram-gen MCP server."""
import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from server import server, list_tools, call_tool


async def main():
    # Test 1: list_tools
    tools = await list_tools()
    names = [t.name for t in tools]
    print(f"Tools: {names}")
    assert "render_mermaid" in names
    assert "render_ascii" in names
    assert "list_themes" in names
    print("PASS: list_tools")

    # Test 2: list_themes
    result = await call_tool("list_themes", {})
    text = result[0].text
    assert "tokyo-night" in text or "github" in text
    print(f"PASS: list_themes ({text.count(chr(10))} lines)")

    # Test 3: render_ascii
    mermaid = "graph LR\n  A-->B"
    result = await call_tool("render_ascii", {"mermaid_code": mermaid})
    ascii_art = result[0].text
    print(f"PASS: render_ascii\n{ascii_art[:200]}")

    # Test 4: render_mermaid (SVG)
    output = "/tmp/diagram-gen-mcp-test.svg"
    result = await call_tool("render_mermaid", {
        "mermaid_code": mermaid,
        "output_path": output,
        "theme": "github-light",
        "transparent": True,
    })
    text = result[0].text
    assert "saved" in text.lower() or "svg" in text.lower(), f"Unexpected: {text}"
    assert Path(output).exists(), f"SVG not created at {output}"
    size = Path(output).stat().st_size
    print(f"PASS: render_mermaid (SVG {size} bytes at {output})")

    print("\nAll tests passed!")


if __name__ == "__main__":
    asyncio.run(main())
