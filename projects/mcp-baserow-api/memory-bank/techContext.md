# Tech Context

## Инфраструктура
- **Baserow**: Docker-контейнер на ноутбуке, порт 8000, API v1.
- **MCP-сервер**: работает через stdio, запускается командой `python mcp_server_baserow.py`.
- **Песочница**: `~/my-ai-stack/analytics/runner.py` (venv).
- **Модели**: Roo Code (Code режим), Kilo Code.

## Используемые API
- **Baserow API**: эндпоинты:
  - `POST /api/user/token-auth/` – получить JWT (административный).
  - `GET /api/workspaces/` – список workspace.
  - `POST /api/workspaces/` – создать workspace.
  - `POST /api/database/workspace/{workspace_id}/` – создать database.
  - `POST /api/database/tables/database/{database_id}/` – создать таблицу.
  - `GET /api/database/tables/table/{table_id}/` – список полей.
  - `GET /api/database/rows/table/{table_id}/` – чтение строк.
  - `POST /api/database/rows/table/{table_id}/` – вставка строки.
  - `PATCH /api/database/rows/table/{table_id}/{row_id}/` – обновление строки.
  - `DELETE` – удаление workspace, таблицы, строки.

## Технологии
- **Python 3.x** – основной язык.
- **mcp** – библиотека для MCP сервера (fastmcp или официальный SDK).
- **httpx** – HTTP клиент для запросов к Baserow API.
- **python-dotenv** – загрузка переменных окружения из `.env`.

## Токены и переменные
- JWT (административный) – получается через `/api/user/token-auth/` (логин/пароль из `.env`).
- Автоматическое обновление JWT при 401 ошибке.
- Переменные окружения: `BASEROW_URL`, `BASEROW_EMAIL`, `BASEROW_PASSWORD` (хранятся в `~/my-ai-stack/analytics/.env`).

## Структура проекта
- **src/** – исходный код MCP сервера.
- **docs/** – документация Baserow API (уже загружена).
- **tests/** – тесты.
- **logs/** – логи работы сервера.
- **memory-bank/** – контекстные файлы проекта.
- **.roo/rules/** – локальные правила проекта.
