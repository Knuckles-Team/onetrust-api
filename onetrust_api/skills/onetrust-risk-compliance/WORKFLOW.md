# OneTrust Risk and Compliance

Risk, vendor and compliance operations on OneTrust: IT risks, controls and treatments, third-party contracts and engagements, audits, workpapers and scopes, issues and their links, and compliance-automation frameworks. Use when the agent must register or review a risk, assess a vendor engagement, run an audit step, or raise and track an issue. Do NOT use for privacy assessments (onetrust-privacy-assessments) or data-subject requests (onetrust-dsar-incident-response).

# OneTrust Risk and Compliance

Risk and compliance records tie controls, vendors, audits and issues together. Risks carry controls and treatments, vendor engagements carry contracts and status, audits carry scopes and workpapers, and issues link to any of them.

## When to use
- Create, read, update and delete risks, their controls, treatments and relationships.
- Create and update vendor contracts and engagements and change engagement status.
- Read audit scopes and workpapers and edit workpaper details.
- Create issues, link them to related records and update them.
- Read compliance-automation frameworks.

## When NOT to use
- Privacy questionnaires: use onetrust-privacy-assessments.
- Policies and notices: use onetrust-governance-content.

## Workflow
1. Read the schema or attributes first so field names are exact.
2. Find the record by filter or id and read it before changing it.
3. Apply the change, then link it to the related risk, vendor or issue.
4. Read the record back and report its status.

## Safety
- Removing a vendor contract or engagement, deleting a risk or audit scope is not recoverable; ask first.

## Tools (94)

Each tool is one API operation; pass its path, query and body fields as named arguments.


### Audit Management

| Tool | Method | Purpose |
|---|---|---|
| `onetrust_get_audit_detail_using_get` | GET | Get Audit |
| `onetrust_get_audit_list_page_using_post` | POST | Get List of Audits |
| `onetrust_get_audit_workpaper_list_view_using_post` | POST | Get List of Workpapers |
| `onetrust_get_workpaper_basic_detail_information_using_get` | GET | Get Workpaper Control Details |
| `onetrust_get_workpaper_result_using_get` | GET | Get Workpaper Results |
| `onetrust_validate_and_create_audit_using_post` | POST | Create Audit |
| `onetrust_edit_workpaper_details_using_post` | PUT | Update Workpaper |
| `onetrust_validate_and_reassign_scopes_using_put` | PUT | Update Audit Scope |
| `onetrust_validate_and_update_audit_using_put` | PUT | Update Audit |
| `onetrust_delete_audit_using_delete` | DELETE | Delete Audit |
| `onetrust_delete_scope_using_delete` | DELETE | Delete Audit Scope |

### Compliance Automation

| Tool | Method | Purpose |
|---|---|---|
| `onetrust_find_all_initiatives_by_filter_using_post` | POST | Get List of Initiatives |
| `onetrust_get_initiative_using_get` | GET | Get Initiative |
| `onetrust_update_initiative_using_put` | PUT | Update Initiative |

### Issues Management

| Tool | Method | Purpose |
|---|---|---|
| `onetrust_find_all_issues_by_filter_using_post` | POST | Get List of Issues |
| `onetrust_get_attributes_by_schema_name_using_get` | GET | Get Attribute Schema |
| `onetrust_get_issue_links_using_get` | GET | Get Issue Relationships |
| `onetrust_get_issue_related_tasks_using_get` | GET | Get Issue Tasks |
| `onetrust_get_issue_using_get` | GET | Get Issue |
| `onetrust_create_issue_relationship_links_using_post` | POST | Create Issue Relationship |
| `onetrust_create_issue_using_post` | POST | Create Issue |
| `onetrust_update_issue_using_patch` | PATCH | Modify Issue |
| `onetrust_update_issue_using_put` | PUT | Update Issue |

### It Risk Management

