# Baserow API — общие сведения

## Базовый URL
- Локально: `http://localhost:8000/api/`
- Внутри Docker: `http://baserow:80/api/`

## Аутентификация
- **JWT**: `POST /api/user/token-auth/` (логин/пароль)
- **Database token**: `POST /api/database/tokens/` (ограниченный доступ к workspace)

## Общие параметры запросов
- `?user_field_names=true` — обращение к полям по именам (рекомендуется всегда)
- Пагинация: `?limit=100&offset=200`
- Формат дат: ISO 8601 (`YYYY-MM-DDTHH:MM:SSZ`)

## Переменные окружения (.env)
BASEROW_URL=http://baserow:80
BASEROW_EMAIL=your@email.com
BASEROW_PASSWORD=your_password
BASEROW_TOKEN=optional_database_token

text
