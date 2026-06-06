# Jobs

## GET /api/jobs/

****  
*operationId: `list_job`*

**Параметры:**

- `generate_ai_values_field_id` (query) — **[Only for type='generate_ai_values']** Filter by the AI field ID.
- `job_ids` (query) — 
- `limit` (query) — 
- `offset` (query) — 
- `states` (query) — 
- `type` (query) — The type of job to filter for. Determines which additional filter fields are available.

* `duplicate_application` - duplicate_application
* `install_template` - install_template
* `create_snapshot` - create_snapshot
* `restore_snapshot` - restore_snapshot
* `export_applications` - export_applications
* `import_applications` - import_applications
* `airtable` - airtable
* `duplicate_table` - duplicate_table
* `duplicate_field` - duplicate_field
* `sync_data_sync_table` - sync_data_sync_table
* `duplicate_page` - duplicate_page
* `publish_domain` - publish_domain
* `duplicate_automation_workflow` - duplicate_automation_workflow
* `publish_automation_workflow` - publish_automation_workflow
* `generate_ai_values` - generate_ai_values
* `audit_log_export` - audit_log_export
* `data_scan_result_export` - data_scan_result_export
* `file_import` - file_import

---

## POST /api/jobs/

****  
*operationId: `create_job`*


**Тело запроса:**


---

## GET /api/jobs/{job_id}/

****  
*operationId: `get_job`*

**Параметры:**

- `job_id` (path) — The job id to lookup information about.

---

## POST /api/jobs/{job_id}/cancel/

****  
*operationId: `cancel_job`*

**Параметры:**

- `job_id` (path) — The job id to cancel.

---
