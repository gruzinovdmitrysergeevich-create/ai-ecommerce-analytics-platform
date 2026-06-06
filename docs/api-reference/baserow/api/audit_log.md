# Audit log

## GET /api/admin/audit-log/

****  
*operationId: `audit_log_list`*

**Параметры:**

- `action_type` (query) — Filter the audit log entries by action type.
- `from_timestamp` (query) — The ISO timestamp to filter the audit log entries from.
- `ids` (query) — A comma-separated list of audit log entries IDs to filter by. When provided, only audit log entries with those IDs are returned.
- `page` (query) — Defines which page should be returned.
- `size` (query) — Defines how many audit log entries should be returned per page.
- `sorts` (query) — A comma separated string of attributes to sort by, each attribute must be prefixed with `+` for a descending sort or a `-` for an ascending sort. The accepted attribute names are: `user, workspace, type, timestamp, ip_address`. For example `sorts=-user,-workspace` will sort the audit log entries first by descending user and then ascending workspace. A sortparameter with multiple instances of the same sort attribute will respond with the ERROR_INVALID_SORT_ATTRIBUTE error.
- `to_timestamp` (query) — The ISO timestamp to filter the audit log entries to.
- `user_id` (query) — Filter the audit log entries by user id.
- `workspace_id` (query) — Filter the audit log entries by workspace id. This filter works only for the admin audit log.

---

## GET /api/admin/audit-log/action-types/

****  
*operationId: `audit_log_action_types`*

**Параметры:**

- `search` (query) — If provided only action_types with name that match the query will be returned.
- `workspace_id` (query) — Return action types related to the workspace.

---

## POST /api/admin/audit-log/export/

****  
*operationId: `async_audit_log_export`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.

**Тело запроса:**

- `url`: *string* (обязательно) — 
- `export_charset`: ** — The character set to use when creating the export file.

* `utf-8` - utf-8
* `iso-8859-6` - iso-8859-6
* `windows-1256` - windows-1256
* `iso-8859-4` - iso-8859-4
* `windows-1257` - windows-1257
* `iso-8859-14` - iso-8859-14
* `iso-8859-2` - iso-8859-2
* `windows-1250` - windows-1250
* `gbk` - gbk
* `gb18030` - gb18030
* `big5` - big5
* `koi8-r` - koi8-r
* `koi8-u` - koi8-u
* `iso-8859-5` - iso-8859-5
* `windows-1251` - windows-1251
* `x-mac-cyrillic` - mac-cyrillic
* `iso-8859-7` - iso-8859-7
* `windows-1253` - windows-1253
* `iso-8859-8` - iso-8859-8
* `windows-1255` - windows-1255
* `euc-jp` - euc-jp
* `iso-2022-jp` - iso-2022-jp
* `shift-jis` - shift-jis
* `euc-kr` - euc-kr
* `macintosh` - macintosh
* `iso-8859-10` - iso-8859-10
* `iso-8859-16` - iso-8859-16
* `windows-874` - cp874
* `windows-1254` - windows-1254
* `windows-1258` - windows-1258
* `iso-8859-1` - iso-8859-1
* `windows-1252` - windows-1252
* `iso-8859-3` - iso-8859-3
- `csv_column_separator`: ** — The value used to separate columns in the resulting csv file.

* `,` - ,
* `;` - ;
* `|` - |
* `tab` - 	
* `record_separator` - 
* `unit_separator` - 
- `csv_first_row_header`: *boolean* — Whether or not to generate a header row at the top of the csv file.
- `filter_user_id`: *integer* — Optional: The user to filter the audit log by.
- `filter_workspace_id`: *integer* — Optional: The workspace to filter the audit log by.
- `filter_action_type`: ** — Optional: The action type to filter the audit log by.

