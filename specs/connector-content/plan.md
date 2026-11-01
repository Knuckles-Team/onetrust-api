# CONN-ONETRUST-API-CONNECTOR-CONTENT — Implementation plan

Governing spec: [spec.md](spec.md). Rows: [requirements.md](requirements.md).

## Summary

This plan states how `onetrust-api` delivers the rows of `CONN-ONETRUST-API-CONNECTOR-CONTENT`. The live caller is the `onetrust-mcp` console script. The owner is the `onetrust_api` package. The rows reuse the `scion-sdk` helpers and add no second authority. The plan changes no runtime code.

## Technical Context

- **Language/Version**: Python >=3.12
- **Primary Dependencies**: scion-sdk[mcp]>=0.6.4,<0.7.0; fastmcp; further pins in `pyproject.toml` (scion-sdk[mcp]>=0.6.4,<0.7.0, python-dotenv>=1.2.4, requests>=2.34.2)
- **Storage**: N/A, the connector keeps no store of its own
- **Testing**: pytest; each row names the proving test as `path::name`
- **Target Platform**: Linux container and stdio or streamable HTTP MCP clients
- **Project Type**: connector
- **Performance Goals**: N/A, the vendor service sets the latency
- **Constraints**: vendor calls go through the SDK governed client; no connector-local transport
- **Scale/Scope**: 2 active row(s) in this spec

## Constitution Check

- Organization constitution 1.5.0, spec-first change: pass. Every behaviour is a row of this spec with a bound or planned test.
- Repository article R-I, connector scope: pass. The rows stay inside this connector's one external system and reuse the SDK for shared capabilities.

## Project Structure

- `pyproject.toml` (existing)
- `onetrust_api/__init__.py` (existing)
- `tests/test_default_content_surfaces.py` (existing)
- `onetrust_api/mcp_server.py` (existing)
- `tests/test_access_contracts.py` (new, planned)

## Phase 0: Research

No unknowns. Every row names its code and test; the caller chain of each row was read from the code.

## Phase 1: Design

### Summary

This plan states how `onetrust-api` delivers the rows of `CONN-ONETRUST-API-CONNECTOR-CONTENT`. The live caller is the `onetrust-mcp` console script. The owner is the `onetrust_api` package. The rows reuse the `scion-sdk` helpers and add no second authority. The plan changes no runtime code.

### Technical Context

- **Language/Version**: Python >=3.12
- **Primary Dependencies**: scion-sdk[mcp]>=0.6.4,<0.7.0; fastmcp; further pins in `pyproject.toml` (scion-sdk[mcp]>=0.6.4,<0.7.0, python-dotenv>=1.2.4, requests>=2.34.2)
- **Storage**: N/A, the connector keeps no store of its own
- **Testing**: pytest; each row names the proving test as `path::name`
- **Target Platform**: Linux container and stdio or streamable HTTP MCP clients
- **Project Type**: connector
- **Performance Goals**: N/A, the vendor service sets the latency
- **Constraints**: vendor calls go through the SDK governed client; no connector-local transport
- **Scale/Scope**: 2 active row(s) in this spec

### Constitution Check

- Organization constitution 1.5.0, spec-first change: pass. Every behaviour is a row of this spec with a bound or planned test.
- Repository article R-I, connector scope: pass. The rows stay inside this connector's one external system and reuse the SDK for shared capabilities.

### Project Structure

- `pyproject.toml` (existing)
- `onetrust_api/__init__.py` (existing)
- `tests/test_default_content_surfaces.py` (existing)
- `onetrust_api/mcp_server.py` (existing)
- `tests/test_access_contracts.py` (new, planned)

### Phase 0: Research

No unknowns. Every row names its code and test; the caller chain of each row was read from the code.

### Phase 1: Design

### Summary

This plan states how `onetrust-api` delivers the rows of `CONN-ONETRUST-API-CONNECTOR-CONTENT`. The live caller is the `onetrust-mcp` console script. The owner is the `onetrust_api` package. The rows reuse the `scion-sdk` helpers and add no second authority. The plan changes no runtime code.

### Technical Context

- **Language/Version**: Python >=3.12
- **Primary Dependencies**: scion-sdk[mcp]>=0.6.4,<0.7.0; fastmcp; further pins in `pyproject.toml` (scion-sdk[mcp]>=0.6.4,<0.7.0, python-dotenv>=1.2.4, requests>=2.34.2)
- **Storage**: N/A, the connector keeps no store of its own
- **Testing**: pytest; each row names the proving test as `path::name`
- **Target Platform**: Linux container and stdio or streamable HTTP MCP clients
- **Project Type**: connector
- **Performance Goals**: N/A, the vendor service sets the latency
- **Constraints**: vendor calls go through the SDK governed client; no connector-local transport
- **Scale/Scope**: 2 active row(s) in this spec

### Constitution Check

