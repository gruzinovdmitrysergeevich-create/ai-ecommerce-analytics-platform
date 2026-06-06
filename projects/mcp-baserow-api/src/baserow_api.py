#!/usr/bin/env python3
"""
Baserow API клиент
Используется MCP сервером и тестами.
"""

import os
import sys
import logging
from pathlib import Path
from typing import Optional

# Читаем .env из ~/my-ai-stack/analytics/.env
ENV_PATH = Path.home() / "my-ai-stack" / "analytics" / ".env"

def load_env():
    """Загрузка переменных окружения из .env файла."""
    if ENV_PATH.exists():
        with open(ENV_PATH) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ.setdefault(key, value)
    else:
        print(f"WARNING: .env not found at {ENV_PATH}", file=sys.stderr)

# Загружаем .env при импорте
load_env()

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    handlers=[
        logging.StreamHandler(sys.stderr)
    ]
)
logger = logging.getLogger("baserow_api")

# Константы из .env
BASEROW_URL = os.getenv("BASEROW_URL", "http://localhost:8000")
BASEROW_EMAIL = os.getenv("BASEROW_EMAIL", "")
BASEROW_PASSWORD = os.getenv("BASEROW_PASSWORD", "")
API_BASE = f"{BASEROW_URL}/api"

# Глобальный JWT токен
jwt_token: Optional[str] = None


def get_auth_header() -> dict:
    """Возвращает заголовок авторизации."""
    global jwt_token
    if jwt_token:
        return {"Authorization": f"JWT {jwt_token}"}
    return {}


def refresh_jwt() -> bool:
    """Обновляет JWT токен. Возвращает True при успехе."""
    global jwt_token
    logger.info("Обновление JWT токена...")
    
    try:
        import httpx
        with httpx.Client(timeout=30) as client:
            response = client.post(
                f"{API_BASE}/user/token-auth/",
                json={"username": BASEROW_EMAIL, "password": BASEROW_PASSWORD}
            )
            if response.status_code == 200:
                jwt_token = response.json().get("token")
                logger.info("JWT токен получен успешно")
                return True
            else:
                logger.error(f"Ошибка получения JWT: {response.status_code} - {response.text}")
                return False
    except Exception as e:
        logger.error(f"Исключение при получении JWT: {e}")
        return False


def api_request(method: str, path: str, **kwargs) -> dict:
    """
    Выполняет HTTP запрос к Baserow API.
    При 401 пробует обновить JWT и повторить запрос.
    """
    global jwt_token
    url = f"{API_BASE}/{path.lstrip('/')}"
    headers = kwargs.pop("headers", {})
    headers.update(get_auth_header())
    headers.setdefault("Content-Type", "application/json")
    
    try:
        import httpx
        with httpx.Client(timeout=30) as client:
            response = client.request(method, url, headers=headers, **kwargs)
        
        # При 401 пробуем обновить токен
        if response.status_code == 401 and jwt_token:
            logger.warning("Получен 401, пробуем обновить JWT...")
            if refresh_jwt():
                headers["Authorization"] = f"JWT {jwt_token}"
                with httpx.Client(timeout=30) as client:
                    response = client.request(method, url, headers=headers, **kwargs)
        
        if response.status_code >= 400:
            logger.error(f"API ошибка {method} {path}: {response.status_code} - {response.text}")
            return {"error": response.status_code, "detail": response.text}
        
        if response.status_code == 204:
            return {"success": True}
        
        return response.json() if response.content else {}
        
    except Exception as e:
        logger.error(f"Исключение в API запросе {method} {path}: {e}")
        return {"error": "exception", "detail": str(e)}


# === API Functions ===

def list_workspaces() -> list:
    """Получить список всех workspace."""
    logger.info("list_workspaces: запрос списка workspace")
    result = api_request("GET", "/workspaces/")
    if isinstance(result, list):
        return result
    return [result]


def create_workspace(name: str) -> dict:
    """Создать новый workspace."""
    logger.info(f"create_workspace: name={name}")
    return api_request("POST", "/workspaces/", json={"name": name})


def delete_workspace(workspace_id: int) -> dict:
    """Удалить workspace (каскадно)."""
    logger.info(f"delete_workspace: workspace_id={workspace_id}")
    return api_request("DELETE", f"/workspaces/{workspace_id}/")


def create_database(workspace_id: int, name: str) -> dict:
    """Создать базу данных (application) в workspace."""
    logger.info(f"create_database: workspace_id={workspace_id}, name={name}")
    return api_request(
        "POST", 
        f"/applications/workspace/{workspace_id}/",
        json={"name": name, "type": "database"}
    )


