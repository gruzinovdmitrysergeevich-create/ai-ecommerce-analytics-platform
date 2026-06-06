# Automation nodes

## PATCH /api/automation/node/{node_id}/

****  
*operationId: `update_automation_node`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `node_id` (path) — The id of the node to update.

**Тело запроса:**


---

## DELETE /api/automation/node/{node_id}/

****  
*operationId: `delete_automation_node`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `node_id` (path) — The id of the node to delete.

---

## POST /api/automation/node/{node_id}/duplicate/

****  
*operationId: `duplicate_automation_node`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `node_id` (path) — The node that is to be duplicated.

---

## POST /api/automation/node/{node_id}/move/

****  
*operationId: `move_automation_node`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `node_id` (path) — The node that is to be moved.

**Тело запроса:**

- `reference_node_id`: *integer* — The reference node.
- `position`: ** — The new position relative to the reference node.

* `south` - South
* `child` - Child
- `output`: *string* — The new output.

---

## POST /api/automation/node/{node_id}/replace/

****  
*operationId: `replace_automation_node`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `node_id` (path) — The node that is to be replaced.

**Тело запроса:**

- `new_type`: ** (обязательно) — The type of the new automation node

* `local_baserow_create_row` - local_baserow_create_row
* `local_baserow_update_row` - local_baserow_update_row
* `local_baserow_delete_row` - local_baserow_delete_row
* `local_baserow_get_row` - local_baserow_get_row
* `local_baserow_list_rows` - local_baserow_list_rows
* `local_baserow_aggregate_rows` - local_baserow_aggregate_rows
* `http_request` - http_request
* `iterator` - iterator
* `smtp_email` - smtp_email
* `router` - router
* `local_baserow_rows_created` - local_baserow_rows_created
* `local_baserow_rows_updated` - local_baserow_rows_updated
* `local_baserow_rows_deleted` - local_baserow_rows_deleted
* `periodic` - periodic
* `http_trigger` - http_trigger
* `ai_agent` - ai_agent
* `slack_write_message` - slack_write_message

---

## POST /api/automation/node/{node_id}/simulate-dispatch/

****  
*operationId: `simulate_dispatch_automation_node`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `node_id` (path) — The node to simulate the dispatch for.

---

## GET /api/automation/workflow/{workflow_id}/nodes/

****  
*operationId: `list_nodes`*

**Параметры:**

- `workflow_id` (path) — Returns the nodes related to a specific workflow.

---

## POST /api/automation/workflow/{workflow_id}/nodes/

****  
*operationId: `create_automation_node`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `workflow_id` (path) — Creates an automation node for the associated workflow.

**Тело запроса:**


---
