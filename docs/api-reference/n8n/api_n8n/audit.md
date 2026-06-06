# Audit API

## POST /audit
Сгенерировать отчёт по безопасности инстанса.

**Тело запроса (необязательно):**
```json
{
  "additionalOptions": {
    "daysAbandonedWorkflow": 90,
    "categories": ["credentials", "database", "nodes", "filesystem", "instance"]
  }
}
Ответ: JSON с разделами по категориям рисков.

Технические параметры
pagination_type: none

max_depth_days: null

batch_size: null

is_async: false

rate_limit_per_sec: null
