# OneTrust Data Mapping

Maintain the OneTrust data map: inventories of assets, vendors, legal entities and processing activities, their relations and hierarchy, the data categories, elements and subjects, the glossary and data catalog, and data-discovery scans with their workers. Use when the agent must enumerate or edit inventory records, link them, classify personal data, or run a discovery scan. Do NOT use for assessments over those records (onetrust-privacy-assessments) or cookie scans (onetrust-cookie-consent).

# OneTrust Data Mapping

The data map answers where personal data lives and how it flows. Inventory records are typed by schema (asset, vendor, legal entity, processing activity), related to each other, and classified by data category, element and subject. Data-discovery scans find personal data in connected systems and feed the same map.

## When to use
- List, filter, read, create, update, copy or delete inventory records of any schema.
- Create and read relations, hierarchies and parent links between records.
- Manage data categories, classifications, elements and subjects.
- Search the glossary, tags, terms and data-asset catalog.
- Register discovery data sources, credentials, scan profiles, detectors and jobs; mirror inventories into the graph.

## When NOT to use
- Questionnaires and approvals over a record: use onetrust-privacy-assessments.
- Cookie inventory: use onetrust-cookie-consent.
- Whole-tenant export: use onetrust-platform-administration.

## Workflow
1. Read the schemas first so the schema name and field names are exact.
2. List or filter records, then read one record by id or external id before changing it.
3. Change a record, then read its relations to confirm links still hold.
4. For discovery, create or read the source, start a job, and poll the job until it finishes.

## Safety
- Deleting an inventory record, category, element or subject removes it from every linked assessment view; ask first.
- Discovery credentials hold secrets by reference only; never echo them.

## Tools (113)

Each tool is one API operation; pass its path, query and body fields as named arguments.


### Data Catalog

| Tool | Method | Purpose |
|---|---|---|
| `onetrust_get_all_data_asset_attribute_names` | GET | Get List of Data Asset Attributes |
| `onetrust_get_all_glossaries_by_names` | GET | Get Glossary |
| `onetrust_get_all_glossaries_names` | GET | Get List of Glossaries |
| `onetrust_get_all_term_attribute_names` | GET | Get List of Term Attributes |
| `onetrust_get_data_asset_attribute_by_name` | GET | Get Data Asset Attribute |
| `onetrust_get_data_asset_v1` | GET | Get Data Asset |
| `onetrust_get_tag_details_with_associated_terms` | GET | Get Tag |
| `onetrust_get_term_attribute_by_name` | GET | Get Term Attribute |
| `onetrust_get_v1_field_details` | GET | Get Search Fields |
| `onetrust_retrieve_all_tags_name` | GET | Get List of Tags |
| `onetrust_retrieve_all_terms` | GET | Get List of Terms |
| `onetrust_retrieve_terms_by_name` | GET | Get Term |
| `onetrust_retrieve_terms_name` | GET | Get List of Term Names |
| `onetrust_create_data_asset_tag_associations_v1` | POST | Create Tag Associations |
| `onetrust_create_data_asset_term_associations_v1` | POST | Create Term Associations |
| `onetrust_create_or_upsert_data_asset_v1` | POST | Create Data Asset |
| `onetrust_create_tag_v2` | POST | Create Tag |
| `onetrust_create_term_using_post` | POST | Create Term |
| `onetrust_delete_data_asset_tag_associations_v1` | POST | Delete Multiple Data Asset Tag Associations |
| `onetrust_delete_data_asset_term_associations_v1` | POST | Delete Multiple Data Asset Term Associations |
| `onetrust_external_search` | POST | Get Catalog Search Results |
| `onetrust_external_search_using_continuationtoken` | POST | Get Catalog Search Results |
| `onetrust_update_data_asset_v1` | PATCH | Modify Data Asset |
| `onetrust_delete_data_asset_v1` | DELETE | Delete Data Asset |

### Data Discovery

