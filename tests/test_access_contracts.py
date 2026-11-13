"""Access contracts bind fields the served read tools return."""

import asyncio
import json
import sys
from pathlib import Path

import pytest
from fastmcp import Client
from scion_sdk.access_contract import parse_access_contracts

from tests.conftest import _make_response

ROOT = Path(__file__).resolve().parents[1]
ONTOLOGY = ROOT / "onetrust_api/ontology"


def _contracts():
    text = (ONTOLOGY / "access_contracts.ttl").read_text()
    return {c.entity: c for c in parse_access_contracts(text)}


def _serve(monkeypatch, mock_session, contract, recording):
    mock_session.request.return_value = _make_response(recording)
    monkeypatch.setattr(sys, "argv", ["onetrust-mcp", "--transport", "stdio"])
    from onetrust_api.mcp_server import get_mcp_instance

    mcp, _args, _mw, _tags = get_mcp_instance()

    async def call():
        async with Client(mcp) as client:
            return await client.call_tool(contract.operation, {})

    result = asyncio.run(call())
    return result.data if result.data is not None else result.structured_content


@pytest.mark.spec("CONN-ONETRUST-API-CONNECTOR-CONTENT-R002")
def test_competency_contracts_certified(monkeypatch, mock_session):
    contract = _contracts()["risk"]
    recording = json.loads((ROOT / "tests/recordings/risk.json").read_text())
    ontology = (ONTOLOGY / "onetrust.ttl").read_text()
    fields = {"name", "serviceRef"}
    assert contract.access_kind == "mcp_tool"
    assert contract.key_field == "id"
    assert {field for _, field in contract.predicates} == fields
    for prop, _ in contract.predicates:
        local = prop.rsplit("#", 1)[-1]
        assert f":{local} a owl:DatatypeProperty" in ontology
    payload = _serve(monkeypatch, mock_session, contract, recording)
    records = payload
    for part in contract.records_path.split("."):
        records = records[part]
    assert records
    for record in records:
        assert contract.key_field in record
        assert all(field in record for field in fields)
