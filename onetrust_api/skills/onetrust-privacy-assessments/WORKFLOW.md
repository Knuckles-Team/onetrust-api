# OneTrust Privacy Assessments

Run privacy, risk and AI-governance assessments on OneTrust: list and read assessments, launch from a template, assign respondents, submit, review, approve, reopen and reassess, and manage templates and AI-governance records. Use when the agent must triage in-flight assessments, start a PIA/DPIA, record responses, or close one with a result. Do NOT use for cookie scans (onetrust-cookie-consent), the data inventory (onetrust-data-mapping) or vendor risk (onetrust-risk-compliance).

# OneTrust Privacy Assessments

Assessments are the core evidence record of a privacy programme. Each assessment is launched from a template, answered by respondents, reviewed, and approved with a result. The AI-governance tools keep the register of AI systems and their risk evaluations next to those assessments.

## When to use
- Triage assessments by status, deadline or archival state.
- Launch an assessment from a template and set its respondents, approvers and primary record.
- Submit responses, review, approve, reopen, send back or reassess an assessment.
- Import, export or delete assessment template versions.
- Read and update AI-governance records.

## When NOT to use
- Cookie or tracker scans: use onetrust-cookie-consent.
- Inventory records and their relations: use onetrust-data-mapping.
- Contracts, engagements and vendor risk: use onetrust-risk-compliance.

## Workflow
1. Resolve the template or assessment: list with the status filters, then read the one you need before changing it.
2. Create from a template with name, organisation and approver; read it back to confirm the workflow stage.
3. Move it through submit, review and approve in order; each step is a separate tool and none is skipped.
4. After a change, read the assessment again and report its stage and result.

## Safety
- Approve, delete, archive and template-version deletion change the record of compliance; ask the person first.
- Never approve with force override unless the person named the override in the request.

## Tools (53)

Each tool is one API operation; pass its path, query and body fields as named arguments.


### Ai Governance

| Tool | Method | Purpose |
|---|---|---|
| `onetrust_find_all_by_type_and_criteria_using_post_1` | POST | Get List of Entity Types |
| `onetrust_find_all_by_type_id_and_criteria_using_post` | POST | Get Full Entity Details |
| `onetrust_find_entity_basic_details_by_type_and_criteria_using_post` | POST | Get Basic Entity Details |
| `onetrust_find_task_using_get_1` | GET | Get Task |
| `onetrust_get_entity_information_using_entity_type_id_or_entity_type_name_using_get` | GET | Get Entity |
| `onetrust_get_entity_type_information_using_get_1` | GET | Get Entity Type |
| `onetrust_get_link_record_information_using_link_type_id_using_get` | GET | Get Relationship Record |
| `onetrust_get_related_entities_for_an_entity_using_post` | POST | Get List of Relationship Records by Entity |
| `onetrust_add_attribute_using_post` | POST | Add Attribute to Schema |
| `onetrust_add_entity_using_entity_type_id_or_entity_type_name_using_post` | POST | Create Entity |
| `onetrust_add_options_using_post` | POST | Add Options to Attribute |
| `onetrust_assign_stage_by_name` | POST | Update Entity Workflow Stage |
| `onetrust_create_link_record_between_entities_using_link_type_id_using_post` | POST | Create Relationship Record between Entities |
| `onetrust_create_task_using_post_1` | POST | Create Task |
| `onetrust_disable_attribute_using_put` | PUT | Disable Attribute |
| `onetrust_enable_attribute_using_put` | PUT | Enable Attribute |
| `onetrust_update_task_using_put_1` | PUT | Update Task |
| `onetrust_update_using_entity_type_id_or_entity_type_name_using_patch` | PATCH | Modify Entity |
| `onetrust_delete_link_record_by_id_and_type_using_link_type_id_using_delete` | DELETE | Remove Relationship Record |
| `onetrust_delete_using_entity_type_id_or_entity_type_name_using_delete` | DELETE | Delete Entity |

### Assessments

| Tool | Method | Purpose |
|---|---|---|
| `onetrust_export_assessment_using_get` | GET | Get Assessment |
| `onetrust_export_template_with_business_keys_using_get` | GET | Export Template |
| `onetrust_get_all_assessment_basic_details_using_get` | GET | Get List of Assessments |
| `onetrust_get_all_basic_template_details_using_get` | GET | Get List of Templates |
| `onetrust_get_assessment_delete_logs_using_get` | GET | Export Deleted Assessment Audit Log |
| `onetrust_get_assessment_results_using_get` | GET | Get List of Assessment Results |
| `onetrust_get_assessments_using_post` | POST | Get List of Assessments by Criteria |
| `onetrust_get_linked_assessments_information_using_get` | GET | Get List of Linked Assessments |
| `onetrust_get_tags_using_get` | GET | Get List of Assessment Tags |
| `onetrust_get_workflow_details_for_assessment_using_get` | GET | Get Assessment Workflow Stages |
| `onetrust_add_manual_assessment_links_using_post` | POST | Link Assessments |
| `onetrust_approve_assessment_using_post` | POST | Approve Assessment |
| `onetrust_create_assessment_risk_using_post` | POST | Create Assessment Risk |
| `onetrust_create_assessment_using_post` | POST | Launch Assessment |
| `onetrust_create_assessment_using_post_1` | POST | Launch Assessment |
| `onetrust_create_bulk_assessment_using_post` | POST | Launch Assessments in Bulk |
| `onetrust_create_task_using_post_x` | POST | Create Assessment Task |
| `onetrust_import_template_by_id_using_post` | POST | Import Template |
| `onetrust_reassess_assessment_using_post` | POST | Reassess Assessment |
| `onetrust_reopen_assessment_using_post` | POST | Reopen Assessment |
| `onetrust_review_assessment_using_post` | POST | Complete Assessment |
| `onetrust_send_back_assessment_to_in_progress_using_post` | POST | Send Back Assessment |
| `onetrust_submit_assessment_using_post` | POST | Submit Assessment |
| `onetrust_submit_responses_using_post` | POST | Submit Responses |
| `onetrust_add_or_update_tags_using_put` | PUT | Update Assessment Tags |
| `onetrust_archive_assessments_using_put` | PUT | Archive Assessment |
| `onetrust_reassign_assessment_using_put` | PUT | Reassign Assessment |
| `onetrust_soft_delete_assessment_using_put` | PUT | Move Assessment to Recycle Bin |
| `onetrust_unarchive_assessments_using_put` | PUT | Unarchive Assessment |
| `onetrust_update_basic_assessment_details_using_patch` | PATCH | Modify Assessment |
| `onetrust_update_primary_record_using_put` | PUT | Set Primary Record |
| `onetrust_delete_template_versions_using_delete` | DELETE | Delete Template |

### Knowledge Graph Ingest

| Tool | Method | Purpose |
|---|---|---|
| `onetrust_ingest_assessments` | POST | Mirror assessments into the knowledge graph as Assessment nodes with a summary Document |