| Tool | Method | Purpose |
|---|---|---|
| `onetrust_get_all_using_get_1` | GET | Get List of Data Sources |
| `onetrust_get_all_using_get_2` | GET | Get List of Scan Profiles |
| `onetrust_get_credential_by_id` | GET | Get Credential |
| `onetrust_get_credentials` | GET | Get List of Credentials |
| `onetrust_get_data_source_by_id_using_get_1` | GET | Get Data Source |
| `onetrust_get_detector_by_classifier_name` | GET | Get Custom Classifier |
| `onetrust_get_docker_repository_tags_using_get` | GET | Get List of Image tags |
| `onetrust_get_job_by_id_using_get` | GET | Get Scan Job |
| `onetrust_get_job_using_get_1` | GET | Get Scan Job |
| `onetrust_get_scan_jobs_by_data_source_using_get_1` | GET | Get List of Scan Jobs |
| `onetrust_get_scan_profile_using_get_1` | GET | Get Scan Profile |
| `onetrust_list_detectors` | GET | Get List of Custom Classifiers |
| `onetrust_create_credential` | POST | Create Credential |
| `onetrust_create_detector` | POST | Create Custom Classifier |
| `onetrust_create_job_using_post_x` | POST | Create Scan Job |
| `onetrust_create_v2_using_post` | POST | Create Scan Profile |
| `onetrust_cancel_job_using_patch` | PATCH | Cancel Scan Job |
| `onetrust_cancel_scan_job` | PATCH | Cancel Scan Job |
| `onetrust_update_credential` | PUT | Update Credential |
| `onetrust_update_detector` | PUT | Update Custom Classifier |
| `onetrust_update_v2_using_put` | PUT | Update Scan Profile |
| `onetrust_upsert_source_system_v3_using_put` | PUT | Create or Update Data Source |
| `onetrust_delete_credential` | DELETE | Delete Credential |
| `onetrust_delete_detector` | DELETE | Delete Custom Classifier |
| `onetrust_delete_scan_profile_using_delete_1` | DELETE | Delete Scan Profile |
| `onetrust_delete_system_using_delete_1` | DELETE | Delete Data Source |

### Data Discovery Worker

| Tool | Method | Purpose |
|---|---|---|
| `onetrust_get_eligible_jobs_using_get` | GET | Get List of Scan Jobs |
| `onetrust_catalog_data_using_post` | POST | Submit Data to Catalog |
| `onetrust_classify_data_using_post` | POST | Submit Data to Classify |
| `onetrust_update_job_status_using_put` | PUT | Update Scan Job Status |

### Data Mapping

| Tool | Method | Purpose |
|---|---|---|
| `onetrust_get_all_schemas_using_get` | GET | Get List of Inventory Schemas |
| `onetrust_get_data_categories_by_partial_name_using_get` | GET | Get List of Data Categories |
| `onetrust_get_data_category_using_get` | GET | Get Data Category |
| `onetrust_get_data_classification_using_get` | GET | Get Data Classification |
| `onetrust_get_data_element_using_get` | GET | Get Data Element |
| `onetrust_get_data_subject_using_get` | GET | Get Data Subject |
| `onetrust_get_data_subjects_by_partial_name_using_get` | GET | Get List of Data Subjects |
| `onetrust_get_hierarchy_for_inventory_id_using_get` | GET | Get List of Child Inventories by Root Inventory |
| `onetrust_get_inventory_by_external_id_using_get` | GET | Get Inventory by External ID |
| `onetrust_get_inventory_by_id_using_get` | GET | Get Inventory by ID |
| `onetrust_get_inventory_relations_by_id_using_get` | GET | Get Inventory Links |
| `onetrust_get_list_of_inventories_by_filter_criteria_using_post` | POST | Get List of Inventories by Criteria |
| `onetrust_get_list_of_inventories_using_get` | GET | Get List of Inventories |
| `onetrust_get_schema_details_using_field_name` | GET | Get Inventory Schema Details |
| `onetrust_add_controls_to_inventory_using_post` | POST | Create Control Implementation |
| `onetrust_copy_inventory_using_post` | POST | Copy Inventory |
| `onetrust_create_data_category_using_post` | POST | Create Data Category |
| `onetrust_create_data_classification_using_post` | POST | Create Data Classification |
| `onetrust_create_data_element_using_post` | POST | Create Data Element |
| `onetrust_create_data_subject_using_post` | POST | Create Data Subject |
| `onetrust_create_inventory_using_post` | POST | Create Inventory |
| `onetrust_create_relations_using_post` | POST | Link Inventory |
| `onetrust_link_asset_inventory_to_parent_asset_id_using_post` | POST | Add Asset Inventory as Child to Parent Inventory |
| `onetrust_link_legal_entity_inventory_to_parent_legal_entity_id_using_post` | POST | Add Legal Entity Inventory as Child to Parent Inventory |
| `onetrust_link_processing_activity_inventory_to_parent_processing_activity_id_using_post` | POST | Add Processing Activity Inventory as Child to Parent Inventory |
| `onetrust_link_vendor_inventory_to_parent_vendor_id_using_post` | POST | Add Vendor Inventory as Child to Parent Inventory |
| `onetrust_set_inventory_as_parent_inventory_using_put` | PUT | Set Inventory as Parent |
| `onetrust_unset_inventory_as_parent_inventory_using_put` | PUT | Unset Inventory as Parent |
| `onetrust_update_advanced_attributes_for_personal_data_association_using_put` | PUT | Update Advanced Attributes for Personal Data Association |
| `onetrust_update_inventory_association_using_put` | PUT | Update Inventory Link |
| `onetrust_update_inventory_status_by_id_using_put` | PUT | Update Inventory Status |
| `onetrust_update_inventory_using_put` | PUT | Update Inventory by ID |
| `onetrust_update_relations_using_put` | PUT | Link Inventory |
| `onetrust_upsert_inventory_using_put` | PUT | Update Inventory by External ID |
| `onetrust_delete_data_category_using_delete` | DELETE | Delete Data Category |
| `onetrust_delete_data_classification_using_delete` | DELETE | Delete Data Classification |
| `onetrust_delete_data_element_using_delete` | DELETE | Delete Data Element |
| `onetrust_delete_data_subject_using_delete` | DELETE | Delete Data Subject |
| `onetrust_delete_inventory_using_delete` | DELETE | Delete Inventory |
| `onetrust_delete_relations_using_delete` | DELETE | Delete Inventory Link |
| `onetrust_unlink_child_inventory_from_hierarchy_using_delete` | DELETE | Remove Child Inventory from Root Inventory |

