# Applications

## GET /api/applications/

****  
*operationId: `list_all_applications`*


---

## GET /api/applications/workspace/{workspace_id}/

****  
*operationId: `workspace_list_applications`*

**Параметры:**

- `workspace_id` (path) — Returns only applications that are in the workspace related to the provided value.

---

## POST /api/applications/workspace/{workspace_id}/

****  
*operationId: `workspace_create_application`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `ClientUndoRedoActionGroupId` (header) — An optional header that marks the action performed by this request as having occurred in a particular action group.Then calling the undo/redo endpoint with the same ClientSessionId header, all the actions belonging to the same action group can be undone/redone together in a single API call.
- `workspace_id` (path) — Creates an application for the workspace related to the provided value.

**Тело запроса:**


---

## POST /api/applications/workspace/{workspace_id}/order/

****  
*operationId: `workspace_order_applications`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `ClientUndoRedoActionGroupId` (header) — An optional header that marks the action performed by this request as having occurred in a particular action group.Then calling the undo/redo endpoint with the same ClientSessionId header, all the actions belonging to the same action group can be undone/redone together in a single API call.
- `workspace_id` (path) — Updates the order of the applications in the workspace related to the provided value.

**Тело запроса:**

- `application_ids`: *array* (обязательно) — Application ids in the desired order.

---

## GET /api/applications/{application_id}/

****  
*operationId: `workspace_get_application`*

**Параметры:**

- `application_id` (path) — Returns the application related to the provided value.

---

## PATCH /api/applications/{application_id}/

****  
*operationId: `workspace_update_application`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `ClientUndoRedoActionGroupId` (header) — An optional header that marks the action performed by this request as having occurred in a particular action group.Then calling the undo/redo endpoint with the same ClientSessionId header, all the actions belonging to the same action group can be undone/redone together in a single API call.
- `application_id` (path) — Updates the application related to the provided value.

**Тело запроса:**


---

## DELETE /api/applications/{application_id}/

****  
*operationId: `workspace_delete_application`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `ClientUndoRedoActionGroupId` (header) — An optional header that marks the action performed by this request as having occurred in a particular action group.Then calling the undo/redo endpoint with the same ClientSessionId header, all the actions belonging to the same action group can be undone/redone together in a single API call.
- `application_id` (path) — Deletes the application related to the provided value.

---

## POST /api/applications/{application_id}/duplicate/async/

****  
*operationId: `duplicate_application_async`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `ClientUndoRedoActionGroupId` (header) — An optional header that marks the action performed by this request as having occurred in a particular action group.Then calling the undo/redo endpoint with the same ClientSessionId header, all the actions belonging to the same action group can be undone/redone together in a single API call.
- `application_id` (path) — The id of the application to duplicate.

---
