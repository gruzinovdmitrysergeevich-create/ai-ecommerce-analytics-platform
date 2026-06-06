#!/usr/bin/env python3
"""
MCP-сервер Baserow API
Транспорт: stdio
Использует: mcp (fastmcp), baserow_api
"""

import sys
import logging
import json
from pathlib import Path
from typing import Optional

# Добавляем путь к baserow_api
sys.path.insert(0, str(Path(__file__).parent))

# Импортируем API функции
from baserow_api import (
    refresh_jwt,
    list_workspaces,
    create_workspace,
    delete_workspace,
    create_database,
    list_databases,
    create_table,
    list_tables,
    delete_table,
    create_field,
    list_fields,
    insert_row,
    get_rows,
    update_row,
    delete_row,
    logger as api_logger
)

# Настройка логирования в logs/mcp.log
LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "mcp.log"

# Добавляем FileHandler к logger из baserow_api
file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
file_handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s"))
api_logger.addHandler(file_handler)

logger = logging.getLogger("baserow_mcp")


# === MCP Server ===

import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import Tool
from mcp.types import TextContent

app = Server("baserow")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """Список доступных инструментов MCP."""
    return [
        Tool(
            name="list_workspaces",
            description="Получить список всех workspace",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="create_workspace",
            description="Создать новый workspace",
            inputSchema={
                "type": "object",
                "properties": {"name": {"type": "string", "description": "Имя workspace"}},
                "required": ["name"]
            }
        ),
        Tool(
            name="delete_workspace",
            description="Удалить workspace (каскадно)",
            inputSchema={
                "type": "object",
                "properties": {"workspace_id": {"type": "integer", "description": "ID workspace"}},
                "required": ["workspace_id"]
            }
        ),
        Tool(
            name="create_database",
            description="Создать базу данных в workspace",
            inputSchema={
                "type": "object",
                "properties": {
                    "workspace_id": {"type": "integer", "description": "ID workspace"},
                    "name": {"type": "string", "description": "Имя базы данных"}
                },
                "required": ["workspace_id", "name"]
            }
        ),
        Tool(
            name="list_databases",
            description="Получить список баз данных в workspace",
            inputSchema={
                "type": "object",
                "properties": {"workspace_id": {"type": "integer", "description": "ID workspace"}},
                "required": ["workspace_id"]
            }
        ),
        Tool(
            name="create_table",
            description="Создать таблицу в базе данных",
            inputSchema={
                "type": "object",
                "properties": {
                    "database_id": {"type": "integer", "description": "ID базы данных"},
                    "name": {"type": "string", "description": "Имя таблицы"},
                    "fields": {
                        "type": "array",
                        "description": "Массив определений полей",
                        "items": {"type": "object"}
                    }
                },
                "required": ["database_id", "name"]
            }
        ),
        Tool(
            name="list_tables",
            description="Получить список таблиц в базе данных",
            inputSchema={
                "type": "object",
                "properties": {"database_id": {"type": "integer", "description": "ID базы данных"}},
                "required": ["database_id"]
            }
        ),
        Tool(
            name="delete_table",
            description="Удалить таблицу",
            inputSchema={
                "type": "object",
                "properties": {"table_id": {"type": "integer", "description": "ID таблицы"}},
                "required": ["table_id"]
            }
        ),
        Tool(
            name="create_field",
            description="Создать поле в таблице",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_id": {"type": "integer", "description": "ID таблицы"},
                    "name": {"type": "string", "description": "Имя поля"},
                    "field_type": {"type": "string", "description": "Тип поля (text, number, boolean, date, etc.)"},
                    "options": {"type": "object", "description": "Доп. параметры поля"}
                },
                "required": ["table_id", "name", "field_type"]
            }
        ),
        Tool(
            name="list_fields",
            description="Получить список полей таблицы",
            inputSchema={
                "type": "object",
                "properties": {"table_id": {"type": "integer", "description": "ID таблицы"}},
                "required": ["table_id"]
            }
        ),
        Tool(
            name="insert_row",
            description="Вставить строку в таблицу",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_id": {"type": "integer", "description": "ID таблицы"},
                    "data": {"type": "object", "description": "Данные строки {поле: значение}"}
                },
                "required": ["table_id", "data"]
            }
        ),
        Tool(
            name="get_rows",
            description="Получить строки таблицы",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_id": {"type": "integer", "description": "ID таблицы"},
                    "page": {"type": "integer", "description": "Номер страницы", "default": 1},
                    "size": {"type": "integer", "description": "Количество строк (до 100)", "default": 100}
                },
                "required": ["table_id"]
            }
        ),
        Tool(
            name="update_row",
            description="Обновить строку",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_id": {"type": "integer", "description": "ID таблицы"},
                    "row_id": {"type": "integer", "description": "ID строки"},
                    "data": {"type": "object", "description": "Новые данные {поле: значение}"}
                },
                "required": ["table_id", "row_id", "data"]
            }
        ),
        Tool(
            name="delete_row",
            description="Удалить строку",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_id": {"type": "integer", "description": "ID таблицы"},
                    "row_id": {"type": "integer", "description": "ID строки"}
                },
                "required": ["table_id", "row_id"]
            }
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Обработка вызовов инструментов."""
    try:
        if name == "list_workspaces":
            result = list_workspaces()
        elif name == "create_workspace":
            result = create_workspace(arguments["name"])
        elif name == "delete_workspace":
            result = delete_workspace(arguments["workspace_id"])
        elif name == "create_database":
            result = create_database(arguments["workspace_id"], arguments["name"])
        elif name == "list_databases":
            result = list_databases(arguments["workspace_id"])
        elif name == "create_table":
            result = create_table(
                arguments["database_id"],
                arguments["name"],
                arguments.get("fields")
            )
        elif name == "list_tables":
            result = list_tables(arguments["database_id"])
        elif name == "delete_table":
            result = delete_table(arguments["table_id"])
        elif name == "create_field":
            result = create_field(
                arguments["table_id"],
                arguments["name"],
                arguments.get("field_type", "text"),
                **(arguments.get("options") or {})
            )
        elif name == "list_fields":
            result = list_fields(arguments["table_id"])
        elif name == "insert_row":
            result = insert_row(arguments["table_id"], arguments["data"])
        elif name == "get_rows":
            result = get_rows(
                arguments["table_id"],
                page=arguments.get("page", 1),
                size=arguments.get("size", 100)
            )
        elif name == "update_row":
            result = update_row(
                arguments["table_id"],
                arguments["row_id"],
                arguments["data"]
            )
        elif name == "delete_row":
            result = delete_row(arguments["table_id"], arguments["row_id"])
        else:
            result = {"error": f"Unknown tool: {name}"}
        
        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    except Exception as e:
        logger.error(f"Ошибка выполнения {name}: {e}")
        return [TextContent(type="text", text=json.dumps({"error": str(e)}, ensure_ascii=False))]


def main():
    """Точка входа - stdio транспорт."""
    from baserow_api import BASEROW_URL, BASEROW_EMAIL, BASEROW_PASSWORD, ENV_PATH
    
    logger.info("=" * 50)
    logger.info("MCP Baserow Server starting...")
    logger.info(f"BASEROW_URL: {BASEROW_URL}")
    logger.info(f"ENV path: {ENV_PATH}")
    logger.info(f"Log file: {LOG_FILE}")
    logger.info("=" * 50)
    
    # Инициализация JWT при старте
    if BASEROW_EMAIL and BASEROW_PASSWORD:
        refresh_jwt()
    else:
        logger.warning("BASEROW_EMAIL или BASEROW_PASSWORD не заданы в .env")
    
    # Запуск сервера stdio
    async def run_server():
        async with stdio_server() as (read, write):
            await app.run(read, write, app.create_initialization_options())
    
    asyncio.run(run_server())


if __name__ == "__main__":
    main()
