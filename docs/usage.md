# Usage

## Python client

```python
from onetrust_api.auth import get_client

client = get_client()  # reads ONETRUST_* environment variables

# Every OpenAPI operation is a method on the composite Api client.
incident = client.create_incident_using_post(body={"name": "Data breach"})
print(incident.status_code, incident.data)

# List endpoints paginate automatically (offset or cursor):
records = client.get_data_subjects_v4(page=0, size=200)
```

Every call returns a `Response` wrapper exposing `.data` (decoded JSON) plus
`.status_code` and `.headers`.

## MCP server

Each API operation is its own tool, named `onetrust_<operation>`. Pass the path,
query and body fields as named arguments:

```jsonc
// tool: onetrust_create_incident_using_post
{ "name": "Data breach", "incidentTypeName": "Breach", "orgGroupId": "..." }
```

```jsonc
// tool: onetrust_get_all_request_queues_v2_using_get
{ "page": 0, "size": 50 }
```

The `custom_api` tool (`onetrust_api_request`) issues arbitrary requests for any
endpoint not yet wrapped:

```jsonc
{ "method": "GET", "endpoint": "/api/incident/v1/incidents",
  "params_json": "{\"params\": {\"page\": 0}}" }
```

## A2A agent

```bash
onetrust-agent --provider openai --model-id gpt-4o --api-key sk-...
```

The agent auto-discovers the MCP tools from `mcp_config.json`; with this multiple
domains the scion-sdk graph router engages automatically to keep the active
tool set focused per turn.
