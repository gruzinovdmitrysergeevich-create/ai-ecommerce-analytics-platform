#!/usr/bin/env python3
"""
Загрузчик внешнего трафика Ozon (vendor UTM) с агрегацией дубликатов по ключу.
Использует /api/client/vendors/statistics, возвращает Excel.
"""

import requests
import time
import logging
import json
import pandas as pd
from io import BytesIO
from collections import defaultdict
from datetime import datetime, timedelta
from wb_base_loader import WBBaseLoader
from urllib.parse import urljoin

logger = logging.getLogger(__name__)

class OzonVendorLoader(WBBaseLoader):
    TABLE_ID = None
    BASE_URL = "https://api-performance.ozon.ru"
    VENDOR_STAT_URL = "/api/client/vendors/statistics"

    HEADER_MAP = {
        'Дата': 'date',
        'Source/Medium': 'source_medium',
        'Campaign': 'campaign',
        'Content': 'content',
        'Term': 'term',
        'Тип продвигаемой страницы': None,
        'Сессии': 'sessions',
        'Переходы на карточку товара': 'product_views',
        'Добавления в корзину': 'add_to_cart',
        'Добавления в избранное': 'add_to_favorites',
        'Отказы': 'bounces',
        'Средняя длительность сессии чч:мм:сс': 'avg_session_duration_sec',
        'Заказано товаров в рамках сессии (шт.)': 'orders_session',
        'Суммарная стоимость товаров, заказанных в рамках сессии (руб.)': 'total_price_session',
        'Суммарная цена товаров, заказанных в рамках сессии (руб.)': 'total_cost_session',
        'Заказано товаров в рамках окна атрибуции (шт.)': 'orders_attribution',
        'Суммарная стоимость товаров, заказанных в рамках окна атрибуции (руб.)': 'total_price_attribution',
        'Суммарная цена товаров, заказанных в рамках окна атрибуции (руб.)': 'total_cost_attribution'
    }

    def __init__(self, auth_token, db_token):
        from baserow_manager import BaserowManager
        bm = BaserowManager()
        table_id = bm.get_table_id_by_name("ozon_utm_stats")
        if not table_id:
            logger.info("Таблица ozon_utm_stats не найдена, создаю...")
            bm.ensure_table("ozon_utm_stats", bm.tables["ozon_utm_stats"])
            table_id = bm.get_table_id_by_name("ozon_utm_stats")
        
        super().__init__(table_id, "ozon_utm_stats", db_token)
        self.auth_token = auth_token
        self.ozon_headers = {
            "Authorization": f"Bearer {auth_token}",
            "Content-Type": "application/json"
        }

    def _parse_duration(self, value):
        if pd.isna(value):
            return 0
        if isinstance(value, str) and ':' in value:
            parts = value.split(':')
            if len(parts) == 3:
                try:
                    return int(parts[0])*3600 + int(parts[1])*60 + int(parts[2])
                except:
                    return 0
        return 0

    def fetch_report(self, date_from, date_to):
        payload = {
            "dateFrom": date_from,
            "dateTo": date_to,
            "type": "TRAFFIC_SOURCES"
        }
        url = f"{self.BASE_URL}{self.VENDOR_STAT_URL}"
        try:
            resp = requests.post(url, headers=self.ozon_headers, json=payload, timeout=30)
            if resp.status_code != 200:
                logger.error(f"Ошибка запуска vendor-отчёта: {resp.text}")
                return []
            data = resp.json()
            uuid = data.get("UUID")
            if not uuid:
                logger.error("Нет UUID в ответе")
                return []
        except Exception as e:
            logger.error(f"Ошибка запроса на генерацию: {e}")
            return []

        max_attempts = 30
        attempt = 0
        while attempt < max_attempts:
            time.sleep(5)
            try:
                status_resp = requests.get(
                    f"{self.BASE_URL}/api/client/vendors/statistics/{uuid}",
                    headers=self.ozon_headers,
                    params={"vendor": "true"},
                    timeout=30
                )
                if status_resp.status_code != 200:
                    logger.error(f"Ошибка проверки статуса: {status_resp.text}")
                    break
                status_data = status_resp.json()
                state = status_data.get("state")
                if state == "OK":
                    link = status_data.get("link")
                    if link:
                        full_link = urljoin(self.BASE_URL, link)
                        return self._download_and_parse_report(full_link)
                    else:
                        logger.error("Нет ссылки на отчёт")
                        return []
                elif state in ("ERROR", "TIMEOUT", "CANCEL"):
                    logger.error(f"Ошибка формирования отчёта: {state}")
                    return []
            except Exception as e:
                logger.error(f"Ошибка при проверке статуса: {e}")
                break
            attempt += 1

        logger.error("Превышено время ожидания отчёта")
        return []

    def _download_and_parse_report(self, link):
        try:
            resp = requests.get(link, headers=self.ozon_headers, timeout=60)
            if resp.status_code != 200:
                logger.error(f"Ошибка скачивания отчёта: {resp.status_code}")
                return []

            excel_data = BytesIO(resp.content)
            df = pd.read_excel(excel_data, engine='openpyxl')
            if df.empty:
                logger.warning("Excel пуст")
                return []

            rows = df.to_dict(orient='records')
            logger.info(f"Заголовки Excel: {list(df.columns)}")
            logger.info(f"Скачано {len(rows)} строк из отчёта")
            return rows
        except Exception as e:
            logger.error(f"Ошибка при скачивании/парсинге Excel: {e}")
            return []

    def fetch_data_for_date(self, date):
        return []

    def load_dates(self, date_list):
        if not date_list:
            return 0
        start = min(date_list)
        end = max(date_list)
        logger.info(f"Загрузка внешнего трафика за период {start} - {end}")
        raw_rows = self.fetch_report(start, end)
        if not raw_rows:
            logger.warning("Нет данных за период")
            return 0

        # Агрегация данных по уникальному ключу
        aggregated = defaultdict(lambda: {
            'sessions': 0, 'product_views': 0, 'add_to_cart': 0, 'add_to_favorites': 0,
            'bounces': 0, 'avg_session_duration_sec': 0, 'orders_session': 0,
            'total_price_session': 0.0, 'total_cost_session': 0.0,
            'orders_attribution': 0, 'total_price_attribution': 0.0, 'total_cost_attribution': 0.0,
            'content': '', 'term': ''
        })

        for r in raw_rows:
            # Сначала извлекаем поля для ключа
            date_val = r.get('Дата')
            if pd.notna(date_val):
                if isinstance(date_val, (datetime, pd.Timestamp)):
                    date_str = date_val.strftime('%Y-%m-%d')
                else:
                    date_str = str(date_val)[:10]
            else:
                continue

            source_medium = str(r.get('Source/Medium', '')) if pd.notna(r.get('Source/Medium')) else ''
            campaign = str(r.get('Campaign', '')) if pd.notna(r.get('Campaign')) else ''
            unique_key = f"{date_str}_{source_medium}_{campaign}"

            # Сохраняем content и term (берём первое непустое)
            content = str(r.get('Content', '')) if pd.notna(r.get('Content')) else ''
            term = str(r.get('Term', '')) if pd.notna(r.get('Term')) else ''
            if content and not aggregated[unique_key]['content']:
                aggregated[unique_key]['content'] = content
            if term and not aggregated[unique_key]['term']:
                aggregated[unique_key]['term'] = term

            # Числовые поля суммируем
            for field in ['Сессии', 'Переходы на карточку товара', 'Добавления в корзину',
                          'Добавления в избранное', 'Отказы']:
                value = r.get(field, 0)
                try:
                    num = int(value) if pd.notna(value) else 0
                except:
                    num = 0
                key_map = {
                    'Сессии': 'sessions',
                    'Переходы на карточку товара': 'product_views',
                    'Добавления в корзину': 'add_to_cart',
                    'Добавления в избранное': 'add_to_favorites',
                    'Отказы': 'bounces'
                }
                aggregated[unique_key][key_map[field]] += num

            # Длительность сессии — берём максимальную? Или среднюю? Лучше пока просто сохраняем последнюю,
            # но в идеале нужно считать взвешенное среднее. Оставим как есть: будем обновлять, если не ноль.
            dur = r.get('Средняя длительность сессии чч:мм:сс')
            if pd.notna(dur):
                aggregated[unique_key]['avg_session_duration_sec'] = self._parse_duration(dur)

            # Заказы и суммы
            for field in ['Заказано товаров в рамках сессии (шт.)',
                          'Суммарная стоимость товаров, заказанных в рамках сессии (руб.)',
                          'Суммарная цена товаров, заказанных в рамках сессии (руб.)',
                          'Заказано товаров в рамках окна атрибуции (шт.)',
                          'Суммарная стоимость товаров, заказанных в рамках окна атрибуции (руб.)',
                          'Суммарная цена товаров, заказанных в рамках окна атрибуции (руб.)']:
                value = r.get(field, 0)
                if pd.isna(value):
                    continue
                if isinstance(value, (int, float)):
                    num = value
                else:
                    try:
                        cleaned = str(value).replace(' ', '').replace(',', '.').replace('руб', '').strip()
                        num = float(cleaned) if cleaned else 0.0
                    except:
                        num = 0.0
                key_map = {
                    'Заказано товаров в рамках сессии (шт.)': 'orders_session',
                    'Суммарная стоимость товаров, заказанных в рамках сессии (руб.)': 'total_price_session',
                    'Суммарная цена товаров, заказанных в рамках сессии (руб.)': 'total_cost_session',
                    'Заказано товаров в рамках окна атрибуции (шт.)': 'orders_attribution',
                    'Суммарная стоимость товаров, заказанных в рамках окна атрибуции (руб.)': 'total_price_attribution',
                    'Суммарная цена товаров, заказанных в рамках окна атрибуции (руб.)': 'total_cost_attribution'
                }
                aggregated[unique_key][key_map[field]] += num

        # Преобразуем агрегированные данные в записи для вставки
        records = []
        for key, agg in aggregated.items():
            date_str, source_medium, campaign = key.split('_', 2)
            record = {
                'date': date_str,
                'source_medium': source_medium,
                'campaign': campaign,
                'content': agg['content'],
                'term': agg['term'],
                'sessions': agg['sessions'],
                'product_views': agg['product_views'],
                'add_to_cart': agg['add_to_cart'],
                'add_to_favorites': agg['add_to_favorites'],
                'bounces': agg['bounces'],
                'avg_session_duration_sec': agg['avg_session_duration_sec'],
                'orders_session': agg['orders_session'],
                'total_price_session': round(agg['total_price_session'], 2),
                'total_cost_session': round(agg['total_cost_session'], 2),
                'orders_attribution': agg['orders_attribution'],
                'total_price_attribution': round(agg['total_price_attribution'], 2),
                'total_cost_attribution': round(agg['total_cost_attribution'], 2),
                'unique_key': key,
                'raw_data': ''  # можно не сохранять сырые данные, чтобы не раздувать
            }
            records.append(record)

        logger.info(f"После агрегации: {len(records)} уникальных записей")

        if not records:
            return 0

        # Вставка батчами
        inserted = 0
        for i in range(0, len(records), 200):
            batch = records[i:i+200]
            try:
                result = self.upload_batch(batch)
                inserted += result
            except Exception as e:
                logger.error(f"Ошибка при вставке батча: {e}")
        return inserted

    def transform_row(self, raw_row):
        return raw_row
