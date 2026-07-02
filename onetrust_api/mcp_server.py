#!/usr/bin/python

import logging
import sys
from typing import Any

from agent_utilities.mcp_utilities import (
    create_mcp_server,
    load_config,
    register_tool_surface,
)
from fastmcp import FastMCP
from fastmcp.utilities.logging import get_logger

from onetrust_api.api._operation_manifest import OPERATIONS
from onetrust_api.api_client import Api
from onetrust_api.auth import get_client

__version__ = "0.2.1"

# Redirect logging to stderr to prevent MCP stdout corruption
logger = get_logger(name="onetrust_mcp")
logger.setLevel(logging.INFO)


def register_prompts(mcp: FastMCP):
    @mcp.prompt(name="example_prompt", description="Example prompt for OneTrust Api.")
    def example_prompt(query: str) -> str:
        """Example prompt."""
        return f"Please help with '{query}' using OneTrust Api"


def get_mcp_instance() -> tuple[Any, Any, Any, Any]:
    """Initialize and return the OneTrust Api MCP instance, args, and middlewares."""
    load_config()

    args, mcp, middlewares = create_mcp_server(
        name="OneTrust Api MCP",
        version=__version__,
        instructions="OneTrust Api MCP Server",
    )

    # One central call selects the surface per MCP_TOOL_MODE: condensed gates each
    # generated TOOL_REGISTRY domain via setting("<TAG>TOOL", True); verbose adds
    # the fully-typed 1:1 tools sourced from the OpenAPI manifest (OPERATIONS).
    from onetrust_api.mcp import TOOL_REGISTRY

    registered_tags = register_tool_surface(
        mcp,
        client_cls=Api,
        get_client=get_client,
        service="onetrust-api",
        tool_registry=TOOL_REGISTRY,
        manifest=OPERATIONS,
    )

    register_prompts(mcp)

    for mw in middlewares:
        mcp.add_middleware(mw)

    return mcp, args, middlewares, registered_tags


def mcp_server():
    mcp, args, middlewares, registered_tags = get_mcp_instance()

    # Clean version announcement (stderr or logger preferred)
    print(f"OneTrust Api MCP v{__version__}", file=sys.stderr)
    print("\nStarting MCP Server", file=sys.stderr)
    print(f"  Transport: {args.transport.upper()}", file=sys.stderr)
    print(f"  Auth: {args.auth_type}", file=sys.stderr)
    print(f"  Dynamic Tags Loaded: {len(registered_tags)}", file=sys.stderr)

    if args.transport == "stdio":
        mcp.run(transport="stdio")
    elif args.transport == "streamable-http":
        mcp.run(transport="streamable-http", host=args.host, port=args.port)
    elif args.transport == "sse":
        mcp.run(transport="sse", host=args.host, port=args.port)
    else:
        logger.error(f"Invalid transport: {args.transport}")
        sys.exit(1)


if __name__ == "__main__":
    mcp_server()
