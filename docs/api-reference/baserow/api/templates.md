# Templates

## GET /api/templates/

****  
*operationId: `list_templates`*


---

## POST /api/templates/install/{workspace_id}/{template_id}/

****  
*operationId: `install_template`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `ClientUndoRedoActionGroupId` (header) — An optional header that marks the action performed by this request as having occurred in a particular action group.Then calling the undo/redo endpoint with the same ClientSessionId header, all the actions belonging to the same action group can be undone/redone together in a single API call.
- `template_id` (path) — The id related to the template that must be installed.
- `workspace_id` (path) — The id related to the workspace where the template applications must be installed into.

---

## POST /api/templates/install/{workspace_id}/{template_id}/async/

****  
*operationId: `install_template_async`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `ClientUndoRedoActionGroupId` (header) — An optional header that marks the action performed by this request as having occurred in a particular action group.Then calling the undo/redo endpoint with the same ClientSessionId header, all the actions belonging to the same action group can be undone/redone together in a single API call.
- `template_id` (path) — The id related to the template that must be installed.
- `workspace_id` (path) — The id related to the workspace where the template applications must be installed into.

---
