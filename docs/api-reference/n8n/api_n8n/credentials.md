# Credentials API

## GET /credentials
Получить список учётных данных (без секретов).

**Параметры:** `limit`, `cursor`.

## POST /credentials
Создать новые учётные данные.

**Тело запроса:**
```json
{
  "name": "My Credential",
  "type": "githubApi",
  "data": {
    "accessToken": "token_value"
  }
}
PATCH /credentials/{id}
Обновить существующие учётные данные.

DELETE /credentials/{id}
Удалить учётные данные.

GET /credentials/schema/{credentialTypeName}
Получить схему данных для указанного типа (например, githubApi).

PUT /credentials/{id}/transfer
Передать учётные данные в другой проект.

Технические параметры
pagination_type: cursor

max_depth_days: null

batch_size: 250

is_async: false

rate_limit_per_sec: null