* `create_group` - create_group
* `delete_group` - delete_group
* `update_group` - update_group
* `order_groups` - order_groups
* `create_application` - create_application
* `update_application` - update_application
* `delete_application` - delete_application
* `order_applications` - order_applications
* `duplicate_application` - duplicate_application
* `install_template` - install_template
* `create_group_invitation` - create_group_invitation
* `delete_group_invitation` - delete_group_invitation
* `accept_group_invitation` - accept_group_invitation
* `reject_group_invitation` - reject_group_invitation
* `update_group_invitation_permissions` - update_group_invitation_permissions
* `leave_group` - leave_group
* `create_initial_workspace` - create_initial_workspace
* `export_applications` - export_applications
* `import_applications` - import_applications
* `create_snapshot` - create_snapshot
* `delete_snapshot` - delete_snapshot
* `restore_snapshot` - restore_snapshot
* `empty_trash` - empty_trash
* `restore_from_trash` - restore_from_trash
* `create_mcp_endpoint` - create_mcp_endpoint
* `update_mcp_endpoint` - update_mcp_endpoint
* `delete_mcp_endpoint` - delete_mcp_endpoint
* `create_user` - create_user
* `update_user` - update_user
* `schedule_user_deletion` - schedule_user_deletion
* `cancel_user_deletion` - cancel_user_deletion
* `sign_in_user` - sign_in_user
* `change_user_password` - change_user_password
* `send_reset_user_password` - send_reset_user_password
* `reset_user_password` - reset_user_password
* `send_verify_email` - send_verify_email
* `verify_email` - verify_email
* `send_change_email_confirmation` - send_change_email_confirmation
* `change_email` - change_email
* `create_db_token` - create_db_token
* `update_db_token_name` - update_db_token_name
* `update_db_token_permissions` - update_db_token_permissions
* `rotate_db_token_key` - rotate_db_token_key
* `delete_db_token_key` - delete_db_token_key
* `create_webhook` - create_webhook
* `delete_webhook` - delete_webhook
* `update_webhook` - update_webhook
* `export_table` - export_table
* `import_database_from_airtable` - import_database_from_airtable
* `create_table` - create_table
* `delete_table` - delete_table
* `order_tables` - order_tables
* `update_table` - update_table
* `duplicate_table` - duplicate_table
* `create_row` - create_row
* `create_rows` - create_rows
* `import_rows` - import_rows
* `delete_row` - delete_row
* `delete_rows` - delete_rows
* `move_row` - move_row
* `update_row` - update_row
* `update_rows` - update_rows
* `create_view` - create_view
* `duplicate_view` - duplicate_view
* `delete_view` - delete_view
* `order_views` - order_views
* `update_view` - update_view
* `create_view_filter` - create_view_filter
* `update_view_filter` - update_view_filter
* `delete_view_filter` - delete_view_filter
* `create_view_sort` - create_view_sort
* `update_view_sort` - update_view_sort
* `delete_view_sort` - delete_view_sort
* `create_view_group` - create_view_group
* `update_view_group` - update_view_group
* `delete_view_group` - delete_view_group
* `submit_form` - submit_form
* `edit_form_row` - edit_form_row
* `rotate_view_slug` - rotate_view_slug
* `update_view_field_options` - update_view_field_options
* `update_view_default_values` - update_view_default_values
* `create_decoration` - create_decoration
* `update_decoration` - update_decoration
* `delete_decoration` - delete_decoration
* `create_view_filter_group` - create_view_filter_group
* `update_view_filter_group` - update_view_filter_group
* `delete_view_filter_group` - delete_view_filter_group
* `create_data_sync_table` - create_data_sync_table
* `update_data_sync_table` - update_data_sync_table
* `sync_data_sync_table` - sync_data_sync_table
* `create_field` - create_field
* `delete_field` - delete_field
* `update_field` - update_field
* `duplicate_field` - duplicate_field
* `change_primary_field` - change_primary_field
* `create_field_rule` - create_field_rule
* `update_field_rule` - update_field_rule
* `delete_field_rule` - delete_field_rule
* `create_widget` - create_widget
* `update_widget` - update_widget
* `delete_widget` - delete_widget
* `update_dashboard_data_source` - update_dashboard_data_source
* `create_automation_workflow` - create_automation_workflow
* `update_automation_workflow` - update_automation_workflow
* `delete_automation_workflow` - delete_automation_workflow
* `duplicate_automation_workflow` - duplicate_automation_workflow
* `order_automation_workflows` - order_automation_workflows
* `create_automation_node` - create_automation_node
* `update_automation_node` - update_automation_node
* `delete_automation_node` - delete_automation_node
* `duplicate_automation_node` - duplicate_automation_node
* `replace_automation_node` - replace_automation_node
* `move_automation_node` - move_automation_node
* `generate_formula_with_ai` - generate_formula_with_ai
* `create_row_comment` - create_row_comment
* `delete_row_comment` - delete_row_comment
* `update_row_comment` - update_row_comment
* `rotate_calendar_ical_view_slug` - rotate_calendar_ical_view_slug
* `create_team` - create_team
* `update_team` - update_team
* `delete_team` - delete_team
* `create_team_subject` - create_team_subject
* `delete_team_subject` - delete_team_subject
* `batch_assign_role` - batch_assign_role
* `update_field_permissions` - update_field_permissions
* `update_periodic_data_sync_interval` - update_periodic_data_sync_interval
* `create_data_scan` - create_data_scan
* `update_data_scan` - update_data_scan
* `delete_data_scan` - delete_data_scan
- `filter_from_timestamp`: *string* — Optional: The start date to filter the audit log by.
- `filter_to_timestamp`: *string* — Optional: The end date to filter the audit log by.
- `exclude_columns`: *string* — Optional: A comma separated list of column names to exclude from the export. Available options are `user_email, user_id, workspace_name, workspace_id, type, description, timestamp, ip_address`.

