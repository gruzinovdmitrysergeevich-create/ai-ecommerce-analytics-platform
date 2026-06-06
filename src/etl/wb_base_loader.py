#!/usr/bin/env python3
import requests
import time
import logging
import json
from datetime import datetime, timedelta
from abc import ABC, abstractmethod
from baserow_manager import BaserowManager

logger = logging.getLogger(__name__)

class WBBaseLoader(ABC):
    # По умолчанию поле даты называется "date". Каждый загрузчик может переопределить.
    DATE_FIELD = "date"

    def __init__(self, table_id, table_name, db_token, baserow_url="http://localhost:8000", baserow_manager=None):
        self.table_id = table_id
        self.table_name = table_name
        self.db_token = db_token
        self.baserow_url = baserow_url
        self.headers = {"Authorization": f"Token {db_token}", "Content-Type": "application/json"}
        self.field_meta = self._get_field_metadata()
        self.baserow_manager = baserow_manager if baserow_manager else BaserowManager()
        
        # Автоматическая настройка числовых полей (разрешение отрицательных)
        try:
            self._ensure_numeric_fields_allow_negative()
        except Exception as e:
            logger.warning(f"Не удалось настроить числовые поля: {e}")
        
        # Автоматическая настройка ограничений полей (уникальность)
        try:
            self._ensure_field_constraints()
        except Exception as e:
            logger.warning(f"Не удалось настроить ограничения полей: {e}")

    def _get_field_metadata(self):
        url = f"{self.baserow_url}/api/database/fields/table/{self.table_id}/"
        try:
            resp = requests.get(url, headers=self.headers, timeout=10)
            if resp.status_code == 200:
                fields = resp.json()
                meta = {}
                for f in fields:
                    meta[f['name']] = {
                        'type': f['type'],
                        'decimal_places': f.get('number_decimal_places', 0)
                    }
                logger.info(f"📋 Загружены метаданные для {len(meta)} полей таблицы {self.table_id}")
                return meta
            else:
                logger.error(f"Не удалось получить метаданные таблицы: {resp.status_code}")
                return {}
        except Exception as e:
            logger.error(f"Ошибка получения метаданных: {e}")
            return {}

    def _format_value(self, value, field_name):
        if field_name not in self.field_meta:
            return value
        meta = self.field_meta[field_name]
        if meta['type'] == 'number':
            try:
                num = float(value) if value is not None else 0.0
                decimals = meta['decimal_places']
                if decimals == 0:
                    return int(round(num))
                else:
                    return round(num, decimals)
            except:
                return 0 if decimals == 0 else 0.0
        elif meta['type'] in ('text', 'long_text'):
            return str(value) if value is not None else ""
        elif meta['type'] == 'boolean':
            return bool(value)
        elif meta['type'] == 'date':
            if isinstance(value, str) and len(value) >= 10:
                return value[:10]
            return None
        else:
            return value

    def is_baserow_available(self):
        try:
            resp = requests.get(f"{self.baserow_url}/api/database/rows/table/{self.table_id}/", 
                                 headers=self.headers, params={"size": 1}, timeout=5)
            return resp.status_code == 200
        except:
            return False

    def get_last_date(self):
        """Возвращает максимальную дату из поля DATE_FIELD в таблице."""
        url = f"{self.baserow_url}/api/database/rows/table/{self.table_id}/"
        params = {"order_by": f"-{self.DATE_FIELD}", "size": 1, "user_field_names": "true"}
        try:
            resp = requests.get(url, headers=self.headers, params=params, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                if data.get("results"):
                    dt = data["results"][0].get(self.DATE_FIELD)
                    if dt and isinstance(dt, str) and len(dt) >= 10:
                        return dt[:10]
            return "2026-01-01"
        except Exception as e:
            logger.error(f"Ошибка получения последней даты из {self.DATE_FIELD}: {e}")
            return "2026-01-01"

    @abstractmethod
    def fetch_data_for_date(self, date):
        pass

    @abstractmethod
    def transform_row(self, raw_row):
        pass

    def _ensure_field_constraints(self):
        target_fields = None
        for table_name, fields in self.baserow_manager.tables.items():
            if table_name == self.table_name:
                target_fields = fields
                break
        
        if not target_fields:
            logger.warning(f"Эталонное описание для таблицы {self.table_name} не найдено")
            return
        
        required_unique = {}
        for f in target_fields:
            if f.get('unique'):
                required_unique[f['name']] = True
        
        if not required_unique:
            return
        
        try:
            current_fields = self.baserow_manager.get_fields(self.table_id)
        except Exception as e:
            logger.error(f"Не удалось получить текущие поля: {e}")
            return
        
        for field_name, required in required_unique.items():
            field_info = next((f for f in current_fields if f['name'] == field_name), None)
            if not field_info:
                logger.warning(f"Поле {field_name} не найдено в таблице {self.table_id}")
                continue
            
            has_constraint = False
            if 'field_constraints' in field_info:
                for constraint in field_info['field_constraints']:
                    if constraint.get('type_name') == 'unique_with_empty':
                        has_constraint = True
                        break
            
            if not has_constraint:
                logger.info(f"Включаю уникальность для поля {field_name} (ID {field_info['id']})")
                try:
                    self.baserow_manager.update_field(
                        field_info['id'], 
                        {'field_constraints': [{'type_name': 'unique_with_empty'}]}
                    )
                except Exception as e:
                    logger.error(f"Не удалось включить уникальность для поля {field_info['id']}: {e}")

    def _ensure_numeric_fields_allow_negative(self):
        try:
            fields = self.baserow_manager.get_fields(self.table_id)
        except Exception as e:
            logger.error(f"Не удалось получить список полей: {e}")
            return
        for field in fields:
            if field['type'] == 'number':
                if not field.get('negative_allowed', False):
                    logger.info(f"Разрешаю отрицательные числа для поля {field['name']} (ID {field['id']})")
                    try:
                        self.baserow_manager.update_field(field['id'], {"negative_allowed": True})
                    except Exception as e:
                        logger.error(f"Не удалось обновить поле {field['id']}: {e}")

    def _extract_field_id_from_error(self, response):
        try:
            err = response.json()
            detail = err.get("detail", {})
            if isinstance(detail, dict):
                for key in detail:
                    if key.startswith("field_"):
                        return int(key.replace("field_", ""))
            elif isinstance(detail, str):
                import re
                match = re.search(r'field[ _]?(\d+)', detail, re.IGNORECASE)
                if match:
                    return int(match.group(1))
        except:
            pass
        return None

    def _handle_field_constraint_error(self, row, field_id):
        try:
            fields = self.baserow_manager.get_fields(self.table_id)
            field_info = next((f for f in fields if f['id'] == field_id), None)
            if not field_info:
                logger.warning(f"Поле {field_id} не найдено в таблице {self.table_id}")
                return False
            if field_info['type'] == 'number':
                self.baserow_manager.update_field(field_id, {"negative_allowed": True})
                logger.info(f"✅ Поле {field_id} теперь разрешает отрицательные числа")
                return True
            return False
        except Exception as e:
            logger.error(f"❌ Не удалось изменить поле {field_id}: {e}")
            return False

    def _insert_single_rows(self, items):
        success = 0
        for idx, row in enumerate(items):
            url = f"{self.baserow_url}/api/database/rows/table/{self.table_id}/batch/?user_field_names=true"
            r = requests.post(url, headers=self.headers, json={"items": [row]}, timeout=30)
            if r.status_code == 200:
                success += 1
            else:
                # Показываем текст ошибки для понимания
                logger.warning(f"     Проблемная запись #{idx}: {r.text[:200]}")
            time.sleep(0.1)
        return success

    def upload_batch(self, rows, retry_count=1):
        if not rows:
            return 0
        url = f"{self.baserow_url}/api/database/rows/table/{self.table_id}/batch/?user_field_names=true"
        items = []
        for r in rows:
            transformed = self.transform_row(r)
            for field, value in list(transformed.items()):
                transformed[field] = self._format_value(value, field)
            items.append(transformed)

        try:
            logger.info(f"Отправляю в Baserow: {json.dumps(items, ensure_ascii=False)}")
            resp = requests.post(url, headers=self.headers, json={"items": items}, timeout=60)
            if resp.status_code == 200:
                created = resp.json().get("items", [])
                logger.info(f"  ✅ Batch: создано {len(created)} из {len(rows)}")
                return len(created)
            elif resp.status_code == 400 and retry_count > 0:
                err_text = resp.text[:500].lower()
                # Проверяем, не ошибка ли это уникальности (можно игнорировать)
                if "unique" in err_text or "field constraint" in err_text or "already exists" in err_text:
                    logger.info("  ⚠️ Ошибка уникальности (записи уже есть) — игнорирую")
                    return 0
                logger.error(f"  ❌ Ошибка 400: {resp.text[:500]}")
                field_id = self._extract_field_id_from_error(resp)
                if field_id:
                    if self._handle_field_constraint_error(None, field_id):
                        logger.info(f"  🔄 Повтор батча после изменения поля {field_id}")
                        return self.upload_batch(rows, retry_count-1)
                logger.info("  🔄 Пробую по одной...")
                return self._insert_single_rows(items)
            elif resp.status_code == 429:
                wait = int(resp.headers.get('Retry-After', 30))
                logger.warning(f"  ⏳ 429, жду {wait} сек...")
                time.sleep(wait)
                return 0
            else:
                logger.warning(f"  ❌ Ошибка {resp.status_code}: {resp.text[:200]}")
                return 0
        except Exception as e:
            logger.warning(f"  ❌ Исключение: {e}")
            return 0

    def load_dates(self, date_list):
        all_rows = []
        for d in date_list:
            logger.info(f"  📥 Загрузка {d}...")
            data = self.fetch_data_for_date(d)
            logger.info(f"     Получено {len(data)} записей")
            all_rows.extend(data)
            time.sleep(1)

        if not all_rows:
            return 0

        uploaded = 0
        for i in range(0, len(all_rows), 200):
            batch = all_rows[i:i+200]
            logger.info(f"  📦 Батч {i//200 + 1}/{(len(all_rows)-1)//200 + 1}")
            uploaded += self.upload_batch(batch)
            time.sleep(0.5)
        return uploaded
