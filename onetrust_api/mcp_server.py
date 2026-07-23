#!/usr/bin/python

import logging
import sys
from typing import Any

from agent_utilities.core.config import load_config
from agent_utilities.mcp.server_factory import create_mcp_server
from agent_utilities.mcp.verbose_tools import register_tool_surface
from fastmcp import FastMCP
from fastmcp.utilities.logging import get_logger

from onetrust_api.api._operation_manifest import OPERATIONS
from onetrust_api.api_client import Api
from onetrust_api.auth import get_client

__version__ = "1.0.0"

# Redirect logging to stderr to prevent MCP stdout corruption
logger = get_logger(name="onetrust_mcp")
logger.setLevel(logging.INFO)


def register_prompts(mcp: FastMCP):
    @mcp.prompt(name="example_prompt", description="Example prompt for OneTrust Api.")
    def example_prompt(query: str) -> str:
        """Example prompt."""
        return f"Please help with '{query}' using OneTrust Api"


def _records(result: Any) -> list[dict[str, Any]]:
    """Normalise a client Response / dict / list into a list of record dicts."""
    data = getattr(result, "data", result)
    if isinstance(data, dict):
        for key in ("content", "data", "items", "results", "records"):
            if isinstance(data.get(key), list):
                return data[key]
        return [data]
    if isinstance(data, list):
        return [r for r in data if isinstance(r, dict)]
    return []


def register_ingest_tools(mcp: FastMCP):
    """Wire-First native KG ingestion tools — list via the real client, push typed nodes.

    CONCEPT:AU-KG.ingest.enterprise-source-extractor. Each tool lists OneTrust records
    through the composite ``Api`` client and pushes them into the epistemic-graph as typed
    OWL nodes (matching onetrust.ttl). Native-ingest failures propagate to the caller.
    """
    from fastmcp import Context
    from fastmcp.dependencies import Depends

    from onetrust_api import kg_ingest

    @mcp.tool(tags={"ingest"})
    async def onetrust_ingest_assessments(
        params_json: str = "{}",
        client=Depends(get_client),
        ctx: Context | None = None,
    ) -> Any:
        """Ingest OneTrust assessments into the KG as typed :Assessment nodes + :Document summaries.

        Lists assessments via ``get_all_assessment_basic_details_using_get`` (params_json is a
        JSON string of its query params, e.g. ``{"size":100}``) and pushes each as an
        :Assessment (+ :AssessmentTemplate / :Person links) plus a companion :Document.
        """
        import json

        kwargs = json.loads(params_json) if params_json else {}
        result = client.get_all_assessment_basic_details_using_get(**kwargs)
        records = _records(result)
        if ctx:
            await ctx.info(f"Ingesting {len(records)} assessments into the KG")
        nodes = kg_ingest.ingest_assessments(records)
        documents = kg_ingest.assessment_documents(records)
        docs = (
            kg_ingest.ingest_documents(documents)
            if documents
            else {"nodes": 0, "edges": 0}
        )
        return {"listed": len(records), "ingested": nodes, "documents": docs}

    @mcp.tool(tags={"ingest"})
    async def onetrust_ingest_cookies(
        params_json: str = "{}",
        client=Depends(get_client),
        ctx: Context | None = None,
    ) -> Any:
        """Ingest OneTrust cookie-scan results into the KG as typed :Cookie (+ :CookieDomain) nodes.

        Lists cookies via ``get_cookies_by_filter`` (params_json = its JSON query/body params).
        """
        import json

        kwargs = json.loads(params_json) if params_json else {}
        result = client.get_cookies_by_filter(**kwargs)
        records = _records(result)
        if ctx:
            await ctx.info(f"Ingesting {len(records)} cookies into the KG")
        nodes = kg_ingest.ingest_cookies(records)
        return {"listed": len(records), "ingested": nodes}

    @mcp.tool(tags={"ingest"})
    async def onetrust_ingest_inventories(
        params_json: str = "{}",
        client=Depends(get_client),
        ctx: Context | None = None,
    ) -> Any:
        """Ingest OneTrust data-inventory records into the KG as typed :Inventory (+ :DataElement) nodes.

        Lists inventories via ``get_list_of_inventories_using_get`` (params_json = its JSON query params).
        """
        import json

        kwargs = json.loads(params_json) if params_json else {}
        result = client.get_list_of_inventories_using_get(**kwargs)
        records = _records(result)
        if ctx:
            await ctx.info(f"Ingesting {len(records)} inventory records into the KG")
        nodes = kg_ingest.ingest_inventories(records)
        return {"listed": len(records), "ingested": nodes}


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
    register_ingest_tools(mcp)

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
