# Projects API

## POST /projects
Создать проект.

**Тело:**
```json
{ "name": "My Project" }
GET /projects
Получить список проектов.

DELETE /projects/{projectId}
Удалить проект.

PUT /projects/{projectId}
Обновить проект.

GET /projects/{projectId}/users
Получить участников проекта.

POST /projects/{projectId}/users
Добавить пользователей в проект.

Тело:

json
{
  "relations": [
    { "userId": "xxx", "role": "project:viewer" }
  ]
}
DELETE /projects/{projectId}/users/{userId}
Удалить пользователя из проекта.

PATCH /projects/{projectId}/users/{userId}
Изменить роль пользователя в проекте.

Технические параметры
pagination_type: cursor

max_depth_days: null

batch_size: 250

is_async: false

rate_limit_per_sec: null
