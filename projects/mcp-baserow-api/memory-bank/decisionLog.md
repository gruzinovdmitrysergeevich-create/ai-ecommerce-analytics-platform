# Decision Log

## 2026-04-08 — Исправление URL в baserow_api.py
**Проблема:** URL формировался как `http://localhost:8000/apiworkspaces/` (без слеша между api и workspaces).
**Причина:** `API_BASE = f"{BASEROW_URL}/api"` (без trailing slash), затем `url = f"{API_BASE}{path.lstrip('/')}"` — слеш терялся.
**Решение:** Изменено на `url = f"{API_BASE}/{path.lstrip('/')}"` — явный слеш перед path.
**Результат:** Все интеграционные тесты пройдены успешно.

## 2026-04-08 — Установка зависимостей в venv
**Проблема:** В venv аналитики не было httpx и mcp.
**Решение:** `pip install httpx mcp python-dotenv`
**Результат:** Зависимости установлены, тесты работают.

## 2026-04-08 — Добавление baserow-api MCP в глобальные правила
**Решение:** Обновлён файл `~/.roo/rules/02-mcp-usage.md` с описанием нового MCP-сервера.
