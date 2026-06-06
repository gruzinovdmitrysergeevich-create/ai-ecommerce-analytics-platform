# Variables API

Управление глобальными и проектными переменными.

## POST /variables
Создать переменную.

**Тело:**
```json
{
  "key": "MY_VAR",
  "value": "secret_value",
  "projectId": "optional"
}
GET /variables
Получить список переменных (с пагинацией, можно фильтровать по projectId).

DELETE /variables/{id}
Удалить переменную.

PUT /variables/{id}
Обновить переменную.

Технические параметры
pagination_type: cursor

max_depth_days: null

batch_size: 250

is_async: false

rate_limit_per_sec: null
