"""100% coverage keystone.

Proves — offline, against the vendored OpenAPI specs — that every OneTrust
operation is reachable as both a typed client method AND an MCP action, and that
the three sets (spec operationIds, client methods, MCP actions) are mutually
consistent. If OneTrust revises a spec and the generator is re-run, this test is
what guarantees nothing silently drops.
"""

import json
from pathlib import Path

import pytest

from onetrust_api.api._operation_manifest import (
    ACTIONS_BY_DOMAIN,
    DOMAINS,
    OPERATIONS,
)
from onetrust_api.api_client import Api

PKG = Path(__file__).resolve().parent.parent / "onetrust_api"
SPECS = PKG / "specs"
MCP = PKG / "mcp"
HTTP_METHODS = ("get", "post", "put", "delete", "patch")


def _count_spec_operations() -> int:
    total = 0
    for spec_path in SPECS.glob("*.json"):
        spec = json.loads(spec_path.read_text())
        for _path, methods in (spec.get("paths") or {}).items():
            for http, op in methods.items():
                if http in HTTP_METHODS and isinstance(op, dict):
                    total += 1
    return total


def test_specs_present():
    assert len(list(SPECS.glob("*.json"))) == 35


#: Operations deliberately not served: the endpoint is deprecated upstream and its
#: ``{action}`` path parameter selects among thirteen workflow states.
NOT_SERVED = 1


def test_manifest_covers_every_spec_operation():
    assert len(OPERATIONS) == _count_spec_operations() - NOT_SERVED
    assert len(OPERATIONS) > 0


def test_every_operation_has_callable_client_method():
    missing = [
        op for op in OPERATIONS if not callable(getattr(Api, op["method"], None))
    ]
    assert not missing, (
        f"{len(missing)} operations without a client method: {missing[:5]}"
    )


def test_method_names_globally_unique():
    methods = [op["method"] for op in OPERATIONS]
    assert len(methods) == len(set(methods))


def test_actions_unique_within_each_domain():
    for domain, actions in ACTIONS_BY_DOMAIN.items():
        assert len(actions) == len(set(actions)), f"duplicate actions in {domain}"


def test_no_action_routed_domain_module_remains():
    """Every operation is its own tool; no per-domain action router is packaged."""
    modules = {path.name for path in MCP.glob("mcp_*.py")}
    assert modules == {"mcp_custom_api.py"}


@pytest.mark.asyncio
async def test_every_operation_is_its_own_tool(monkeypatch):
    from unittest.mock import patch

    from onetrust_api.mcp_server import get_mcp_instance

    with patch("sys.argv", ["onetrust-mcp", "--transport", "stdio"]):
        mcp, *_ = get_mcp_instance()
        names = {tool.name for tool in await mcp.list_tools()}
    missing = [
        op["method"] for op in OPERATIONS if f"onetrust_{op['method']}" not in names
    ]
    assert not missing, missing[:5]


def test_custom_api_escape_hatch_present():
    src = (MCP / "mcp_custom_api.py").read_text()
    assert "onetrust_api_request" in src
    assert callable(Api.api_request)


def test_manifest_operations_carry_typed_params():
    """Verbose typed tier: ops with inputs expose a normalized ``params`` list."""
    assert all("params" in op and "summary" in op for op in OPERATIONS)
    # the vast majority of operations take inputs (path/query/body)
    with_params = [op for op in OPERATIONS if op["params"]]
    assert len(with_params) > len(OPERATIONS) // 2
    sample = with_params[0]["params"][0]
    assert set(sample) >= {"name", "type", "required", "description"}


@pytest.mark.asyncio
@pytest.mark.parametrize("legacy_mode", ["condensed", "verbose", "both", "intent"])
async def test_legacy_modes_keep_current_gated_domain_surface(monkeypatch, legacy_mode):
    """The supported SDK always registers action-routed, gated domain tools."""
    from unittest.mock import patch

    from onetrust_api.mcp_server import get_mcp_instance

    monkeypatch.setenv("MCP_TOOL_MODE", legacy_mode)
    with patch("sys.argv", ["onetrust-mcp", "--transport", "stdio"]):
        mcp, *_ = get_mcp_instance()
        tools = {tool.name: tool for tool in await mcp.list_tools()}
    # SDK >= 0.3.0 serves one gated tool per API operation in every legacy mode.
    assert len(tools) > 500
    assert {
        "onetrust_api_request",
        "onetrust_ingest_assessments",
        "onetrust_ingest_cookies",
        "onetrust_ingest_inventories",
    } <= set(tools)
    assert not {f"onetrust_{domain}" for domain in DOMAINS} & set(tools)
    assert {"granular", "gated"} <= tools["onetrust_api_request"].tags
