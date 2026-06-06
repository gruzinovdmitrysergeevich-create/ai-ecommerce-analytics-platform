#!/usr/bin/env python3
"""
Загрузчик детализированных транзакций Ozon (v3/finance/transaction/list).
Сохраняет каждую операцию с расшифровкой по товарам (items) и услугам (services).
"""

import requests
import logging
import json
import time
from datetime import datetime, timedelta
from wb_base_loader import WBBaseLoader

logger = logging.getLogger(__name__)

class OzonTransactionsDetailLoader(WBBaseLoader):
    DATE_FIELD = "operation_date"
    TABLE_ID = None
    API_URL = "https://api-seller.ozon.ru/v3/finance/transaction/list"

    def __init__(self, ozon_client_id, ozon_api_key, db_token):
        from baserow_manager import BaserowManager
        bm = BaserowManager()
        table_id = bm.get_table_id_by_name("ozon_transactions_detail")
        if not table_id:
            logger.info("Таблица ozon_transactions_detail не найдена, создаю...")
            bm.ensure_table("ozon_transactions_detail", bm.tables["ozon_transactions_detail"])
            table_id = bm.get_table_id_by_name("ozon_transactions_detail")
        
        super().__init__(table_id, "ozon_transactions_detail", db_token)
        self.ozon_client_id = ozon_client_id
        self.ozon_api_key = ozon_api_key
        self.ozon_headers = {
            "Client-Id": ozon_client_id,
            "Api-Key": ozon_api_key,
            "Content-Type": "application/json"
        }

    def fetch_data_for_date(self, date):
        """
        Получает все транзакции за указанную дату (пагинация).
        Возвращает список сырых операций (уже с товарами и услугами).
        """
        all_operations = []
        page = 1
        page_size = 1000
        from_dt = f"{date}T00:00:00.000Z"
        to_dt = f"{date}T23:59:59.999Z"

        while True:
            payload = {
                "filter": {
                    "date": {
                        "from": from_dt,
                        "to": to_dt
                    }
                },
                "page": page,
                "page_size": page_size
            }
            try:
                resp = requests.post(self.API_URL, headers=self.ozon_headers, json=payload, timeout=60)
                if resp.status_code != 200:
                    logger.error(f"Ошибка запроса транзакций: {resp.text}")
                    break
                data = resp.json()
                operations = data.get('result', {}).get('operations', [])
                if not operations:
                    break
                all_operations.extend(operations)
                page_count = data.get('result', {}).get('page_count', 0)
                if page >= page_count:
                    break
                page += 1
                time.sleep(0.5)  # задержка между страницами
            except Exception as e:
                logger.error(f"Исключение при запросе транзакций: {e}")
                break
        return all_operations

    def _operation_to_rows(self, operation):
        """
        Преобразует одну операцию в список записей для вставки.
        Каждая запись соответствует одному товару (items) или услуге (services).
        """
        rows = []
        operation_id = operation.get("operation_id")
        operation_type = operation.get("operation_type", "")
        operation_date = operation.get("operation_date", "")
        if operation_date and " " in operation_date:
            operation_date = operation_date.split(" ")[0]  # оставляем только дату

        amount = float(operation.get("amount", 0))
        accruals_for_sale = float(operation.get("accruals_for_sale", 0))
        sale_commission = float(operation.get("sale_commission", 0))

        posting = operation.get("posting", {})
        posting_number = posting.get("posting_number", "")

        items = operation.get("items", [])
        services = operation.get("services", [])

        # Если нет ни товаров, ни услуг, создаём одну запись с общей суммой
        if not items and not services:
            rows.append({
                "operation_id": f"{operation_id}_0",
                "operation_type": operation_type,
                "operation_date": operation_date,
                "posting_number": posting_number,
                "product_id": None,
                "product_name": "",
                "quantity": 0,
                "price": 0.0,
                "commission_amount": sale_commission,
                "commission_percent": 0,
                "payout": 0,
                "accruals_for_sale": accruals_for_sale,
                "total_amount": amount,
                "old_price": 0.0,
                "total_discount_value": 0.0,
                "cluster_from": "",
                "cluster_to": "",
                "date": operation_date,
                "raw_data": json.dumps(operation, ensure_ascii=False)
            })
        else:
            # Обрабатываем товары
            for idx, item in enumerate(items):
                product_id = item.get("sku")
                product_name = item.get("name", "")
                quantity = item.get("quantity", 1)
                price = float(item.get("price", 0))
                commission_amount = float(item.get("commission_amount", 0))
                commission_percent = float(item.get("commission_percent", 0))
                payout = float(item.get("payout", 0))

                rows.append({
                    "operation_id": f"{operation_id}_{idx}",
                    "operation_type": operation_type,
                    "operation_date": operation_date,
                    "posting_number": posting_number,
                    "product_id": product_id,
                    "product_name": product_name,
                    "quantity": quantity,
                    "price": price,
                    "commission_amount": commission_amount,
                    "commission_percent": commission_percent,
                    "payout": payout,
                    "accruals_for_sale": accruals_for_sale,
                    "total_amount": amount,
                    "old_price": 0.0,
                    "total_discount_value": 0.0,
                    "cluster_from": "",
                    "cluster_to": "",
                    "date": operation_date,
                    "raw_data": json.dumps(operation, ensure_ascii=False)
                })
            # Обрабатываем услуги (например, реклама)
            for idx, service in enumerate(services):
                service_name = service.get("name", "")
                service_amount = float(service.get("amount", 0))
                rows.append({
                    "operation_id": f"{operation_id}_service_{idx}",
                    "operation_type": operation_type,
                    "operation_date": operation_date,
                    "posting_number": posting_number,
                    "product_id": None,
                    "product_name": service_name,
                    "quantity": 0,
                    "price": service_amount,
                    "commission_amount": 0,
                    "commission_percent": 0,
                    "payout": 0,
                    "accruals_for_sale": accruals_for_sale,
                    "total_amount": amount,
                    "old_price": 0.0,
                    "total_discount_value": 0.0,
                    "cluster_from": "",
                    "cluster_to": "",
                    "date": operation_date,
                    "raw_data": json.dumps(operation, ensure_ascii=False)
                })
        return rows

    def load_dates(self, date_list):
        all_rows = []
        for date in date_list:
            logger.info(f"  📥 Загрузка транзакций за {date}...")
            operations = self.fetch_data_for_date(date)
            logger.info(f"     Получено {len(operations)} операций")
            for op in operations:
                rows = self._operation_to_rows(op)
                all_rows.extend(rows)
            time.sleep(1)  # задержка между днями

        if not all_rows:
            logger.info("Нет новых записей для вставки")
            return 0

        # Вставка батчами
        inserted = 0
        for i in range(0, len(all_rows), 200):
            batch = all_rows[i:i+200]
            try:
                result = self.upload_batch(batch)
                inserted += result
            except Exception as e:
                logger.error(f"Ошибка при вставке батча: {e}")
        return inserted

    def transform_row(self, raw_row):
        return raw_row
