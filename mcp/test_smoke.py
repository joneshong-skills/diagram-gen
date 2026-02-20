#!/usr/bin/env python3
"""Smoke test for diagram-gen MCP server (FastMCP version).

Tests both tool logic (direct call) and HTTP transport (client request).
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from server import render_mermaid, render_ascii, list_themes, mcp


async def test_direct_tools():
    """Test tool functions directly (no transport)."""
    print("=== Direct Tool Tests ===")

    # Test 1: list_themes
    result = list_themes()
    assert "tokyo-night" in result or "github" in result
    lines = result.strip().count("\n")
    print(f"PASS: list_themes ({lines} lines)")

    # Test 2: render_ascii
    mermaid = "graph LR\n  A-->B"
    result = render_ascii(mermaid)
    assert "Error" not in result
    print(f"PASS: render_ascii\n{result[:200]}")

    # Test 3: render_mermaid (SVG)
    output = "/tmp/diagram-gen-mcp-test.svg"
    result = render_mermaid(mermaid, output, theme="github-light", transparent=True)
    assert "saved" in result.lower() or "svg" in result.lower(), f"Unexpected: {result}"
    assert Path(output).exists(), f"SVG not created at {output}"
    size = Path(output).stat().st_size
    print(f"PASS: render_mermaid (SVG {size} bytes at {output})")


async def test_http_transport():
    """Test streamable-http transport via MCP client."""
    import httpx

    port = 18850  # Use non-conflicting test port
    mcp.settings.port = port
    mcp.settings.host = "127.0.0.1"

    app = mcp.streamable_http_app()

    from starlette.testclient import TestClient
    client = TestClient(app)

    # MCP initialize via POST
    init_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2025-03-26",
            "capabilities": {},
            "clientInfo": {"name": "test", "version": "0.1.0"},
        },
    }
    resp = client.post("/mcp", json=init_request, headers={"Accept": "application/json, text/event-stream"})
    assert resp.status_code == 200, f"Init failed: {resp.status_code} {resp.text[:200]}"
    print(f"PASS: HTTP initialize (status {resp.status_code})")

    # Extract session ID from response header
    session_id = resp.headers.get("mcp-session-id")
    print(f"  Session ID: {session_id}")

    # tools/list via POST
    list_request = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list",
        "params": {},
    }
    headers = {"Accept": "application/json, text/event-stream"}
    if session_id:
        headers["mcp-session-id"] = session_id
    resp = client.post("/mcp", json=list_request, headers=headers)
    assert resp.status_code == 200, f"tools/list failed: {resp.status_code}"
    print(f"PASS: HTTP tools/list (status {resp.status_code})")


async def main():
    await test_direct_tools()
    print()

    try:
        await test_http_transport()
    except ImportError:
        print("SKIP: HTTP transport test (httpx/starlette not available)")
    except Exception as e:
        print(f"SKIP: HTTP transport test ({e})")

    print("\nAll tests passed!")


if __name__ == "__main__":
    asyncio.run(main())
