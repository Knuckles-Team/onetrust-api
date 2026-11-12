---
name: onetrust-consent-preferences
skill_type: skill
description: >-
  Consent and preference management on OneTrust: collection points, purposes, preference
  centres, data subjects and their profiles, consent receipts and transactions, linked
  identities, custom preferences and merge requests. Use when the agent must record or
  read a consent, look up a data subject's purposes, withdraw consent, or administer
  purposes and preference centres. Do NOT use for cookie banners (onetrust-cookie-consent)
  or privacy requests (onetrust-dsar-incident-response).
license: MIT
tags: [onetrust, consent, preferences, receipts, data-subjects, privacy, mcp]
metadata:
  author: Knuckles-Team
  version: '1.0.0'
---
# OneTrust Consent Preferences

Consent management stores what each data subject agreed to, for which purpose, through which collection point. A receipt is the proof of one consent transaction; a profile is the current standing of one subject.

## When to use
- Create consent receipts, singly or in bulk, and read them back.
- Read data subjects, profiles, purposes and linked identity groups.
- Withdraw consent for a purpose and identifier.
- Administer collection points, purposes, custom preferences and preference centres.
- Manage merge requests for duplicate data subjects.

## When NOT to use
- Website cookie banners: use onetrust-cookie-consent.
- Access, deletion and correction requests: use onetrust-dsar-incident-response.

## Workflow
1. Resolve the data subject by identifier and read the profile before any change.
2. Resolve the purpose and collection point the consent belongs to.
3. Record the receipt or withdrawal, then read the receipt or profile back.
4. Report the receipt id and the resulting standing per purpose.

## Safety
- A withdrawal takes effect for downstream systems at once; confirm the identifier and purpose first.
- Merging data subjects cannot be split again; ask first.

## Tools (100)

Each tool is one API operation; pass its path, query and body fields as named arguments.


### Consent Receipts

| Tool | Method | Purpose |
|---|---|---|
| `onetrust_create_bulk_consent_receipt_using_post` | POST | Create Consent Receipts in Bulk |
| `onetrust_create_consent_receipt_using_post` | POST | Create Consent Receipts |
| `onetrust_create_identified_consent_receipt_using_post` | POST | Create Identified Consent Receipts |

### Universal Consent

