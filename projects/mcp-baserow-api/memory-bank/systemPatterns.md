# System Patterns

## Архитектура MCP сервера
- **Транспорт**: stdio (стандартный MCP протокол).
- **Библиотека**: `mcp` (официальный SDK или fastmcp) + `httpx` для HTTP запросов.
- **Аутентификация**: JWT через `POST /api/user/token-auth/`, автоматическое обновление при 401.

## Паттерны кода
- **Модульность**: каждый инструмент MCP – отдельная функция с чёткой сигнатурой.
- **Обработка ошибок**: try/except для всех API вызовов, логирование в `logs/mcp.log`.
- **Комментарии на русском**: каждый блок кода комментируется кратко.

## Инструменты MCP
- **Read**: `list_workspaces`, `list_databases`, `list_tables`, `list_fields`, `get_rows`.
- **Create**: `create_workspace`, `create_database`, `create_table`, `create_field`, `insert_row`.
- **Update**: `update_row`, `update_field`.
- **Delete**: `delete_workspace`, `delete_table`, `delete_row`.

## Безопасность
- MCP сервер не меняет Docker Compose и системные настройки.
- Все операции через официальное Baserow API.
- Секреты хранятся в `.env`, не в коде.
- Логирование всех действий для аудита.

## Интеграция с агентами
- Roo Code / Kilo Code подключают сервер через MCP Servers интерфейс.
- Команда запуска: `python mcp_server_baserow.py`.
- OpenCode (терминальный агент) не использует этот MCP напрямую.
