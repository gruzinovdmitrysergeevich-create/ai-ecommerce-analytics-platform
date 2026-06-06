#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Валидатор конфигураций, использующий логику universal_loader для точной проверки.
"""
import sys, json, argparse
from pathlib import Path
from datetime import datetime, timedelta, timezone
from typing import Set, List, Dict, Any

# Добавляем src в sys.path для импорта из universal_loader
sys.path.insert(0, str(Path(__file__).parent))
from universal_loader import (
    build_api_headers,
    _fetch_single_period,
    extract_items_from_response,
    CONFIGS_DIR,
    MSK,
    now_msk,
    load_dotenv,
    ENV_PATH
)

load_dotenv(ENV_PATH)

def get_all_fields_from_items(items: List[Dict], prefix: str = "") -> Set[str]:
    fields = set()
    for item in items:
        if isinstance(item, dict):
            for k, v in item.items():
                full_key = f"{prefix}.{k}" if prefix else k
                fields.add(full_key)
                if isinstance(v, dict):
                    fields.update(get_all_fields_from_items([v], full_key))
                elif isinstance(v, list) and v and isinstance(v[0], dict):
                    fields.update(get_all_fields_from_items(v, full_key))
    return fields

def diagnose_config(config_path: Path) -> bool:
    with open(config_path, "r", encoding="utf-8") as f:
        cfg = json.load(f)

    service = "wildberries" if "wildberries" in str(config_path) else "ozon"
    report_name = cfg["report_name"]
    headers = build_api_headers(service, cfg["api_key_env"])
    if not headers:
        print(f"❌ {config_path.name}: нет учётных данных")
        return False

    # Определяем короткий период для проверки (как в загрузчике)
    to_date = now_msk()
    if cfg.get("split_by_month"):
        to_date = to_date.replace(day=1) - timedelta(days=1)
        from_date = to_date.replace(day=1)
    else:
        from_date = to_date - timedelta(days=3)

    from_str = from_date.strftime("%Y-%m-%d")
    to_str = to_date.strftime("%Y-%m-%d")

    print(f"\n🔍 Диагностика {config_path.name} ({from_str} — {to_str})")

    try:
        raw_data = _fetch_single_period(cfg, service, from_str, to_str)
    except Exception as e:
        print(f"   ❌ Ошибка выполнения запроса: {e}")
        return False

    if not raw_data:
        print(f"   ⚠️ Нет данных за выбранный период")
        return True  # не ошибка конфига, просто нет данных

    actual_fields = get_all_fields_from_items(raw_data)
    expected_fields = set(cfg["field_mapping"].keys())
    missing = expected_fields - actual_fields

    print(f"   📊 Получено записей: {len(raw_data)}")
    print(f"   📋 Ожидаемых полей: {len(expected_fields)}")
    print(f"   ✅ Найдено полей: {len(actual_fields)}")

    if missing:
        print(f"   ❌ Отсутствуют поля ({len(missing)}):")
        for f in sorted(missing)[:10]:
            print(f"      - {f}")
        if len(missing) > 10:
            print(f"      ... и ещё {len(missing)-10}")
        return False
    else:
        print(f"   ✅ Все ожидаемые поля присутствуют")
        return True

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--config", type=str)
    args = parser.parse_args()

    if args.config:
        files = [Path(args.config)]
    elif args.all:
        files = []
        for svc in ["wildberries", "ozon"]:
            d = CONFIGS_DIR / svc
            if d.exists():
                files.extend(sorted(d.glob("*.json")))
    else:
        print("Укажите --all или --config")
        sys.exit(1)

    all_ok = True
    for f in files:
        ok = diagnose_config(f)
        if not ok:
            all_ok = False

    sys.exit(0 if all_ok else 1)

if __name__ == "__main__":
    main()
