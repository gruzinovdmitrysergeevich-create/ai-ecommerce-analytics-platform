# Workflows API

## GET /workflows
Получить список всех workflow.

**Параметры запроса:**
| Имя | Тип | Описание |
|-----|-----|----------|
| `active` | boolean | Фильтр по активности |
| `tags` | string | Список тегов через запятую |
| `name` | string | Имя workflow |
| `projectId` | string | ID проекта |
| `limit` | number | Лимит (макс. 250) |
| `cursor` | string | Курсор пагинации |

**Пример:**
```bash
curl -X GET "$N8N_BASE_URL/workflows?active=true&limit=100" \
  -H "X-N8N-API-KEY: $N8N_API_KEY"
POST /workflows
Создать новый workflow.

Тело запроса (обязательные поля):

json
{
  "name": "My Workflow",
  "nodes": [...],
  "connections": {...},
  "settings": {...}
}
GET /workflows/{id}
Получить workflow по ID.

PUT /workflows/{id}
Обновить workflow (полная замена).

DELETE /workflows/{id}
Удалить workflow.

POST /workflows/{id}/activate
Активировать (опубликовать) workflow.

POST /workflows/{id}/deactivate
Деактивировать workflow.

GET /workflows/{id}/{versionId}
Получить конкретную версию workflow.

GET /workflows/{id}/tags
Получить теги workflow.

PUT /workflows/{id}/tags
Обновить теги workflow.

PUT /workflows/{id}/transfer
Передать workflow в другой проект.

Технические параметры (для мета-таблицы)
pagination_type: cursor

max_depth_days: null

batch_size: 250

is_async: false

rate_limit_per_sec: null
