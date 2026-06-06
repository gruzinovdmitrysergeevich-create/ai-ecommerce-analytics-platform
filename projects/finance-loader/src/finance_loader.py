#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Универсальный загрузчик в Baserow (исправление типов и Google-путей).
"""

import os, sys, json, hashlib, logging, re
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Any
import pandas as pd
import requests
from dotenv import load_dotenv
from dateutil import parser as dateparser

ENV_PATH = Path.home() / "my-ai-stack" / "analytics" / ".env"
load_dotenv(ENV_PATH)

BASEROW_URL = os.getenv("BASEROW_URL", "http://localhost:8000")
BASEROW_EMAIL = os.getenv("BASEROW_EMAIL")
BASEROW_PASSWORD = os.getenv("BASEROW_PASSWORD")
GOOGLE_TOKEN_PATH = Path.home() / "my-ai-stack" / "analytics" / "token.json"
GOOGLE_CREDS_PATH = Path.home() / "my-ai-stack" / "analytics" / "credentials_google_drive.json"
SERVICE_ACCOUNT_PATH = Path.home() / "my-ai-stack" / "analytics" / "service_account.json"

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIGS_DIR = BASE_DIR / "configs"
LOG_DIR = BASE_DIR / "logs"
STATUS_LOG = LOG_DIR / "status.md"
LOG_DIR.mkdir(exist_ok=True)

MSK = timezone(timedelta(hours=3))
def now_msk():
    return datetime.now(MSK)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / f"run_{now_msk().strftime('%Y-%m-%d_%H-%M-%S')}.log", encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class StatusLogger:
    def __init__(self, log_path: Path):
        self.log_path = log_path
        self.lines: List[str] = []
        self.start_time = now_msk()
        self._write_header()

    def _write_header(self):
        self.lines.append(f"# 🚀 FINANCE LOADER | {self.start_time:%Y-%m-%d %H:%M:%S MSK}\n")

    def config_info(self, name, db, table, source):
        self.lines.append(f"\n### 📄 {name}")
        self.lines.append(f"  🗄 БД: {db}")
        self.lines.append(f"  📋 Таблица: {table}")
        self.lines.append(f"  📂 Источник: {source}")

    def ok(self, msg): self.lines.append(f"  ✅ {msg}")
    def warning(self, msg): self.lines.append(f"  ⚠️ {msg}")
    def error(self, msg): self.lines.append(f"  ❌ {msg}")

    def file_processed(self, fname, total_rows, inserted, dups, new_cols, deleted):
        icon = "🗑" if deleted else "📥"
        self.lines.append(f"  {icon} Файл: {fname} – строк: {total_rows}, загружено: {inserted}, дубликатов: {dups}")
        if new_cols:
            self.lines.append(f"     🆕 Новые колонки: {', '.join(new_cols)}")
        if not deleted and (inserted == 0 and dups == 0):
            self.lines.append(f"     ⚠️ Ничего не загружено, файл сохранён")
        if not deleted and new_cols:
            self.lines.append(f"     ⚠️ Файл не удалён из-за новых колонок")

    def totals(self, configs, total_rows, errors):
        elapsed = (now_msk() - self.start_time).total_seconds()
        self.lines.append(f"\n---\n## 📋 ИТОГИ\n⏱ {elapsed:.1f}с  |  📋 конфигов: {configs}  |  📥 строк: {total_rows}  |  ошибок: {errors}")
        status = "✅ УСПЕШНО" if errors == 0 else f"⚠️ ЗАВЕРШЕНО С ОШИБКАМИ ({errors})"
        self.lines.append(f"\n**{status}**\n")

    def flush(self):
        with open(self.log_path, "w", encoding="utf-8") as f:
            f.write("\n".join(self.lines))

class BaserowClient:
    def __init__(self, url, email, password):
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

    def _req(self, method, url, **kwargs):
        kwargs.setdefault("timeout", 60)
        kwargs.setdefault("headers", self.headers)
        resp = requests.request(method, url, **kwargs)
        if resp.status_code == 401:
            self._authenticate()
            kwargs["headers"] = self.headers
            resp = requests.request(method, url, **kwargs)
        return resp

    def get_or_create_workspace(self, name):
        resp = self._req("GET", f"{self.url}/api/workspaces/")
        resp.raise_for_status()
        for ws in resp.json():
            if ws["name"] == name:
                return ws["id"]
        resp = self._req("POST", f"{self.url}/api/workspaces/", json={"name": name})
        resp.raise_for_status()
        logger.info(f"Workspace создан: {name}")
        return resp.json()["id"]

    def get_or_create_database(self, workspace_id, name):
        resp = self._req("GET", f"{self.url}/api/applications/workspace/{workspace_id}/")
        resp.raise_for_status()
        for app in resp.json():
            if app.get("type") == "database" and app["name"] == name:
                return app["id"]
        resp = self._req("POST", f"{self.url}/api/applications/workspace/{workspace_id}/", json={"type": "database", "name": name})
        resp.raise_for_status()
        logger.info(f"БД создана: {name}")
        return resp.json()["id"]

    def get_or_create_table(self, database_id, name):
        resp = self._req("GET", f"{self.url}/api/database/tables/database/{database_id}/")
        resp.raise_for_status()
        for t in resp.json():
            if t["name"] == name:
                return t["id"]
        resp = self._req("POST", f"{self.url}/api/database/tables/database/{database_id}/", json={"name": name})
        resp.raise_for_status()
        logger.info(f"Таблица создана: {name}")
        return resp.json()["id"]

    def get_fields(self, table_id):
        resp = self._req("GET", f"{self.url}/api/database/fields/table/{table_id}/")
        resp.raise_for_status()
        return {f["name"]: f for f in resp.json()}

    def create_field(self, table_id, field_name, field_type):
        clean_name = field_name.replace(".", "_").replace("/", "_").replace(" ", "_")
        if clean_name in ("id", "order", "created_on", "updated_on"):
            clean_name = f"row_{clean_name}"
        type_map = {"integer": "number", "number": "number", "date": "date", "text": "text", "long_text": "long_text"}
        bt = type_map.get(field_type, "text")
        payload = {"name": clean_name, "type": bt}
        if bt == "number":
            payload["number_negative"] = True
            payload["number_decimal_places"] = 0 if field_type == "integer" else 2
        resp = self._req("POST", f"{self.url}/api/database/fields/table/{table_id}/", json=payload)
        if resp.status_code == 409:
            logger.warning(f"Поле {clean_name} уже существует")
            return None
        resp.raise_for_status()
        logger.info(f"Создано поле: {clean_name} ({bt})")
        return resp.json()["id"]

    def ensure_field(self, table_id, field_name, field_type):
        clean_name = field_name.replace(".", "_").replace("/", "_").replace(" ", "_")
        if clean_name in ("id", "order", "created_on", "updated_on"):
            clean_name = f"row_{clean_name}"
        existing = self.get_fields(table_id)
        if clean_name not in existing:
            self.create_field(table_id, clean_name, field_type)

    def get_existing_hashes(self, table_id):
        hashes = set()
        page = 1
        while True:
            resp = self._req("GET", f"{self.url}/api/database/rows/table/{table_id}/", params={"page": page, "size": 200, "user_field_names": "true"})
            resp.raise_for_status()
            data = resp.json()
            for row in data["results"]:
                h = row.get("hash")
                if h:
                    hashes.add(h)
            if not data.get("next"):
                break
            page += 1
        logger.info(f"Загружено {len(hashes)} хешей")
        return hashes

    def insert_rows(self, table_id, rows):
        if not rows:
            return 0
        total = 0
        for i in range(0, len(rows), 200):
            batch = rows[i:i+200]
            resp = self._req("POST", f"{self.url}/api/database/rows/table/{table_id}/batch/", params={"user_field_names": "true"}, json={"items": batch})
            if resp.status_code == 200:
                total += len(resp.json().get("items", []))
            else:
                logger.error(f"Ошибка вставки: {resp.status_code} {resp.text[:200]}")
                raise Exception(resp.text)
        return total

# ===== GOOGLE DRIVE (Service Account — не протухает) =====
def get_drive_service():
    from googleapiclient.discovery import build
    from google.oauth2 import service_account

    SCOPES = ['https://www.googleapis.com/auth/drive']
    creds = service_account.Credentials.from_service_account_file(
        str(SERVICE_ACCOUNT_PATH), scopes=SCOPES
    )
    return build('drive', 'v3', credentials=creds)

def list_drive_files(service, folder_id):
    query = f"'{folder_id}' in parents and trashed = false"
    return service.files().list(q=query, fields="files(id, name)").execute().get('files', [])

def download_drive_file(service, file_id, dest):
    """Скачивает или экспортирует файл с Google Диска."""
    # Определяем MIME-тип — Google Sheets/Docs требуют export, не download
    meta = service.files().get(fileId=file_id, fields="mimeType").execute()
    mime = meta.get("mimeType", "")
    if mime == "application/vnd.google-apps.spreadsheet":
        request = service.files().export_media(
            fileId=file_id,
            mimeType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        request = service.files().get_media(fileId=file_id)
    with open(dest, 'wb') as f:
        f.write(request.execute())

def resolve_drive_folder(service, folder_path: str) -> str:
    """Возвращает ID папки по пути. Ищет глобально — работает с расшаренными папками."""
    parts = folder_path.strip('/').split('/')
    parent_id = 'root'
    for i, part in enumerate(parts):
        # Сначала ищем как вложенную в parent
        q = f"'{parent_id}' in parents and name='{part}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
        results = service.files().list(q=q, fields="files(id)").execute().get('files', [])
        # Если не нашли — ищем глобально (для расшаренных папок)
        if not results:
            q = f"name='{part}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
            results = service.files().list(q=q, fields="files(id)").execute().get('files', [])
        if not results:
            raise FileNotFoundError(f"Папка не найдена: {part} в пути {folder_path}")
        parent_id = results[0]['id']
    return parent_id

def find_drive_file(service, folder_id, file_name):
    # Сначала ищем в указанной папке
    q = f"'{folder_id}' in parents and name='{file_name}' and trashed=false"
    results = service.files().list(q=q, fields="files(id)").execute().get('files', [])
    # Если не нашли — ищем глобально (для расшаренных файлов)
    if not results:
        q = f"name='{file_name}' and trashed=false"
        results = service.files().list(q=q, fields="files(id)").execute().get('files', [])
    if not results:
        raise FileNotFoundError(f"Файл '{file_name}' не найден")
    return results[0]['id']

# ===== ОПРЕДЕЛЕНИЕ ТИПА (ИСПРАВЛЕНО) =====

# Pure number patterns: integer or decimal (with comma/dot)
# "12", "285", "285,0", "25,90", "285.0" → NOT dates
_NUMBER_RE = re.compile(r'^-?\d+$|^-?\d+[.,]\d+$')

def is_date_string(s):
    """Фильтр: не считаем датой числа и денежные/процентные строки"""
    s_stripped = str(s).strip()
    # 1. Reject currency/percent symbols
    if any(ch in s_stripped for ch in ['₽', 'руб', 'RUB', '%']):
        return False
    # 2. Reject pure numbers (dateparser parses "12" → 2026-05-12, "25,90" → 1990-05-25)
    if _NUMBER_RE.match(s_stripped):
        return False
    # 3. Only accept if dateparser returns a non-None result
    try:
        result = dateparser.parse(s_stripped)
        return result is not None
    except:
        return False

def guess_field_type(series: pd.Series) -> str:
    non_null = series.dropna()
    if len(non_null) == 0:
        return "text"
    # Числовая проверка (с поддержкой русской десятичной запятой)
    numeric_vals = pd.to_numeric(non_null, errors='coerce')
    numeric_ratio = numeric_vals.notna().sum() / len(non_null)
    # Если стандартное преобразование не сработало — пробуем заменить запятую на точку
    if numeric_ratio < 0.8:
        converted = non_null.astype(str).str.replace(',', '.')
        numeric_vals2 = pd.to_numeric(converted, errors='coerce')
        ratio2 = numeric_vals2.notna().sum() / len(non_null)
        if ratio2 > numeric_ratio:
            numeric_vals = numeric_vals2
            numeric_ratio = ratio2
    if numeric_ratio >= 0.8:
        try:
            if (numeric_vals == numeric_vals.astype(int)).all():
                return "integer"
        except:
            pass
        return "number"
    # Проверка на дату с фильтром
    date_count = 0
    for v in non_null.head(200):
        if isinstance(v, datetime):
            date_count += 1
        elif isinstance(v, str):
            if is_date_string(v):
                date_count += 1
    if date_count >= 0.8 * min(200, len(non_null)):
        return "date"
    return "text"

def normalize_value(value, field_type):
    if pd.isna(value) or value is None:
        return None
    if field_type in ("text", "long_text"):
        return str(value).strip()
    if field_type in ("integer", "number"):
        try:
            s = str(value).replace(',', '.')
            n = pd.to_numeric(s)
            if pd.isna(n):
                return None
            if field_type == "integer":
                return int(n)
            return round(float(n), 2)
        except:
            return None
    if field_type == "date":
        if isinstance(value, datetime):
            return value.strftime("%Y-%m-%d")
        try:
            dt = dateparser.parse(str(value))
            return dt.strftime("%Y-%m-%d") if dt else None
        except:
            return None
    return None

def _fix_excel_headers(df, file_path, sheet_name):
    """Detect and fix multilevel/VTB headers in Excel sheets."""
    sheet_label = f" (лист '{sheet_name}')" if sheet_name and isinstance(sheet_name, str) else ""

    # Case 1: VTB bank statement (col 0 = "ВЫПИСКА", real headers at row 6)
    # Check this FIRST — VTB sheets also have many Unnamed columns
    if len(df.columns) > 0 and str(df.columns[0]) == "ВЫПИСКА":
        logger.info("  VTB header detected%s, re-reading with header=6", sheet_label)
        df = pd.read_excel(file_path, sheet_name=sheet_name, dtype=str, header=6, skipfooter=1)
        df = df.dropna(how="all")
        return df

    # Case 2: Upravlenka ("УПРАВЛЕНЧЕСКИЙ" appears as a column name, real headers at row 2)
    cols_text = " ".join(str(c) for c in df.columns[:15])
    if "УПРАВЛЕНЧЕСКИЙ" in cols_text:
        logger.info("  Upravlenka header detected%s, re-reading with header=2", sheet_label)
        df = pd.read_excel(file_path, sheet_name=sheet_name, dtype=str, header=2)
        df = df.dropna(how="all")
        return df

    # Case 2: Multilevel header (ozon_internal: row 0 = report period, rest Unnamed)
    unnamed_count = sum(1 for c in df.columns if str(c).startswith("Unnamed:"))
    if unnamed_count > len(df.columns) * 0.5 and len(df) > 0:
        logger.info("  Multilevel header detected%s (%d/%d Unnamed), re-reading with header=1",
                    sheet_label, unnamed_count, len(df.columns))
        df = pd.read_excel(file_path, sheet_name=sheet_name, dtype=str, header=1)
        df = df.dropna(how="all")
        return df

    return df

def process_config(config, client, status, drive_service):
    source = config["source_type"]
    db_name = config["database"]
    table_name = config["table_name"]
    hash_fields = config["hash_fields"]
    defaults = config.get("defaults", {})
    delete_after = config.get("delete_after_upload", False)
    incremental = config.get("incremental", False)
    file_filter = config.get("file_filter", None)
    sheet_name = config.get("sheet_name", 0)
    skip_sheets = config.get("skip_sheets", [])

    status.config_info(config.get("_filename", ""), db_name, table_name, config["path"])

    ws_id = client.get_or_create_workspace(db_name)
    db_id = client.get_or_create_database(ws_id, db_name)
    table_id = client.get_or_create_table(db_id, table_name)

    existing_hashes = client.get_existing_hashes(table_id) if (incremental or hash_fields) else set()

    files = []
    if source == "google_drive":
        try:
            raw_path = config["path"]
            # Определяем, файл или папка
            if raw_path.endswith(".xls") or raw_path.endswith(".xlsx"):
                folder_part = "/".join(raw_path.split("/")[:-1])
                file_part = raw_path.split("/")[-1]
                folder_id = resolve_drive_folder(drive_service, folder_part)
                file_id = find_drive_file(drive_service, folder_id, file_part)
                files.append(("drive", file_id, file_part))
            else:
                folder_id = resolve_drive_folder(drive_service, raw_path)
                for f in list_drive_files(drive_service, folder_id):
                    if file_filter:
                        if '*' in file_filter:
                            if not f["name"].endswith(file_filter.replace("*", "")):
                                continue
                        elif f["name"] != file_filter:
                            continue
                    files.append(("drive", f["id"], f["name"]))
        except Exception as e:
            logger.error(f"Ошибка Google Диска: {e}")
            status.error(str(e))
            return 0
    else:
        local_path = Path(config["path"])
        if local_path.is_file():
            files.append(("local", str(local_path), local_path.name))
        else:
            pattern = file_filter if file_filter else "*.*"
            for f in local_path.glob(pattern):
                if f.is_file():
                    files.append(("local", str(f), f.name))

    total_inserted = 0
    for src_type, src_id, fname in files:
        logger.info(f"Обработка: {fname}")
        try:
            if src_type == "drive":
                safe_fname = fname.replace("/", "_")
                tmp = LOG_DIR / safe_fname
                download_drive_file(drive_service, src_id, tmp)
                file_path = tmp
            else:
                file_path = Path(src_id)

            if file_path.suffix.lower() == ".csv":
                df = pd.read_csv(file_path, dtype=str)
            else:
                sheets_raw = pd.read_excel(file_path, sheet_name=sheet_name, dtype=str)
                if isinstance(sheets_raw, dict):
                    # Multi-sheet: process each sheet individually, skip unwanted sheets
                    dfs = []
                    for sname, sdf in sheets_raw.items():
                        if any(sname.startswith(sk) for sk in skip_sheets):
                            logger.info("  Skipping sheet '%s'", sname)
                            continue
                        sdf = _fix_excel_headers(sdf, file_path, sname)
                        if sdf is not None:
                            dfs.append(sdf)
                    df = pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()
                else:
                    df = _fix_excel_headers(sheets_raw, file_path, sheet_name)

            field_types = {}
            for col in df.columns:
                if col in ("hash",):
                    continue
                ft = guess_field_type(df[col])
                field_types[col] = ft
                logger.info(f"  Столбец '{col}' → тип {ft}")

            for col, ftype in field_types.items():
                client.ensure_field(table_id, col, ftype)
            # Always ensure hash field exists for deduplication
            client.ensure_field(table_id, "hash", "text")
            for dcol, dval in defaults.items():
                if isinstance(dval, int): dt = "integer"
                elif isinstance(dval, float): dt = "number"
                elif isinstance(dval, bool): dt = "boolean"
                else: dt = "text"
                client.ensure_field(table_id, dcol, dt)

            records = []
            for _, row in df.iterrows():
                rec = {}
                for col, ftype in field_types.items():
                    val = normalize_value(row[col], ftype)
                    clean_col = col.replace(".", "_").replace("/", "_").replace(" ", "_")
                    if clean_col in ("id", "order", "created_on", "updated_on"):
                        clean_col = f"row_{clean_col}"
                    if val is not None:
                        rec[clean_col] = val
                for dcol, dval in defaults.items():
                    clean_dcol = dcol.replace(".", "_").replace("/", "_").replace(" ", "_")
                    rec[clean_dcol] = dval
                hash_str = ""
                for hf in hash_fields:
                    if hf in df.columns:
                        raw = row[hf]
                        hash_str += str(raw) if pd.notna(raw) else ""
                    elif hf in defaults:
                        hash_str += str(defaults[hf])
                    hash_str += "|"
                rec["hash"] = hashlib.md5(hash_str.encode()).hexdigest()
                records.append(rec)

            new_records = []
            dup_count = 0
            seen = set()
            for rec in records:
                h = rec["hash"]
                if h in existing_hashes or h in seen:
                    dup_count += 1
                else:
                    new_records.append(rec)
                    seen.add(h)

            inserted = 0
            if new_records:
                inserted = client.insert_rows(table_id, new_records)
                existing_hashes.update(seen)

            existing_fields = set(client.get_fields(table_id).keys())
            new_cols = [col for col in field_types if col not in existing_fields]
            can_delete = delete_after and (inserted > 0 or dup_count > 0) and not new_cols
            if can_delete:
                if src_type == "local":
                    os.unlink(src_id)
                else:
                    drive_service.files().delete(fileId=src_id).execute()
                logger.info(f"Файл удалён: {fname}")

            status.file_processed(fname, len(records), inserted, dup_count, new_cols, can_delete)
            total_inserted += inserted

            if src_type == "drive":
                tmp.unlink()
        except Exception as e:
            logger.exception(f"Ошибка в файле {fname}: {e}")
            status.error(f"{fname}: {e}")

    return total_inserted

def main():
    logger.info("=== Запуск finance_loader ===")
    status = StatusLogger(STATUS_LOG)

    if not BASEROW_EMAIL or not BASEROW_PASSWORD:
        logger.error("BASEROW_EMAIL/PASSWORD не заданы")
        sys.exit(1)
    client = BaserowClient(BASEROW_URL, BASEROW_EMAIL, BASEROW_PASSWORD)

    config_files = list(CONFIGS_DIR.glob("*.json"))
    has_drive = any(json.load(open(cf)).get("source_type") == "google_drive" for cf in config_files)
    drive_service = None
    if has_drive:
        try:
            drive_service = get_drive_service()
            logger.info("Google Диск готов")
        except Exception as e:
            logger.error(f"Google авторизация: {e}")
            status.error(f"Google Drive: {e}")

    total_configs = len(config_files)
    total_rows = 0
    errors = 0
    for cf in config_files:
        with open(cf) as f:
            config = json.load(f)
        config["_filename"] = cf.name
        try:
            rows = process_config(config, client, status, drive_service)
            total_rows += rows
        except Exception as e:
            logger.exception(f"Конфиг {cf.name}: {e}")
            status.error(f"{cf.name}: {e}")
            errors += 1

    status.totals(total_configs, total_rows, errors)
    status.flush()
    logger.info("=== Завершено ===")

if __name__ == "__main__":
    main()
