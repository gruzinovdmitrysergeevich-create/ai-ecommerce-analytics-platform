#!/usr/bin/env python3
"""
Загрузчик отчёта о реализации Ozon (версия 2).
Использует API /v2/finance/realization, возвращает JSON.
Данные за месяц, с детализацией по товарам.
Загружает отчёт только один раз для первого числа месяца.
"""

import requests
import logging
import json
from datetime import datetime
from wb_base_loader import WBBaseLoader

logger = logging.getLogger(__name__)

class OzonFinanceV2Loader(WBBaseLoader):
    TABLE_ID = None
    API_URL = "https://api-seller.ozon.ru/v2/finance/realization"
    DATE_FIELD = "month"  # поле даты в таблице (первый день месяца)

    def __init__(self, ozon_client_id, ozon_api_key, db_token):
        from baserow_manager import BaserowManager
        bm = BaserowManager()
        table_id = bm.get_table_id_by_name("ozon_finance_realization")
        if not table_id:
            logger.info("Таблица ozon_finance_realization не найдена, создаю...")
            bm.ensure_table("ozon_finance_realization", bm.tables["ozon_finance_realization"])
            table_id = bm.get_table_id_by_name("ozon_finance_realization")
        
        super().__init__(table_id, "ozon_finance_realization", db_token)
        self.ozon_client_id = ozon_client_id
        self.ozon_api_key = ozon_api_key
        self.ozon_headers = {
            "Client-Id": ozon_client_id,
            "Api-Key": ozon_api_key,
            "Content-Type": "application/json"
        }

    def fetch_data_for_date(self, date):
        """
        Загружает отчёт за месяц, соответствующий указанной дате.
        Если дата не является первым днём месяца, возвращает пустой список.
        """
        # Проверяем, является ли дата первым числом месяца
        try:
            dt = datetime.strptime(date, "%Y-%m-%d")
            if dt.day != 1:
                return []
        except:
            return []

        month = dt.month
        year = dt.year

        logger.info(f"Загружаю отчёт за {year}-{month:02d}...")

        payload = {"month": month, "year": year}
        try:
            resp = requests.post(self.API_URL, headers=self.ozon_headers, json=payload, timeout=60)
            if resp.status_code != 200:
                logger.error(f"Ошибка запроса: {resp.status_code} - {resp.text}")
                return []
            data = resp.json()
        except Exception as e:
            logger.error(f"Исключение при запросе: {e}")
            return []

        if 'result' not in data or 'rows' not in data['result']:
            logger.warning("Нет данных в ответе")
            return []

        rows = data['result']['rows']
        logger.info(f"Получено {len(rows)} строк")
        return rows

    def transform_row(self, raw_row):
        """Преобразует строку отчёта в запись для вставки."""
        month_str = raw_row.get('month')  # ожидается, что это поле уже есть? Нет, в сырых данных нет.
        # На самом деле в сыром ответе нет поля month, его нужно добавить в fetch_data_for_date.
        # Переделаем так, чтобы fetch_data_for_date возвращал список словарей, уже обогащённых month.
        # Но проще добавить month здесь, но month нужно знать.
        # Проблема: мы не знаем месяц в transform_row. Значит, нужно передавать месяц через контекст.
        # Лучше fetch_data_for_date будет возвращать готовые записи.
        # Переделаем fetch_data_for_date, чтобы он сразу формировал записи.
        # Сейчас это не так, поэтому transform_row не будет работать.
        # Придётся переделать загрузчик полностью.
        # Давай сделаем так: fetch_data_for_date будет возвращать сырые строки, но мы добавим в них поле month.
        # Для этого в fetch_data_for_date нужно знать месяц. Мы его знаем.
        # Перепишем fetch_data_for_date.

        # Оставим transform_row заглушкой, но fetch_data_for_date будет возвращать готовые записи.
        return raw_row

    def load_dates(self, date_list):
        """
        Обрабатывает список дат, но загружает отчёт только для первого числа каждого месяца.
        """
        # Собираем уникальные месяцы из списка дат
        months = set()
        for d in date_list:
            try:
                dt = datetime.strptime(d, "%Y-%m-%d")
                months.add((dt.year, dt.month))
            except:
                continue

        if not months:
            return 0

        all_records = []
        for year, month in months:
            # Формируем дату первого числа
            first_day = f"{year}-{month:02d}-01"
            logger.info(f"Загружаю отчёт за {year}-{month:02d} (первый день: {first_day})...")

            payload = {"month": month, "year": year}
            try:
                resp = requests.post(self.API_URL, headers=self.ozon_headers, json=payload, timeout=60)
                if resp.status_code != 200:
                    logger.error(f"Ошибка запроса: {resp.status_code} - {resp.text}")
                    continue
                data = resp.json()
            except Exception as e:
                logger.error(f"Исключение при запросе: {e}")
                continue

            if 'result' not in data or 'rows' not in data['result']:
                logger.warning("Нет данных в ответе")
                continue

            rows = data['result']['rows']
            logger.info(f"Получено {len(rows)} строк")

            # Преобразуем строки в записи для вставки
            for row in rows:
                item = row.get('item', {})
                sku = item.get('sku')
                offer_id = item.get('offer_id', '')
                name = item.get('name', '')
                barcode = item.get('barcode', '')

                row_number = row.get('rowNumber')
                seller_price = float(row.get('seller_price_per_instance', 0))
                commission_ratio = float(row.get('commission_ratio', 0))

                delivery = row.get('delivery_commission') or {}
                delivery_total = float(delivery.get('total', 0))
                delivery_standard = float(delivery.get('standard_fee', 0))

                ret_comm = row.get('return_commission') or {}
                ret_total = float(ret_comm.get('total', 0))
                ret_standard = float(ret_comm.get('standard_fee', 0))

                unique_key = f"{first_day}_{sku}_{row_number}"

                record = {
                    "month": first_day,
                    "sku": sku,
                    "offer_id": offer_id,
                    "name": name,
                    "barcode": barcode,
                    "row_number": row_number,
                    "seller_price_per_instance": seller_price,
                    "commission_ratio": commission_ratio,
                    "delivery_commission_total": delivery_total,
                    "delivery_commission_standard_fee": delivery_standard,
                    "return_commission_total": ret_total,
                    "return_commission_standard_fee": ret_standard,
                    "unique_key": unique_key,
                    "raw_data": json.dumps(row, ensure_ascii=False)
                }
                all_records.append(record)

        if not all_records:
            return 0

        # Вставка батчами
        inserted = 0
        for i in range(0, len(all_records), 200):
            batch = all_records[i:i+200]
            try:
                result = self.upload_batch(batch)
                inserted += result
            except Exception as e:
                logger.error(f"Ошибка при вставке батча: {e}")
        return inserted

    def fetch_data_for_date(self, date):
        # Не используется напрямую, так как load_dates переопределён
        return []
