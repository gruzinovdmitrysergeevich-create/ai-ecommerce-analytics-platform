#!/usr/bin/env python3
"""
Загрузчик финансовых транзакций Ozon (детализация по заказам).
Использует актуальный API /v3/finance/transaction/list.
"""

import requests
import time
import logging
from datetime import datetime, timedelta
from wb_base_loader import WBBaseLoader

logger = logging.getLogger(__name__)

class OzonRealizationLoader(WBBaseLoader):
    DATE_FIELD = "operation_date"
    """Загрузчик транзакций Ozon (таблица ozon_realization)"""

    TABLE_ID = None
    API_URL = "https://api-seller.ozon.ru/v3/finance/transaction/list"

    def __init__(self, ozon_client_id, ozon_api_key, db_token):
        from baserow_manager import BaserowManager
        bm = BaserowManager()
        table_id = bm.get_table_id_by_name("ozon_realization")
        if not table_id:
            logger.info("Таблица ozon_realization не найдена, создаю...")
            bm.ensure_table("ozon_realization", bm.tables["ozon_realization"])
            table_id = bm.get_table_id_by_name("ozon_realization")
        
        super().__init__(table_id, "ozon_realization", db_token)
        self.ozon_client_id = ozon_client_id
        self.ozon_api_key = ozon_api_key
        self.ozon_headers = {
            "Client-Id": ozon_client_id,
            "Api-Key": ozon_api_key,
            "Content-Type": "application/json"
        }

    def fetch_data_for_date(self, date):
        """
        Загружает все транзакции за указанную дату (пагинация).
        Возвращает список словарей, готовых для вставки в Baserow.
        """
        all_rows = []
        page = 1
        page_size = 1000
        max_retries = 3
        retry_delay = 5

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

            for attempt in range(max_retries):
                try:
                    resp = requests.post(
                        self.API_URL,
                        headers=self.ozon_headers,
                        json=payload,
                        timeout=60  # увеличенный timeout
                    )
                    if resp.status_code != 200:
                        logger.error(f"Ошибка получения транзакций: {resp.text}")
                        break

                    data = resp.json()
                    result = data.get("result", {})
                    operations = result.get("operations", [])
                    if not operations:
                        break

                    for op in operations:
                        rows = self._operation_to_rows(op)
                        all_rows.extend(rows)

                    page_count = result.get("page_count", 0)
                    if page >= page_count:
                        return all_rows
                    page += 1
                    break  # успешно, выходим из retry-цикла

                except requests.exceptions.Timeout:
                    logger.warning(f"Таймаут при запросе страницы {page}, попытка {attempt+1}/{max_retries}")
                    if attempt == max_retries - 1:
                        logger.error("Превышено количество попыток, прерываю загрузку")
                        return all_rows
                    time.sleep(retry_delay * (2 ** attempt))
                except Exception as e:
                    logger.error(f"Ошибка при запросе транзакций: {e}")
                    return all_rows

            # Если мы вышли из цикла без break (т.е. все попытки исчерпаны и не удалось получить данные)
            else:
                logger.error("Не удалось получить данные после нескольких попыток")
                break

        return all_rows

    def _operation_to_rows(self, operation):
        """
        Преобразует одну операцию в список строк (по одному товару в строке).
        """
        rows = []
        operation_id = operation.get("operation_id")
        operation_type = operation.get("operation_type", "")
        operation_date = operation.get("operation_date", "")
        if operation_date and " " in operation_date:
            operation_date = operation_date.split(" ")[0]

        posting = operation.get("posting", {})
        posting_number = posting.get("posting_number", "")

        amount = float(operation.get("amount", 0))
        accruals_for_sale = float(operation.get("accruals_for_sale", 0))
        sale_commission = float(operation.get("sale_commission", 0))

        items = operation.get("items", [])
        if not items:
            # Строка без товаров
            rows.append({
                "operation_id": f"{operation_id}_0",  # уникальный ID
                "operation_type": operation_type,
                "operation_date": operation_date,
                "date": operation_date,
                "posting_number": posting_number,
                "product_id": None,
                "product_name": "",
                "quantity": 0,
                "price": 0.0,
                "commission_amount": sale_commission,
                "accruals_for_sale": accruals_for_sale,
                "total_amount": amount,
                "raw_data": self._safe_json(operation)
            })
        else:
            for idx, item in enumerate(items):
                product_id = item.get("sku")
                product_name = item.get("name", "")
                quantity = item.get("quantity", 1)
                price = float(item.get("price", 0))

                rows.append({
                    "operation_id": f"{operation_id}_{idx}",
                    "operation_type": operation_type,
                    "operation_date": operation_date,
                "date": operation_date,
                    "posting_number": posting_number,
                    "product_id": product_id,
                    "product_name": product_name,
                    "quantity": quantity,
                    "price": price,
                    "commission_amount": sale_commission,
                    "accruals_for_sale": accruals_for_sale,
                    "total_amount": amount,
                    "raw_data": self._safe_json(operation)
                })
        return rows

    def _safe_json(self, obj):
        import json
        try:
            return json.dumps(obj, ensure_ascii=False)
        except:
            return str(obj)

    def transform_row(self, raw_row):
        """
        Возвращает строку для вставки в Baserow (уже подготовлена в fetch_data_for_date).
        """
        return raw_row
