# Dashboard widgets

## PATCH /api/dashboard/widgets/{widget_id}/

****  
*operationId: `update_dashboard_widget`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `ClientUndoRedoActionGroupId` (header) — An optional header that marks the action performed by this request as having occurred in a particular action group.Then calling the undo/redo endpoint with the same ClientSessionId header, all the actions belonging to the same action group can be undone/redone together in a single API call.
- `widget_id` (path) — The id of the widget

**Тело запроса:**


---

## DELETE /api/dashboard/widgets/{widget_id}/

****  
*operationId: `delete_dashboard_widget`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `ClientUndoRedoActionGroupId` (header) — An optional header that marks the action performed by this request as having occurred in a particular action group.Then calling the undo/redo endpoint with the same ClientSessionId header, all the actions belonging to the same action group can be undone/redone together in a single API call.
- `widget_id` (path) — The id of the widget

---

## GET /api/dashboard/{dashboard_id}/widgets/

****  
*operationId: `list_dashboard_widgets`*

**Параметры:**

- `dashboard_id` (path) — Returns only the widgets of the dashboard related to the provided Id.

---

## POST /api/dashboard/{dashboard_id}/widgets/

****  
*operationId: `create_dashboard_widget`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `ClientUndoRedoActionGroupId` (header) — An optional header that marks the action performed by this request as having occurred in a particular action group.Then calling the undo/redo endpoint with the same ClientSessionId header, all the actions belonging to the same action group can be undone/redone together in a single API call.
- `dashboard_id` (path) — Creates a widget for the dashboard related to the provided value.

**Тело запроса:**


---
