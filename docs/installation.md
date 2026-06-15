# Installation

```bash
pip install onetrust-api[all]      # client + MCP + agent
# or scoped:
pip install onetrust-api[mcp]      # client + MCP server
pip install onetrust-api[agent]    # client + A2A agent
pip install onetrust-api           # client only
```

## Credentials

OneTrust uses OAuth2. Use **one** of:

1. **Pre-minted bearer token** — create credentials in *Global Settings >
   Access Management > Credentials* and set `ONETRUST_TOKEN`.
2. **Client-credentials** — set `ONETRUST_CLIENT_ID` and `ONETRUST_CLIENT_SECRET`;
   the client exchanges them at `/api/access/v1/oauth/token` and refreshes
   automatically before expiry.

## Host configuration

Set `ONETRUST_URL` to your tenant pod (e.g. `https://acme.my.onetrust.com`), or
set `ONETRUST_REGION` to use a shared regional pod (`us`, `eu`, `de`, `uk`, `au`,
`ca`, `fr`, `in`, `jp`, `trial`, `uat`, …). Consent-transaction and on-prem worker
endpoints can be pointed elsewhere with `ONETRUST_CONSENT_URL` and
`ONETRUST_WORKER_URL`.

See `.env.example` for the full list.
