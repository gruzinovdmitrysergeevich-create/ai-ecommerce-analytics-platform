# Integrations

## GET /api/application/{application_id}/integrations/

****  
*operationId: `list_application_integrations`*

**Параметры:**

- `application_id` (path) — Returns only the integrations of the application related to the provided Id.

---

## POST /api/application/{application_id}/integrations/

****  
*operationId: `create_application_integration`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `application_id` (path) — Creates an integration for the application related to the provided value.

**Тело запроса:**


---

## PATCH /api/integration/{integration_id}/

****  
*operationId: `update_application_integration`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `integration_id` (path) — The id of the integration

**Тело запроса:**


---

## DELETE /api/integration/{integration_id}/

****  
*operationId: `delete_application_integration`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `integration_id` (path) — The id of the integration

---

## PATCH /api/integration/{integration_id}/move/

****  
*operationId: `move_application_integration`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `integration_id` (path) — The id of the integration to move

**Тело запроса:**

- `before_id`: *integer* — If provided, the integration is moved before the integration with this Id. Otherwise the integration is placed at the end of the page.

---