- Organization constitution 1.5.0, spec-first change: pass. Every behaviour is a row of this spec with a bound or planned test.
- Repository article R-I, connector scope: pass. The rows stay inside this connector's one external system and reuse the SDK for shared capabilities.

### Project Structure

- `pyproject.toml` (existing)
- `onetrust_api/__init__.py` (existing)
- `tests/test_default_content_surfaces.py` (existing)
- `onetrust_api/mcp_server.py` (existing)
- `tests/test_access_contracts.py` (new, planned)

### Phase 0: Research

No unknowns. Every row names its code and test; the caller chain of each row was read from the code.

### Phase 1: Design

### Architecture

`pyproject.toml` declares `onetrust-mcp` as the connector identity. `create_mcp_server` resolves the packaged content of `onetrust_api` from it.

### Phase 2: Task approach

`tasks.md` holds one task per row, producer first. Rows that depend on none run in parallel. A task is checked when its `Spec:` trailer is on the default branch.

### Complexity Tracking

None. The constitution check passed.

### Build contract

- `pre-commit run --all-files` runs ruff check, ruff format, the shared `connector-standard`, `spec`, `secrets` and `dependency-readiness` gates at the pinned shared revision.
- `uv run pytest tests` runs the proving tests; the shared complexity, duplication and KISS gates apply their org thresholds and this repository sets no local override.
- A change adds no scanner suppression and no duplicate implementation of an SDK helper.

### Production caller chain

- `CONN-ONETRUST-API-CONNECTOR-CONTENT-R001`: `onetrust-mcp` in `pyproject.toml` runs `onetrust_api.mcp_server:mcp_server`, which builds the server from the `scion_sdk.connector` entry point `onetrust_api:connector` (`onetrust_api/__init__.py:75`); the SDK `Connector` then lists the packaged skills, ontology and prompts.
- `CONN-ONETRUST-API-CONNECTOR-CONTENT-R002`: arbora `fleet.call` reaches the existing read tool of `onetrust_api/mcp_server.py`, whose result is validated against the `ac:AccessContract` rows declared in `onetrust_api/ontology/access_contracts.ttl`.

### Cross-repo seams

None. The rows depend only on the published `scion-sdk` package, which the connector imports.

### Phase 2: Task approach

`tasks.md` holds one task per row, producer first. Rows that depend on none run in parallel. A task is checked when its `Spec:` trailer is on the default branch.

### Complexity Tracking

None. The constitution check passed.

### Build contract

- `pre-commit run --all-files` runs ruff check, ruff format, the shared `connector-standard`, `spec`, `secrets` and `dependency-readiness` gates at the pinned shared revision.
- `uv run pytest tests` runs the proving tests; the shared complexity, duplication and KISS gates apply their org thresholds and this repository sets no local override.
- A change adds no scanner suppression and no duplicate implementation of an SDK helper.

### Production caller chain

- `CONN-ONETRUST-API-CONNECTOR-CONTENT-R001`: `onetrust-mcp` in `pyproject.toml` runs `onetrust_api.mcp_server:mcp_server`, which builds the server from the `scion_sdk.connector` entry point `onetrust_api:connector` (`onetrust_api/__init__.py:75`); the SDK `Connector` then lists the packaged skills, ontology and prompts.
- `CONN-ONETRUST-API-CONNECTOR-CONTENT-R002`: arbora `fleet.call` reaches the existing read tool of `onetrust_api/mcp_server.py`, whose result is validated against the `ac:AccessContract` rows declared in `onetrust_api/ontology/access_contracts.ttl`.

### Cross-repo seams

None. The rows depend only on the published `scion-sdk` package, which the connector imports.

## Phase 2: Task approach

`tasks.md` holds one task per row, producer first. Rows that depend on none run in parallel. A task is checked when its `Spec:` trailer is on the default branch.

## Complexity Tracking

None. The constitution check passed.

## Build contract

- `pre-commit run --all-files` runs ruff check, ruff format, the shared `connector-standard`, `spec`, `secrets` and `dependency-readiness` gates at the pinned shared revision.
- `uv run pytest tests` runs the proving tests; the shared complexity, duplication and KISS gates apply their org thresholds and this repository sets no local override.
- A change adds no scanner suppression and no duplicate implementation of an SDK helper.

## Production caller chain

- `CONN-ONETRUST-API-CONNECTOR-CONTENT-R001`: `onetrust-mcp` in `pyproject.toml` runs `onetrust_api.mcp_server:mcp_server`, which builds the server from the `scion_sdk.connector` entry point `onetrust_api:connector` (`onetrust_api/__init__.py:75`); the SDK `Connector` then lists the packaged skills, ontology and prompts.
- `CONN-ONETRUST-API-CONNECTOR-CONTENT-R002`: arbora `fleet.call` reaches the existing read tool of `onetrust_api/mcp_server.py`, whose result is validated against the `ac:AccessContract` rows declared in `onetrust_api/ontology/access_contracts.ttl`.

## Cross-repo seams

None. The rows depend only on the published `scion-sdk` package, which the connector imports.
