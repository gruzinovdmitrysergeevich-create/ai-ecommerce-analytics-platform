# Builder workflow actions

## GET /api/builder/domains/published/page/{page_id}/workflow_actions/

****  
*operationId: `list_public_builder_page_workflow_actions`*

**Параметры:**

- `page_id` (path) — Returns only the public workflow actions of the page related to the provided Id.

---

## GET /api/builder/page/{page_id}/workflow_actions/

****  
*operationId: `list_builder_page_workflow_actions`*

**Параметры:**

- `page_id` (path) — Returns only the workflow actions of the page related to the provided Id.

---

## POST /api/builder/page/{page_id}/workflow_actions/

****  
*operationId: `create_builder_page_workflow_action`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `page_id` (path) — Creates a workflow action for the builder page related to the provided value.

**Тело запроса:**


---

## POST /api/builder/page/{page_id}/workflow_actions/order/

****  
*operationId: `order_builder_workflow_actions`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `page_id` (path) — The page the workflow actions belong to

**Тело запроса:**

- `workflow_action_ids`: *array* (обязательно) — The ids of the workflow actions in the order they are supposed to be set in
- `element_id`: *integer* — The element the workflow actions belong to

---

## PATCH /api/builder/workflow_action/{workflow_action_id}/

****  
*operationId: `update_builder_page_workflow_action`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `workflow_action_id` (path) — The id of the workflow action

**Тело запроса:**


---

## DELETE /api/builder/workflow_action/{workflow_action_id}/

****  
*operationId: `delete_builder_page_workflow_action`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `workflow_action_id` (path) — The id of the workflow action

---

## POST /api/builder/workflow_action/{workflow_action_id}/dispatch/

****  
*operationId: `dispatch_builder_page_workflow_action`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `workflow_action_id` (path) — The id of the workflow_action you want to call the dispatch for.

---
