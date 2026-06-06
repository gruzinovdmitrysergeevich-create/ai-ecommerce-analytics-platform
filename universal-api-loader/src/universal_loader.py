#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Универсальный загрузчик данных из API маркетплейсов в Baserow.
Версия 3.1 – исправленная пагинация, подробное логирование.
"""

import os
import sys
import json
import logging
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from requests.exceptions import ChunkedEncodingError, ConnectionError

import requests
from dotenv import load_dotenv

# ========== 1. НАСТРОЙКА ==========
ENV_PATH = Path("/home/werna81/my-ai-stack/analytics/.env")
load_dotenv(ENV_PATH)

BASEROW_URL = os.getenv("BASEROW_URL", "http://localhost:8000")
BASEROW_EMAIL = os.getenv("BASEROW_EMAIL")
BASEROW_PASSWORD = os.getenv("BASEROW_PASSWORD")

CONFIGS_DIR = Path(__file__).resolve().parent.parent / "configs"
SERVICES = ["wildberries", "ozon"]
WORKSPACE_NAME = "Дмитрий Грузинов"
DATABASES = {"wildberries": "wildberries", "ozon": "ozon"}

LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)
STATUS_LOG = LOG_DIR / "status.md"
STATE_DIR = Path(__file__).resolve().parent.parent / "state"
STATE_DIR.mkdir(exist_ok=True)
LAST_RUN_FILE = STATE_DIR / "last_run.json"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    handlers=[logging.FileHandler(LOG_DIR / "loader.log", encoding="utf-8"), logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

MSK = timezone(timedelta(hours=3))
def now_msk():
    return datetime.now(MSK)

# ========== 2. КЛАСС ДЛЯ КРАСИВОГО ЛОГА (STATUS.MD) ==========
class StatusLogger:
    def __init__(self, log_path: Path):
        self.log_path = log_path
        self.lines: List[str] = []
        self.start_time = now_msk()
        self._write_header()

    def _write_header(self):
        now = self.start_time.strftime("%Y-%m-%d %H:%M:%S MSK")
        self.lines.append(f"# 🚀 ЗАГРУЗЧИК ДАННЫХ | {now}\n")

    def section(self, title: str):
        self.lines.append(f"\n## {title}\n")

    def service_header(self, service_name: str):
        self.lines.append(f"\n### 📊 {service_name.upper()}\n")

    def workspace_info(self, ws_name: str, ws_id: int, created: bool):
        icon = "🆕" if created else "✅"
        verb = "создан" if created else "найден"
        self.lines.append(f"  {icon} Workspace: {ws_name} (ID: {ws_id}) — {verb}")

    def database_info(self, db_name: str, db_id: int, created: bool):
        icon = "🆕" if created else "✅"
        verb = "создана" if created else "найдена"
        self.lines.append(f"  {icon} БД: {db_name} (ID: {db_id}) — {verb}")

    def report_status(self, report_name: str, table_id: int,
                      received: int = 0, inserted: int = 0, duplicates: int = 0,
                      error: str = None, from_date: str = "", to_date: str = ""):
        icon = "✅" if error is None else "❌"
        self.lines.append(f"  {icon} Отчёт: **{report_name}** → таблица {table_id}")
        if from_date and to_date:
            self.lines.append(f"     📅 Период: {from_date} — {to_date}")
        if error:
            self.lines.append(f"     ❌ Ошибка: {error}")
            return
        self.lines.append(f"     📥 Получено: {received} записей")
        if inserted > 0:
            self.lines.append(f"     ✅ Загружено новых: {inserted}")
        if duplicates > 0:
            self.lines.append(f"     🔃 Дубликатов отфильтровано: {duplicates}")
        if received == 0:
            self.lines.append(f"     ☁️ Нет данных за период")

    def async_skipped(self, report_name: str):
        self.lines.append(f"  ⏭️ {report_name}: асинхронный отчёт (заглушка)")

    def totals(self, workspaces: int, tables: int, rows: int, errors: int = 0):
        self.lines.append(f"\n---\n\n## 📋 ИТОГИ\n")
        elapsed = (now_msk() - self.start_time).total_seconds()
        self.lines.append(f"⏱ Время выполнения: {elapsed:.1f}с")
        self.lines.append(f"🏗 Workspace создано: {workspaces}")
        self.lines.append(f"📋 Таблиц обработано: {tables}")
        self.lines.append(f"📥 Строк загружено: {rows}")
        if errors > 0:
            self.lines.append(f"❌ Ошибок: {errors}")
        status = "✅ УСПЕШНО" if errors == 0 else f"⚠️ ЗАВЕРШЕНО С ОШИБКАМИ ({errors})"
        self.lines.append(f"\n**{status}**\n")

    def flush(self):
        with open(self.log_path, "w", encoding="utf-8") as f:
            f.write("\n".join(self.lines))

# ========== 3. BASEROW CLIENT ==========
class BaserowClient:
    def __init__(self, url: str, email: str, password: str):
        self.url = url
        self.email = email
        self.password = password
        self.token = None
        self._authenticate()

    def _authenticate(self):
        resp = requests.post(f"{self.url}/api/user/token-auth/", json={"username": self.email, "password": self.password}, timeout=30)
        resp.raise_for_status()
        self.token = resp.json()["access_token"]
        logger.info("JWT получен")

    @property
    def headers(self):
        return {"Authorization": f"JWT {self.token}", "Content-Type": "application/json"}

    def _request(self, method: str, url: str, **kwargs) -> requests.Response:
        kwargs.setdefault("timeout", 60)
        resp = requests.request(method, url, headers=self.headers, **kwargs)
        if resp.status_code == 401:
            logger.warning("JWT истёк, переавторизация...")
            self._authenticate()
            resp = requests.request(method, url, headers=self.headers, **kwargs)
        return resp

    def get_workspace_id_by_name(self, name: str) -> Optional[int]:
        resp = requests.get(f"{self.url}/api/workspaces/", headers=self.headers, timeout=30)
        resp.raise_for_status()
        for ws in resp.json():
            if ws["name"] == name:
                return ws["id"]
        return None

    def create_workspace(self, name: str) -> int:
        resp = requests.post(f"{self.url}/api/workspaces/", headers=self.headers, json={"name": name}, timeout=30)
        resp.raise_for_status()
        ws_id = resp.json()["id"]
        logger.info(f"Создан workspace: {name} (ID: {ws_id})")
        return ws_id

    def get_database_id_by_name(self, workspace_id: int, name: str) -> Optional[int]:
        resp = requests.get(f"{self.url}/api/applications/workspace/{workspace_id}/", headers=self.headers, timeout=30)
        resp.raise_for_status()
        for app in resp.json():
            if app.get("type") == "database" and app["name"] == name:
                return app["id"]
        return None

    def create_database(self, workspace_id: int, name: str) -> int:
        resp = requests.post(f"{self.url}/api/applications/workspace/{workspace_id}/", headers=self.headers, json={"type": "database", "name": name}, timeout=30)
        resp.raise_for_status()
        db_id = resp.json()["id"]
        logger.info(f"Создана БД: {name} (ID: {db_id})")
        return db_id

    def create_table(self, database_id: int, name: str) -> int:
        resp = requests.post(f"{self.url}/api/database/tables/database/{database_id}/", headers=self.headers, json={"name": name}, timeout=30)
        resp.raise_for_status()
        table_id = resp.json()["id"]
        logger.info(f"Создана таблица: {name} (ID: {table_id})")
        return table_id

    def get_table_id_by_name(self, database_id: int, name: str) -> Optional[int]:
        resp = requests.get(f"{self.url}/api/database/tables/database/{database_id}/", headers=self.headers, timeout=30)
        resp.raise_for_status()
        for t in resp.json():
            if t["name"] == name:
                return t["id"]
        return None

    def create_field(self, table_id: int, name: str, field_type: str = "text"):
        baserow_name = name.replace(".", "_")
        if baserow_name in ["id", "order", "created_on", "updated_on"]:
            baserow_name = f"row_{baserow_name}"
        type_map = {"text": "text", "number": "number", "integer": "number", "date": "date", "boolean": "boolean", "long_text": "long_text"}
        baserow_type = type_map.get(field_type, "text")
        payload = {"name": baserow_name, "type": baserow_type}
        if baserow_type == "number":
            payload["number_negative"] = True
            payload["number_decimal_places"] = 0 if field_type == "integer" else 2
        resp = requests.post(f"{self.url}/api/database/fields/table/{table_id}/", headers=self.headers, json=payload, timeout=30)
        if resp.status_code == 409:
            logger.warning(f"Поле {baserow_name} уже существует")
            return None
        resp.raise_for_status()
        logger.info(f"Создано поле: {baserow_name} ({baserow_type})")
        return resp.json()["id"]

    def get_fields(self, table_id: int) -> Dict[str, Any]:
        resp = requests.get(f"{self.url}/api/database/fields/table/{table_id}/", headers=self.headers, timeout=30)
        resp.raise_for_status()
        return {f["name"]: f for f in resp.json()}

    def insert_rows(self, table_id: int, rows: List[Dict]) -> int:
        if not rows:
            return 0
        url = f"{self.url}/api/database/rows/table/{table_id}/batch/"
        params = {"user_field_names": "true"}
        total = 0
        for i in range(0, len(rows), 200):
            batch = rows[i:i+200]
            resp = requests.post(url, headers=self.headers, params=params, json={"items": batch}, timeout=300)
            if resp.status_code == 200:
                data = resp.json()
                total += len(data.get("items", []))
            else:
                logger.error(f"Ошибка вставки батча: {resp.status_code} {resp.text[:200]}")
                raise Exception(f"Insert failed: {resp.text}")
        return total

    def get_existing_unique_keys(self, table_id: int, unique_key: str, unique_key_fields: Optional[List[str]] = None) -> set:
        existing = set()
        if unique_key_fields:
            baserow_fields = []
            for kf in unique_key_fields:
                bf = kf.replace(".", "_")
                if bf in ["id", "order", "created_on", "updated_on"]:
                    bf = f"row_{bf}"
                baserow_fields.append(bf)
            page = 1
            while True:
                resp = requests.get(f"{self.url}/api/database/rows/table/{table_id}/", headers=self.headers, params={"page": page, "size": 200, "user_field_names": "true"}, timeout=60)
                resp.raise_for_status()
                data = resp.json()
                for row in data["results"]:
                    parts = []
                    all_present = True
                    for bf in baserow_fields:
                        v = row.get(bf)
                        if v is None:
                            all_present = False
                            break
                        parts.append(str(v))
                    if all_present:
                        existing.add("||".join(parts))
                if not data.get("next"):
                    break
                page += 1
            logger.info(f"Найдено {len(existing)} составных уникальных ключей")
            return existing
        baserow_key = unique_key.replace(".", "_")
        if baserow_key in ["id", "order", "created_on", "updated_on"]:
            baserow_key = f"row_{baserow_key}"
        page = 1
        while True:
            resp = requests.get(f"{self.url}/api/database/rows/table/{table_id}/", headers=self.headers, params={"page": page, "size": 200, "user_field_names": "true"}, timeout=60)
            resp.raise_for_status()
            data = resp.json()
            for row in data["results"]:
                val = row.get(baserow_key)
                if val is not None:
                    existing.add(str(val))
            if not data.get("next"):
                break
            page += 1
        logger.info(f"Найдено {len(existing)} уникальных ключей")
        return existing

# ========== 4. РАБОТА С LAST_RUN ==========
def load_last_run() -> Dict[str, str]:
    if LAST_RUN_FILE.exists():
        with open(LAST_RUN_FILE, "r") as f:
            return json.load(f)
    return {}

def save_last_run(last_run: Dict[str, str]):
    with open(LAST_RUN_FILE, "w") as f:
        json.dump(last_run, f, indent=2)

# ========== 5. API ЗАГРУЗКА С ПОДРОБНЫМ ЛОГИРОВАНИЕМ ==========

MAX_RETRIES = 5
RETRY_BACKOFF = 2

REQUEST_TIMEOUT = 120

def _request_with_retry(method: str, url: str, **kwargs) -> requests.Response:
    kwargs.setdefault("timeout", REQUEST_TIMEOUT)
    last_resp = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            if method.upper() == "GET":
                resp = requests.get(url, **kwargs)
            else:
                resp = requests.post(url, **kwargs)
            if resp.status_code == 429 and attempt < MAX_RETRIES:
                retry_after = int(resp.headers.get("Retry-After", RETRY_BACKOFF ** attempt))
                logger.warning(f"HTTP 429 (rate limit), попытка {attempt}/{MAX_RETRIES}, ждём {retry_after}с... URL={url}")
                time.sleep(retry_after)
                last_resp = resp
                continue
            return resp
        except (ChunkedEncodingError, ConnectionError, requests.exceptions.RequestException) as e:
            if attempt == MAX_RETRIES:
                raise
            wait = RETRY_BACKOFF ** attempt
            logger.warning(f"Сетевая ошибка ({type(e).__name__}), попытка {attempt}/{MAX_RETRIES}, ждём {wait}с...")
            time.sleep(wait)
    if last_resp is not None:
        return last_resp
    raise RuntimeError("Неожиданный выход из цикла повторных попыток")

def build_api_headers(service_name: str, api_key_env: str) -> Optional[Dict[str, str]]:
    creds = os.getenv(api_key_env, "")
    if not creds:
        logger.warning(f"Переменная {api_key_env} не найдена в .env, отчёт будет пропущен")
        return None
    if service_name == "ozon":
        parts = creds.split(",")
        if len(parts) == 2:
            return {"Client-Id": parts[0].strip(), "Api-Key": parts[1].strip(), "Content-Type": "application/json"}
        else:
            raise ValueError(f"Некорректный формат OZON_CREDS: {creds}")
    else:
        return {"Authorization": creds, "Content-Type": "application/json"}

def extract_items_from_response(data: Any, response_data_path: str) -> List[Dict]:
    if isinstance(data, list):
        return data
    if not isinstance(data, dict):
        return []
    if response_data_path:
        parts = response_data_path.split(".")
        cur = data
        for p in parts:
            if isinstance(cur, dict):
                cur = cur.get(p)
            else:
                return []
        if isinstance(cur, list):
            return cur
    # fallback
    for key in ("result", "data", "items", "rows", "operations", "postings", "returns", "warehouseList"):
        if key in data and isinstance(data[key], list):
            return data[key]
    return []

def _extract_nested(data: Any, path: str) -> Any:
    if not path:
        return data
    parts = path.split(".")
    cur = data
    for p in parts:
        if isinstance(cur, dict):
            cur = cur.get(p)
        else:
            return None
    return cur

def fetch_async_data(config: Dict, service_name: str, from_date: str, to_date: str,
                     headers: Dict, full_url: str, response_data_path: str) -> List[Dict]:
    ac = config.get("async_config", {})
    delay = 1.0 / config.get("rate_limit_per_sec", 1.0)

    template = config.get("request_body_template", "")
    try:
        from_dt_iso = datetime.strptime(from_date, "%Y-%m-%d").isoformat() + ".000000000"
        to_dt_iso = datetime.strptime(to_date, "%Y-%m-%d").isoformat() + ".000000000"
    except ValueError:
        from_dt_iso = from_date
        to_dt_iso = to_date
    body_str = template.replace("{from_date}", from_date).replace("{to_date}", to_date)
    body_str = body_str.replace("{from_date_iso}", from_dt_iso).replace("{to_date_iso}", to_dt_iso)
    template_vars = config.get("template_vars", {})
    if template_vars:
        try:
            from_dt = datetime.strptime(from_date, "%Y-%m-%d")
            to_dt = datetime.strptime(to_date, "%Y-%m-%d")
        except ValueError:
            from_dt = to_dt = None
        prev_m = from_dt - timedelta(days=from_dt.day) if from_dt else None
        for var_name, var_source in template_vars.items():
            placeholder = "{" + var_name + "}"
            if placeholder not in body_str:
                continue
            val = ""
            if from_dt:
                if var_source == "from_month":
                    val = str(from_dt.month)
                elif var_source == "from_year":
                    val = str(from_dt.year)
                elif var_source == "to_month":
                    val = str(to_dt.month)
                elif var_source == "to_year":
                    val = str(to_dt.year)
                elif var_source == "prev_month" and prev_m:
                    val = str(prev_m.month)
                elif var_source == "prev_year" and prev_m:
                    val = str(prev_m.year)
            body_str = body_str.replace(placeholder, val)
    try:
        json_body = json.loads(body_str)
    except json.JSONDecodeError:
        json_body = {}

    async_headers = headers.copy()
    async_base_url = ac.get("api_base_url", config.get("api_base_url", ""))
    create_endpoint = ac.get("create_endpoint", config.get("api_endpoint", ""))
    create_url = f"{async_base_url.rstrip('/')}{create_endpoint}"
    auth_type = ac.get("auth_type", "default")
    if auth_type == "oauth_client_credentials":
        oauth_env = ac.get("oauth_client_id_env", ""), ac.get("oauth_client_secret_env", "")
        client_id_val = os.getenv(oauth_env[0], "") if oauth_env[0] else ""
        client_secret_val = os.getenv(oauth_env[1], "") if oauth_env[1] else ""
        if not client_id_val or not client_secret_val:
            logger.error(f"async: не найдены OAuth credentials ({oauth_env})")
            return []
        token_url = ac.get("oauth_token_url", "")
        if not token_url:
            logger.error("async: не указан oauth_token_url в async_config")
            return []
        try:
            tr = _request_with_retry("POST", token_url, json={
                "client_id": client_id_val,
                "client_secret": client_secret_val,
                "grant_type": "client_credentials"
            }, headers={"Content-Type": "application/json"}, timeout=30)
            if tr.status_code != 200:
                logger.error(f"async: ошибка OAuth: HTTP {tr.status_code}: {tr.text[:200]}")
                return []
            access_token = tr.json().get("access_token", "")
            if not access_token:
                logger.error(f"async: нет access_token в OAuth-ответе")
                return []
            logger.info("async: OAuth-токен получен")
        except Exception as e:
            logger.error(f"async: ошибка получения OAuth-токена: {e}")
            return []
        async_headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    elif auth_type == "bearer":
        api_key_env = config.get("api_key_env", "")
        creds = os.getenv(api_key_env, "")
        if service_name == "ozon" and "," in creds:
            api_key = creds.split(",")[1].strip()
        else:
            api_key = creds
        async_headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    logger.info(f"async: создание задачи {config['report_name']}")

    prefill_key = ac.get("prefill_list_key", "")
    prefill_endpoint = ac.get("prefill_list_endpoint", "")
    if prefill_key and prefill_endpoint and prefill_key in json_body and json_body[prefill_key] == []:
        pf_url = f"{async_base_url.rstrip('/')}{prefill_endpoint}"
        logger.info(f"async: заполнение {prefill_key} из {pf_url}")
        try:
            pf_resp = _request_with_retry("GET", pf_url, headers=async_headers)
            if pf_resp.status_code == 200:
                pf_data = pf_resp.json()
                id_path = ac.get("prefill_id_path", "id")
                ids = []
                if isinstance(pf_data, list):
                    source = pf_data
                elif isinstance(pf_data, dict):
                    source = None
                    for key in ("result", "data", "items", "list", prefill_key):
                        if key in pf_data and isinstance(pf_data[key], list):
                            source = pf_data[key]
                            break
                    if source is None:
                        source = []
                else:
                    source = []
                pf_filter = ac.get("prefill_filter", {})
                if pf_filter and isinstance(source, list) and source and isinstance(source[0], dict):
                    ff_field = pf_filter.get("field", "")
                    ff_values = pf_filter.get("values", None)
                    ff_exclude = pf_filter.get("exclude_values", None)
                    if ff_field:
                        before = len(source)
                        if ff_values is not None:
                            if isinstance(ff_values, str):
                                ff_values = [v.strip() for v in ff_values.split(",")]
                            source = [it for it in source if str(_extract_nested(it, ff_field) or "") in [str(v) for v in ff_values]]
                        if ff_exclude is not None:
                            if isinstance(ff_exclude, str):
                                ff_exclude = [v.strip() for v in ff_exclude.split(",")]
                            source = [it for it in source if str(_extract_nested(it, ff_field) or "") not in [str(v) for v in ff_exclude]]
                        logger.info(f"async: prefill_filter по '{ff_field}': {before} → {len(source)} элементов")
                for item in source:
                    if isinstance(item, dict):
                        val = _extract_nested(item, id_path)
                        if val is not None:
                            ids.append(int(val) if not isinstance(val, int) else val)
                    elif isinstance(item, (int, str)):
                        ids.append(int(item))
                logger.info(f"async: найдено {len(ids)} элементов для {prefill_key}")
                json_body[prefill_key] = ids
            else:
                logger.warning(f"async: не удалось получить список {prefill_key}: HTTP {pf_resp.status_code}")
        except Exception as e:
            logger.warning(f"async: ошибка получения списка {prefill_key}: {e}")

    resp = _request_with_retry("POST", create_url, headers=async_headers, json=json_body)
    if resp.status_code != 200:
        logger.error(f"async: ошибка создания задачи: HTTP {resp.status_code}: {resp.text[:300]}")
        return []
    create_data = resp.json()
    uuid_path = ac.get("uuid_path", "UUID")
    task_uuid = _extract_nested(create_data, uuid_path)
    if not task_uuid:
        logger.error(f"async: не найден UUID по пути '{uuid_path}' в ответе: {create_data}")
        return []
    logger.info(f"async: задача создана, UUID={task_uuid}")

    poll_endpoint = ac.get("poll_endpoint", "").replace("{uuid}", str(task_uuid))
    poll_url = f"{async_base_url.rstrip('/')}{poll_endpoint}"
    poll_interval = ac.get("poll_interval_sec", 10)
    poll_max = ac.get("poll_max_attempts", 60)
    status_path = ac.get("status_path", "state")
    status_ready_list = [s.strip() for s in ac.get("status_ready", "OK,ready,SUCCESS").split(",")]
    status_error_list = [s.strip() for s in ac.get("status_error", "FAILED,ERROR,CANCELED").split(",") if s.strip()]

    for attempt in range(1, poll_max + 1):
        time.sleep(poll_interval)
        logger.info(f"async: опрос {attempt}/{poll_max}, UUID={task_uuid}")
        poll_resp = _request_with_retry("GET", poll_url, headers=async_headers)
        if poll_resp.status_code != 200:
            logger.warning(f"async: HTTP {poll_resp.status_code} при опросе")
            continue
        poll_data = poll_resp.json()
        current_status = str(_extract_nested(poll_data, status_path) or "")
        logger.info(f"async: статус={current_status}, ответ={json.dumps(poll_data)[:300]}")
        if current_status in status_ready_list:
            break
        if status_error_list and current_status in status_error_list:
            logger.error(f"async: задача завершилась с ошибкой: {poll_data}")
            return []
    else:
        logger.error(f"async: превышен лимит ожидания ({poll_max} попыток)")
        return []

    result_type = ac.get("result_type", "url")
    if result_type == "url":
        result_url_path = ac.get("result_url_path", "link")
        download_url = _extract_nested(poll_data, result_url_path)
        if not download_url:
            logger.error(f"async: не найден URL результата по пути '{result_url_path}' в {list(poll_data.keys())}")
            return []
        if download_url.startswith("/"):
            download_url = f"{async_base_url.rstrip('/')}{download_url}"
        logger.info(f"async: скачивание результата из {download_url}")
        dl_resp = _request_with_retry("GET", download_url)
        if dl_resp.status_code != 200:
            logger.error(f"async: ошибка скачивания: HTTP {dl_resp.status_code}")
            return []
        content_type = dl_resp.headers.get("Content-Type", "")
        if "csv" in content_type or "text" in content_type:
            import csv
            import io
            reader = csv.DictReader(io.StringIO(dl_resp.text))
            items = list(reader)
            logger.info(f"async: получено {len(items)} записей из CSV")
            return items
        try:
            data = dl_resp.json()
            items = extract_items_from_response(data, response_data_path)
            logger.info(f"async: получено {len(items)} записей из JSON")
            return items
        except Exception:
            logger.error("async: не удалось распарсить ответ")
            return []
    elif result_type == "inline":
        items = extract_items_from_response(poll_data, response_data_path)
        logger.info(f"async: получено {len(items)} записей (inline)")
        return items
    logger.error(f"async: неизвестный result_type={result_type}")
    return []

def _split_period_by_month(from_date: str, to_date: str) -> List[Tuple[str, str]]:
    periods = []
    from_dt = datetime.strptime(from_date, "%Y-%m-%d")
    to_dt = datetime.strptime(to_date, "%Y-%m-%d")
    cur = from_dt
    while cur < to_dt:
        next_month = (cur.replace(day=1) + timedelta(days=32)).replace(day=1)
        end = min(next_month - timedelta(days=1), to_dt)
        periods.append((cur.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")))
        cur = next_month
    return periods

def _get_entity_list(config: Dict, service_name: str, headers: Dict) -> List[Any]:
    el = config.get("entity_list", {})
    if not el:
        return []
    endpoint = el.get("endpoint", "")
    if not endpoint:
        return []
    api_base_url = el.get("api_base_url", config.get("api_base_url", ""))
    url = f"{api_base_url.rstrip('/')}{endpoint}"
    method = el.get("method", "GET").upper()
    logger.info(f"entity_list: получение из {url}")
    try:
        if method == "POST":
            body = json.loads(el.get("body", "{}"))
            resp = _request_with_retry("POST", url, headers=headers, json=body)
        else:
            resp = _request_with_retry("GET", url, headers=headers)
        if resp.status_code != 200:
            logger.error(f"entity_list: HTTP {resp.status_code}: {resp.text[:200]}")
            return []
        data = resp.json()
        id_path = el.get("id_path", "id")
        response_path = el.get("response_path", "")
        nested_list_path = el.get("nested_list_path", "")
        if response_path:
            source = _extract_nested(data, response_path)
            if not isinstance(source, list):
                source = []
        elif isinstance(data, list):
            source = data
        elif isinstance(data, dict):
            source = []
            for key in ("result", "data", "items"):
                if key in data and isinstance(data[key], list):
                    source = data[key]
                    break
        else:
            source = []
        ids = []
        for item in source:
            if nested_list_path and isinstance(item, dict):
                nested = _extract_nested(item, nested_list_path)
                if isinstance(nested, list):
                    for sub in nested:
                        if isinstance(sub, dict):
                            val = _extract_nested(sub, id_path)
                            if val is not None:
                                ids.append(val)
                        elif isinstance(sub, (int, str)):
                            ids.append(sub)
                continue
            if isinstance(item, dict):
                val = _extract_nested(item, id_path)
                if val is not None:
                    ids.append(val)
            elif isinstance(item, (int, str)):
                ids.append(item)
        logger.info(f"entity_list: найдено {len(ids)} сущностей")
        return ids
    except Exception as e:
        logger.error(f"entity_list: ошибка: {e}")
        return []

def fetch_api_data(config: Dict, service_name: str, from_date: str, to_date: str) -> List[Dict]:
    el = config.get("entity_list", {})
    if el:
        headers = build_api_headers(service_name, config["api_key_env"])
        if not headers:
            logger.warning(f"Пропускаем {config['report_name']}: нет API-ключа ({config['api_key_env']})")
            return []
        entity_ids = _get_entity_list(config, service_name, headers)
        if not entity_ids:
            logger.warning(f"entity_list: список пуст, пропускаем {config['report_name']}")
            return []
        all_data = []
        param_name = el.get("param_name", "id")
        for eid in entity_ids:
            logger.info(f"entity_list: загрузка для {param_name}={eid}")
        cfg = dict(config)
        endpoint = cfg.get("api_endpoint", "")
        placeholder = "{" + param_name + "}"
        if placeholder in endpoint:
            cfg["api_endpoint"] = endpoint.replace(placeholder, str(eid))
        elif cfg.get("method", "GET").upper() == "GET":
            extra = cfg.get("extra_params", {})
            extra[param_name] = eid
            cfg["extra_params"] = extra
        else:
            template = cfg.get("request_body_template", "")
            if placeholder in template:
                template = template.replace(placeholder, str(eid))
                cfg["request_body_template"] = template
            else:
                body = json.loads(template) if template else {}
                body[param_name] = eid
                cfg["request_body_template"] = json.dumps(body)
            del cfg["entity_list"]
            chunk = fetch_api_data(cfg, service_name, from_date, to_date)
            all_data.extend(chunk)
            time.sleep(1.0 / config.get("rate_limit_per_sec", 1.0))
        logger.info(f"entity_list итого: {len(all_data)} записей")
        return all_data

    if config.get("split_by_month", False):
        periods = _split_period_by_month(from_date, to_date)
        logger.info(f"split_by_month: период {from_date}..{to_date} разбит на {len(periods)} месяцев")
        all_data = []
        for p_from, p_to in periods:
            logger.info(f"split_by_month: загрузка {p_from}..{p_to}")
            chunk = _fetch_single_period(config, service_name, p_from, p_to)
            all_data.extend(chunk)
            time.sleep(1.0 / config.get("rate_limit_per_sec", 1.0))
        logger.info(f"split_by_month итого: {len(all_data)} записей")
        return all_data
    return _fetch_single_period(config, service_name, from_date, to_date)

def _fetch_single_period(config: Dict, service_name: str, from_date: str, to_date: str) -> List[Dict]:
    method = config.get("method", "GET").upper()
    endpoint = config["api_endpoint"]
    api_base_url = config["api_base_url"]
    api_key_env = config["api_key_env"]
    headers = build_api_headers(service_name, api_key_env)
    if not headers:
        logger.warning(f"Пропускаем {config['report_name']}: нет API-ключа ({api_key_env})")
        return []
    full_url = f"{api_base_url.rstrip('/')}{endpoint}"
    pagination_type = config.get("pagination_type", "none")
    batch_size = config.get("batch_size", 1000)
    delay = 1.0 / config.get("rate_limit_per_sec", 1.0)
    response_data_path = config.get("response_data_path", "")
    is_async = config.get("is_async", False)

    if is_async:
        ac = config.get("async_config", {})
        if not ac:
            logger.warning(f"Асинхронный отчёт {config['report_name']}: нет async_config, пропускаем")
            return []
        return fetch_async_data(config, service_name, from_date, to_date, headers, full_url, response_data_path)

    # Базовые параметры дат
    params = {}
    json_body = None
    if method == "POST":
        template = config.get("request_body_template", "")
        if template:
            try:
                from_dt_iso = datetime.strptime(from_date, "%Y-%m-%d").isoformat() + ".000000000"
                to_dt_iso = datetime.strptime(to_date, "%Y-%m-%d").isoformat() + ".000000000"
            except ValueError:
                from_dt_iso = from_date
                to_dt_iso = to_date
            body_str = template.replace("{from_date}", from_date).replace("{to_date}", to_date)
            body_str = body_str.replace("{from_date_iso}", from_dt_iso).replace("{to_date_iso}", to_dt_iso)
            template_vars = config.get("template_vars", {})
            if template_vars:
                try:
                    from_dt = datetime.strptime(from_date, "%Y-%m-%d")
                    to_dt = datetime.strptime(to_date, "%Y-%m-%d")
                except ValueError:
                    from_dt = to_dt = None
                prev_m = from_dt - timedelta(days=from_dt.day) if from_dt else None
                for var_name, var_source in template_vars.items():
                    placeholder = "{" + var_name + "}"
                    if placeholder not in body_str:
                        continue
                    val = ""
                    if from_dt:
                        if var_source == "from_month":
                            val = str(from_dt.month)
                        elif var_source == "from_year":
                            val = str(from_dt.year)
                        elif var_source == "to_month":
                            val = str(to_dt.month)
                        elif var_source == "to_year":
                            val = str(to_dt.year)
                        elif var_source == "from_date_iso":
                            val = from_dt.isoformat()
                        elif var_source == "to_date_iso":
                            val = to_dt.isoformat()
                        elif var_source == "prev_month" and prev_m:
                            val = str(prev_m.month)
                        elif var_source == "prev_year" and prev_m:
                            val = str(prev_m.year)
                    body_str = body_str.replace(placeholder, val)
            try:
                json_body = json.loads(body_str)
            except json.JSONDecodeError as e:
                logger.error(f"Ошибка парсинга тела запроса: {e}, body_str={body_str[:200]}")
                json_body = {}
        else:
            json_body = {}
    else:
        params = {
            config.get("date_from_param", "dateFrom"): from_date,
            config.get("date_to_param", "dateTo"): to_date
        }
        extra_params = config.get("extra_params", {})
        if extra_params:
            params.update(extra_params)

    all_data = []
    logger.info(f"Загрузка {config['report_name']}: pagination={pagination_type}, batch_size={batch_size}, period={from_date}..{to_date}")

    # ---- rrdid ----
    if pagination_type == "rrdid":
        pc = config.get("pagination_config", {})
        rrdid_param = pc.get("rrdid_param", "rrdid")
        limit_param = pc.get("limit_param", "limit")
        empty_response_code = config.get("empty_response_code", None)
        rrdid = 0
        page_num = 1
        while True:
            logger.info(f"rrdid запрос {page_num}: rrdid={rrdid}")
            if method == "POST":
                body = json_body.copy() if json_body else {}
                body[limit_param] = batch_size
                body[rrdid_param] = rrdid
                resp = _request_with_retry("POST", full_url, headers=headers, json=body)
            else:
                qparams = {
                    "dateFrom": from_date,
                    "dateTo": to_date,
                    limit_param: batch_size,
                    rrdid_param: rrdid
                }
                resp = _request_with_retry("GET", full_url, headers=headers, params=qparams)
            if resp.status_code == empty_response_code:
                logger.info(f"rrdid страница {page_num}: HTTP {empty_response_code} (пустой ответ), завершаем")
                break
            if resp.status_code != 200:
                logger.error(f"HTTP {resp.status_code}: {resp.text[:200]}")
                break
            data = resp.json()
            items = extract_items_from_response(data, response_data_path)
            if not items:
                logger.info(f"rrdid страница {page_num}: нет данных, завершаем")
                break
            logger.info(f"rrdid страница {page_num}: получено {len(items)} записей")
            all_data.extend(items)
            last_rrdid = None
            for item in reversed(items):
                if rrdid_param in item:
                    last_rrdid = item[rrdid_param]
                    break
            if last_rrdid is None or last_rrdid == rrdid:
                logger.info(f"rrdid останов: последний rrdid={last_rrdid}, предыдущий={rrdid}")
                break
            rrdid = last_rrdid
            page_num += 1
            time.sleep(delay)
        logger.info(f"rrdid итого: {len(all_data)} записей")
        return all_data

    # ---- page_number ----
    if pagination_type == "page_number":
        page = 1
        while True:
            if method == "POST":
                body = json_body.copy() if json_body else {}
                body["page"] = page
                body["page_size"] = batch_size
                resp = _request_with_retry("POST", full_url, headers=headers, json=body)
            else:
                p = params.copy()
                p["page"] = page
                p["page_size"] = batch_size
                resp = _request_with_retry("GET", full_url, headers=headers, params=p)
            if resp.status_code != 200:
                logger.error(f"HTTP {resp.status_code} на странице {page}")
                break
            data = resp.json()
            items = extract_items_from_response(data, response_data_path)
            if not items:
                logger.info(f"Страница {page}: пусто, завершаем")
                break
            logger.info(f"Страница {page}: получено {len(items)} записей")
            all_data.extend(items)
            if len(items) < batch_size:
                logger.info(f"Страница {page}: меньше {batch_size}, завершаем")
                break
            page += 1
            time.sleep(delay)
        logger.info(f"page_number итого: {len(all_data)} записей")
        return all_data

    # ---- offset ----
    if pagination_type == "offset":
        offset = 0
        while True:
            if method == "POST":
                body = json_body.copy() if json_body else {}
                body["offset"] = offset
                body["limit"] = batch_size
                resp = _request_with_retry("POST", full_url, headers=headers, json=body)
            else:
                p = params.copy()
                p["offset"] = offset
                p["limit"] = batch_size
                resp = _request_with_retry("GET", full_url, headers=headers, params=p)
            if resp.status_code != 200:
                logger.error(f"HTTP {resp.status_code} при offset={offset}")
                break
            data = resp.json()
            items = extract_items_from_response(data, response_data_path)
            if not items:
                logger.info(f"offset={offset}: пусто, завершаем")
                break
            logger.info(f"offset={offset}: получено {len(items)} записей")
            all_data.extend(items)
            if len(items) < batch_size:
                logger.info(f"offset={offset}: меньше {batch_size}, завершаем")
                break
            offset += batch_size
            time.sleep(delay)
        logger.info(f"offset итого: {len(all_data)} записей")
        return all_data

    # ---- last_id ----
    if pagination_type == "last_id":
        pc = config.get("pagination_config", {})
        last_id_param = pc.get("last_id_param", "last_id")
        limit_param = pc.get("limit_param", "limit")
        last_id = 0
        while True:
            body = json_body.copy() if json_body else {}
            body[last_id_param] = last_id
            body[limit_param] = batch_size
            resp = _request_with_retry("POST", full_url, headers=headers, json=body)
            if resp.status_code != 200:
                logger.error(f"HTTP {resp.status_code} при last_id={last_id}")
                break
            data = resp.json()
            items = extract_items_from_response(data, response_data_path)
            if not items:
                logger.info(f"last_id={last_id}: пусто, завершаем")
                break
            logger.info(f"last_id={last_id}: получено {len(items)} записей")
            all_data.extend(items)
            next_last_id = data.get("last_id")
            if next_last_id is None:
                if items and "id" in items[-1]:
                    next_last_id = items[-1]["id"]
                else:
                    break
            if next_last_id == last_id or len(items) < batch_size:
                logger.info(f"last_id останов: next={next_last_id}, prev={last_id}, rows={len(items)}")
                break
            last_id = next_last_id
            time.sleep(delay)
        logger.info(f"last_id итого: {len(all_data)} записей")
        return all_data

    # ---- none ----
    if method == "POST":
        resp = _request_with_retry("POST", full_url, headers=headers, json=json_body)
    else:
        resp = _request_with_retry("GET", full_url, headers=headers, params=params)
    if resp.status_code == 200:
        data = resp.json()
        items = extract_items_from_response(data, response_data_path)
        if isinstance(items, list):
            logger.info(f"none: получено {len(items)} записей")
            return items
    else:
        logger.error(f"HTTP {resp.status_code}: {resp.text[:200]}")
    return []

# ========== 6. ТРАНСФОРМАЦИЯ ДАННЫХ ==========
def normalize_value(value: Any, field_type: str) -> Any:
    if value is None:
        return None
    if field_type in ("text", "long_text"):
        return str(value).strip() if str(value).strip() else None
    if field_type == "integer":
        try:
            return int(float(value))
        except:
            return None
    if field_type == "number":
        try:
            return round(float(value), 2)
        except:
            return None
    if field_type == "date":
        if isinstance(value, str):
            for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%SZ", "%d.%m.%Y", "%d/%m/%Y"):
                try:
                    dt = datetime.strptime(value, fmt)
                    return dt.strftime("%Y-%m-%d")
                except:
                    continue
        return None
    if field_type == "boolean":
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ("true", "1", "yes", "да")
        return bool(value)
    return None

def transform_data(raw_data: List[Dict], field_mapping: Dict[str, str]) -> List[Dict]:
    transformed = []
    for record in raw_data:
        row = {}
        for field_name, field_type in field_mapping.items():
            value = record.get(field_name)
            if value is None and "." in field_name:
                parts = field_name.split(".")
                v = record
                for p in parts:
                    if isinstance(v, dict):
                        v = v.get(p)
                    else:
                        v = None
                        break
                value = v
            normalized = normalize_value(value, field_type)
            if normalized is not None:
                baserow_name = field_name.replace(".", "_")
                if baserow_name in ["id", "order", "created_on", "updated_on"]:
                    baserow_name = f"row_{baserow_name}"
                row[baserow_name] = normalized
        if row:
            transformed.append(row)
    return transformed

def _get_row_key(row: Dict, unique_key: str, unique_key_fields: Optional[List[str]]) -> Optional[str]:
    if unique_key_fields:
        parts = []
        for kf in unique_key_fields:
            bf = kf.replace(".", "_")
            if bf in ["id", "order", "created_on", "updated_on"]:
                bf = f"row_{bf}"
            v = row.get(bf)
            if v is None:
                return None
            parts.append(str(v))
        return "||".join(parts)
    key_field = unique_key.replace(".", "_")
    if key_field in ["id", "order", "created_on", "updated_on"]:
        key_field = f"row_{key_field}"
    val = row.get(key_field)
    return str(val) if val is not None else None


def filter_duplicates(data: List[Dict], unique_key: str, unique_key_fields: Optional[List[str]], existing_keys: set) -> Tuple[List[Dict], int]:
    if not unique_key and not unique_key_fields:
        return data, 0
    seen = set()
    filtered = []
    dup_count = 0
    for row in data:
        key = _get_row_key(row, unique_key, unique_key_fields)
        if key is None:
            filtered.append(row)
            continue
        if key in existing_keys or key in seen:
            dup_count += 1
            continue
        seen.add(key)
        filtered.append(row)
    return filtered, dup_count

# ========== 7. ОСНОВНАЯ ЛОГИКА ==========
def run_loader():
    logger.info("Запуск универсального загрузчика (JSON-конфиги)")
    start_time = now_msk()
    status_log = StatusLogger(STATUS_LOG)

    if not BASEROW_EMAIL or not BASEROW_PASSWORD:
        raise ValueError("BASEROW_EMAIL и BASEROW_PASSWORD не заданы")
    client = BaserowClient(BASEROW_URL, BASEROW_EMAIL, BASEROW_PASSWORD)

    # Workspace
    ws_id = client.get_workspace_id_by_name(WORKSPACE_NAME)
    created_ws = False
    if not ws_id:
        ws_id = client.create_workspace(WORKSPACE_NAME)
        created_ws = True
    status_log.workspace_info(WORKSPACE_NAME, ws_id, created_ws)

    # Загружаем last_run
    last_run_data = load_last_run()

    total_workspaces = 1 if created_ws else 0
    total_tables = 0
    total_rows = 0
    total_errors = 0

    for service in SERVICES:
        db_name = DATABASES[service]
        db_id = client.get_database_id_by_name(ws_id, db_name)
        created_db = False
        if not db_id:
            db_id = client.create_database(ws_id, db_name)
            created_db = True
        status_log.database_info(db_name, db_id, created_db)
        status_log.service_header(service)

        config_dir = CONFIGS_DIR / service
        if not config_dir.exists():
            logger.warning(f"Папка {config_dir} не существует, пропускаем")
            continue

        for json_file in config_dir.glob("*.json"):
            with open(json_file, "r", encoding="utf-8") as f:
                config = json.load(f)

            report_name = config["report_name"]
            table_name = report_name
            table_id = client.get_table_id_by_name(db_id, table_name)
            if not table_id:
                table_id = client.create_table(db_id, table_name)
                for field_name, field_type in config["field_mapping"].items():
                    client.create_field(table_id, field_name, field_type)
                total_tables += 1
            else:
                existing_fields = client.get_fields(table_id)
                for field_name, field_type in config["field_mapping"].items():
                    baserow_name = field_name.replace(".", "_")
                    if baserow_name in ["id", "order", "created_on", "updated_on"]:
                        baserow_name = f"row_{baserow_name}"
                    if baserow_name not in existing_fields:
                        client.create_field(table_id, field_name, field_type)

            # Определяем период загрузки
            max_depth_days = config.get("max_depth_days", 30)
            unique_key = config.get("unique_key", "")
            unique_key_fields = config.get("unique_key_fields", None)
            last_run_key = f"{service}_{report_name}"
            last_run_date = last_run_data.get(last_run_key)

            if last_run_date:
                from_date = last_run_date
                to_date = now_msk().strftime("%Y-%m-%d")
                logger.info(f"Инкрементальная загрузка {report_name}: {from_date} -> {to_date}")
            else:
                from_date = (now_msk() - timedelta(days=max_depth_days)).strftime("%Y-%m-%d")
                to_date = now_msk().strftime("%Y-%m-%d")
                logger.info(f"Полная загрузка {report_name} за {max_depth_days} дней: {from_date} -> {to_date}")

            try:
                raw_data = fetch_api_data(config, service, from_date, to_date)
                received = len(raw_data)
                if not raw_data:
                    status_log.report_status(report_name, table_id, received=0, from_date=from_date, to_date=to_date)
                    continue

                transformed = transform_data(raw_data, config["field_mapping"])
                logger.info(f"Трансформация: {len(raw_data)} → {len(transformed)} строк")
                if transformed and len(transformed) > 0:
                    logger.info(f"Пример строки: {list(transformed[0].keys())}")
                if unique_key or unique_key_fields:
                    existing_keys = client.get_existing_unique_keys(table_id, unique_key, unique_key_fields)
                    transformed, dup_count = filter_duplicates(transformed, unique_key, unique_key_fields, existing_keys)
                    logger.info(f"Фильтр дубликатов: {len(transformed)} уникальных, {dup_count} дубликатов")
                else:
                    dup_count = 0

                inserted = 0
                if transformed:
                    inserted = client.insert_rows(table_id, transformed)
                    logger.info(f"Вставлено: {inserted} строк в таблицу {table_id}")
                    total_rows += inserted
                    if inserted > 0:
                        last_run_data[last_run_key] = to_date
                        save_last_run(last_run_data)
                status_log.report_status(report_name, table_id, received=received, inserted=inserted, duplicates=dup_count, from_date=from_date, to_date=to_date)
            except Exception as e:
                logger.error(f"Ошибка при загрузке {report_name}: {e}", exc_info=True)
                status_log.report_status(report_name, table_id, error=str(e), from_date=from_date, to_date=to_date)
                total_errors += 1

    status_log.totals(total_workspaces, total_tables, total_rows, total_errors)
    status_log.flush()
    logger.info(f"Загрузка завершена. Статус: {STATUS_LOG}")

if __name__ == "__main__":
    run_loader()
