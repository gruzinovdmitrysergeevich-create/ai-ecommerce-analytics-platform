# Database table view sortings

## GET /api/database/views/sort/{view_sort_id}/

****  
*operationId: `get_database_table_view_sort`*

**Параметры:**

- `view_sort_id` (path) — Returns the view sort related to the provided value.

---

## PATCH /api/database/views/sort/{view_sort_id}/

****  
*operationId: `update_database_table_view_sort`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `ClientUndoRedoActionGroupId` (header) — An optional header that marks the action performed by this request as having occurred in a particular action group.Then calling the undo/redo endpoint with the same ClientSessionId header, all the actions belonging to the same action group can be undone/redone together in a single API call.
- `view_sort_id` (path) — Updates the view sort related to the provided value.

**Тело запроса:**

- `field`: *integer* — The field that must be sorted on.
- `order`: ** — Indicates the sort order direction. ASC (Ascending) is from A to Z and DESC (Descending) is from Z to A.

* `ASC` - Ascending
* `DESC` - Descending
- `type`: *string* — Indicates the sort type. Will automatically fall back to `default` if incompatible with field type.

---

## DELETE /api/database/views/sort/{view_sort_id}/

****  
*operationId: `delete_database_table_view_sort`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `ClientUndoRedoActionGroupId` (header) — An optional header that marks the action performed by this request as having occurred in a particular action group.Then calling the undo/redo endpoint with the same ClientSessionId header, all the actions belonging to the same action group can be undone/redone together in a single API call.
- `view_sort_id` (path) — Deletes the sort related to the provided value.

---

## GET /api/database/views/{view_id}/sortings/

****  
*operationId: `list_database_table_view_sortings`*

**Параметры:**

- `view_id` (path) — Returns only sortings of the view related to the provided value.

---

## POST /api/database/views/{view_id}/sortings/

****  
*operationId: `create_database_table_view_sort`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `ClientUndoRedoActionGroupId` (header) — An optional header that marks the action performed by this request as having occurred in a particular action group.Then calling the undo/redo endpoint with the same ClientSessionId header, all the actions belonging to the same action group can be undone/redone together in a single API call.
- `view_id` (path) — Creates a sort for the view related to the provided value.

**Тело запроса:**

- `field`: *integer* (обязательно) — The field that must be sorted on.
- `order`: ** — Indicates the sort order direction. ASC (Ascending) is from A to Z and DESC (Descending) is from Z to A.

* `ASC` - Ascending
* `DESC` - Descending
- `type`: *string* — Indicates the sort type. Will automatically fall back to `default` if incompatible with field type.

---