def list_databases(workspace_id: int) -> list:
    """Получить список баз данных в workspace."""
    logger.info(f"list_databases: workspace_id={workspace_id}")
    result = api_request("GET", f"/applications/workspace/{workspace_id}/")
    if isinstance(result, list):
        return result
    return [result]


def create_table(database_id: int, name: str, fields: Optional[list] = None) -> dict:
    """
    Создать таблицу в базе данных.
    fields - массив объектов [{'name': 'Name', 'type': 'text'}, ...]
    """
    logger.info(f"create_table: database_id={database_id}, name={name}, fields={fields}")
    
    # Создаём таблицу без данных
    payload = {"name": name}
    result = api_request("POST", f"/database/tables/database/{database_id}/", json=payload)
    
    if "error" in result:
        return result
    
    table_id = result.get("id")
    
    # Добавляем поля по одному (пропуская уже существующие)
    if fields and table_id:
        existing_fields = list_fields(table_id)
        existing_names = {f.get("name") for f in existing_fields if isinstance(f, dict)}
        
        for field_def in fields:
            field_name = field_def.get("name")
            if field_name in existing_names:
                logger.info(f"create_table: поле '{field_name}' уже существует, пропускаем")
                continue
            field_type = field_def.get("type", "text")
            options = {k: v for k, v in field_def.items() if k not in ("name", "type")}
            create_field(table_id, field_name, field_type, **options)
        
        # Перечитываем таблицу с новыми полями
        result = api_request("GET", f"/database/tables/{table_id}/")
    
    return result


def list_tables(database_id: int) -> list:
    """Получить список таблиц в базе данных."""
    logger.info(f"list_tables: database_id={database_id}")
    result = api_request("GET", f"/database/tables/database/{database_id}/")
    if isinstance(result, list):
        return result
    return [result]


def delete_table(table_id: int) -> dict:
    """Удалить таблицу."""
    logger.info(f"delete_table: table_id={table_id}")
    return api_request("DELETE", f"/database/tables/{table_id}/")


def create_field(table_id: int, name: str, field_type: str = "text", **options) -> dict:
    """
    Создать поле в таблице.
    field_type: text, long_text, number, boolean, date, link_row, single_select, etc.
    **options: доп. параметры (number_decimal_places, text_default, etc.)
    """
    logger.info(f"create_field: table_id={table_id}, name={name}, type={field_type}, options={options}")
    
    payload = {"name": name, "type": field_type}
    payload.update(options)
    
    return api_request("POST", f"/database/fields/table/{table_id}/", json=payload)


def list_fields(table_id: int) -> list:
    """Получить список полей таблицы."""
    logger.info(f"list_fields: table_id={table_id}")
    result = api_request("GET", f"/database/fields/table/{table_id}/")
    if isinstance(result, list):
        return result
    return [result]


def insert_row(table_id: int, data: dict, user_field_names: bool = True) -> dict:
    """
    Вставить строку в таблицу.
    data - словарь {поле: значение, ...}
    """
    logger.info(f"insert_row: table_id={table_id}, data={data}")
    
    params = {"user_field_names": "true" if user_field_names else "false"}
    return api_request("POST", f"/database/rows/table/{table_id}/", json=data, params=params)


def get_rows(table_id: int, user_field_names: bool = True, page: int = 1, size: int = 100) -> dict:
    """
    Получить строки таблицы.
    Возвращает {count, results, next, previous}
    """
    logger.info(f"get_rows: table_id={table_id}, page={page}, size={size}")
    
    params = {
        "user_field_names": "true" if user_field_names else "false",
        "page": page,
        "size": min(size, 100)
    }
    return api_request("GET", f"/database/rows/table/{table_id}/", params=params)


def update_row(table_id: int, row_id: int, data: dict, user_field_names: bool = True) -> dict:
    """Обновить строку."""
    logger.info(f"update_row: table_id={table_id}, row_id={row_id}, data={data}")
    
    params = {"user_field_names": "true" if user_field_names else "false"}
    return api_request("PATCH", f"/database/rows/table/{table_id}/{row_id}/", json=data, params=params)


def delete_row(table_id: int, row_id: int) -> dict:
    """Удалить строку."""
    logger.info(f"delete_row: table_id={table_id}, row_id={row_id}")
    return api_request("DELETE", f"/database/rows/table/{table_id}/{row_id}/")
