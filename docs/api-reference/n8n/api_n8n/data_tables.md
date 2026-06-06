# Data Tables API

API для работы с таблицами данных (аналог простой БД).

## GET /data-tables
Получить список таблиц.

## POST /data-tables
Создать таблицу.

**Тело:**
```json
{
  "name": "customers",
  "columns": [
    { "name": "email", "type": "string" },
    { "name": "age", "type": "number" }
  ]
}
GET /data-tables/{dataTableId}
Получить таблицу по ID.

PATCH /data-tables/{dataTableId}
Обновить имя таблицы.

DELETE /data-tables/{dataTableId}
Удалить таблицу.

GET /data-tables/{dataTableId}/rows
Получить строки таблицы (с фильтрацией и пагинацией).

POST /data-tables/{dataTableId}/rows
Вставить строки.

PATCH /data-tables/{dataTableId}/rows/update
Обновить строки по фильтру.

POST /data-tables/{dataTableId}/rows/upsert
Вставить или обновить строку.

DELETE /data-tables/{dataTableId}/rows/delete
Удалить строки по фильтру.

Технические параметры
pagination_type: cursor

max_depth_days: null

batch_size: 250 (limit)

is_async: false

rate_limit_per_sec: null
