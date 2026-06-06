# Tags API

## POST /tags
Создать тег.

**Тело:**
```json
{ "name": "production" }
GET /tags
Получить список тегов.

GET /tags/{id}
Получить тег по ID.

DELETE /tags/{id}
Удалить тег.

PUT /tags/{id}
Обновить тег.

Технические параметры
pagination_type: cursor

max_depth_days: null

batch_size: 250

is_async: false

rate_limit_per_sec: null
