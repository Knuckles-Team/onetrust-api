#!/usr/bin/python

import logging
import sys
from typing import Any

from agent_utilities.core.config import setting
from agent_utilities.mcp_utilities import (
    create_mcp_server,
    load_config,
    register_verbose_tools,
    tool_mode,
)
from fastmcp import FastMCP
from fastmcp.utilities.logging import get_logger

from onetrust_api.api._operation_manifest import OPERATIONS
from onetrust_api.api_client import Api
from onetrust_api.auth import get_client

__version__ = "0.2.0"

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
    mode = tool_mode()

    args, mcp, middlewares = create_mcp_server(
        name="OneTrust Api MCP",
        version=__version__,
        instructions="OneTrust Api MCP Server",
    )

    registered_tags = []
    # condensed: per-domain action-routed tools, each gated by a {TAG}TOOL env var
    # (default True). TOOL_REGISTRY is generated from the vendored OpenAPI specs.
    if mode in ("condensed", "both"):
        from onetrust_api.mcp import TOOL_REGISTRY

        for tag, env_var, register_fn in TOOL_REGISTRY:
            if setting(env_var, True):
                register_fn(mcp)
                registered_tags.append(tag)

    # verbose: one fully-typed 1:1 tool per API method, sourced from the OpenAPI
    # manifest (params drive the typed signatures).
    if mode in ("verbose", "both"):
        register_verbose_tools(
            mcp, Api, get_client, service="onetrust-api", manifest=OPERATIONS
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
