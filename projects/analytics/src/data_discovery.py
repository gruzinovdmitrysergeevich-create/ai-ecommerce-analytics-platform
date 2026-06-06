#!/usr/bin/env python3
"""
data_discovery.py — авто-обнаружение таблиц Baserow и их схем.

Использование:
    from data_discovery import DataDiscovery
    dd = DataDiscovery()
    tables = dd.list_tables()           # все таблицы всех воркспейсов
    schema = dd.get_schema("wb_aggregated")  # колонки таблицы
    sample = dd.get_sample("wb_aggregated", 5)  # первые 5 строк
"""

import requests
import yaml
from pathlib import Path
from typing import Optional

CONFIG_PATH = Path(__file__).parent.parent / "config.yaml"


class DataDiscovery:
    """Обнаружение и чтение данных из Baserow."""

    def __init__(self, config_path: str = None):
        cfg_path = config_path or CONFIG_PATH
        with open(cfg_path) as f:
            self.config = yaml.safe_load(f)
        self._url = self.config["baserow"]["url"]
        self._jwt = None
        self._cache_tables = None  # кэш списка таблиц
        self._cache_schemas = {}  # кэш схем таблиц

    # ====== Авторизация ======

    def _get_jwt(self) -> str:
        if self._jwt:
            return self._jwt
        r = requests.post(
            f"{self._url}/api/user/token-auth/",
            json={
                "username": self.config["baserow"]["email"],
                "password": self.config["baserow"]["password"],
            },
            timeout=10,
        )
        r.raise_for_status()
        self._jwt = r.json().get("access_token") or r.json().get("token")
        return self._jwt

    @property
    def _headers(self):
        return {"Authorization": f"JWT {self._get_jwt()}"}

    # ====== Воркспейсы ======

    def list_workspaces(self) -> list[dict]:
        """Список всех воркспейсов (databases)."""
        r = requests.get(f"{self._url}/api/applications/", headers=self._headers, timeout=10)
        r.raise_for_status()
        return [{"id": a["id"], "name": a["name"]} for a in r.json() if a.get("type") == "database"]

    # ====== Таблицы ======

    def list_tables(self, refresh: bool = False) -> list[dict]:
        """Список ВСЕХ таблиц во всех воркспейсах.
        Возвращает: [{workspace_id, workspace_name, table_id, table_name}, ...]
        """
        if self._cache_tables is not None and not refresh:
            return self._cache_tables

        tables = []
        for ws in self.list_workspaces():
            r = requests.get(
                f"{self._url}/api/database/tables/database/{ws['id']}/",
                headers=self._headers,
                timeout=10,
            )
            if r.status_code == 200:
                for t in r.json():
                    tables.append({
                        "workspace_id": ws["id"],
                        "workspace_name": ws["name"],
                        "table_id": t["id"],
                        "table_name": t["name"],
                    })

        self._cache_tables = tables
        return tables

    def find_table(self, name: str) -> Optional[dict]:
        """Найти таблицу по имени (частичное совпадение)."""
        for t in self.list_tables():
            if name.lower() in t["table_name"].lower():
                return t
        return None

    # ====== Схема ======

    def get_schema(self, table_identifier, refresh: bool = False) -> list[dict]:
        """Колонки таблицы. table_identifier: имя таблицы или ID.
        Возвращает: [{name, type, ...}, ...]
        """
        table = self._resolve_table(table_identifier)
        if not table:
            return []

        tid = table["table_id"]
        if tid in self._cache_schemas and not refresh:
            return self._cache_schemas[tid]

        r = requests.get(
            f"{self._url}/api/database/fields/table/{tid}/",
            headers=self._headers,
            timeout=10,
        )
        if r.status_code != 200:
            return []

        schema = [{"name": f["name"], "type": f["type"]} for f in r.json()]
        self._cache_schemas[tid] = schema
        return schema

    def get_column_names(self, table_identifier) -> list[str]:
        """Только имена колонок."""
        return [f["name"] for f in self.get_schema(table_identifier)]

    # ====== Данные ======

    def get_sample(self, table_identifier, size: int = 5) -> list[dict]:
        """Первые N строк таблицы."""
        table = self._resolve_table(table_identifier)
        if not table:
            return []
        r = requests.get(
            f"{self._url}/api/database/rows/table/{table['table_id']}/",
            headers=self._headers,
            params={"size": size, "user_field_names": "true"},
            timeout=15,
        )
        if r.status_code != 200:
            return []
        return r.json().get("results", [])

    def get_all_rows(self, table_identifier, max_rows: int = 10000) -> list[dict]:
        """Все строки таблицы (с пагинацией)."""
        table = self._resolve_table(table_identifier)
        if not table:
            return []
        rows = []
        page = 1
        while len(rows) < max_rows:
            r = requests.get(
                f"{self._url}/api/database/rows/table/{table['table_id']}/",
                headers=self._headers,
                params={"page": page, "size": 200, "user_field_names": "true"},
                timeout=30,
            )
            if r.status_code != 200:
                break
            data = r.json()
            rows.extend(data["results"])
            if not data.get("next"):
                break
            page += 1
        return rows

    def get_row_count(self, table_identifier) -> int:
        """Количество строк в таблице."""
        table = self._resolve_table(table_identifier)
        if not table:
            return 0
        r = requests.get(
            f"{self._url}/api/database/rows/table/{table['table_id']}/",
            headers=self._headers,
            params={"size": 1, "count": ""},
            timeout=10,
        )
        # Baserow может вернуть count в ответе или заголовках
        try:
            return r.json().get("count", 0)
        except:
            return 0

    # ====== Вспомогательное ======

    def _resolve_table(self, identifier) -> Optional[dict]:
        """Разрешает имя таблицы или ID в полную запись."""
        if isinstance(identifier, int):
            for t in self.list_tables():
                if t["table_id"] == identifier:
                    return t
        else:
            return self.find_table(str(identifier))
        return None

    def build_context(self, table_name: str) -> dict:
        """Строит контекст для промпта: схема + пример + число строк."""
        table = self.find_table(table_name)
        if not table:
            return {"error": f"Таблица '{table_name}' не найдена"}

        schema = self.get_schema(table["table_id"])
        sample = self.get_sample(table["table_id"], 3)
        count = self.get_row_count(table["table_id"])

        return {
            "table_name": table["table_name"],
            "workspace": table["workspace_name"],
            "table_id": table["table_id"],
            "row_count": count,
            "columns": schema,
            "sample_rows": sample,
        }


if __name__ == "__main__":
    dd = DataDiscovery()
    print("=== Воркспейсы ===")
    for ws in dd.list_workspaces():
        print(f"  [{ws['id']}] {ws['name']}")
    print(f"\n=== Таблицы ({len(dd.list_tables())} шт) ===")
    for t in dd.list_tables():
        print(f"  [{t['table_id']}] {t['workspace_name']} / {t['table_name']}")
