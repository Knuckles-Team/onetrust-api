"""CONN-ONETRUST-API-CONNECTOR-CONTENT-R001: the served surface is complete (contracts, links, locations, roles, prompts, skills)."""

import pytest

pytestmark = pytest.mark.spec("CONN-ONETRUST-API-CONNECTOR-CONTENT-R001")


def test_served_surface_has_no_gaps(monkeypatch):
    from scion_sdk.testing.surface_check import surface_check

    monkeypatch.setenv("ONETRUST_URL", "https://tenant.example.invalid")
    assert surface_check("onetrust_api") == []


def test_every_tool_has_exactly_one_typed_operation():
    from onetrust_api.api._operation_manifest import OPERATIONS
    from onetrust_api.connector_contracts import CONTRACTS

    called = {step.tool for contract in CONTRACTS for step in contract.steps}
    missing = [
        op["method"] for op in OPERATIONS if f"onetrust_{op['method']}" not in called
    ]
    assert not missing, missing[:5]