---

## GET /api/admin/audit-log/users/

****  
*operationId: `audit_log_users`*

**Параметры:**

- `ids` (query) — A comma-separated list of users IDs to filter by. When provided, only users with those IDs are returned.
- `page` (query) — Defines which page should be returned.
- `search` (query) — If provided only users with email that match the query will be returned.
- `size` (query) — Defines how many users should be returned per page.
- `workspace_id` (query) — Return users belonging to the given workspace_id.

---

## GET /api/audit-log/

****  
*operationId: `audit_log_list_2`*

**Параметры:**

- `action_type` (query) — Filter the audit log entries by action type.
- `from_timestamp` (query) — The ISO timestamp to filter the audit log entries from.
- `ids` (query) — A comma-separated list of audit log entries IDs to filter by. When provided, only audit log entries with those IDs are returned.
- `page` (query) — Defines which page should be returned.
- `size` (query) — Defines how many audit log entries should be returned per page.
- `sorts` (query) — A comma separated string of attributes to sort by, each attribute must be prefixed with `+` for a descending sort or a `-` for an ascending sort. The accepted attribute names are: `user, workspace, type, timestamp, ip_address`. For example `sorts=-user,-workspace` will sort the audit log entries first by descending user and then ascending workspace. A sortparameter with multiple instances of the same sort attribute will respond with the ERROR_INVALID_SORT_ATTRIBUTE error.
- `to_timestamp` (query) — The ISO timestamp to filter the audit log entries to.
- `user_id` (query) — Filter the audit log entries by user id.
- `workspace_id` (query) — Filter the audit log entries by workspace id. This filter works only for the admin audit log.

---

## GET /api/audit-log/action-types/

****  
*operationId: `audit_log_action_types_2`*

**Параметры:**

- `search` (query) — If provided only action_types with name that match the query will be returned.
- `workspace_id` (query) — Return action types related to the workspace.

---

## POST /api/audit-log/export/

****  
*operationId: `async_audit_log_export_2`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.

**Тело запроса:**

- `url`: *string* (обязательно) — 
- `export_charset`: ** — The character set to use when creating the export file.

