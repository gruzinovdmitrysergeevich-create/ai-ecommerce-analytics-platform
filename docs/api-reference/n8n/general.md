# Общая информация по API n8n

## Базовый URL
Для локальной self-hosted установки:
http://localhost:5678/api/v1

text

Для n8n Cloud:
https://<instance>.app.n8n.cloud/api/v1

text

## Аутентификация
Все запросы требуют API-ключ, передаваемый в заголовке:
X-N8N-API-KEY: <ваш_ключ>

text

### Получение API-ключа
1. Войдите в n8n UI (http://localhost:5678).
2. Перейдите **Settings** → **n8n API**.
3. Нажмите **Create an API Key**, укажите label и срок действия.
4. Скопируйте ключ и сохраните в переменную окружения `N8N_API_KEY`.

## Пагинация
Большинство списочных эндпоинтов поддерживают пагинацию через:
- `limit` – максимальное количество записей на странице (по умолчанию 100, максимум 250).
- `cursor` – курсор для следующей страницы (возвращается в ответе как `nextCursor`).

Пример ответа с курсором:
```json
{
  "data": [...],
  "nextCursor": "MTIzZTQ1NjctZTg5Yi0xMmQzLWE0NTYtNDI2NjE0MTc0MDA"
}
Особенности self-hosted
Порт по умолчанию: 5678.

UI защищён Basic Auth (если настроен N8N_BASIC_AUTH_ACTIVE=true).

Webhook URL: http://localhost:5678/webhook/.

API-ключи создаются локально в UI.

Технические параметры (для мета-таблицы Baserow)
pagination_type: cursor

max_depth_days: null

batch_size: 250 (максимальный limit)

is_async: false

rate_limit_per_sec: null
