# OneTrust Governance Content

Governance content on OneTrust: policies and their versions, privacy notices, awareness-training courses and enrollments, ESG disclosures and emission factors, documents and attachments, tasks, and custom objects with their types, links and models. Use when the agent must publish or version a policy, read a notice, track training, read ESG data, fetch a document, or work with custom objects. Do NOT use for assessments (onetrust-privacy-assessments) or users and access (onetrust-platform-administration).

# OneTrust Governance Content

Governance content is the written side of the programme: the policies staff must follow, the notices shown to the public, the training that proves awareness, and the custom objects an organisation adds for its own records.

## When to use
- Create policies and versions, attach documents, read published versions.
- Read privacy notices and their versions.
- List courses and read enrollment progress.
- Read ESG emission factors and disclosures.
- Download attachments, manage tasks, and create or query custom objects, types and links.

## When NOT to use
- Questionnaire workflows: use onetrust-privacy-assessments.
- User and group administration: use onetrust-platform-administration.

## Workflow
1. Find the policy, notice, course or object by listing, then read the one you need.
2. Create a new version rather than editing a published one.
3. Read the item back and report its version and status.

## Safety
- Publishing a policy version or deleting a custom object type changes what staff and the public see; ask first.

## Tools (62)

Each tool is one API operation; pass its path, query and body fields as named arguments.


### Documents

| Tool | Method | Purpose |
|---|---|---|
| `onetrust_file_location` | GET | Get File Location |
| `onetrust_file_upload` | POST | Upload File |

### Esg

| Tool | Method | Purpose |
|---|---|---|
| `onetrust_fetch_metrics_details` | POST | Get Metric Details |
| `onetrust_find_all_by_type_and_criteria` | POST | Get List of Emission Details |
| `onetrust_get_all_emission_factors_basic_entity_details` | GET | Get List of Emission Factors |
| `onetrust_add_emission_factor` | POST | Create Emission Factor |
| `onetrust_add_emission_transaction` | POST | Create Emission Transaction |

### Object Manager

| Tool | Method | Purpose |
|---|---|---|
| `onetrust_find_all_by_link_type_and_criteria_using_post` | POST | Get List of Relationship Link Types |
| `onetrust_find_all_by_type_and_criteria_using_post` | POST | Get List of Object Types |
| `onetrust_find_all_by_type_id_and_criteria_using_post_x` | POST | Get Full Object Details |
| `onetrust_find_entity_basic_details_by_type_and_criteria_using_post_x` | POST | Get Basic Object Details |
| `onetrust_find_model_basic_details_by_query_criteria_using_post` | POST | Get Basic Model Object Details |
| `onetrust_find_models_by_list_criteria_using_post` | POST | Get Model Object Details |
| `onetrust_find_project_basic_details_by_query_criteria_using_post` | POST | Get Basic Project Object Details |
| `onetrust_find_projects_by_list_criteria_using_post` | POST | Get Project Object Details |
| `onetrust_find_task_using_get_1_x` | GET | Get Task |
| `onetrust_get_entity_information_using_entity_type_id_or_entity_type_name_using_get_x` | GET | Get Object |
| `onetrust_get_entity_type_information_using_get` | GET | Get Object Type by ID |
| `onetrust_get_entity_type_information_using_get_1_x` | GET | Get Object Type by Name |
| `onetrust_get_link_record_information_using_link_type_id_using_get_x` | GET | Get Relationship Record |
| `onetrust_get_link_type_using_get` | GET | Get Relationship Type |
| `onetrust_get_model_using_get` | GET | Get Model Object |
| `onetrust_get_project_using_get` | GET | Get Project Object |
| `onetrust_add_attribute_using_post_x` | POST | Add Attribute to Schema |
| `onetrust_add_entity_using_entity_type_id_or_entity_type_name_using_post_x` | POST | Create Object |
| `onetrust_add_options_using_post_x` | POST | Add Options to Attribute |
| `onetrust_create_custom_link_type_using_post` | POST | Create Relationship Type between Objects |
| `onetrust_create_link_record_between_entities_using_link_type_id_using_post_x` | POST | Create Relationship Record between Objects |
| `onetrust_create_model_using_post` | POST | Create Model Object |
| `onetrust_create_project_using_post` | POST | Create Project Object |
| `onetrust_create_task_using_post_1_x` | POST | Create Task |
| `onetrust_disable_attribute_using_put_x` | PUT | Disable Attribute |
| `onetrust_enable_attribute_using_put_x` | PUT | Enable Attribute |
| `onetrust_enabled_custom_entity_type_using_put` | PUT | Enable Custom Object Type by ID |
| `onetrust_enabled_custom_entity_type_using_put_1` | PUT | Enable Custom Object Type by Name |
| `onetrust_update_custom_entity_type_using_patch` | PATCH | Modify Custom Object Type by ID |
| `onetrust_update_custom_entity_type_using_patch_1` | PATCH | Modify Custom Object Type by Name |
| `onetrust_update_model_using_put` | PUT | Modify Model Object |
| `onetrust_update_project_using_put` | PUT | Modify Project Object |
| `onetrust_update_task_using_put_1_x` | PUT | Update Task |
| `onetrust_update_using_entity_type_id_or_entity_type_name_using_patch_x` | PATCH | Modify Object |
| `onetrust_delete_link_record_by_id_and_type_using_link_type_id_using_delete_x` | DELETE | Remove Relationship Record |
| `onetrust_delete_model_using_delete` | DELETE | Delete Model Object |
| `onetrust_delete_project_using_delete` | DELETE | Delete Project Object |
| `onetrust_delete_using_entity_type_id_or_entity_type_name_using_delete_x` | DELETE | Delete Object |

### Policy Management

| Tool | Method | Purpose |
|---|---|---|
| `onetrust_get_latest_policies` | GET | Get List of Documents |
| `onetrust_get_policy` | GET | Get Document |
| `onetrust_get_published_policy_version` | GET | Get Document Version |
| `onetrust_add_document_to_policy` | POST | Add Document Attachments |
| `onetrust_create_policy` | POST | Create Document |
| `onetrust_create_policy_versions` | POST | Create Document Version |

### Privacy Notices

| Tool | Method | Purpose |
|---|---|---|
| `onetrust_get_privacy_notice_version_by_published_date_using_get` | GET | Get Privacy Notice Version |
| `onetrust_get_privacy_notice_versions_using_get` | GET | Get List of Privacy Notice Versions |
| `onetrust_get_privacy_notices_using_get` | GET | Get List of Privacy Notices |

### Task Management

| Tool | Method | Purpose |
|---|---|---|
| `onetrust_get_task_by_id_and_task_type_name_key_using_get` | GET | Get Task |
| `onetrust_create_task_using_post` | POST | Create Task |
| `onetrust_update_task_using_put` | PUT | Update Task |

### Training

| Tool | Method | Purpose |
|---|---|---|
| `onetrust_get_enrollment_details_using_post` | POST | Get Enrollment Details |
| `onetrust_get_status_of_enrollment_using_get` | GET | Get User's Enrollment Status |
| `onetrust_list_of_courses_using_get` | GET | Get List of Courses |
| `onetrust_enroll_users_to_course_using_post` | POST | Enroll Users to Course |
| `onetrust_un_enroll_user_using_delete` | DELETE | Unenroll User from Course |
