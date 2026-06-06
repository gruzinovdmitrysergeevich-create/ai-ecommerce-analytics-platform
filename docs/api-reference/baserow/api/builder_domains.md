# Builder domains

## GET /api/builder/domains/ask-public-domain-exists/

****  
*operationId: `ask_public_builder_domain_exists`*

**Параметры:**

- `domain` (query) — The domain name for which

---

## PATCH /api/builder/domains/{domain_id}/

****  
*operationId: `update_builder_domain`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `domain_id` (path) — The id of the domain

**Тело запроса:**

- `type`: ** — The type of the domain.

* `custom` - custom
* `sub_domain` - sub_domain
- `domain_name`: *string* — 

---

## DELETE /api/builder/domains/{domain_id}/

****  
*operationId: `delete_builder_domain`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `domain_id` (path) — The id of the domain

---

## POST /api/builder/domains/{domain_id}/publish/async/

****  
*operationId: `publish_builder_domain`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `domain_id` (path) — The builder application id the user wants to publish.

---

## GET /api/builder/{builder_id}/domains/

****  
*operationId: `get_builder_domains`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `builder_id` (path) — Gets all the domains for the specified builder

---

## POST /api/builder/{builder_id}/domains/

****  
*operationId: `create_builder_domain`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `builder_id` (path) — Creates a domain for the application builder related tothe provided value

**Тело запроса:**


---

## POST /api/builder/{builder_id}/domains/order/

****  
*operationId: `order_builder_domains`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `builder_id` (path) — The builder the domain belongs to

**Тело запроса:**

- `domain_ids`: *array* (обязательно) — The ids of the domains in the order they are supposed to be set in

---
