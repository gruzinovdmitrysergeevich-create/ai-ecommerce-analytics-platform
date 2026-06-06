# Executions API

## GET /executions
Получить список выполнений.

**Параметры:**
| Имя | Тип | Описание |
|-----|-----|----------|
| `status` | string | Статус: `success`, `error`, `running` и др. |
| `workflowId` | string | ID workflow |
| `projectId` | string | ID проекта |
| `includeData` | boolean | Включить полные данные |
| `limit` | number | Лимит |
| `cursor` | string | Курсор |

**Пример:**
```bash
curl -X GET "$N8N_BASE_URL/executions?status=success&limit=50" \
  -H "X-N8N-API-KEY: $N8N_API_KEY"
GET /executions/{id}
Получить выполнение по ID. Можно добавить ?includeData=true.

DELETE /executions/{id}
Удалить выполнение.

POST /executions/{id}/retry
Повторить выполнение.

POST /executions/{id}/stop
Остановить выполнение.

POST /executions/stop
Остановить несколько выполнений по фильтру (статусы queued, running, waiting).

GET /executions/{id}/tags
Получить теги выполнения.

PUT /executions/{id}/tags
Обновить теги выполнения.

Технические параметры
pagination_type: cursor

max_depth_days: null

batch_size: 250

is_async: false

rate_limit_per_sec: null
