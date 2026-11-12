---
name: onetrust-cookie-consent
skill_type: skill
description: >-
  Cookie and consent-banner operations on OneTrust: scan domains and mobile apps, read and
  categorize discovered cookies, manage geolocation rule groups, templates and branding,
  publish consent scripts, and read consent-management-platform vendors and interfaces.
  Use when the agent must launch or check a scan, categorize cookies in bulk, or publish a
  banner script. Do NOT use for consent receipts and preferences (onetrust-consent-
  preferences) or assessments (onetrust-privacy-assessments).
license: MIT
tags: [onetrust, cookies, consent, cmp, scanning, privacy, mcp]
metadata:
  author: Knuckles-Team
  version: '1.0.0'
---
# OneTrust Cookie Consent

A cookie programme scans each site or app, categorizes what it finds, and publishes a consent script that enforces those categories. Scans run asynchronously, so results are read only after the scan status reports completion.

## When to use
- Create applications and domains, schedule or start scans and poll their status.
- Read scan summaries, deltas and detailed results.
- Search, add, edit, recategorize and delete cookies.
- Manage geolocation rule groups, templates and branding attributes.
- Publish or download consent scripts; mirror cookies into the graph.

## When NOT to use
- Consent transactions and preference centres: use onetrust-consent-preferences.
- Data-subject requests: use onetrust-dsar-incident-response.

## Workflow
1. Resolve the domain or application, then list its scans.
2. Start or schedule a scan and poll the scan status until it completes.
3. Read the scan summary, then the detailed results, before categorizing.
4. Apply category changes in bulk, then publish the script only after the person approves.

## Safety
- Publishing a script changes a live banner on a production site; ask first and name the site.
- Bulk delete of cookies and domain deletion are not reversible from this connector.

## Tools (58)

Each tool is one API operation; pass its path, query and body fields as named arguments.


### Cmp

| Tool | Method | Purpose |
|---|---|---|
| `onetrust_get_banner` | GET | Get Banner Data |
| `onetrust_get_preferences` | GET | Get Preference Center Data |
| `onetrust_get_ucpurposes` | GET | Get Universal Consent Purposes |
| `onetrust_get_vendors` | GET | Get IAB and Google Vendors |
| `onetrust_post_log_consent` | POST | Log Consent |

### Consent Interfaces

| Tool | Method | Purpose |
|---|---|---|
| `onetrust_get_realtime_preferences` | GET | Get Data Subject's Preferences |

### Cookie Consent

| Tool | Method | Purpose |
|---|---|---|
| `onetrust_check_scans_status` | POST | Get Scan Statuses |
| `onetrust_download_script_file` | GET | Download Script File |
| `onetrust_get_app_script_details` | GET | Get Script for Application |
| `onetrust_get_application_branding_attribute_list` | GET | Get Branding Attributes for Application |
| `onetrust_get_applications` | GET | Get List of Applications |
| `onetrust_get_branding_attribute_list` | GET | Get Branding Attributes for Domain |
| `onetrust_get_categorized_cookies` | POST | Get Categorized Cookies |
| `onetrust_get_cookies_by_filter` | POST | Get List of Cookies by Criteria |
| `onetrust_get_detailed_scan_result_information` | GET | Get Scan Results |
| `onetrust_get_domain_scans` | GET | Get List of Scans by Domain |
| `onetrust_get_domains_scanned_by_sort` | GET | Get List of Websites |
| `onetrust_get_geo_rule_group_details` | GET | Get Geolocation Rule Group |
| `onetrust_get_geo_rule_groups` | GET | Get List of Geolocation Rule Groups |
| `onetrust_get_scan_delta_details` | GET | Get List of Added or Removed Cookies |
| `onetrust_get_scan_result_summary` | GET | Get Scan Result Summary |
| `onetrust_get_script_details` | GET | Get Script for Domain |
| `onetrust_get_script_for_website` | GET | Get Script for Website |
| `onetrust_get_template_details` | GET | Get Template Details |
| `onetrust_get_templates` | GET | Get List of Templates |
| `onetrust_add_scans` | POST | Scan Websites |
| `onetrust_archive_scans` | POST | Archive Scans |
| `onetrust_bulk_add_cookies` | POST | Add Cookies |
| `onetrust_bulk_cancel_domain_schedule` | POST | Cancel Scheduled Website Scans |
| `onetrust_create_application` | POST | Create Application |
| `onetrust_create_domain_group` | POST | Create or Update Domain Group |
| `onetrust_schedule_scans` | POST | Schedule Website Scans |
| `onetrust_assign_entities_to_geo_rule_group` | PUT | Assign Geolocation Rule Group |
| `onetrust_bulk_edit_cookies` | PUT | Edit Cookies |
| `onetrust_cancel_scan` | PUT | Cancel Scan |
| `onetrust_publish_app_script` | PUT | Publish Application SDK |
| `onetrust_publish_script_to_site` | PUT | Publish Script to Website |
| `onetrust_recategorize_cookies_by_scan` | PUT | Recategorize Cookies |
| `onetrust_scan_application` | PUT | Scan Application |
| `onetrust_update_application_branding_attributes_for_public_api` | PUT | Update Branding Attributes for Application |
| `onetrust_update_branding_attributes_for_public_api` | PUT | Update Branding Attributes for Domain |
| `onetrust_bulk_delete_cookies` | DELETE | Delete Cookies |
| `onetrust_delete_domain` | DELETE | Delete Domain |

### Cookie Consent Legacy

| Tool | Method | Purpose |
|---|---|---|
| `onetrust_download_to_local_using_get` | GET | Download Script File |
| `onetrust_get_categorized_cookies_using_get` | POST | Categorize Cookies by Domain |
| `onetrust_get_categorized_cookies_with_cookie_ids_using_get` | POST | Categorize Cookies by Domain and Cookie ID |
| `onetrust_get_cookie_reports_using_post` | POST | Get List of Cookies by Criteria |
| `onetrust_get_domains_scanned_by_sort_using_get` | GET | Get List of Websites |
| `onetrust_get_script_for_website_using_get` | GET | Get Script for Website |
| `onetrust_create_domain_group_using_post` | POST | Create or Update Domain Group |
| `onetrust_create_new_cookie` | POST | Create Cookie |
| `onetrust_request_bulk_add_domain_using_post` | POST | Add Websites to Scan |
| `onetrust_publish_to_site_using_put` | PUT | Publish Script to Website |
| `onetrust_update_cookie` | PUT | Update Cookie |

### Cookie Domain Data

| Tool | Method | Purpose |
|---|---|---|
| `onetrust_domaindata` | GET | Get Domain Data |

### Cross Device Consent

| Tool | Method | Purpose |
|---|---|---|
| `onetrust_get_preferences_using_get` | GET | Get Data Subject's Preferences |

### Knowledge Graph Ingest

| Tool | Method | Purpose |
|---|---|---|
| `onetrust_ingest_cookies` | POST | Mirror scanned cookies into the knowledge graph as Cookie and CookieDomain nodes |

### Mobile App Consent

| Tool | Method | Purpose |
|---|---|---|
| `onetrust_applicationdata` | GET | Get SDK Configuration |
