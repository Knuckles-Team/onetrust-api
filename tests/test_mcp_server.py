"""MCP server build / tool-count tests."""

import asyncio
import sys

from onetrust_api.api._operation_manifest import DOMAINS


def test_mcp_server_lists_all_tools(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["onetrust-mcp", "--transport", "stdio"])
    from onetrust_api.mcp_server import get_mcp_instance

    mcp, args, middlewares, tags = get_mcp_instance()
    # Domain tools and the custom API escape hatch retain their registered tags.
    assert len(tags) == len(DOMAINS) + 1
    tools = asyncio.run(mcp.list_tools())
    names = {tool.name for tool in tools}
    assert names == {f"onetrust_{domain}" for domain in DOMAINS} | {
        "onetrust_api_request",
        "onetrust_ingest_assessments",
        "onetrust_ingest_cookies",
        "onetrust_ingest_inventories",
    }


def test_tool_toggles_disable_domains(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["onetrust-mcp", "--transport", "stdio"])
    monkeypatch.setenv("INCIDENTSTOOL", "False")
    from onetrust_api.mcp_server import get_mcp_instance

    _mcp, _args, _mw, tags = get_mcp_instance()
    assert "incidents" not in tags


def test_agent_server_importable():
    from onetrust_api.agent_server import agent_server

    assert callable(agent_server)
