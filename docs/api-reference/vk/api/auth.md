# Авторизация (Client Credentials Grant)

## Получение токена
**POST** `/api/v2/oauth2/token.json`

**Заголовок:** `Content-Type: application/x-www-form-urlencoded`

**Параметры тела:**
- `grant_type=client_credentials`
- `client_id` – из кабинета VK Ads (Настройки → Доступ к API)
- `client_secret` – секретный ключ

**Пример ответа:**
```json
{
  "access_token": "vk1.a.xxx...",
  "token_type": "bearer",
  "expires_in": 86400,
  "refresh_token": "vk1.b.xxx..."
}
expires_in – 24 часа (86400 секунд).

Обновление токена
POST /api/v2/oauth2/token.json

Параметры:

grant_type=refresh_token

refresh_token – из предыдущего ответа

client_id

client_secret

Agency Client Credentials Grant
Для получения токена клиента агентства добавьте параметр:

agency_client_name или agency_client_id

Удаление токенов
POST /api/v2/oauth2/token/delete.json
Параметры: client_id, client_secret, username или user_id.
