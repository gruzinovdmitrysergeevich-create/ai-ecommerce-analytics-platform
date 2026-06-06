# Database tokens

## GET /api/database/tokens/

****  
*operationId: `list_database_tokens`*


---

## POST /api/database/tokens/

****  
*operationId: `create_database_token`*


**Тело запроса:**

- `name`: *string* (обязательно) — The human readable name of the database token for the user.
- `workspace`: *integer* (обязательно) — Only the tables of the workspace can be accessed.

---

## GET /api/database/tokens/check/

****  
*operationId: `check_database_token`*


---

## GET /api/database/tokens/{token_id}/

****  
*operationId: `get_database_token`*

**Параметры:**

- `token_id` (path) — Returns the database token related to the provided value.

---

## PATCH /api/database/tokens/{token_id}/

****  
*operationId: `update_database_token`*

**Параметры:**

- `token_id` (path) — Updates the database token related to the provided value.

**Тело запроса:**

- `name`: *string* — The human readable name of the database token for the user.
- `permissions`: *object* — Indicates per operation which permissions the database token has within the whole workspace. If the value of for example `create` is `true`, then the token can create rows in all tables related to the workspace. If a list is provided with for example `[["table", 1]]` then the token only has create permissions for the table with id 1. Same goes for if a database references is provided. `[['database', 1]]` means create permissions for all tables in the database with id 1.

Example:
```json
{
  "create": true// Allows creating rows in all tables.
  // Allows reading rows from database 1 and table 10.
  "read": [["database", 1], ["table", 10]],
  "update": false  // Denies updating rows in all tables.
  "delete": []  // Denies deleting rows in all tables.
 }
```
- `rotate_key`: *boolean* — Indicates if a new key must be generated.

---

## DELETE /api/database/tokens/{token_id}/

****  
*operationId: `delete_database_token`*

**Параметры:**

- `token_id` (path) — Deletes the database token related to the provided value.

---
