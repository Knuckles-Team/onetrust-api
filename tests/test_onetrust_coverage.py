"""100% coverage keystone.

Proves — offline, against the vendored OpenAPI specs — that every OneTrust
operation is reachable as both a typed client method AND an MCP action, and that
the three sets (spec operationIds, client methods, MCP actions) are mutually
consistent. If OneTrust revises a spec and the generator is re-run, this test is
what guarantees nothing silently drops.
"""

import json
import re
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


def test_manifest_covers_every_spec_operation():
    assert len(OPERATIONS) == _count_spec_operations()
    assert len(OPERATIONS) > 0


def test_every_operation_has_callable_client_method():
    missing = [
        op for op in OPERATIONS if not callable(getattr(Api, op["method"], None))
    ]
    assert (
        not missing
    ), f"{len(missing)} operations without a client method: {missing[:5]}"


def test_method_names_globally_unique():
    methods = [op["method"] for op in OPERATIONS]
    assert len(methods) == len(set(methods))


def test_actions_unique_within_each_domain():
    for domain, actions in ACTIONS_BY_DOMAIN.items():
        assert len(actions) == len(set(actions)), f"duplicate actions in {domain}"


@pytest.mark.parametrize("domain", sorted(DOMAINS))
def test_every_action_is_routed_in_its_mcp_tool(domain):
    """Spec operations == manifest actions == actions routed in the generated tool."""
    src = (MCP / f"mcp_{domain}.py").read_text()
    # Whitespace-tolerant: the formatter wraps long ``elif action == "..."`` lines.
    routed = set(re.findall(r'action\s*==\s*"([^"]+)"', src))
    expected = set(ACTIONS_BY_DOMAIN[domain])
    assert routed == expected, f"{domain}: {routed ^ expected}"
    assert f"def onetrust_{domain}(" in src


def test_custom_api_escape_hatch_present():
    src = (MCP / "mcp_custom_api.py").read_text()
    assert "onetrust_api_request" in src
    assert callable(Api.api_request)
