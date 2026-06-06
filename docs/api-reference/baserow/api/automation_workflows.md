# Automation workflows

## GET /api/automation/workflows/{workflow_id}/

****  
*operationId: `get_automation_workflow`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `workflow_id` (path) — The id of the workflow.

---

## PATCH /api/automation/workflows/{workflow_id}/

****  
*operationId: `update_automation_workflow`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `workflow_id` (path) — The id of the workflow.

**Тело запроса:**

- `name`: *string* — 
- `allow_test_run`: *boolean* — If provided, enables the workflow to be triggerable for the next 5 minutes.
- `state`: ** — 

---

## DELETE /api/automation/workflows/{workflow_id}/

****  
*operationId: `delete_automation_workflow`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `workflow_id` (path) — The id of the workflow.

---

## POST /api/automation/workflows/{workflow_id}/duplicate/async/

****  
*operationId: `duplicate_automation_workflow_async`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `workflow_id` (path) — The workflow to duplicate.

---

## GET /api/automation/workflows/{workflow_id}/history/

****  
*operationId: `get_automation_workflow_history`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `workflow_id` (path) — The id of the workflow.

---

## POST /api/automation/workflows/{workflow_id}/publish/async/

****  
*operationId: `publish_automation_workflow`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `workflow_id` (path) — The workflow id the user wants to publish.

---

## POST /api/automation/workflows/{workflow_id}/test/

****  
*operationId: `test_automation_workflow`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `workflow_id` (path) — The workflow id the user wants to test.

---

## POST /api/automation/{automation_id}/workflows/

****  
*operationId: `create_automation_workflow`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `automation_id` (path) — Creates a new Automation Workflow.

**Тело запроса:**

- `name`: *string* (обязательно) — 

---

## POST /api/automation/{automation_id}/workflows/order/

****  
*operationId: `order_automation_workflows`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `automation_id` (path) — The automation the workflow belongs to.

**Тело запроса:**

- `workflow_ids`: *array* (обязательно) — The ids of the workflows in the order they are supposed to be set in.

---
