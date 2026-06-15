#!/usr/bin/python
# coding: utf-8

import os
import sys
import logging
from typing import Optional, List, Dict, Union, Any

from dotenv import load_dotenv, find_dotenv
from fastmcp import FastMCP
from pydantic import Field
from agent_utilities.base_utilities import to_boolean
from agent_utilities.mcp_utilities import create_mcp_server, config
from agent_utilities.utilities import get_logger
from onetrust_api.auth import get_client

__version__ = "0.1.0"

# Redirect logging to stderr to prevent MCP stdout corruption
logger = get_logger(name="MCP_Server")
logger.setLevel(logging.INFO)


def register_prompts(mcp: FastMCP):
    @mcp.prompt(
        name="example_prompt", description="Example prompt for OneTrust Api."
    )
    def example_prompt(query: str) -> str:
        """Example prompt."""
        return f"Please help with '{query}' using OneTrust Api"


def get_mcp_instance() -> tuple[Any, Any, Any, Any]:
    """Initialize and return the OneTrust Api MCP instance, args, and middlewares."""
    load_dotenv(find_dotenv())

    args, mcp, middlewares = create_mcp_server(
        name="OneTrust Api MCP",
        version=__version__,
        instructions="OneTrust Api MCP Server",
    )

    # TODO: Register tool groups here with env-var toggles.
    # Pattern: if to_boolean(os.getenv("TOOL_TAG_NAME", "True")): register_tools(mcp)

    register_prompts(mcp)

    for mw in middlewares:
        mcp.add_middleware(mw)

    registered_tags = []
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
