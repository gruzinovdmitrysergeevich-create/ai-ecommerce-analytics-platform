# Workspaces

## GET /api/workspaces/

****  
*operationId: `list_workspaces`*


---

## POST /api/workspaces/

****  
*operationId: `create_workspace`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.

**Тело запроса:**

- `id`: *integer* (обязательно) — 
- `name`: *string* (обязательно) — 
- `generative_ai_models_enabled`: *string* (обязательно) — 

---

## POST /api/workspaces/create-initial-workspace/

****  
*operationId: `create_initial_workspace`*


---

## POST /api/workspaces/order/

****  
*operationId: `order_workspaces`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `ClientUndoRedoActionGroupId` (header) — An optional header that marks the action performed by this request as having occurred in a particular action group.Then calling the undo/redo endpoint with the same ClientSessionId header, all the actions belonging to the same action group can be undone/redone together in a single API call.

**Тело запроса:**

- `workspaces`: *array* (обязательно) — Workspace ids in the desired order.

---

## GET /api/workspaces/users/workspace/{workspace_id}/

****  
*operationId: `list_workspace_users`*

**Параметры:**

- `search` (query) — Search for workspace users by username, or email.
- `sorts` (query) — Sort workspace users by name, email or role.
- `workspace_id` (path) — Lists workspace users related to the provided workspace value.

---

## PATCH /api/workspaces/users/{workspace_user_id}/

****  
*operationId: `update_workspace_user`*

**Параметры:**

- `workspace_user_id` (path) — Updates the workspace user related to the provided value.

**Тело запроса:**

- `permissions`: *string* — The permissions that the user has within the workspace.

---

## DELETE /api/workspaces/users/{workspace_user_id}/

****  
*operationId: `delete_workspace_user`*

**Параметры:**

- `workspace_user_id` (path) — Deletes the workspace user related to the provided value.

---

## PATCH /api/workspaces/{workspace_id}/

****  
*operationId: `update_workspace`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `ClientUndoRedoActionGroupId` (header) — An optional header that marks the action performed by this request as having occurred in a particular action group.Then calling the undo/redo endpoint with the same ClientSessionId header, all the actions belonging to the same action group can be undone/redone together in a single API call.
- `workspace_id` (path) — Updates the workspace related to the provided value.

**Тело запроса:**

- `id`: *integer* — 
- `name`: *string* — 
- `generative_ai_models_enabled`: *string* — 

---

## DELETE /api/workspaces/{workspace_id}/

****  
*operationId: `delete_workspace`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `ClientUndoRedoActionGroupId` (header) — An optional header that marks the action performed by this request as having occurred in a particular action group.Then calling the undo/redo endpoint with the same ClientSessionId header, all the actions belonging to the same action group can be undone/redone together in a single API call.
- `workspace_id` (path) — Deletes the workspace related to the provided value.

---

## GET /api/workspaces/{workspace_id}/export/

****  
*operationId: `list_workspace_exports`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `workspace_id` (path) — The id of the workspace that is being exported.

---

## POST /api/workspaces/{workspace_id}/export/async/

****  
*operationId: `export_workspace_applications_async`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `workspace_id` (path) — The id of the workspace that must be exported.

---

## POST /api/workspaces/{workspace_id}/import/async/

****  
*operationId: `import_workspace_applications_async`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `workspace_id` (path) — The id of the workspace where the application will be imported.

---

## POST /api/workspaces/{workspace_id}/import/upload-file/

****  
*operationId: `import_resource_upload_file`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `workspace_id` (path) — The id of the workspace for which file is uploaded.

---

## DELETE /api/workspaces/{workspace_id}/import/{resource_id}/

****  
*operationId: `import_export_resource`*

**Параметры:**

- `resource_id` (path) — 
- `workspace_id` (path) — 

---

## POST /api/workspaces/{workspace_id}/leave/

****  
*operationId: `leave_workspace`*

**Параметры:**

- `workspace_id` (path) — Leaves the workspace related to the value.

---

## GET /api/workspaces/{workspace_id}/permissions/

****  
*operationId: `workspace_permissions`*

**Параметры:**

- `workspace_id` (path) — The workspace id we want the permission object for.

---

## GET /api/workspaces/{workspace_id}/settings/generative-ai/

****  
*operationId: `get_workspace_generative_ai_models_settings`*

**Параметры:**

- `workspace_id` (path) — 

---

## PATCH /api/workspaces/{workspace_id}/settings/generative-ai/

****  
*operationId: `update_workspace_generative_ai_models_settings`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `workspace_id` (path) — Updates the workspace settings for the generative AI models available.

**Тело запроса:**

- `openai`: ** — 
- `anthropic`: ** — 
- `mistral`: ** — 
- `ollama`: ** — 
- `openrouter`: ** — 

---
