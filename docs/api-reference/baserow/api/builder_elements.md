# Builder elements

## GET /api/builder/domains/published/page/{page_id}/elements/

****  
*operationId: `list_public_builder_page_elements`*

**Параметры:**

- `page_id` (path) — Returns the elements of the page related to the provided Id.

---

## PATCH /api/builder/element/{element_id}/

****  
*operationId: `update_builder_page_element`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `element_id` (path) — The id of the element

**Тело запроса:**


---

## DELETE /api/builder/element/{element_id}/

****  
*operationId: `delete_builder_page_element`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `element_id` (path) — The id of the element

---

## POST /api/builder/element/{element_id}/duplicate/

****  
*operationId: `duplicate_builder_page_element`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `element_id` (path) — The id of the element to duplicate

---

## PATCH /api/builder/element/{element_id}/move/

****  
*operationId: `move_builder_page_element`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `element_id` (path) — The id of the element to move

**Тело запроса:**

- `before_id`: *integer* — If provided, the element is moved before the element with this Id. Otherwise the element is placed at the end of the page.
- `parent_element_id`: *integer* — If provided, the element is moved as a child of the element with the given id.
- `place_in_container`: *string* — The place in the container.
- `target_page_id`: *integer* — If provided, the new target page for the element.

---

## GET /api/builder/page/{page_id}/elements/

****  
*operationId: `list_builder_page_elements`*

**Параметры:**

- `page_id` (path) — Returns only the elements of the page related to the provided Id.

---

## POST /api/builder/page/{page_id}/elements/

****  
*operationId: `create_builder_page_element`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `page_id` (path) — Creates an element for the builder page related to the provided value.

**Тело запроса:**


---
