# Database table webhooks

## GET /api/database/webhooks/table/{table_id}/

****  
*operationId: `list_database_table_webhooks`*

**Параметры:**

- `table_id` (path) — Returns only webhooks of the table related to this value.

---

## POST /api/database/webhooks/table/{table_id}/

****  
*operationId: `create_database_table_webhook`*

**Параметры:**

- `table_id` (path) — Creates a webhook for the table related to the provided value.

**Тело запроса:**

- `url`: *string* (обязательно) — The URL that must be called when the webhook is triggered.
- `include_all_events`: *boolean* — Indicates whether this webhook should listen to all events.
- `events`: *array* — A list containing the events that will trigger this webhook.
- `event_config`: *array* — A list containing the addition event options.
- `request_method`: ** — The request method that be used when the event occurs.

* `POST` - Post
* `GET` - Get
* `PUT` - Put
* `PATCH` - Patch
* `DELETE` - Delete
- `headers`: *object* — The additional headers as an object where the key is the name and the value the value.
- `name`: *string* (обязательно) — An internal name of the webhook.
- `use_user_field_names`: *boolean* — Indicates whether the field names must be used as payload key instead of the id.

---

## POST /api/database/webhooks/table/{table_id}/test-call/

****  
*operationId: `test_call_database_table_webhook`*

**Параметры:**

- `table_id` (path) — The id of the table that must be tested.

**Тело запроса:**

- `url`: *string* (обязательно) — The URL that must be called when the webhook is triggered.
- `event_type`: ** (обязательно) — The event type that must be used for the test call.

* `rows.created` - rows.created
* `rows.updated` - rows.updated
* `rows.deleted` - rows.deleted
* `field.created` - field.created
* `field.updated` - field.updated
* `field.deleted` - field.deleted
* `view.created` - view.created
* `view.updated` - view.updated
* `view.deleted` - view.deleted
* `view.rows_entered` - view.rows_entered
- `request_method`: ** — The request method that be used when the event occurs.

* `POST` - Post
* `GET` - Get
* `PUT` - Put
* `PATCH` - Patch
* `DELETE` - Delete
- `headers`: *object* — The additional headers as an object where the key is the name and the value the value.
- `use_user_field_names`: *boolean* — Indicates whether the field names must be used as payload key instead of the id.

---

## GET /api/database/webhooks/{webhook_id}/

****  
*operationId: `get_database_table_webhook`*

**Параметры:**

- `webhook_id` (path) — Returns the webhook related to the provided value.

---

## PATCH /api/database/webhooks/{webhook_id}/

****  
*operationId: `update_database_table_webhook`*

**Параметры:**

- `webhook_id` (path) — Updates the webhook related to the provided value.

**Тело запроса:**

- `url`: *string* — The URL that must be called when the webhook is triggered.
- `include_all_events`: *boolean* — Indicates whether this webhook should listen to all events.
- `events`: *array* — A list containing the events that will trigger this webhook.
- `event_config`: *array* — A list containing the addition event options.
- `request_method`: ** — The request method that be used when the event occurs.

* `POST` - Post
* `GET` - Get
* `PUT` - Put
* `PATCH` - Patch
* `DELETE` - Delete
- `headers`: *object* — The additional headers as an object where the key is the name and the value the value.
- `name`: *string* — An internal name of the webhook.
- `active`: *boolean* — Indicates whether the web hook is active. When a webhook has failed multiple times, it will automatically be deactivated.
- `use_user_field_names`: *boolean* — Indicates whether the field names must be used as payload key instead of the id.

---

## DELETE /api/database/webhooks/{webhook_id}/

****  
*operationId: `delete_database_table_webhook`*

**Параметры:**

- `webhook_id` (path) — Deletes the webhook related to the provided value.

---
