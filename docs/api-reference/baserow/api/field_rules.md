# Field rules

## GET /api/database/field-rules/{table_id}/

****  
*operationId: `get_field_rules`*

**Параметры:**

- `table_id` (path) — The ID of the table to get field rules.

---

## POST /api/database/field-rules/{table_id}/

****  
*operationId: `create_field_rule`*

**Параметры:**

- `table_id` (path) — The ID of the table to set a field rule.

**Тело запроса:**


---

## GET /api/database/field-rules/{table_id}/invalid-rows/

****  
*operationId: `get_invalid_rows`*

**Параметры:**

- `table_id` (path) — The ID of the table to get a list of invalid row ids.

---

## PUT /api/database/field-rules/{table_id}/rule/{rule_id}/

****  
*operationId: `update_field_rule`*

**Параметры:**

- `rule_id` (path) — The ID of the rule to update.
- `table_id` (path) — The ID of the table.

**Тело запроса:**


---

## DELETE /api/database/field-rules/{table_id}/rule/{rule_id}/

****  
*operationId: `delete_field_rule`*

**Параметры:**

- `rule_id` (path) — The ID of the rule to delete.
- `table_id` (path) — The ID of the table.

---