* `utf-8` - utf-8
* `iso-8859-6` - iso-8859-6
* `windows-1256` - windows-1256
* `iso-8859-4` - iso-8859-4
* `windows-1257` - windows-1257
* `iso-8859-14` - iso-8859-14
* `iso-8859-2` - iso-8859-2
* `windows-1250` - windows-1250
* `gbk` - gbk
* `gb18030` - gb18030
* `big5` - big5
* `koi8-r` - koi8-r
* `koi8-u` - koi8-u
* `iso-8859-5` - iso-8859-5
* `windows-1251` - windows-1251
* `x-mac-cyrillic` - mac-cyrillic
* `iso-8859-7` - iso-8859-7
* `windows-1253` - windows-1253
* `iso-8859-8` - iso-8859-8
* `windows-1255` - windows-1255
* `euc-jp` - euc-jp
* `iso-2022-jp` - iso-2022-jp
* `shift-jis` - shift-jis
* `euc-kr` - euc-kr
* `macintosh` - macintosh
* `iso-8859-10` - iso-8859-10
* `iso-8859-16` - iso-8859-16
* `windows-874` - cp874
* `windows-1254` - windows-1254
* `windows-1258` - windows-1258
* `iso-8859-1` - iso-8859-1
* `windows-1252` - windows-1252
* `iso-8859-3` - iso-8859-3
- `csv_column_separator`: ** — The value used to separate columns in the resulting csv file.

* `,` - ,
* `;` - ;
* `|` - |
* `tab` - 	
* `record_separator` - 
* `unit_separator` - 
- `csv_first_row_header`: *boolean* — Whether or not to generate a header row at the top of the csv file.
- `filter_user_id`: *integer* — Optional: The user to filter the audit log by.
- `filter_workspace_id`: *integer* — Optional: The workspace to filter the audit log by.
- `filter_action_type`: ** — Optional: The action type to filter the audit log by.