| Tool | Method | Purpose |
|---|---|---|
| `onetrust_find_all_control_implementations_attributes_and_options_by_using_post` | POST | Search Control Implementation Attributes |
| `onetrust_find_all_control_implementations_using_post` | POST | Get List of Control Implementations |
| `onetrust_find_all_evidences_by_search_criteria_1` | POST | Get List of Evidence Task Implementations |
| `onetrust_find_associated_control_implementations_using_post` | POST | Get List of Control Implementations by Entity |
| `onetrust_find_controls_by_criteria_using_post_1` | POST | Get List of Controls |
| `onetrust_find_evidence_implementations_by_id_1` | GET | Get Evidence Task Implementation |
| `onetrust_find_threats_by_criteria_using_post` | POST | Get List of Threats |
| `onetrust_find_vulnerabilities_by_criteria_using_post` | POST | Get List of Vulnerabilities |
| `onetrust_get_active_categories_using_get` | GET | Get List of Risk Categories |
| `onetrust_get_all_enabled_control_entity_types_using_get` | GET | Get List of Control Entity Source Types |
| `onetrust_get_all_enabled_risk_entity_types_using_get` | GET | Get List of Risk Entity Types |
| `onetrust_get_all_enabled_source_entity_types_using_get` | GET | Get List of Risk Entity Source Types |
| `onetrust_get_all_related_control_entity_types_using_get` | GET | Get Related Control Entity Types |
| `onetrust_get_control_implementation_details_using_get` | GET | Get Control Implementation |
| `onetrust_get_linked_risks_information_using_post` | POST | Get List of Linked Risks |
| `onetrust_get_matrix_score_setting_using_get` | GET | Get Risk Matrix Configuration |
| `onetrust_get_risk_page_view_using_post` | POST | Get List of Risks |
| `onetrust_get_risk_template_using_get` | GET | Get Risk Template |
| `onetrust_get_risk_using_get` | GET | Get Risk |
| `onetrust_get_standard_score_setting_using_get` | GET | Get Standard Risk Configuration |
| `onetrust_add_attachments_to_implementation_using_post` | POST | Attach Files to Control Implementation |
| `onetrust_add_control_using_post` | POST | Create Control |
| `onetrust_add_controls_to_risk_using_post` | POST | Add Controls to Risk |
| `onetrust_add_evidence_implementation_attachment` | POST | Add Attachments to Evidence Task Implementation |
| `onetrust_add_threat_to_risk` | POST | Add Threat to Risk |
| `onetrust_add_threat_using_post_1` | POST | Create Threat |
| `onetrust_add_threats_using_post` | POST | Create Multiple Threats |
| `onetrust_add_vulnerabilities_to_risk` | POST | Add Vulnerabilities to Risk |
| `onetrust_add_vulnerabilities_using_post` | POST | Create Multiple Vulnerabilities |
| `onetrust_add_vulnerability_using_post_1` | POST | Create Vulnerability |
| `onetrust_bulk_create_links_using_post` | POST | Link Controls |
| `onetrust_change_risk_stage_using_post` | POST | Update Risk Stage |
| `onetrust_create_risk_using_post` | POST | Create Risk |
| `onetrust_create_stand_alone_risk_using_post` | POST | Create Risk |
| `onetrust_unlink_risks_from_entity_using_post` | POST | Unlink Risks |
| `onetrust_approve_risk_using_put` | PUT | Approve Risk |
| `onetrust_create_update_risk_using_put` | PUT | Create or Update Risk |
| `onetrust_grant_risk_exception_using_put` | PUT | Grant Risk Exception |
| `onetrust_reopen_risk_using_put` | PUT | Reopen Risk |
| `onetrust_request_risk_exception_using_put` | PUT | Request Risk Exception |
| `onetrust_send_back_risk_using_put` | PUT | Send Back Risk |
| `onetrust_submit_risk_using_put` | PUT | Submit Risk |
| `onetrust_update_control_implementation_by_implementation_id_using_put` | PUT | Update Control Implementation |
| `onetrust_update_control_using_put_1` | PUT | Update Control |
| `onetrust_update_risk_approvers_using_put` | PUT | Update Risk Approvers |
| `onetrust_update_risk_categories_using_put` | PUT | Update Risk Categories |
| `onetrust_update_risk_owners_using_put` | PUT | Update Risk Owners |
| `onetrust_update_risk_using_patch` | PATCH | Modify Risk |
| `onetrust_update_risk_using_put` | PUT | Update Risk |
| `onetrust_update_threats_using_put` | PUT | Update Threats |
| `onetrust_update_vulnerabilities_using_put` | PUT | Update Vulnerabilities |
| `onetrust_delete_risk_using_delete` | DELETE | Delete Risk |
| `onetrust_remove_control_implementation_by_entity_and_implementation_id_using_delete` | DELETE | Delete Control Implementation |
| `onetrust_remove_control_using_delete_1` | DELETE | Delete Control |
| `onetrust_remove_threat_using_delete` | DELETE | Delete Threat |
| `onetrust_remove_vulnerability_using_delete` | DELETE | Delete Vulnerability |

### Tprm

| Tool | Method | Purpose |
|---|---|---|
| `onetrust_fetch_all_contract_types_using_get` | GET | Get List of Contract Types |
| `onetrust_get_contract_schema_using_get` | GET | Get Contract Schema |
| `onetrust_get_engagement_schema_using_get` | GET | Get Engagement Schema |
| `onetrust_load_engagement_by_engagement_id_using_get` | GET | Get Engagement |
| `onetrust_load_engagement_using_get` | POST | Search Engagements |
| `onetrust_load_vendor_contract_by_contract_id_using_get` | GET | Get Contract |
| `onetrust_search_contract_by_vendor_and_criteria_using_post` | POST | Search Contracts |
| `onetrust_create_engagement_using_post` | POST | Create Engagement |
| `onetrust_create_vendor_contract_using_post` | POST | Create Contract |
| `onetrust_update_engagement_status` | PUT | Update Engagement Status |
| `onetrust_update_engagement_using_patch` | PATCH | Modify Engagement |
| `onetrust_update_engagement_using_put` | PUT | Update Engagement |
| `onetrust_update_vendor_contract_using_put` | PUT | Update Contract |
| `onetrust_remove_engagement_using_delete` | DELETE | Delete Engagement |
| `onetrust_remove_vendor_contract_using_delete` | DELETE | Delete Contract |
