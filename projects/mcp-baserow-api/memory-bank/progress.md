# Progress

## Выполнено
- Создан MCP-сервер `src/mcp_server_baserow.py`
- Реализованы все инструменты: list_workspaces, create_workspace, create_database, list_databases, create_table, list_tables, create_field, list_fields, insert_row, get_rows, update_row, delete_row, delete_table, delete_workspace
- Настроена аутентификация JWT с автообновлением при 401
- Логирование в logs/mcp.log
- Транспорт stdio
- **Шаг 4: Интеграционные тесты пройдены успешно** (2026-04-08)
  - Исправлен баг URL (пропущен слеш в API_BASE)
  - Исправлен `create_table` — Baserow создаёт таблицу с авто-полями, теперь пропускаем дубликаты
  - Установлены зависимости: httpx, mcp
  - Полный цикл: create workspace → db → table → insert row → read → update → delete → cleanup
- **Шаг 5: Глобальные правила обновлены** (02-mcp-usage.md)
- Тестовые данные созданы в Baserow: Workspace `MCP_Test_Real` → DB `MCP_Test_DB` → Table `MCP_Test_Table` с записью "Ivan"

## Библиотеки
- mcp (fastmcp)
- httpx (используется для HTTP запросов)
- python-dotenv
