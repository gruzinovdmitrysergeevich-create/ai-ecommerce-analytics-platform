# Database tables

## GET /api/data-sync/{data_sync_id}/periodic-interval/

****  
*operationId: `get_periodic_data_sync_interval`*

**Параметры:**

- `data_sync_id` (path) — The data sync where to fetch the periodic settings for.

---

## PATCH /api/data-sync/{data_sync_id}/periodic-interval/

****  
*operationId: `update_periodic_data_sync_interval`*

**Параметры:**

- `data_sync_id` (path) — Updates the data sync related to the provided value.

**Тело запроса:**

- `interval`: ** — 
- `when`: *string* — 
- `automatically_deactivated`: *boolean* — Indicates whether the periodic data sync has been deactivated.

---

## POST /api/database/data-sync/database/{database_id}/

****  
*operationId: `create_database_data_sync_table`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `ClientUndoRedoActionGroupId` (header) — An optional header that marks the action performed by this request as having occurred in a particular action group.Then calling the undo/redo endpoint with the same ClientSessionId header, all the actions belonging to the same action group can be undone/redone together in a single API call.
- `database_id` (path) — Creates a data sync table for the database related to theprovided value.

**Тело запроса:**


---

## POST /api/database/data-sync/properties/

****  
*operationId: `get_table_data_sync_type_properties`*


**Тело запроса:**


---

## GET /api/database/data-sync/{data_sync_id}/

****  
*operationId: `get_table_data_sync`*

**Параметры:**

- `data_sync_id` (path) — The data sync that must be fetched.

---

## PATCH /api/database/data-sync/{data_sync_id}/

****  
*operationId: `update_table_data_sync`*

**Параметры:**

- `data_sync_id` (path) — Updates the data sync related to the provided value.

**Тело запроса:**


---

## GET /api/database/data-sync/{data_sync_id}/properties/

****  
*operationId: `get_table_data_sync_properties`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `data_sync_id` (path) — Lists properties related to the provided ID.

---

## POST /api/database/data-sync/{data_sync_id}/sync/async/

****  
*operationId: `sync_data_sync_table_async`*

**Параметры:**

- `data_sync_id` (path) — Starts a job to sync the data sync table related to the provided value.

---

## GET /api/database/tables/all-tables/

****  
*operationId: `list_all_token_tables`*


---

## GET /api/database/tables/database/{database_id}/

****  
*operationId: `list_database_tables`*

**Параметры:**

- `database_id` (path) — Returns only tables that are related to the provided value.

---

## POST /api/database/tables/database/{database_id}/

****  
*operationId: `create_database_table`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `ClientUndoRedoActionGroupId` (header) — An optional header that marks the action performed by this request as having occurred in a particular action group.Then calling the undo/redo endpoint with the same ClientSessionId header, all the actions belonging to the same action group can be undone/redone together in a single API call.
- `database_id` (path) — Creates a table for the database related to the provided value.

**Тело запроса:**

- `name`: *string* (обязательно) — 
- `data`: *array* — A list of rows that needs to be created as initial table data. Each row is a list of values that are going to be added in the new table in the same order as provided.

Ex: 
```json
[
  ["row1_field1_value", "row1_field2_value"],
  ["row2_field1_value", "row2_field2_value"],
]
```
for creating a two rows table with two fields.

If not provided, some example data is going to be created.
- `first_row_header`: *boolean* — Indicates if the first provided row is the header. If true the field names are going to be the values of the first row. Otherwise they will be called "Field N"

---

## POST /api/database/tables/database/{database_id}/async/

****  
*operationId: `create_database_table_async`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `database_id` (path) — Creates a table for the database related to the provided value.

**Тело запроса:**

- `name`: *string* (обязательно) — 
- `data`: *array* — A list of rows that needs to be created as initial table data. Each row is a list of values that are going to be added in the new table in the same order as provided.

Ex: 
```json
[
  ["row1_field1_value", "row1_field2_value"],
  ["row2_field1_value", "row2_field2_value"],
]
```
for creating a two rows table with two fields.

If not provided, some example data is going to be created.
- `first_row_header`: *boolean* — Indicates if the first provided row is the header. If true the field names are going to be the values of the first row. Otherwise they will be called "Field N"

---

## POST /api/database/tables/database/{database_id}/order/

****  
*operationId: `order_database_tables`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `ClientUndoRedoActionGroupId` (header) — An optional header that marks the action performed by this request as having occurred in a particular action group.Then calling the undo/redo endpoint with the same ClientSessionId header, all the actions belonging to the same action group can be undone/redone together in a single API call.
- `database_id` (path) — Updates the order of the tables in the database related to the provided value.

**Тело запроса:**

- `table_ids`: *array* (обязательно) — Table ids in the desired order.

---

## GET /api/database/tables/{table_id}/

****  
*operationId: `get_database_table`*

**Параметры:**

- `table_id` (path) — Returns the table related to the provided value.

---

## PATCH /api/database/tables/{table_id}/

****  
*operationId: `update_database_table`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `ClientUndoRedoActionGroupId` (header) — An optional header that marks the action performed by this request as having occurred in a particular action group.Then calling the undo/redo endpoint with the same ClientSessionId header, all the actions belonging to the same action group can be undone/redone together in a single API call.
- `table_id` (path) — Updates the table related to the provided value.

**Тело запроса:**

- `name`: *string* — 

---

## DELETE /api/database/tables/{table_id}/

****  
*operationId: `delete_database_table`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `ClientUndoRedoActionGroupId` (header) — An optional header that marks the action performed by this request as having occurred in a particular action group.Then calling the undo/redo endpoint with the same ClientSessionId header, all the actions belonging to the same action group can be undone/redone together in a single API call.
- `table_id` (path) — Deletes the table related to the provided value.

---

## POST /api/database/tables/{table_id}/duplicate/async/

****  
*operationId: `duplicate_database_table_async`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `ClientUndoRedoActionGroupId` (header) — An optional header that marks the action performed by this request as having occurred in a particular action group.Then calling the undo/redo endpoint with the same ClientSessionId header, all the actions belonging to the same action group can be undone/redone together in a single API call.
- `table_id` (path) — The table to duplicate.

---

## POST /api/database/tables/{table_id}/import/async/

****  
*operationId: `import_data_database_table_async`*

**Параметры:**

- `table_id` (path) — Import data into the table related to the provided value.

**Тело запроса:**

- `data`: *array* (обязательно) — A list of rows you want to add to the specified table. Each row is a list of values, one for each **writable** field. The field values must be ordered according to the field order in the table. All values must be compatible with the corresponding field type.

Ex: 
```json
[
  ["row1_field1_value", "row1_field2_value"],
  ["row2_field1_value", "row2_field2_value"],
]
```
for adding two rows to a table with two writable fields.
- `configuration`: ** — 

---
