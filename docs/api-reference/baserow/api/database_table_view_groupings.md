# Database table view groupings

## GET /api/database/views/group_by/{view_group_by_id}/

****  
*operationId: `get_database_table_view_group`*

**Параметры:**

- `view_group_by_id` (path) — Returns the view group by related to the provided value.

---

## PATCH /api/database/views/group_by/{view_group_by_id}/

****  
*operationId: `update_database_table_view_group`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `ClientUndoRedoActionGroupId` (header) — An optional header that marks the action performed by this request as having occurred in a particular action group.Then calling the undo/redo endpoint with the same ClientSessionId header, all the actions belonging to the same action group can be undone/redone together in a single API call.
- `view_group_by_id` (path) — Updates the view group by related to the provided value.

**Тело запроса:**

- `field`: *integer* — The field that must be grouped by.
- `order`: ** — Indicates the sort order direction. ASC (Ascending) is from A to Z and DESC (Descending) is from Z to A.

* `ASC` - Ascending
* `DESC` - Descending
- `width`: *integer* — The pixel width of the group by in the related view.
- `type`: *string* — Indicates the sort type. Will automatically fall back to `default` if incompatible with field type.

---

## DELETE /api/database/views/group_by/{view_group_by_id}/

****  
*operationId: `delete_database_table_view_group`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `ClientUndoRedoActionGroupId` (header) — An optional header that marks the action performed by this request as having occurred in a particular action group.Then calling the undo/redo endpoint with the same ClientSessionId header, all the actions belonging to the same action group can be undone/redone together in a single API call.
- `view_group_by_id` (path) — Deletes the group by related to the provided value.

---

## GET /api/database/views/{view_id}/group_bys/

****  
*operationId: `list_database_table_view_groupings`*

**Параметры:**

- `view_id` (path) — Returns only groupings of the view related to the provided value.

---

## POST /api/database/views/{view_id}/group_bys/

****  
*operationId: `create_database_table_view_group`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `ClientUndoRedoActionGroupId` (header) — An optional header that marks the action performed by this request as having occurred in a particular action group.Then calling the undo/redo endpoint with the same ClientSessionId header, all the actions belonging to the same action group can be undone/redone together in a single API call.
- `view_id` (path) — Creates a group by for the view related to the provided value.

**Тело запроса:**

- `field`: *integer* (обязательно) — The field that must be grouped by.
- `order`: ** — Indicates the sort order direction. ASC (Ascending) is from A to Z and DESC (Descending) is from Z to A.

* `ASC` - Ascending
* `DESC` - Descending
- `width`: *integer* — The pixel width of the group by in the related view.
- `type`: *string* — Indicates the sort type. Will automatically fall back to `default` if incompatible with field type.

---
