# Database table view decorations

## GET /api/database/views/decoration/{view_decoration_id}/

****  
*operationId: `get_database_table_view_decoration`*

**Параметры:**

- `view_decoration_id` (path) — Returns the view decoration related to the provided id.

---

## PATCH /api/database/views/decoration/{view_decoration_id}/

****  
*operationId: `update_database_table_view_decoration`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `ClientUndoRedoActionGroupId` (header) — An optional header that marks the action performed by this request as having occurred in a particular action group.Then calling the undo/redo endpoint with the same ClientSessionId header, all the actions belonging to the same action group can be undone/redone together in a single API call.
- `view_decoration_id` (path) — Updates the view decoration related to the provided value.

**Тело запроса:**


---

## DELETE /api/database/views/decoration/{view_decoration_id}/

****  
*operationId: `delete_database_table_view_decoration`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `ClientUndoRedoActionGroupId` (header) — An optional header that marks the action performed by this request as having occurred in a particular action group.Then calling the undo/redo endpoint with the same ClientSessionId header, all the actions belonging to the same action group can be undone/redone together in a single API call.
- `view_decoration_id` (path) — Deletes the decoration related to the provided value.

---

## GET /api/database/views/{view_id}/decorations/

****  
*operationId: `list_database_table_view_decorations`*

**Параметры:**

- `view_id` (path) — Returns only decoration of the view given to the provided value.

---

## POST /api/database/views/{view_id}/decorations/

****  
*operationId: `create_database_table_view_decoration`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `ClientUndoRedoActionGroupId` (header) — An optional header that marks the action performed by this request as having occurred in a particular action group.Then calling the undo/redo endpoint with the same ClientSessionId header, all the actions belonging to the same action group can be undone/redone together in a single API call.
- `view_id` (path) — Creates a decoration for the view related to the given value.

**Тело запроса:**


---
