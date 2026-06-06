# Dashboard data sources

## PATCH /api/dashboard/data-sources/{data_source_id}/

****  
*operationId: `update_dashboard_data_source`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `ClientUndoRedoActionGroupId` (header) — An optional header that marks the action performed by this request as having occurred in a particular action group.Then calling the undo/redo endpoint with the same ClientSessionId header, all the actions belonging to the same action group can be undone/redone together in a single API call.
- `data_source_id` (path) — The id of the dashboard data source.

**Тело запроса:**


---

## POST /api/dashboard/data-sources/{data_source_id}/dispatch/

****  
*operationId: `dispatch_dashboard_data_source`*

**Параметры:**

- `data_source_id` (path) — The id of the data source you want to call the dispatch for

---

## GET /api/dashboard/{dashboard_id}/data-sources/

****  
*operationId: `list_dashboard_data_sources`*

**Параметры:**

- `dashboard_id` (path) — Returns only the data sources of the dashboard related to the provided Id.

---
