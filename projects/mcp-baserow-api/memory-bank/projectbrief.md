# Project Brief: MCP-сервер Baserow API

## Цель
Создать MCP-сервер (Model Context Protocol) на Python, который предоставляет агентам (Roo Code, Kilo Code) полный контроль над **self-hosted Baserow** через REST API. Сервер работает без изменений в Docker Compose.

## Функциональные требования

### 1. Просмотр (Read)
- `list_workspaces` – получить список всех workspace
- `list_databases(workspace_id)` – список баз данных в workspace
- `list_tables(database_id)` – список таблиц в базе
- `list_fields(table_id)` – список полей (колонок) таблицы
- `get_rows(table_id, filters=None, limit=100)` – чтение строк

### 2. Создание (Create)
- `create_workspace(name)` – создать workspace
- `create_database(workspace_id, name)` – создать базу данных (application типа database)
- `create_table(database_id, name, fields[])` – создать таблицу с полями (поля: name, type, optional params)
- `create_field(table_id, name, type, options=None)` – добавить поле в существующую таблицу
- `insert_row(table_id, data)` – вставить строку

### 3. Обновление (Update)
- `update_row(table_id, row_id, data)` – обновить строку
- `update_field(table_id, field_id, name=None, options=None)` – изменить поле (опционально)

### 4. Удаление (Delete) – для тестов и очистки
- `delete_workspace(workspace_id)` – удалить workspace (каскадно)
- `delete_table(table_id)` – удалить таблицу
- `delete_row(table_id, row_id)` – удалить строку

## Технические требования

- **Транспорт:** stdio (стандарт MCP)
- **Библиотека:** `mcp` (fastmcp или официальный SDK) + `httpx` для запросов
- **Аутентификация:** 
  - При запуске читает `.env` (путь `~/my-ai-stack/analytics/.env`) – логин, пароль администратора Baserow.
  - Получает JWT через `POST /api/user/token-auth/`.
  - При получении 401 автоматически обновляет JWT.
- **API Base URL:** `http://localhost:8000/api/`
- **Workspace по умолчанию:** не задан, агент сам выбирает или создаёт новый.

## Ограничения безопасности

- MCP-сервер не меняет Docker Compose и не лезет в системные настройки.
- Все изменения в Baserow делаются через официальное API.
- Логирование действий в `logs/mcp.log`.

## Критерии приёмки

1. MCP-сервер запускается командой `python mcp_server_baserow.py` и отвечает на запросы stdio.
2. Агенты (Roo Code, Kilo Code) могут подключить сервер через интерфейс MCP Servers (command + args).
3. Сервер умеет создавать workspace, базу данных, таблицу с полями, вставлять строки, читать их, обновлять, удалять (тестовый цикл).
4. Все операции логируются.
5. OpenCode (терминальный агент) не использует этот MCP, но получает инструкцию по его подключению для Roo/Kilo.

## Переменные окружения (.env)
BASEROW_URL=http://localhost:8000
BASEROW_EMAIL=gruzinov.dmitry.sergeevich@gmail.com
BASEROW_PASSWORD=1I9N59!_09&

## Дополнительно

- Для операций с данными (вставка/чтение/обновление строк) можно использовать тот же JWT (он работает). Database token (`S79owXt...`) не используется в этой версии.
- При создании таблиц обязательно указывать типы полей: `text`, `long_text`, `number`, `date`, `boolean`, `link_row` (если нужно).
