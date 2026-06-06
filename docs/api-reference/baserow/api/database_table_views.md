# Database table views

## PATCH /api/database/view/{view_id}/premium

****  
*operationId: `premium_view_attributes_update`*

**Параметры:**

- `view_id` (path) — Sets show_logo of this view.

**Тело запроса:**

- `show_logo`: *boolean* — 
- `allow_public_export`: *boolean* — 

---

## GET /api/database/views/calendar/{ical_slug}.ics

****  
*operationId: `calendar_ical_feed`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `ical_slug` (path) — ICal feed unique slug.

---

## POST /api/database/views/calendar/{view_id}/ical_slug_rotate/

****  
*operationId: `rotate_calendar_view_ical_feed_slug`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `ClientUndoRedoActionGroupId` (header) — An optional header that marks the action performed by this request as having occurred in a particular action group.Then calling the undo/redo endpoint with the same ClientSessionId header, all the actions belonging to the same action group can be undone/redone together in a single API call.
- `view_id` (path) — Rotates the ical feed slug of the calendar view related to the provided id.

---

## GET /api/database/views/table/{table_id}/

****  
*operationId: `list_database_table_views`*

**Параметры:**

- `include` (query) — A comma separated list of extra attributes to include on each view in the response. The supported attributes are `filters`, `sortings`, `decorations`, `group_bys` and `default_row_values`. For example `include=filters,sortings` will add the attributes `filters` and `sortings` to every returned view, containing a list of the views filters and sortings respectively.
- `limit` (query) — The maximum amount of views that must be returned. This endpoint doesn't support pagination, but if you for example just need to fetch the first view, you can do that by setting a limit. There isn't a limit by default.
- `table_id` (path) — Returns only views of the table related to the provided value.
- `type` (query) — Optionally filter on the view type. If provided, only views of that type will be returned.

---

## POST /api/database/views/table/{table_id}/

****  
*operationId: `create_database_table_view`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `ClientUndoRedoActionGroupId` (header) — An optional header that marks the action performed by this request as having occurred in a particular action group.Then calling the undo/redo endpoint with the same ClientSessionId header, all the actions belonging to the same action group can be undone/redone together in a single API call.
- `include` (query) — A comma separated list of extra attributes to include on each view in the response. The supported attributes are `filters`, `sortings` and `decorations`. For example `include=filters,sortings` will add the attributes `filters` and `sortings` to every returned view, containing a list of the views filters and sortings respectively.
- `table_id` (path) — Creates a view for the table related to the provided value.

**Тело запроса:**


---

## POST /api/database/views/table/{table_id}/order/

****  
*operationId: `order_database_table_views`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `ClientUndoRedoActionGroupId` (header) — An optional header that marks the action performed by this request as having occurred in a particular action group.Then calling the undo/redo endpoint with the same ClientSessionId header, all the actions belonging to the same action group can be undone/redone together in a single API call.
- `table_id` (path) — Updates the order of the views in the table related to the provided value.

**Тело запроса:**

- `view_ids`: *array* (обязательно) — View ids in the desired order.

---

## GET /api/database/views/{slug}/link-row-field-lookup/{field_id}/

****  
*operationId: `database_table_public_view_link_row_field_lookup`*

**Параметры:**

- `field_id` (path) — The field id of the link row field.
- `search` (query) — If provided only rows with data that matches the search query are going to be returned.
- `search_mode` (query) — If provided, allows API consumers to determine what kind of search experience they wish to have. If the default `SearchMode.FT_WITH_COUNT` is used, then Postgres full-text search is used. If `SearchMode.COMPAT` is provided then the search term will be exactly searched for including whitespace on each cell. This is the Baserow legacy search behaviour.
- `slug` (path) — The slug related to the view.

---

## POST /api/database/views/{slug}/public/auth/

****  
*operationId: `public_view_token_auth`*

**Параметры:**

- `slug` (path) — The slug of the grid view to get public information about.

**Тело запроса:**

- `password`: *string* (обязательно) — 

---

## GET /api/database/views/{slug}/public/info/

****  
*operationId: `get_public_view_info`*

**Параметры:**

- `slug` (path) — The slug of the view to get public information about.

---

## GET /api/database/views/{slug}/row/{row_id}/

****  
*operationId: `get_public_view_row`*

**Параметры:**

- `row_id` (path) — The ID of the row to retrieve from the public view.
- `slug` (path) — The slug of the view from which to get the row data.

---

## GET /api/database/views/{view_id}/

****  
*operationId: `get_database_table_view`*

**Параметры:**

- `include` (query) — A comma separated list of extra attributes to include on the returned view. The supported attributes are `filters`, `sortings` and `decorations`. For example `include=filters,sortings` will add the attributes `filters` and `sortings` to every returned view, containing a list of the views filters and sortings respectively.
- `view_id` (path) — Returns the view related to the provided value.

---

## PATCH /api/database/views/{view_id}/

****  
*operationId: `update_database_table_view`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `ClientUndoRedoActionGroupId` (header) — An optional header that marks the action performed by this request as having occurred in a particular action group.Then calling the undo/redo endpoint with the same ClientSessionId header, all the actions belonging to the same action group can be undone/redone together in a single API call.
- `include` (query) — A comma separated list of extra attributes to include on the returned view. The supported attributes are `filters`, `sortings` and `decorations`. For example `include=filters,sortings` will add the attributes `filters` and `sortings` to every returned view, containing a list of the views filters and sortings respectively.
- `view_id` (path) — Updates the view related to the provided value.

**Тело запроса:**


---

## DELETE /api/database/views/{view_id}/

****  
*operationId: `delete_database_table_view`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `ClientUndoRedoActionGroupId` (header) — An optional header that marks the action performed by this request as having occurred in a particular action group.Then calling the undo/redo endpoint with the same ClientSessionId header, all the actions belonging to the same action group can be undone/redone together in a single API call.
- `view_id` (path) — Deletes the view related to the provided value.

---

## PATCH /api/database/views/{view_id}/default-values/

****  
*operationId: `update_view_default_values`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `view_id` (path) — Updates the default row values for the view with the given id.

---

## POST /api/database/views/{view_id}/duplicate/

****  
*operationId: `duplicate_database_table_view`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `ClientUndoRedoActionGroupId` (header) — An optional header that marks the action performed by this request as having occurred in a particular action group.Then calling the undo/redo endpoint with the same ClientSessionId header, all the actions belonging to the same action group can be undone/redone together in a single API call.
- `view_id` (path) — Duplicates the view related to the provided value.

---

## GET /api/database/views/{view_id}/field-options/

****  
*operationId: `get_database_table_view_field_options`*

**Параметры:**

- `view_id` (path) — Responds with field options related to the provided value.

---

## PATCH /api/database/views/{view_id}/field-options/

****  
*operationId: `update_database_table_view_field_options`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `ClientUndoRedoActionGroupId` (header) — An optional header that marks the action performed by this request as having occurred in a particular action group.Then calling the undo/redo endpoint with the same ClientSessionId header, all the actions belonging to the same action group can be undone/redone together in a single API call.
- `view_id` (path) — Updates the field options related to the provided value.

**Тело запроса:**


---

## POST /api/database/views/{view_id}/rotate-slug/

****  
*operationId: `rotate_database_view_slug`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `ClientUndoRedoActionGroupId` (header) — An optional header that marks the action performed by this request as having occurred in a particular action group.Then calling the undo/redo endpoint with the same ClientSessionId header, all the actions belonging to the same action group can be undone/redone together in a single API call.
- `view_id` (path) — Rotates the slug of the view related to the provided value.

---
