#!/usr/bin/env python3
"""
Универсальный агрегатор данных из Baserow.
Читает сырые таблицы, агрегирует по периодам,
создаёт/обновляет компактные таблицы в том же workspace.
"""

import os
import sys
import json
import logging
import re
from datetime import datetime
from collections import defaultdict
from pathlib import Path

import requests

# -----------------------------------------------------------------------------
# Настройки и пути
# -----------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = BASE_DIR / "configs" / "aggregation_rules.json"
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

ENV_PATH = Path.home() / "my-ai-stack" / "analytics" / ".env"
BASEROW_URL = "http://localhost:8000"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / f"run_{datetime.now():%Y%m%d_%H%M%S}.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger("aggregator")


def load_env(path: Path) -> dict:
    """Парсит .env файл и возвращает словарь."""
    env = {}
    if not path.exists():
        logger.error(".env не найден: %s", path)
        return env
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip()
    return env


def get_jwt(env: dict) -> str:
    """Авторизуется в Baserow и возвращает JWT."""
    email = env.get("BASEROW_EMAIL")
    password = env.get("BASEROW_PASSWORD")
    if not email or not password:
        raise RuntimeError("BASEROW_EMAIL или BASEROW_PASSWORD не заданы в .env")
    resp = requests.post(
        f"{BASEROW_URL}/api/user/token-auth/",
        json={"email": email, "password": password},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()["token"]


def api_get(path: str, jwt: str, params: dict = None) -> dict:
    """GET-запрос к Baserow API."""
    headers = {"Authorization": f"JWT {jwt}"}
    resp = requests.get(f"{BASEROW_URL}{path}", headers=headers, params=params, timeout=60)
    resp.raise_for_status()
    return resp.json()


def api_post(path: str, jwt: str, json_data: dict) -> dict:
    """POST-запрос к Baserow API."""
    headers = {"Authorization": f"JWT {jwt}", "Content-Type": "application/json"}
    resp = requests.post(f"{BASEROW_URL}{path}", headers=headers, json=json_data, timeout=60)
    resp.raise_for_status()
    return resp.json()


def api_delete(path: str, jwt: str) -> None:
    """DELETE-запрос к Baserow API."""
    headers = {"Authorization": f"JWT {jwt}"}
    resp = requests.delete(f"{BASEROW_URL}{path}", headers=headers, timeout=60)
    if resp.status_code not in (200, 204):
        logger.warning("DELETE %s вернул %s: %s", path, resp.status_code, resp.text[:200])


# -----------------------------------------------------------------------------
# Работа с Baserow: workspaces, tables, fields, rows
# -----------------------------------------------------------------------------

def get_workspaces(jwt: str) -> dict:
    """workspace_name -> id"""
    data = api_get("/api/applications/", jwt)
    return {item["name"]: item["id"] for item in data if item.get("type") == "database"}


def get_tables(workspace_id: int, jwt: str) -> dict:
    """table_name -> id"""
    data = api_get(f"/api/database/tables/database/{workspace_id}/", jwt)
    return {t["name"]: t["id"] for t in data}


def get_fields(table_id: int, jwt: str) -> dict:
    """field_name -> field_info"""
    data = api_get(f"/api/database/fields/table/{table_id}/", jwt)
    return {f["name"]: f for f in data}


def fetch_all_rows(table_id: int, jwt: str, page_size: int = 200) -> list:
    """Получает ВСЕ строки таблицы постранично."""
    rows = []
    params = {"user_field_names": "true", "size": page_size}
    while True:
        data = api_get(f"/api/database/rows/table/{table_id}/", jwt, params=params)
        batch = data.get("results", [])
        if not batch:
            break
        rows.extend(batch)
        if not data.get("next"):
            break
        # парсим next URL для параметра page
        match = re.search(r"page=(\d+)", data["next"])
        if match:
            params["page"] = int(match.group(1))
        else:
            break
    logger.info("Получено %d строк из таблицы %d", len(rows), table_id)
    return rows


def create_table(workspace_id: int, name: str, jwt: str) -> int:
    """Создаёт таблицу в workspace."""
    data = api_post(f"/api/database/tables/database/{workspace_id}/", jwt, {"name": name})
    logger.info("Создана таблица '%s' (id=%d)", name, data["id"])
    return data["id"]


def create_field(table_id: int, name: str, field_type: str, jwt: str, **kwargs) -> int:
    """Создаёт поле в таблице."""
    payload = {"name": name, "type": field_type}
    payload.update(kwargs)
    headers = {"Authorization": f"JWT {jwt}", "Content-Type": "application/json"}
    resp = requests.post(f"{BASEROW_URL}/api/database/fields/table/{table_id}/", headers=headers, json=payload, timeout=60)
    if resp.status_code == 409:
        logger.warning("Поле '%s' уже существует в таблице %d", name, table_id)
        return None
    resp.raise_for_status()
    data = resp.json()
    logger.info("Создано поле '%s' (type=%s) в таблице %d", name, field_type, table_id)
    return data["id"]


def delete_all_rows(table_id: int, jwt: str) -> None:
    """Удаляет ВСЕ строки из таблицы."""
    rows = fetch_all_rows(table_id, jwt, page_size=100)
    for row in rows:
        api_delete(f"/api/database/rows/table/{table_id}/{row['id']}/", jwt)
    logger.info("Удалено %d строк из таблицы %d", len(rows), table_id)


def create_rows_batch(table_id: int, rows: list, jwt: str, batch_size: int = 50) -> None:
    """Пакетное создание строк. Baserow не поддерживает батч-вставку из коробки,
    поэтому отправляем по одной на запрос с малыми батчами."""
    for i in range(0, len(rows), batch_size):
        batch = rows[i : i + batch_size]
        for row in batch:
            try:
                api_post(f"/api/database/rows/table/{table_id}/?user_field_names=true", jwt, row)
            except requests.exceptions.HTTPError as e:
                logger.error("Ошибка создания строки: %s", e)
                logger.error("Тело запроса: %s", json.dumps(row, ensure_ascii=False))
                raise
        logger.info("Загружено %d/%d строк в таблицу %d", min(i + batch_size, len(rows)), len(rows), table_id)


# -----------------------------------------------------------------------------
# Агрегация
# -----------------------------------------------------------------------------

def normalize_date(value) -> str:
    """Приводит любую дату к YYYY-MM-DD."""
    if value is None:
        return ""
    s = str(value).strip()
    if not s:
        return ""
    # Попытки парсинга разных форматов
    for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%d.%m.%Y", "%d/%m/%Y"):
        try:
            return datetime.strptime(s.split(".")[0] if fmt.startswith("%Y") else s, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    # Если дата в виде ISO с точностью до микросекунд
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00")).strftime("%Y-%m-%d")
    except Exception:
        pass
    # Попытаемся вытащить YYYY-MM-DD из строки регуляркой
    m = re.search(r"(\d{4}-\d{2}-\d{2})", s)
    if m:
        return m.group(1)
    return s


def to_float(value) -> float:
    """Безопасное преобразование в float."""
    if value is None or value == "":
        return 0.0
    try:
        # учитываем русскую запятую
        s = str(value).replace(" ", "").replace("\u00a0", "").replace("\u202f", "")
        if "," in s and "." not in s:
            s = s.replace(",", ".")
        elif "," in s and "." in s:
            # формат типа 1.234,56 → 1234.56
            s = s.replace(".", "").replace(",", ".")
        return float(s)
    except (ValueError, TypeError):
        return 0.0


def aggregate_rows(rows: list, group_by: str, metrics: list) -> dict:
    """
    Агрегирует строки по группе group_by (нормализованная дата).
    Возвращает dict: group_key -> {metric_name: value}.
    """
    groups = defaultdict(lambda: defaultdict(list))
    for row in rows:
        raw_val = row.get(group_by)
        group_key = normalize_date(raw_val)
        if not group_key:
            continue
        for metric in metrics:
            src = metric["source_field"]
            if src == group_by:
                groups[group_key][metric["name"]].append(raw_val)
            elif metric.get("formula"):
                # вычисляемое поле — обрабатывается отдельно
                pass
            else:
                groups[group_key][metric["name"]].append(row.get(src))

    result = {}
    for key, data in groups.items():
        row = {}
        for metric in metrics:
            mname = metric["name"]
            agg = metric["agg"]
            values = data.get(mname, [])
            if agg == "first":
                # для поля date используем нормализованный group_key (дата)
                if metric.get("baserow_type") == "date":
                    row[mname] = key
                else:
                    row[mname] = next((v for v in values if v is not None and str(v).strip() != ""), key)
            elif agg == "sum":
                val = round(sum(to_float(v) for v in values), metric.get("precision", 2))
                if metric.get("precision") == 0:
                    val = int(val)
                row[mname] = val
            elif agg == "count_unique":
                row[mname] = len({v for v in values if v is not None and str(v).strip() not in ("", "None", "null")})
            else:
                row[mname] = None
        result[key] = row
    return result


def apply_computed(rows: dict, metrics: list) -> dict:
    """Применяет формулы к уже агрегированным строкам."""
    for key, row in rows.items():
        for metric in metrics:
            if metric.get("formula"):
                try:
                    # простейшая обработка формул: "a - b"
                    parts = metric["formula"].replace(" ", "").split("-")
                    if len(parts) == 2:
                        a = to_float(row.get(parts[0], 0))
                        b = to_float(row.get(parts[1], 0))
                        row[metric["name"]] = round(a - b, metric.get("precision", 2))
                except Exception:
                    row[metric["name"]] = 0.0
    return rows


# -----------------------------------------------------------------------------
# Основная логика
# -----------------------------------------------------------------------------

def ensure_target_table(workspace_id: int, table_name: str, metrics: list, jwt: str) -> int:
    """
    Находит или создаёт целевую таблицу с нужными полями."""
    tables = get_tables(workspace_id, jwt)
    if table_name in tables:
        table_id = tables[table_name]
        logger.info("Целевая таблица '%s' уже существует (id=%d)", table_name, table_id)
    else:
        table_id = create_table(workspace_id, table_name, jwt)

    existing_fields = get_fields(table_id, jwt)

    for metric in metrics:
        fname = metric["name"]
        ftype = metric.get("baserow_type", "text")
        if fname in existing_fields:
            continue
        kwargs = {}
        if ftype == "number":
            kwargs["number_decimal_places"] = metric.get("precision", 2)
            kwargs["number_negative"] = True
        elif ftype == "date":
            kwargs["date_include_time"] = False
        create_field(table_id, fname, ftype, jwt, **kwargs)

    return table_id


def run_aggregation(rule: dict, workspaces: dict, jwt: str) -> None:
    """Выполняет одно правило агрегации."""
    ws_name = rule["workspace"]
    src_name = rule["source_table"]
    tgt_name = rule["name"]
    group_by = rule["group_by"]
    metrics = rule["metrics"]

    ws_id = workspaces.get(ws_name)
    if not ws_id:
        raise ValueError(f"Workspace '{ws_name}' не найден")

    tables = get_tables(ws_id, jwt)
    src_id = tables.get(src_name)
    if not src_id:
        logger.error("Исходная таблица '%s' не найдена в workspace '%s'", src_name, ws_name)
        return

    logger.info("Начинаем агрегацию '%s' из '%s' по полю '%s'", tgt_name, src_name, group_by)

    # 1. Читаем исходные данные
    rows = fetch_all_rows(src_id, jwt)
    if not rows:
        logger.warning("Исходная таблица '%s' пустая", src_name)
        return

    # 2. Агрегируем
    aggregated = aggregate_rows(rows, group_by, metrics)
    aggregated = apply_computed(aggregated, metrics)

    if not aggregated:
        logger.warning("Нет данных для агрегации '%s'", tgt_name)
        return

    logger.info("Получено %d агрегированных записей", len(aggregated))

    # 3. Создаём/обновляем целевую таблицу
    tgt_id = ensure_target_table(ws_id, tgt_name, metrics, jwt)

    # 4. Очищаем целевую таблицу
    delete_all_rows(tgt_id, jwt)

    # 5. Загружаем новые данные
    payload = []
    for key in sorted(aggregated.keys()):
        row = aggregated[key]
        payload.append(row)

    create_rows_batch(tgt_id, payload, jwt)
    logger.info("Агрегация '%s' завершена. Загружено %d записей.", tgt_name, len(payload))


def main():
    logger.info("Старт aggregator.py")

    # Загружаем .env
    env = load_env(ENV_PATH)
    if not env:
        logger.error("Не удалось загрузить .env из %s", ENV_PATH)
        sys.exit(1)

    # Авторизация
    try:
        jwt = get_jwt(env)
    except Exception as e:
        logger.error("Ошибка авторизации: %s", e)
        sys.exit(1)

    # Загружаем правила
    if not CONFIG_PATH.exists():
        logger.error("Файл правил не найден: %s", CONFIG_PATH)
        sys.exit(1)
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        rules = json.load(f)

    # Получаем workspaces
    workspaces = get_workspaces(jwt)
    logger.info("Найдено workspaces: %s", list(workspaces.keys()))

    # Выполняем каждое правило
    for rule in rules.get("aggregations", []):
        try:
            run_aggregation(rule, workspaces, jwt)
        except Exception as e:
            logger.exception("Ошибка при агрегации '%s': %s", rule.get("name"), e)

    logger.info("Работа aggregator.py завершена")


if __name__ == "__main__":
    main()