* `create_group` - create_group
* `delete_group` - delete_group
* `update_group` - update_group
* `order_groups` - order_groups
* `create_application` - create_application
* `update_application` - update_application
* `delete_application` - delete_application
* `order_applications` - order_applications
* `duplicate_application` - duplicate_application
* `install_template` - install_template
* `create_group_invitation` - create_group_invitation
* `delete_group_invitation` - delete_group_invitation
* `accept_group_invitation` - accept_group_invitation
* `reject_group_invitation` - reject_group_invitation
* `update_group_invitation_permissions` - update_group_invitation_permissions
* `leave_group` - leave_group
* `create_initial_workspace` - create_initial_workspace
* `export_applications` - export_applications
* `import_applications` - import_applications
* `create_snapshot` - create_snapshot
* `delete_snapshot` - delete_snapshot
* `restore_snapshot` - restore_snapshot
* `empty_trash` - empty_trash
* `restore_from_trash` - restore_from_trash
* `create_mcp_endpoint` - create_mcp_endpoint
* `update_mcp_endpoint` - update_mcp_endpoint
* `delete_mcp_endpoint` - delete_mcp_endpoint
* `create_user` - create_user
* `update_user` - update_user
* `schedule_user_deletion` - schedule_user_deletion
* `cancel_user_deletion` - cancel_user_deletion
* `sign_in_user` - sign_in_user
* `change_user_password` - change_user_password
* `send_reset_user_password` - send_reset_user_password
* `reset_user_password` - reset_user_password
* `send_verify_email` - send_verify_email
* `verify_email` - verify_email
* `send_change_email_confirmation` - send_change_email_confirmation
* `change_email` - change_email
* `create_db_token` - create_db_token
* `update_db_token_name` - update_db_token_name
* `update_db_token_permissions` - update_db_token_permissions
* `rotate_db_token_key` - rotate_db_token_key
* `delete_db_token_key` - delete_db_token_key
* `create_webhook` - create_webhook
* `delete_webhook` - delete_webhook
* `update_webhook` - update_webhook
* `export_table` - export_table
* `import_database_from_airtable` - import_database_from_airtable
* `create_table` - create_table
* `delete_table` - delete_table
* `order_tables` - order_tables
* `update_table` - update_table
* `duplicate_table` - duplicate_table
* `create_row` - create_row
* `create_rows` - create_rows
* `import_rows` - import_rows
* `delete_row` - delete_row
* `delete_rows` - delete_rows
* `move_row` - move_row
* `update_row` - update_row
* `update_rows` - update_rows
* `create_view` - create_view
* `duplicate_view` - duplicate_view
* `delete_view` - delete_view
* `order_views` - order_views
* `update_view` - update_view
* `create_view_filter` - create_view_filter
* `update_view_filter` - update_view_filter
* `delete_view_filter` - delete_view_filter
* `create_view_sort` - create_view_sort
* `update_view_sort` - update_view_sort
* `delete_view_sort` - delete_view_sort
* `create_view_group` - create_view_group
* `update_view_group` - update_view_group
* `delete_view_group` - delete_view_group
* `submit_form` - submit_form
* `edit_form_row` - edit_form_row
* `rotate_view_slug` - rotate_view_slug
* `update_view_field_options` - update_view_field_options
* `update_view_default_values` - update_view_default_values
* `create_decoration` - create_decoration
* `update_decoration` - update_decoration
* `delete_decoration` - delete_decoration
* `create_view_filter_group` - create_view_filter_group
* `update_view_filter_group` - update_view_filter_group
* `delete_view_filter_group` - delete_view_filter_group
* `create_data_sync_table` - create_data_sync_table
* `update_data_sync_table` - update_data_sync_table
* `sync_data_sync_table` - sync_data_sync_table
* `create_field` - create_field
* `delete_field` - delete_field
* `update_field` - update_field
* `duplicate_field` - duplicate_field
* `change_primary_field` - change_primary_field
* `create_field_rule` - create_field_rule
* `update_field_rule` - update_field_rule
* `delete_field_rule` - delete_field_rule
* `create_widget` - create_widget
* `update_widget` - update_widget
* `delete_widget` - delete_widget
* `update_dashboard_data_source` - update_dashboard_data_source
* `create_automation_workflow` - create_automation_workflow
* `update_automation_workflow` - update_automation_workflow
* `delete_automation_workflow` - delete_automation_workflow
* `duplicate_automation_workflow` - duplicate_automation_workflow
* `order_automation_workflows` - order_automation_workflows
* `create_automation_node` - create_automation_node
* `update_automation_node` - update_automation_node
* `delete_automation_node` - delete_automation_node
* `duplicate_automation_node` - duplicate_automation_node
* `replace_automation_node` - replace_automation_node
* `move_automation_node` - move_automation_node
* `generate_formula_with_ai` - generate_formula_with_ai
* `create_row_comment` - create_row_comment
* `delete_row_comment` - delete_row_comment
* `update_row_comment` - update_row_comment
* `rotate_calendar_ical_view_slug` - rotate_calendar_ical_view_slug
* `create_team` - create_team
* `update_team` - update_team
* `delete_team` - delete_team
* `create_team_subject` - create_team_subject
* `delete_team_subject` - delete_team_subject
* `batch_assign_role` - batch_assign_role
* `update_field_permissions` - update_field_permissions
* `update_periodic_data_sync_interval` - update_periodic_data_sync_interval
* `create_data_scan` - create_data_scan
* `update_data_scan` - update_data_scan
* `delete_data_scan` - delete_data_scan
- `filter_from_timestamp`: *string* — Optional: The start date to filter the audit log by.
- `filter_to_timestamp`: *string* — Optional: The end date to filter the audit log by.
- `exclude_columns`: *string* — Optional: A comma separated list of column names to exclude from the export. Available options are `user_email, user_id, workspace_name, workspace_id, type, description, timestamp, ip_address`.

---

## GET /api/audit-log/users/

****  
*operationId: `audit_log_users_2`*

**Параметры:**

- `ids` (query) — A comma-separated list of users IDs to filter by. When provided, only users with those IDs are returned.
- `page` (query) — Defines which page should be returned.
- `search` (query) — If provided only users with email that match the query will be returned.
- `size` (query) — Defines how many users should be returned per page.
- `workspace_id` (query) — Return users belonging to the given workspace_id.

---
