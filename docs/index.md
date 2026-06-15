# onetrust-api

Python **OneTrust** API client + **MCP** server + **A2A** agent, with **100%
coverage** of the OneTrust public API.

Every operation across all 35 OpenAPI specifications (~600 operations, 7 product
areas) is exposed as both a typed client method and an action-routed MCP tool —
all generated from the vendored specs and verified by a coverage test.

- **[Overview](overview.md)** — what the package covers and how it is built.
- **[Installation](installation.md)** — install and configure credentials.
- **[Usage](usage.md)** — Python client, MCP server, and A2A agent.
- **[Deployment](deployment.md)** — Docker and container deployment.

```bash
pip install onetrust-api[all]
```
