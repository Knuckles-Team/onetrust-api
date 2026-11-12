# OneTrust Data-Subject Requests and Incidents

Handle privacy requests and incidents on OneTrust: search and read data-subject requests, verify the requester, run sub-tasks and discovery updates, move requests through stages with resolutions, issue deletion certificates, and log, search, stage and link privacy incidents to inventory. Use when the agent must work a request to closure or record and progress a breach or incident. Do NOT use for consent receipts (onetrust-consent-preferences) or assessments (onetrust-privacy-assessments).

# OneTrust Data-Subject Requests and Incidents

A data-subject request moves through verification, data discovery by sub-task, a decision and a closing resolution inside a legal deadline. A privacy incident follows a staged workflow and is linked to the inventory records it affects.

## When to use
- Search requests and read one with its history, sub-tasks and verification methods.
- Create, update, complete and reprocess sub-tasks; add comments and attachments.
- Pause or resume a deadline, link requests, and move a request to its next stage.
- Manage resolutions and fetch deletion certificates.
- Create, update, search and stage incidents and link them to inventory.

## When NOT to use
- Consent records: use onetrust-consent-preferences.
- Compliance issues and audits: use onetrust-risk-compliance.

## Workflow
1. Search for the request and read it; confirm the requester is verified before touching personal data.
2. Work sub-tasks to completion, adding discovery results.
3. Move the stage only with a resolution that matches the outcome.
4. For an incident, create it, link the affected inventory, then advance its stage.

## Safety
- Bulk delete of requests and stage moves that close a request are final; ask first.
- Do not share results summaries with anyone but the verified requester.

## Tools (46)

Each tool is one API operation; pass its path, query and body fields as named arguments.


### Dsar

| Tool | Method | Purpose |
|---|---|---|
| `onetrust_get_all_group_and_attachment_details_using_get` | GET | Get Targeted Data Discovery Group |
| `onetrust_get_all_group_by_request_using_get` | GET | Get List of Targeted Data Discovery Groups |
| `onetrust_get_all_request_queues_v2_using_get` | GET | Get List of Requests |
| `onetrust_get_all_sub_task_by_ref_id_using_get` | GET | Get List of Subtasks by Request |
| `onetrust_get_all_subtasks_v3_using_post` | POST | Get List of Subtasks by Criteria |
| `onetrust_get_all_v2_resolutions_using_get` | GET | Get List of Resolutions |
| `onetrust_get_all_v2_verification_methods_by_id_using_get` | GET | Get Verification Method |
| `onetrust_get_all_v2_verification_methods_using_get` | GET | Get List of Verification Methods |
| `onetrust_get_deletion_certificate_using_get` | GET | Get Deletion Certificate |
| `onetrust_get_request_by_id_using_get` | GET | Get Request |
| `onetrust_get_request_creation_logs_using_get` | GET | Get Request Creation Logs |
| `onetrust_get_request_history` | GET | Get Request Audit History |
| `onetrust_get_request_history_by_id_using_get` | GET | Get Request Audit History |
| `onetrust_get_subtask_by_idusing_get` | GET | Get Subtask |
| `onetrust_search_for_request_using_post` | POST | Search Requests |
| `onetrust_subtasks_using_get` | GET | Get List of Subtasks |
| `onetrust_add_new_resolution_using_post` | POST | Create Resolution |
| `onetrust_create_request_queue_from_message_using_post` | POST | Create Request |
| `onetrust_create_request_queue_v2_using_post` | POST | Create Request |
| `onetrust_create_sub_task_from_template_using_post` | POST | Add Subtask to Request using Subtask Template |
| `onetrust_create_sub_task_using_post` | POST | Add Subtask to Request |
| `onetrust_create_v2_verification_method_using_post` | POST | Create Verification Method |
| `onetrust_data_discovery_updates_using_post` | POST | Add Targeted Data Discovery Results Summary to Request |
| `onetrust_share_results_summary_using_post` | POST | Share Results Summary |
| `onetrust_unstructured_data_discovery_updates_using_post` | POST | Add Data Points to Targeted Data Discovery Results Summary |
| `onetrust_add_comments_using_put` | PUT | Add Comment to Request |
| `onetrust_add_data_discovery_using_put` | PUT | Add Targeted Data Discovery Details to Subtask |
| `onetrust_bulk_delete_using_put` | PUT | Delete Requests |
| `onetrust_complete_sub_task_using_put` | PUT | Complete Subtask |
| `onetrust_link_requests_using_put` | PUT | Link Requests |
| `onetrust_move_status_by_request_ref_id_using_put` | PUT | Update Request Stage |
| `onetrust_pause_or_resume_deadline_using_put` | PUT | Pause Request Deadline |
| `onetrust_reprocess_subtask_using_put` | PUT | Reprocess System Subtask |
| `onetrust_update_custom_fields_using_put` | PUT | Update Request Custom Fields |
| `onetrust_update_resolution_using_put` | PUT | Update Resolution |
| `onetrust_update_sub_task_using_put` | PUT | Update Subtask |
| `onetrust_update_subtask_status_using_put` | PUT | Update Subtask Status |
| `onetrust_update_v2_verification_method_using_put` | PUT | Update Verification Method |
| `onetrust_delete_resolution_using_delete` | DELETE | Delete Resolution |

### Incidents

| Tool | Method | Purpose |
|---|---|---|
| `onetrust_get_incident_detail_by_incident_id_using_get` | GET | Get Incident |
| `onetrust_search_incidents_using_post` | POST | Search Incidents |
| `onetrust_assign_stage_by_name_1` | POST | Update Incident Stage by Type |
| `onetrust_assign_stage_by_name_x` | POST | Update Incident Stage |
| `onetrust_create_incident_using_post` | POST | Create Incident |
| `onetrust_create_inventory_links` | POST | Link Incident to Inventory |
| `onetrust_update_incident_using_put` | PUT | Update Incident |
