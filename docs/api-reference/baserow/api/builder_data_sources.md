# Builder data sources

## PATCH /api/builder/data-source/{data_source_id}/

****  
*operationId: `update_builder_page_data_source`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `data_source_id` (path) — The id of the data_source

**Тело запроса:**


---

## DELETE /api/builder/data-source/{data_source_id}/

****  
*operationId: `delete_builder_page_data_source`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `data_source_id` (path) — The id of the data_source

---

## POST /api/builder/data-source/{data_source_id}/dispatch/

****  
*operationId: `dispatch_builder_page_data_source`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `data_source_id` (path) — The id of the data_source you want to call the dispatch for

**Тело запроса:**

- `metadata`: ** — Metadata of the dispatch payload. Can be either an object or a serialized string.

---

## PATCH /api/builder/data-source/{data_source_id}/move/

****  
*operationId: `move_builder_page_data_source`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `data_source_id` (path) — The id of the data_source to move

**Тело запроса:**

- `before_id`: *integer* — If provided, the data_source is moved before the data_source with this Id. Otherwise the data_source is placed  last for this page.

---

## GET /api/builder/data-source/{data_source_id}/record-names/

****  
*operationId: `get_record_names_builder_page_data_source`*

**Параметры:**

- `data_source_id` (path) — The id of the data_source to find the record names.
- `record_ids` (query) — A comma separated list of the record ids to search for.

---

## POST /api/builder/domains/published/data-source/{data_source_id}/dispatch/

****  
*operationId: `dispatch_public_builder_page_data_source`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `data_source_id` (path) — The id of the data_source you want to call the dispatch for

**Тело запроса:**

- `metadata`: ** — Metadata of the dispatch payload. Can be either an object or a serialized string.

---

## GET /api/builder/domains/published/page/{page_id}/data_sources/

****  
*operationId: `list_public_builder_page_data_sources`*

**Параметры:**

- `page_id` (path) — Returns only the data_sources of the page related to the provided Id if the related builder is public.

---

## POST /api/builder/domains/published/page/{page_id}/dispatch-data-sources/

****  
*operationId: `dispatch_public_builder_page_data_sources`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `page_id` (path) — The page we want to dispatch the data source for.

---

## GET /api/builder/page/{page_id}/data-sources/

****  
*operationId: `list_builder_page_data_sources`*

**Параметры:**

- `page_id` (path) — Returns only the data_sources of the page related to the provided Id.

---

## POST /api/builder/page/{page_id}/data-sources/

****  
*operationId: `create_builder_page_data_source`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `page_id` (path) — Creates a data_source for the builder page related to the provided value.

**Тело запроса:**


---

## POST /api/builder/page/{page_id}/dispatch-data-sources/

****  
*operationId: `dispatch_builder_page_data_sources`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `page_id` (path) — The page we want to dispatch the data source for.

**Тело запроса:**

- `metadata`: ** — Metadata of the dispatch payload. Can be either an object or a serialized string.

---
