# OneTrust Platform Administration

Administer the OneTrust tenant: organizations, users, user groups and access levels, SCIM user and group provisioning, integration workflows, bulk export jobs, and a raw request tool for endpoints without a typed tool. Use when the agent must manage who can do what, provision users, import or export a workflow, or export tenant data. Do NOT use for privacy content (the other onetrust skills).

# OneTrust Platform Administration

Administration controls who can reach the tenant and how data leaves it. Users and groups can be managed through the access API or through SCIM provisioning; exports run as jobs with a credit budget.

## When to use
- Read and change organizations, users, user groups, members and access levels.
- Provision users and groups through the SCIM tools and read the service-provider configuration.
- Import or export integration workflows.
- Start, poll, download and cancel bulk export jobs.
- Send a raw request when no typed tool covers an endpoint.

## When NOT to use
- Any privacy record: use the matching onetrust skill.

## Workflow
1. Read the current user, group or access level first.
2. Apply one change at a time and read the result back.
3. For an export, check the credits, start the job, poll the run, then fetch the download commands.

## Safety
- Removing a user, group or access level can lock people out; ask first.
- Never print tokens, client secrets or the OAuth token response.
- Prefer a typed tool over the raw request tool whenever one exists.

## Tools (74)

Each tool is one API operation; pass its path, query and body fields as named arguments.


### Access Management

| Tool | Method | Purpose |
|---|---|---|
| `onetrust_get_access_levels_for_user_group_by_id_v2` | GET | Get User Group Roles |
| `onetrust_get_all_user_details_v2` | GET | Get List of Users |
| `onetrust_get_all_user_group_with_filters_v2` | GET | Get List of User Groups |
| `onetrust_get_members_from_auser_group_by_id_v2` | GET | Get List of Users in User Group |
| `onetrust_get_oauth_token` | POST | Generate Access Token |
| `onetrust_get_user_access_levels_v2` | GET | Get User Roles |
| `onetrust_get_user_group_by_id_v2` | GET | Get User Group |
| `onetrust_get_user_v2` | GET | Get User |
| `onetrust_login_history` | GET | Get Audit Records for Login History |
| `onetrust_organization_tree_structure_using_get` | GET | Get List of Organizations |
| `onetrust_retrieve_members_using_get` | GET | Get User Group Members |
| `onetrust_retrieve_user_groups_using_get` | GET | Get List of User Groups |
| `onetrust_user_activity` | GET | Get Audit Records for User's Profile |
| `onetrust_add_access_levels_for_user_group_by_id_v2` | POST | Add User Group Roles |
| `onetrust_add_amember_for_user_group_by_id_v2` | POST | Add User to User Group |
| `onetrust_add_members_using_post` | POST | Add Members to User Group |
| `onetrust_add_multiple_members_for_user_group_by_id_v2` | POST | Add Multiple Users to User Group |
| `onetrust_add_user_access_level_v2` | POST | Add User Role |
| `onetrust_create_organization_using_post` | POST | Create Organization |
| `onetrust_create_user_group_using_post` | POST | Create User Group |
| `onetrust_create_user_group_v2` | POST | Create User Group |
| `onetrust_create_user_v2` | POST | Create User |
| `onetrust_set_user_default_organization_v2` | PATCH | Modify User Default Organization |
| `onetrust_update_access_level_for_user_group_by_id_v2` | PUT | Update User Group Roles |
| `onetrust_update_organization_using_put` | PUT | Update Organization |
| `onetrust_update_user_group_by_id_v2` | PUT | Update User Group |
| `onetrust_update_user_group_using_put` | PUT | Update User Group |
| `onetrust_update_user_v2` | PUT | Update User |
| `onetrust_delete_organization_post` | DELETE | Delete Organization |
| `onetrust_delete_user_group_by_id_v2` | DELETE | Delete User Group |
| `onetrust_delete_user_group_using_delete` | DELETE | Delete User Group |
| `onetrust_remove_access_level_for_user_group_by_id_v2` | DELETE | Remove User Group Roles |
| `onetrust_remove_amember_for_user_group_by_id_v2` | DELETE | Remove User from User Group |
| `onetrust_remove_members_using_delete` | DELETE | Remove Members from User Group |
| `onetrust_remove_multiple_members_for_user_group_by_id_v2` | DELETE | Remove Multiple Users from User Group |
| `onetrust_remove_user_access_level_v2` | DELETE | Remove User Role |

### Bulk Export

| Tool | Method | Purpose |
|---|---|---|
| `onetrust_get_attachment_download_commands_get` | GET | Get Bulk Export Download Details |
| `onetrust_get_credits_information_get` | GET | Get Bulk Export Credit Details |
| `onetrust_get_export_run_details_get` | GET | Get Bulk Export Status |
| `onetrust_get_export_runs_get` | GET | Get List of Bulk Exports |
| `onetrust_get_paginated_attachment_download_commands_get` | GET | Get List of Bulk Export Download Details |
| `onetrust_start_export_run_post` | POST | Create Bulk Export |
| `onetrust_cancel_bulk_export_delete` | DELETE | Cancel Bulk Export |

### Integrations

| Tool | Method | Purpose |
|---|---|---|
| `onetrust_export_workflow_using_get_1` | GET | Export Workflow |
| `onetrust_create_v2_using_post_x` | POST | Create System Credential |
| `onetrust_import_workflow_using_post_1` | POST | Import Workflow |
| `onetrust_update_v2_using_put_x` | PUT | Update System Credential |

### Platform Request

| Tool | Method | Purpose |
|---|---|---|
| `onetrust_api_request` | POST | Send one raw REST request to the tenant for an endpoint no typed tool covers |

### User Provisioning

| Tool | Method | Purpose |
|---|---|---|
| `onetrust_get_all_users_using_get` | GET | Get List of Users |
| `onetrust_get_group_by_id` | GET | Get User Group |
| `onetrust_get_group_resource_using_get` | GET | Get Group |
| `onetrust_get_groups` | GET | Get List of User Groups |
| `onetrust_get_resource_types_by_name_using_get` | GET | Get Supported Resource Types |
| `onetrust_get_resource_types_using_get` | GET | Get Supported Resources |
| `onetrust_get_schemas_by_name_using_get` | GET | Get SCIM Schema |
| `onetrust_get_schemas_using_get` | GET | Get List of Supported SCIM Schemas |
| `onetrust_get_service_provider_config_using_get` | GET | Get Service Provider Configuration |
| `onetrust_get_user_by_id` | GET | Get User |
| `onetrust_get_user_using_get` | GET | Get User |
| `onetrust_get_users` | GET | Get List of Users |
| `onetrust_list_groups_using_get` | GET | Get List of Groups |
| `onetrust_create_group` | POST | Create User Group |
| `onetrust_create_user` | POST | Create User |
| `onetrust_create_user_using_post` | POST | Create User |
| `onetrust_modify_group` | PATCH | Modify User Group |
| `onetrust_modify_user` | PATCH | Modify User |
| `onetrust_patch_user_using_patch` | PATCH | Modify User |
| `onetrust_update_group` | PUT | Update User Group |
| `onetrust_update_group_members_using_patch` | PATCH | Modify Group |
| `onetrust_update_group_members_using_put` | PUT | Update Group |
| `onetrust_update_user` | PUT | Update User |
| `onetrust_update_user_using_put` | PUT | Update User |
| `onetrust_delete_group` | DELETE | Delete User Group |
| `onetrust_delete_user_using_delete` | DELETE | Delete User |
