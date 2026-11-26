---
name: onetrust-api-operations
skill_type: skill
description: >-
  Operate onetrust-api through its governed MCP and Arbora capabilities, including cookie consent, data mapping, privacy assessments, consent preferences, privacy requests, risk and compliance, governance content and platform administration. Use when a request requires this provider's read, change, automation, ingestion, troubleshooting, or evidence workflows.
---

# Onetrust Api Operations

Use the provider's governed MCP tools through Arbora delegation.

## Workflow

1. Establish the verified GraphSession and tenant before discovery or retrieval.
2. Discover the current typed tool surface (one tool per API operation); never assume a stale tool name or schema.
3. Prefer read-only inspection first. For changes, present impact and use the provider's
   dry-run or preview mode when available.
4. Execute mutations as fenced WorkItems so retries remain idempotent and auditable.
5. Ingest source data only through the signed connector preset and ChangeEnvelope path.
6. Verify the durable result and its trace/evidence before reporting completion.

## Safety contract

- Never persist credentials, endpoints, raw personal identifiers, hostnames, or local paths.
- Resolve TLS trust and verification from environment/configuration; never hardcode bypasses.
- Treat unknown ACL, tenant, schema, or tool-contract state as a hard failure.
- Require explicit approval for destructive, externally visible, or irreversible actions.
- Keep runtime traces policy-scoped and privacy-sanitized.

## Steps

1. Open `references/catalog.md` to pick the one OneTrust skill whose scope matches the request, and verify the request is not covered by a sibling skill's When NOT to use list.
2. Discover the current typed tool surface through Arbora with `find` and verify the exact tool name and its parameter schema before any call.
3. Run a read-only `ask` call for the target record and verify the response returns the record id and current status you expect.
4. For a change, state the impact to the person and verify explicit approval exists before the `write` or `act` preview is executed with `execute=true`.
5. Execute the single mutation as a fenced WorkItem with `act` and verify the call returned a success status and an evidence reference.
6. Read the record back with the same `ask` read call and verify the changed field now holds the new value before reporting completion.

## Failure recovery

| Failure | Cause | Recovery |
|---|---|---|
| 401 or 403 response | `ONETRUST_TOKEN` or the client id and secret pair is missing or expired, or `ONETRUST_URL` points at the wrong tenant | Set `ONETRUST_TOKEN` (or `ONETRUST_CLIENT_ID` with `ONETRUST_CLIENT_SECRET`) and `ONETRUST_URL` or `ONETRUST_REGION` in the environment, restart the server, and repeat the first read call |
| Tool not found or schema mismatch | The tool name came from memory and the surface changed | Call `find` again for the operation and use the name and parameters it returns |
| Mutation rejected for missing approval | The destructive or externally visible action had no explicit approval recorded | Ask the person to approve the named action, record the approval, and resubmit the same WorkItem |

## Specialized workflows

Read [the workflow catalog](references/catalog.md) only when the request needs a
provider-specific procedure, parameter map, script, or reference asset.
