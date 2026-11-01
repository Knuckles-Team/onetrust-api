# CONN-ONETRUST-API-CONNECTOR-IDENTITY — Requirements

Governing spec: [spec.md](spec.md).

Each row is one requirement. A row names the file it touches and the test that proves it. The generator sets each row's state in `status.json`.

| ID | Requirement | Acceptance |
|---|---|---|
| `CONN-ONETRUST-API-CONNECTOR-IDENTITY-R001` | **Fleet name.** `pyproject.toml` declares `onetrust-mcp` as the single `scion_sdk.connector` entry point. The content pack, the manifest `connector`, the fingerprints and the ingest binding all carry `onetrust-mcp`. Caller chain: `onetrust-mcp` in `pyproject.toml` runs `onetrust_api.mcp_server:mcp_server`, which builds the server from the `scion_sdk.connector` entry point `onetrust_api:connector` (`onetrust_api/__init__.py:75`); `connector_name("onetrust_api")` in the SDK resolves the same entry point name for the content pack, the manifest and the ingest binding. Shape: `pyproject.toml` entry point `onetrust-mcp`, the `connector_name` helper of the SDK and the `ConnectorContent`/`IngestBinding` calls under `onetrust_api/`; reuses the SDK name resolution and adds no second constant. Proving test: `tests/test_fleet_name.py::test_connector_name_is_the_fleet_name`. | Every connector name in the package is `onetrust-mcp`. |
