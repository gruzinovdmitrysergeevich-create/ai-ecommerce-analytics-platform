# Users API

Доступно только владельцу инстанса (owner).

## GET /users
Получить список пользователей.

**Параметры:** `limit`, `cursor`, `includeRole`, `projectId`.

## POST /users
Создать одного или нескольких пользователей (отправка приглашений).

**Тело:**
```json
[
  { "email": "user@example.com", "role": "global:member" }
]
GET /users/{id}
Получить пользователя по ID или email.

DELETE /users/{id}
Удалить пользователя.

PATCH /users/{id}/role
Изменить глобальную роль пользователя.

Тело:

json
{ "newRoleName": "global:member" }
Технические параметры
pagination_type: cursor

max_depth_days: null

batch_size: 250

is_async: false

rate_limit_per_sec: null
