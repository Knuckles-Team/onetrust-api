---
name: onetrust-cookie-consent
description: >-
  Cookie-consent scanning and categorization on the OneTrust Cookie Consent API
  via the onetrust-api MCP server — scan domains/apps, list discovered cookies,
  categorize/recategorize them, and publish consent scripts with the domain-typed
  tool. Use when the agent must launch or check a cookie scan, review the cookies
  found on a domain, bulk edit/categorize cookies, or publish a banner script. Do
  NOT use for privacy assessments (onetrust-privacy-assessments) or the data
  inventory (onetrust-data-mapping); prefer those.
license: MIT
tags: [onetrust, cookies, consent, cmp, scanning, privacy, mcp]
metadata:
  author: Genius
  version: '0.1.0'
---
# OneTrust Cookie Consent

Domain-typed access to the OneTrust **Cookie Consent** API for website/app cookie
scanning, cookie categorization, and consent-script publishing. Prefer the
condensed `onetrust_cookie_consent` tool over raw HTTP.

## When to use
- Kick off or check a cookie scan of a domain or mobile app.
- List / filter the cookies discovered by scans and read scan result summaries.
- Bulk add / edit / delete / recategorize cookies.
- Publish a consent script to a site or app, or download the script file.

## When NOT to use
- Privacy / risk assessments → `onetrust-privacy-assessments`.
- The data inventory (assets/vendors) and data elements → `onetrust-data-mapping`.
- Consent **receipts** / universal consent transactions → `onetrust_consent_receipts`
  / `onetrust_universal_consent`.
- Legacy cookie endpoints → the `cookie_consent_legacy` tag if a tenant still uses it.

## Prerequisites & environment
Connect via the `mcp-client` skill against the **`onetrust-api`** MCP server.

| Variable | Required | Notes |
|----------|----------|-------|
| `ONETRUST_HOSTNAME` | ✅ | Tenant host, e.g. `app.onetrust.com` |
| `ONETRUST_API_TOKEN` | ✅ | Bearer OAuth token (or client-credentials pair) |
| `ONETRUST_CLIENT_ID` / `ONETRUST_CLIENT_SECRET` | optional | OAuth2 client-credentials |

Enable the `cookie_consent` tag (default in the condensed surface). `MCP_TOOL_MODE`
selects condensed vs. verbose.

## Tools & actions
| Condensed tool | Key actions |
|----------------|-------------|
| `onetrust_cookie_consent` | `get_applications`, `create_application`, `scan_application`, `add_scans`, `schedule_scans`, `check_scans_status`, `get_domain_scans`, `get_scan_result_summary`, `get_detailed_scan_result_information`, `get_cookies_by_filter`, `get_categorized_cookies`, `bulk_add_cookies`, `bulk_edit_cookies`, `bulk_delete_cookies`, `recategorize_cookies_by_scan`, `publish_script_to_site`, `download_script_file` |

### Key parameters
- `get_cookies_by_filter` — filter/page body selecting cookies to return.
- `add_scans` / `schedule_scans` — the domain(s) or app(s) to scan.
- `recategorize_cookies_by_scan` — a scan id to re-run categorization against.
- Cookie records expose `cookieId`, `cookieName`, `host`, `lifespan`,
  `displayGroupName` (category), and `thirdParty`.

## Recipes (`params_json`)
List cookies via filter:
```json
{"action":"get_cookies_by_filter","params_json":"{\"page\":0,\"size\":100}"}
```
Check the status of running scans:
```json
{"action":"check_scans_status","params_json":"{\"scanIds\":[\"<scanId>\"]}"}
```
Get a scan's result summary:
```json
{"action":"get_scan_result_summary","params_json":"{\"scanId\":\"<scanId>\"}"}
```

## Gotchas
- `params_json` is a **string** of JSON, not an object — serialize it (note the
  escaped inner JSON in the recipes above).
- Scans are asynchronous: `add_scans`/`scan_application` return quickly; poll
  `check_scans_status` before reading results.
- Cookie category lives in `displayGroupName` (the OneTrust display group), while
  `cookiepediaCategory` is the Cookiepedia-suggested category — they can differ.
- `thirdParty` is a boolean flag; a missing value means "unknown", not "first party".
- Publishing a script (`publish_script_to_site`) is a **write** that changes the
  live banner — confirm the domain/app id before calling.

## Related
- **KG ingestion:** `onetrust_ingest_cookies` (Wire-First) lists cookies and pushes
  them into the knowledge graph as typed `:Cookie` nodes with `:scannedOnDomain`
  links to `:CookieDomain`. Use it for ingestion, not the scan/publish recipes.
- **Prompt:** the `consent_cookie_specialist` prompt composes this skill.
- **Sibling skills:** `onetrust-privacy-assessments`, `onetrust-data-mapping`.
