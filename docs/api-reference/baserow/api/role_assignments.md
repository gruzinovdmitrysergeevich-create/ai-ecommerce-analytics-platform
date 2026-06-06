# Role assignments

## GET /api/role/{workspace_id}/

****  
*operationId: `list_role_assignments`*

**Параметры:**

- `scope_id` (query) — The id of the scope you are trying to get all roleassignments for.
- `scope_type` (query) — The type of scope you are trying to get all roleassignments for.
- `workspace_id` (path) — The workspace in which the role assignments are related to.

---

## POST /api/role/{workspace_id}/

****  
*operationId: `assign_role`*

**Параметры:**

- `workspace_id` (path) — The workspace in which the role assignment takes place.

**Тело запроса:**

- `subject_id`: *integer* (обязательно) — The subject ID. A subject is an actor that can do operations.
- `subject_type`: ** (обязательно) — The subject type.

* `auth.User` - auth.User
* `anonymous` - anonymous
* `user_source.user` - user_source.user
* `core.Token` - core.Token
* `baserow_enterprise.Team` - baserow_enterprise.Team
- `role`: *string* (обязательно) — The uid of the role you want to assign to the user or team in the given workspace. You can omit this property if you want to remove the role.
- `scope_id`: *integer* (обязательно) — The ID of the scope object. The scope object limit the role assignment to this scope and all its descendants.
- `scope_type`: ** (обязательно) — The scope object type.

* `core` - core
* `application` - application
* `workspace` - workspace
* `workspace_invitation` - workspace_invitation
* `snapshot` - snapshot
* `workspace_user` - workspace_user
* `integration` - integration
* `user_source` - user_source
* `mcp_endpoint` - mcp_endpoint
* `database` - database
* `database_table` - database_table
* `database_field` - database_field
* `database_view` - database_view
* `database_view_decoration` - database_view_decoration
* `database_view_sort` - database_view_sort
* `database_view_group` - database_view_group
* `database_view_filter` - database_view_filter
* `database_view_filter_group` - database_view_filter_group
* `token` - token
* `builder` - builder
* `builder_page` - builder_page
* `builder_element` - builder_element
* `builder_domain` - builder_domain
* `builder_data_source` - builder_data_source
* `builder_workflow_action` - builder_workflow_action
* `dashboard` - dashboard
* `dashboard_data_source` - dashboard_data_source
* `dashboard_widget` - dashboard_widget
* `automation` - automation
* `automation_workflow` - automation_workflow
* `automation_node` - automation_node
* `team` - team
* `team_subject` - team_subject
* `license` - license

---

## POST /api/role/{workspace_id}/batch/

****  
*operationId: `batch_assign_role`*

**Параметры:**

- `workspace_id` (path) — The workspace in which the role assignment takes place.

**Тело запроса:**

- `items`: *array* (обязательно) — 

---
