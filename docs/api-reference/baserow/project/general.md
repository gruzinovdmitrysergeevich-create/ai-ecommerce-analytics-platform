# Baserow — общие сведения

## Базовый URL
- Локально: `http://localhost:8000/api/`
- Внутри Docker: `http://baserow:80/api/`

## Аутентификация
- **JWT**: `POST /api/user/token-auth/` (логин/пароль)
- **Database token**: `POST /api/database/tokens/`

## Общие параметры
- `?user_field_names=true` — обязательно для работы с именами полей
- Пагинация: `?limit=100&offset=200`
- Формат дат: ISO 8601

## Переменные окружения
BASEROW_URL=http://baserow:80
BASEROW_EMAIL=gruzinov.dmitry.sergeevich@gmail.com
BASEROW_PASSWORD=1I9N59!_09&
BASEROW_TOKEN=S79owXt1Q4XlvhGW8q825aOntwVI0wiE

text
