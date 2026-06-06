#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Управление загрузчиками данных (WB, Ozon, Bank, Aggregator).
Парсит реальные логи из директорий проектов.
"""

import os
import subprocess
import sys
import re
from datetime import datetime
from typing import List, Dict, Any

ANALYTICS_DIR = os.path.expanduser("~/my-ai-stack/analytics")
PROJECTS_DIR = os.path.expanduser("~/my-ai-stack/projects")
LOG_DIR = os.path.expanduser("~/my-ai-stack/ui-dashboard/logs")
os.makedirs(LOG_DIR, exist_ok=True)

LOADER_REGISTRY = [
    {
        "id": "api_loader",
        "name": "Универсальный загрузчик API",
        "icon": "🛰️",
        "description": "WB + Ozon · Сырые данные",
        "script": os.path.join(PROJECTS_DIR, "universal-api-loader/src/universal_loader.py"),
        "args": [],
        "cwd": os.path.join(PROJECTS_DIR, "universal-api-loader"),
        "log_dir": os.path.join(PROJECTS_DIR, "universal-api-loader/logs"),
        "status_file": os.path.join(PROJECTS_DIR, "universal-api-loader/logs/status.md"),
        "log_files": ["loader.log"],
    },
    {
        "id": "fin_loader",
        "name": "Загрузчик фин. документов",
        "icon": "🏦",
        "description": "Банк + Выгрузки + Счета",
        "script": os.path.join(PROJECTS_DIR, "finance-loader/src/finance_loader.py"),
        "args": [],
        "cwd": os.path.join(PROJECTS_DIR, "finance-loader"),
        "log_dir": os.path.join(PROJECTS_DIR, "finance-loader/logs"),
        "status_file": os.path.join(PROJECTS_DIR, "finance-loader/logs/status.md"),
        "log_files": [],
    },
    {
        "id": "aggregator",
        "name": "Агрегатор",
        "icon": "🧮",
        "description": "WB + Ozon + Finance → Baserow",
        "script": os.path.join(PROJECTS_DIR, "aggregator/src/aggregator.py"),
        "args": [],
        "cwd": os.path.join(PROJECTS_DIR, "aggregator"),
        "log_dir": os.path.join(PROJECTS_DIR, "aggregator/logs"),
        "status_file": None,
        "log_files": [],
    },
]


def _parse_status_md(path: str) -> Dict[str, Any]:
    """Парсит status.md и возвращает структурированную инфу."""
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
    except:
        return {}

    result = {
        "timestamp": "",
        "reports": [],
        "loaded_total": 0,
        "duplicates_total": 0,
        "errors_total": 0,
        "runtime": "",
        "status": "unknown",
    }

    # Дата запуска
    m = re.search(r"(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})", text)
    if m:
        result["timestamp"] = m.group(1)

    # Статус
    if "УСПЕШНО" in text or "SUCCESS" in text:
        result["status"] = "success"
    elif "ОШИБКА" in text or "ERROR" in text:
        result["status"] = "error"

    # Итоги
    m = re.search(r"Время выполнения:\s*([\d.]+)с", text)
    if m:
        result["runtime"] = f"{m.group(1)}с"

    m = re.search(r"Строк загружено:\s*(\d+)", text)
    if m:
        result["loaded_total"] = int(m.group(1))

    # Отчёты (для universal-api-loader)
    report_pattern = re.compile(
        r"(?:✅|❌|⚠️)\s*Отчёт:\s*\*?\*?(\w[\w_]*)\*?\*?\s*→.*?"
        r"Получено:\s*(\d+)\s*записей.*?"
        r"(?:Загружено новых:\s*(\d+).*?)?"
        r"(?:Дубликатов отфильтровано:\s*(\d+))?",
        re.DOTALL,
    )
    for m in report_pattern.finditer(text):
        report = {
            "name": m.group(1),
            "received": int(m.group(2) or 0),
            "loaded": int(m.group(3) or 0),
            "duplicates": int(m.group(4) or 0),
        }
        result["reports"].append(report)
        result["loaded_total"] += report["loaded"]
        result["duplicates_total"] += report["duplicates"]

    # Для finance-loader
    file_pattern = re.compile(
        r"📥\s*Файл:\s*(.+?)\s*–\s*строк:\s*(\d+),\s*загружено:\s*(\d+),\s*дубликатов:\s*(\d+)"
    )
    for m in file_pattern.finditer(text):
        report = {
            "name": m.group(1).strip(),
            "received": int(m.group(2)),
            "loaded": int(m.group(3)),
            "duplicates": int(m.group(4)),
        }
        # Не дублируем если уже есть отчёты
        if not result["reports"]:
            result["reports"].append(report)
        result["loaded_total"] += report["loaded"]
        result["duplicates_total"] += report["duplicates"]

    # Итоги finance-loader
    m = re.search(r"⏱\s*([\d.]+)с", text)
    if m and not result["runtime"]:
        result["runtime"] = f"{m.group(1)}с"
    m = re.search(r"строк:\s*(\d+)", text)
    if m and not result["loaded_total"]:
        result["loaded_total"] = int(m.group(1))
    m = re.search(r"ошибок:\s*(\d+)", text)
    if m:
        result["errors_total"] = int(m.group(1))

    return result


def _parse_aggregator_log(log_path: str) -> Dict[str, Any]:
    """Парсит лог агрегатора."""
    if not os.path.exists(log_path):
        return {}
    try:
        with open(log_path, "r", encoding="utf-8") as f:
            text = f.read()
    except:
        return {}

    result = {
        "timestamp": "",
        "aggregations": [],
        "loaded_total": 0,
        "runtime": "",
        "status": "success",
    }

    m = re.search(r"(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})", text)
    if m:
        result["timestamp"] = m.group(1)

    # Агрегации
    agg_pattern = re.compile(
        r"Агрегация\s*'(\w+)'\s*завершена\.\s*Загружено\s*(\d+)\s*записей"
    )
    for m in agg_pattern.finditer(text):
        result["aggregations"].append({"table": m.group(1), "rows": int(m.group(2))})
        result["loaded_total"] += int(m.group(2))

    return result


def _find_latest_log(log_dir: str, prefix: str = "run") -> str:
    """Находит последний лог-файл в директории."""
    if not os.path.isdir(log_dir):
        return ""
    files = [f for f in os.listdir(log_dir) if f.startswith(prefix) and f.endswith((".log", ".md"))]
    if not files:
        return ""
    files.sort(reverse=True)
    return os.path.join(log_dir, files[0])


def get_loader_status(loader_id: str) -> Dict[str, Any]:
    """Структурированный статус загрузчика из реальных логов."""
    loader = next((l for l in LOADER_REGISTRY if l["id"] == loader_id), None)
    if not loader:
        return {"error": f"Загрузчик {loader_id} не найден", "loaded": 0, "duplicates": 0, "runtime": "", "last_run": "Никогда"}

    result = {
        "loaded": 0,
        "duplicates": 0,
        "errors": 0,
        "runtime": "",
        "last_run": "Никогда",
    }

    # Пробуем status.md (universal-api-loader, finance-loader)
    status_file = loader.get("status_file", "")
    if status_file and os.path.exists(status_file):
        parsed = _parse_status_md(status_file)
        result["loaded"] = parsed.get("loaded_total", 0)
        result["duplicates"] = parsed.get("duplicates_total", 0)
        result["errors"] = parsed.get("errors_total", 0)
        result["runtime"] = parsed.get("runtime", "")
        result["last_run"] = parsed.get("timestamp", "Никогда")
        result["reports"] = parsed.get("reports", [])
        return result

    # Пробуем run_*.log (aggregator, finance-loader)
    log_dir = loader.get("log_dir", "")
    if log_dir:
        latest = _find_latest_log(log_dir, "run")
        if latest:
            parsed = _parse_aggregator_log(latest)
            result["loaded"] = parsed.get("loaded_total", 0)
            result["runtime"] = ""
            result["last_run"] = parsed.get("timestamp", "Никогда")
            result["aggregations"] = parsed.get("aggregations", [])
            return result

    # Fallback: loader.log (universal-api-loader)
    if log_dir:
        for lf in loader.get("log_files", []):
            fp = os.path.join(log_dir, lf)
            if os.path.exists(fp):
                result["last_run"] = datetime.fromtimestamp(os.path.getmtime(fp)).strftime("%Y-%m-%d %H:%M")
                # Грубая оценка размера
                size_kb = os.path.getsize(fp) // 1024
                result["log_size"] = f"{size_kb} КБ"
                return result

    return result


def list_loaders() -> List[Dict[str, Any]]:
    """Список загрузчиков с метаданными о последнем запуске."""
    result = []
    for loader in LOADER_REGISTRY:
        entry = dict(loader)
        status = get_loader_status(loader["id"])
        entry["last_run"] = status.get("last_run", "Никогда")
        entry["last_loaded"] = status.get("loaded", 0)
        entry["last_duplicates"] = status.get("duplicates", 0)
        entry["runtime"] = status.get("runtime", "")
        entry["log_size"] = status.get("log_size", "")
        result.append(entry)
    return result


def run_loader(loader_id: str) -> str:
    """Запуск загрузчика по id."""
    loader = next((l for l in LOADER_REGISTRY if l["id"] == loader_id), None)
    if not loader:
        return f"Загрузчик {loader_id} не найден"

    script_path = loader["script"]
    if not os.path.exists(script_path):
        return f"Скрипт не найден: {script_path}"

    log_file = os.path.join(LOG_DIR, f"loader_{loader_id}.log")
    venv_python = os.path.join(ANALYTICS_DIR, "venv", "bin", "python")
    if not os.path.exists(venv_python):
        venv_python = sys.executable

    cmd = [venv_python, script_path] + loader.get("args", [])
    cwd = loader.get("cwd", os.path.dirname(script_path))

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"\n{'='*60}\n[{timestamp}] Запуск {loader['name']}\n")
        f.write(f"CMD: {' '.join(cmd)}\n")
        f.write(f"CWD: {cwd}\n")

    try:
        p = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            cwd=cwd,
            text=True,
            encoding="utf-8",
        )
        stdout_lines = []
        try:
            for line in p.stdout:
                stdout_lines.append(line)
                with open(log_file, "a", encoding="utf-8") as f:
                    f.write(line)
            p.wait(timeout=300)
            rc = p.returncode
        except subprocess.TimeoutExpired:
            p.kill()
            rc = -1
            stdout_lines.append("[TIMEOUT] Превышено время ожидания (5 мин)\n")

        stdout_text = "".join(stdout_lines)
        end_ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"[{end_ts}] Завершено с кодом {rc}\n")

        if rc == 0:
            return f"Завершено успешно"
        else:
            return f"Ошибка (code {rc})"
    except Exception as e:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"[EXCEPTION] {e}\n")
        return f"Исключение: {e}"


def get_loader_logs(loader_id: str, tail: int = 100) -> str:
    """Получить последние строки лога загрузчика из реальной директории."""
    loader = next((l for l in LOADER_REGISTRY if l["id"] == loader_id), None)
    if not loader:
        return "Загрузчик не найден."

    # Сначала пробуем status.md
    status_file = loader.get("status_file", "")
    if status_file and os.path.exists(status_file):
        try:
            with open(status_file, "r", encoding="utf-8") as f:
                content = f.read()
            # Возвращаем последние N строк
            lines = content.split("\n")
            return "\n".join(lines[-tail:])
        except:
            pass

    # Затем run_*.log 
    log_dir = loader.get("log_dir", "")
    if log_dir:
        latest = _find_latest_log(log_dir, "run")
        if latest:
            try:
                with open(latest, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                return "".join(lines[-tail:])
            except:
                pass

    # Fallback: наш лог
    dashboard_log = os.path.join(LOG_DIR, f"loader_{loader_id}.log")
    if os.path.exists(dashboard_log):
        try:
            with open(dashboard_log, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
                return "".join(lines[-tail:])
        except Exception as e:
            return f"Ошибка чтения лога: {e}"

    return "Лог пока не создан."
