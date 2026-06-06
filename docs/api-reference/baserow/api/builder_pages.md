# Builder pages

## PATCH /api/builder/pages/{page_id}/

****  
*operationId: `update_builder_page`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `page_id` (path) — The id of the page

**Тело запроса:**

- `name`: *string* — 
- `path`: *string* — 
- `path_params`: *array* — 
- `visibility`: ** — Controls the page's visibility. When set to 'logged-in', the builder's login_page must also be set.

* `all` - All
* `logged-in` - Logged In
- `role_type`: ** — Role type is used in conjunction with roles to control access to this page.

* `allow_all` - Allow All
* `allow_all_except` - Allow All Except
* `disallow_all_except` - Disallow All Except
- `roles`: ** — List of user roles that are associated with this page. Used in conjunction with role_type.
- `query_params`: *array* — 

---

## DELETE /api/builder/pages/{page_id}/

****  
*operationId: `delete_builder_page`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `page_id` (path) — The id of the page

---

## POST /api/builder/pages/{page_id}/duplicate/async/

****  
*operationId: `duplicate_builder_page_async`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `page_id` (path) — The page to duplicate.

---

## POST /api/builder/{builder_id}/pages/

****  
*operationId: `create_builder_page`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `builder_id` (path) — Creates a page for the application builder related to the provided value.

**Тело запроса:**

- `name`: *string* (обязательно) — 
- `path`: *string* (обязательно) — 
- `path_params`: *array* — 
- `query_params`: *array* — 

---

## POST /api/builder/{builder_id}/pages/order/

****  
*operationId: `order_builder_pages`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `builder_id` (path) — The builder the page belongs to

**Тело запроса:**

- `page_ids`: *array* (обязательно) — The ids of the pages in the order they are supposed to be set in

---
