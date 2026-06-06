# Discover API

## GET /discover
Возвращает список доступных эндпоинтов и операций для текущего API-ключа (с учётом scopes).

**Параметры:**
- `include` – `schemas` (включить схемы запросов)
- `resource` – фильтр по ресурсу (например, `workflow`)
- `operation` – фильтр по операции (`read`, `create`, `list`)

**Ответ:** объект с `resources`, `scopes`, `filters`, `specUrl`.

## Технические параметры
- `pagination_type`: `none`
- `max_depth_days`: `null`
- `batch_size`: `null`
- `is_async`: `false`
- `rate_limit_per_sec`: `null`