| Tool | Method | Purpose |
|---|---|---|
| `onetrust_download_consent_attachments` | GET | Download All Consent Attachments |
| `onetrust_download_given_consent_attachments` | GET | Download Consent Attachment |
| `onetrust_exportduplicatedatasubject` | GET | Generate Export of Duplicate Data Subjects |
| `onetrust_find_by_guid_using_get` | GET | Get Purpose Preference |
| `onetrust_find_receipt_using_get` | GET | Get Receipt |
| `onetrust_get_all_profiles_by_data_subject_v4` | GET | Get List of All Purpose Details by Data Subject |
| `onetrust_get_collection_points_using_get` | GET | Get List of Collection Points |
| `onetrust_get_collection_points_using_get_1` | GET | Get List of Collection Points |
| `onetrust_get_consent_group_list_using_get` | GET | Get List of Consent Groups |
| `onetrust_get_consent_group_settings_using_get` | GET | Get Priority Scores for Purpose Statuses |
| `onetrust_get_consent_group_using_get` | GET | Get Consent Group |
| `onetrust_get_data_subject_basic_details_v4` | GET | Get Data Subject |
| `onetrust_get_data_subject_details_v4` | GET | Get Data Subject Details |
| `onetrust_get_data_subject_groups_list_v4` | GET | Get List of Data Subject Groups |
| `onetrust_get_data_subject_profile_using_get` | GET | Get List of Data Subjects |
| `onetrust_get_data_subject_profile_v4` | GET | Get Purpose Details by Data Subject |
| `onetrust_get_data_subject_profiles_unordered_v4` | GET | Get Optimized List of All Purpose Details for All Data Subjects |
| `onetrust_get_data_subject_profiles_v4` | GET | Get List of All Purpose Details for All Data Subjects |
| `onetrust_get_data_subject_purposes_by_identifier_using_get` | GET | Get List of Purposes for a Data Subject |
| `onetrust_get_data_subject_purposes_by_identifier_using_get_1` | GET | Get Data Subject's Preferences in a Preference Center |
| `onetrust_get_data_subjects_for_purposes_using_get` | GET | Get List of Data Subjects by Purpose |
| `onetrust_get_data_subjects_unordered_v4` | GET | Get Optimized List of Data Subjects |
| `onetrust_get_data_subjects_using_get` | GET | Get List of Data Subjects |
| `onetrust_get_data_subjects_v4` | GET | Get List of Data Subjects |
| `onetrust_get_email_link_token_by_data_subject_v4` | GET | Get Data Subject Token |
| `onetrust_get_email_link_tokens_list_v4` | GET | Get List of Data Subject Tokens |
| `onetrust_get_grouped_purposes_v2` | GET | Get List of Purpose Versions |
| `onetrust_get_index_creation_status` | GET | Get Index Creation Status |
| `onetrust_get_link_tokens_using_get` | GET | Get List of Data Subject Tokens |
| `onetrust_get_linked_identity_group_members_v4` | GET | Get List of Data Subject Group Members |
| `onetrust_get_linked_identity_group_using_get` | GET | Get Data Subject Group |
| `onetrust_get_linked_identity_groups_by_data_subject_v4` | GET | Get List of Data Subject Group Associations by Data Subject |
| `onetrust_get_linked_identity_groups_using_get` | GET | Get List of Data Subject Groups |
| `onetrust_get_list_of_deletion_certificates` | GET | Get List of Deletion Certificates |
| `onetrust_get_list_using_get` | GET | Get List of Purpose Preferences |
| `onetrust_get_merge_request_using_get` | GET | Get Scheduled Export |
| `onetrust_get_paged_merge_request_using_get` | GET | Get List of Scheduled Exports |
| `onetrust_get_preference_center_by_id_using_get` | GET | Get Preference Center Schema |
| `onetrust_get_preference_center_page_schema_using_get` | GET | Get Preference Center Page Schema |
| `onetrust_get_preference_centers_using_get` | GET | Get List of Preference Centers |
| `onetrust_get_purpose_detail_using_get` | GET | Get Purpose |
| `onetrust_get_purposes_using_get` | GET | Get List of Purposes |
| `onetrust_get_receipt_list_details_using_get` | GET | Get List of Receipt Details by Data Subject |
| `onetrust_get_receipt_list_details_using_post` | POST | Get List of Receipts |
| `onetrust_get_receipt_list_using_get` | GET | Get List of Receipts by Data Subject |
| `onetrust_get_root_schema_using_get` | GET | Get Preference Center Root Schema |
| `onetrust_get_token_using_get` | GET | Get Collection Point Token |
| `onetrust_get_transactions_using_post` | POST | Get List of Transactions |
| `onetrust_get_v3_datasubject_profiles_using_post` | GET | Get List of Data Subjects |
| `onetrust_get_v3_datasubjects_profile_using_get` | GET | Get Data Subject |
| `onetrust_search_data_subjects_by_element_v4` | POST | Search Data Subjects by Data Element |
| `onetrust_search_data_subjects_post_using_post` | POST | Search Data Subjects |
| `onetrust_withdraw_transaction_by_purpose_and_identifier_using_get` | GET | Withdraw Data Subject's Consent |
| `onetrust_add_consent_groups_to_consent_group_using_post` | POST | Add Consent Groups to Parent Consent Group |
| `onetrust_add_data_subjects_to_consent_group_using_post` | POST | Add Data Subjects to Parent Consent Group |
| `onetrust_add_purpose_rules_to_consent_group_using_post` | POST | Add Purpose Rules to Consent Group |
| `onetrust_create_collection_point_using_post` | POST | Create Collection Point |
| `onetrust_create_consent_group_using_post` | POST | Create Consent Group |
| `onetrust_create_custom_preference_using_post` | POST | Create Purpose Preference |
| `onetrust_create_data_subject_group_v4` | POST | Create Data Subject Group |
| `onetrust_create_index` | POST | Create Custom Index |
| `onetrust_create_job_using_post` | POST | Create Job |
| `onetrust_create_linked_identity_group_using_post` | POST | Create Data Subject Group |
| `onetrust_create_new_purpose_version_using_post` | POST | Create New Purpose Version |
| `onetrust_create_or_update_data_subject_using_post` | POST | Update Data Subject's Data Elements |
| `onetrust_create_purpose_using_post` | POST | Create Purpose |
| `onetrust_create_version_using_post` | POST | Create New Collection Point Version |
| `onetrust_merge_datasubject_using_post` | POST | Deduplicate Data Subjects |
| `onetrust_schedule_merge_request_using_post` | POST | Create Scheduled Export of Duplicate Data Subjects |
| `onetrust_upload_consent_attachments` | POST | Upload Consent Attachment |
| `onetrust_disable_collection_point_using_put` | PUT | Update Collection Point Status |
| `onetrust_edit_collection_point_using_put` | PUT | Update Existing Collection Point |
| `onetrust_edit_custom_preference_using_put` | PUT | Update Purpose Preference |
| `onetrust_edit_purpose_using_put` | PUT | Update Purpose |
| `onetrust_merge_data_subjects_using_post` | PUT | Deduplicate Data Subjects |
| `onetrust_publish_purpose_using_put` | PUT | Publish Purpose |
| `onetrust_set_retirement_using_put` | PUT | Retire Purpose |
| `onetrust_update_consent_group_settings_using_put` | PUT | Update Priority Scores for Purpose Statuses |
| `onetrust_update_data_subject_group_v4` | PUT | Update Data Subject Group |
| `onetrust_update_linked_identity_group_using_put` | PUT | Update Data Subject Group |
| `onetrust_update_preferences_for_data_subject_api_using_put` | PUT | Update Data Subject's Preferences in a Preference Center |
| `onetrust_update_purpose_rules_to_consent_group_using_put` | PUT | Update Consent Group Purpose Rule |
| `onetrust_withdraw_transaction_behalf_of_datasubject_using_put` | PUT | Withdraw Consent on Behalf of a Data Subject |
| `onetrust_cross_device_consent_using_delete` | DELETE | Delete Cross Device Consents and Receipts |
| `onetrust_delete_consent_group_purpose_rule_using_delete` | DELETE | Remove Purpose Rule from Consent Group |
| `onetrust_delete_data_subject_profile_using_delete` | DELETE | Delete Data Subjects |
| `onetrust_delete_data_subject_profiles_using_delete` | DELETE | Delete Purposes from Data Subject |
| `onetrust_delete_data_subject_using_ttl` | DELETE | Delete Data Subject |
| `onetrust_delete_data_subjects_to_consent_group_using_delete` | DELETE | Remove Data Subject from Parent Consent Group |
| `onetrust_delete_merge_request_using_delete` | DELETE | Delete Scheduled Export |
| `onetrust_delete_purpose_from_data_subject_using_delete` | DELETE | Delete Purpose from Data Subjects |
| `onetrust_delete_purpose_from_data_subjects_using_ttl` | DELETE | Delete Purposes from Data Subjects |
| `onetrust_delete_using_delete` | DELETE | Delete Data Subject Group |
| `onetrust_remove_all_consent_attachment_refs` | DELETE | Remove All Consent Attachments |
| `onetrust_remove_given_consent_attachment_refs` | DELETE | Remove Consent Attachment |
| `onetrust_unlink_consent_group_using_delete` | DELETE | Remove Consent Groups from Parent Consent Group |
| `onetrust_withdraw_preferences_api_using_delete` | DELETE | Withdraw Data Subject's Consent for All Purposes in a Preference Center |