### Data Mapping Legacy

| Tool | Method | Purpose |
|---|---|---|
| `onetrust_get_inventory_v2_schemas_attributes_attribute_id_values_value_id` | GET | Get Attribute Options |
| `onetrust_get_schema_using_get_1` | GET | Get Inventory Schema |
| `onetrust_list_all_data_classifications_using_get` | GET | Get List of Data Classifications |
| `onetrust_list_all_data_elements_using_get` | GET | Get List of Data Elements |

### Inventory

| Tool | Method | Purpose |
|---|---|---|
| `onetrust_get_inventory_relationship_using_relationship_type_name` | GET | Get Relationship by Type ID |
| `onetrust_get_inventory_relationship_using_relationship_type_name_1` | GET | Get Relationship by Type Name |
| `onetrust_get_personal_data_for_relationships_using_post` | POST | Get Personal Data for Relationship by Type ID |
| `onetrust_get_personal_data_for_relationships_using_post_1` | POST | Get Personal Data for Relationship by Type Name |
| `onetrust_list_all_inventory_relationships_using_post` | POST | Get List of Relationships |
| `onetrust_add_relationship_between_entities_using_post` | POST | Create Relationship |
| `onetrust_create_inventory_relations_using_post` | POST | Create Relationship |
| `onetrust_link_or_unlink_inventory_relationships_using_relationship_using_put` | PUT | Link or Unlink Personal Data to Relationship by Type ID |
| `onetrust_link_or_unlink_inventory_relationships_using_relationship_using_put_1` | PUT | Link or Unlink Personal Data to Relationship by Type Name |
| `onetrust_update_inventory_relations_using_entity_type_name` | PUT | Update Relationship by Type ID |
| `onetrust_update_inventory_relations_using_entity_type_name_1` | PUT | Update Relationship by Type Name |
| `onetrust_delete_inventory_relations_using_relationship_type_name` | DELETE | Delete Relationship by Type ID |
| `onetrust_delete_inventory_relations_using_relationship_type_name_1` | DELETE | Delete Relationship by Type Name |

### Knowledge Graph Ingest

| Tool | Method | Purpose |
|---|---|---|
| `onetrust_ingest_inventories` | POST | Mirror data-inventory records into the knowledge graph as Inventory and DataElement nodes |
