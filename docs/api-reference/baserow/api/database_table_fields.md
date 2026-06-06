# Database table fields

## POST /api/database/fields/password-authentication/

****  
*operationId: `password_field_authentication`*


**Тело запроса:**

- `field_id`: *integer* (обязательно) — The field where to check the password for.
- `row_id`: *integer* (обязательно) — The row where to check the password for.
- `password`: *string* (обязательно) — The password to check.

---

## GET /api/database/fields/table/{table_id}/

****  
*operationId: `list_database_table_fields`*

**Параметры:**

- `table_id` (path) — Returns only the fields of the table related to the provided value.

---

## POST /api/database/fields/table/{table_id}/

****  
*operationId: `create_database_table_field`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `ClientUndoRedoActionGroupId` (header) — An optional header that marks the action performed by this request as having occurred in a particular action group.Then calling the undo/redo endpoint with the same ClientSessionId header, all the actions belonging to the same action group can be undone/redone together in a single API call.
- `table_id` (path) — Creates a new field for the provided table related to the value.

**Тело запроса:**


---

## POST /api/database/fields/table/{table_id}/change-primary-field/

****  
*operationId: `change_primary_field`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `ClientUndoRedoActionGroupId` (header) — An optional header that marks the action performed by this request as having occurred in a particular action group.Then calling the undo/redo endpoint with the same ClientSessionId header, all the actions belonging to the same action group can be undone/redone together in a single API call.
- `table_id` (path) — The table where to update the primary field in.

**Тело запроса:**

- `new_primary_field_id`: *integer* (обязательно) — The ID of the new primary field.

---

## POST /api/database/fields/table/{table_id}/generate-ai-formula/

****  
*operationId: `generate_formula_with_ai`*

**Параметры:**

- `table_id` (path) — The table to generate the formula for.

**Тело запроса:**

- `ai_type`: *string* (обязательно) — The AI model type that must be used when generating the formula.
- `ai_model`: *string* (обязательно) — The AI model that must be used when generating the formula.
- `ai_temperature`: *number* — Between 0 and 2, adjusts response randomness—lower values yield focused answers, while higher values increase creativity.
- `ai_prompt`: *string* (обязательно) — The human readable input used to generate the formula.

---

## GET /api/database/fields/{field_id}/

****  
*operationId: `get_database_table_field`*

**Параметры:**

- `field_id` (path) — Returns the field related to the provided value.

---

## PATCH /api/database/fields/{field_id}/

****  
*operationId: `update_database_table_field`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `ClientUndoRedoActionGroupId` (header) — An optional header that marks the action performed by this request as having occurred in a particular action group.Then calling the undo/redo endpoint with the same ClientSessionId header, all the actions belonging to the same action group can be undone/redone together in a single API call.
- `field_id` (path) — Updates the field related to the provided value.

**Тело запроса:**


---

## DELETE /api/database/fields/{field_id}/

****  
*operationId: `delete_database_table_field`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `ClientUndoRedoActionGroupId` (header) — An optional header that marks the action performed by this request as having occurred in a particular action group.Then calling the undo/redo endpoint with the same ClientSessionId header, all the actions belonging to the same action group can be undone/redone together in a single API call.
- `field_id` (path) — Deletes the field related to the provided value.

---

## POST /api/database/fields/{field_id}/duplicate/async/

****  
*operationId: `duplicate_table_field`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `ClientUndoRedoActionGroupId` (header) — An optional header that marks the action performed by this request as having occurred in a particular action group.Then calling the undo/redo endpoint with the same ClientSessionId header, all the actions belonging to the same action group can be undone/redone together in a single API call.
- `field_id` (path) — The field to duplicate.

---

## POST /api/database/fields/{field_id}/generate-ai-field-values/

****  
*operationId: `generate_table_ai_field_value`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `ClientUndoRedoActionGroupId` (header) — An optional header that marks the action performed by this request as having occurred in a particular action group.Then calling the undo/redo endpoint with the same ClientSessionId header, all the actions belonging to the same action group can be undone/redone together in a single API call.
- `field_id` (path) — The field to generate the value for.

**Тело запроса:**

- `row_ids`: *array* (обязательно) — The ids of the rows that the values should be generated for.

---

## GET /api/database/fields/{field_id}/unique_row_values/

****  
*operationId: `get_database_field_unique_row_values`*

**Параметры:**

- `field_id` (path) — Returns the values related to the provided field.
- `limit` (query) — Defines how many values should be returned.
- `split_comma_separated` (query) — Indicates whether the original column values must be splitted by comma.

---

## POST /api/database/formula/{table_id}/type/

****  
*operationId: `type_formula_field`*

**Параметры:**

- `table_id` (path) — The table id of the formula field to type.

**Тело запроса:**

- `formula`: *string* (обязательно) — 
- `name`: *string* (обязательно) — 

---
