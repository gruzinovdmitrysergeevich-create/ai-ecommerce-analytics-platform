#!/usr/bin/env python3
"""
Загрузчик отправлений Ozon FBO (постинги) для актуального API v2.
Заполняет расширенную таблицу с аналитическими и финансовыми полями.
"""

import requests
import time
import logging
from datetime import datetime
from wb_base_loader import WBBaseLoader

logger = logging.getLogger(__name__)

class OzonPostingsLoader(WBBaseLoader):
    DATE_FIELD = "created_at"
    """Загрузчик постингов Ozon (таблица ozon_postings)"""

    TABLE_ID = None  
    OZON_API_URL = "https://api-seller.ozon.ru/v2/posting/fbo/list"

    def __init__(self, ozon_client_id, ozon_api_key, db_token):
        from baserow_manager import BaserowManager
        bm = BaserowManager()
        table_id = bm.get_table_id_by_name("ozon_postings")
        if not table_id:
            logger.info("Таблица ozon_postings не найдена, создаю...")
            bm.ensure_table("ozon_postings", bm.tables["ozon_postings"])
            table_id = bm.get_table_id_by_name("ozon_postings")
        
        super().__init__(table_id, "ozon_postings", db_token)
        self.ozon_client_id = ozon_client_id
        self.ozon_api_key = ozon_api_key
        # Исправление: создаём отдельный атрибут для Ozon, не трогаем self.headers (он для Baserow)
        self.ozon_headers = {
            "Client-Id": ozon_client_id,
            "Api-Key": ozon_api_key,
            "Content-Type": "application/json"
        }

    def fetch_data_for_date(self, date):
        all_postings = []
        offset = 0
        limit = 1000

        since = f"{date}T00:00:00.000Z"
        to = f"{date}T23:59:59.999Z"

        while True:
            payload = {
                "dir": "asc",
                "filter": {
                    "since": since,
                    "to": to
                },
                "limit": limit,
                "offset": offset,
                "with": {
                    "analytics_data": True,
                    "financial_data": True
                }
            }

            for attempt in range(3):
                try:
                    # Используем self.ozon_headers для запроса к Ozon
                    resp = requests.post(
                        self.OZON_API_URL,
                        headers=self.ozon_headers,
                        json=payload,
                        timeout=30
                    )
                    if resp.status_code == 200:
                        data = resp.json()
                        postings = data.get("result", [])
                        all_postings.extend(postings)
                        
                        if not data.get("has_next", False):
                            return all_postings
                        offset += limit
                        break
                    
                    elif resp.status_code == 429:
                        retry_after = int(resp.headers.get('Retry-After', 60))
                        wait = retry_after * (2 ** attempt)
                        logger.warning(f"⚠️ 429, жду {wait} сек...")
                        time.sleep(wait)
                    else:
                        logger.error(f"❌ Ошибка Ozon {resp.status_code}: {resp.text[:200]}")
                        return []
                
                except Exception as e:
                    logger.error(f"❌ Ошибка запроса Ozon: {e}")
                    return []
            
            logger.error("Не удалось получить данные после 3 попыток")
            return []

    def transform_row(self, posting):
        # Основные поля
        products = posting.get("products", [])
        products_count = len(products)

        created_at = posting.get("created_at", "")
        if created_at and "T" in created_at:
            created_at = created_at.split("T")[0]
        
        in_process_at = posting.get("in_process_at", "")
        if in_process_at and "T" in in_process_at:
            in_process_at = in_process_at.split("T")[0]
        else:
            in_process_at = None

        # Расчёт сумм по товарам
        total_price = 0.0
        total_commission = 0.0
        total_payout = 0.0

        financial = posting.get("financial_data", {})
        products_fin = financial.get("products", [])
        fin_by_product = {}
        for pf in products_fin:
            pid = pf.get("product_id")
            if pid:
                fin_by_product[pid] = pf

        for prod in products:
            sku = prod.get("sku")
            price = float(prod.get("price", 0))
            quantity = prod.get("quantity", 1)
            total_price += price * quantity

            fin = fin_by_product.get(sku, {})
            commission = float(fin.get("commission_amount", 0))
            payout = float(fin.get("payout", 0))
            total_commission += commission
            total_payout += payout

        # Аналитические данные
        analytics = posting.get("analytics_data", {})
        city = analytics.get("city", "")
        delivery_type = analytics.get("delivery_type", "")
        is_premium = analytics.get("is_premium", False)
        payment_type = analytics.get("payment_type_group_name", "")
        warehouse_name = analytics.get("warehouse_name", "")

        # Кластеры
        cluster_from = financial.get("cluster_from", "")
        cluster_to = financial.get("cluster_to", "")

        import json
        raw_data = json.dumps(posting, ensure_ascii=False)

        return {
            "posting_number": posting.get("posting_number", ""),
            "order_id": posting.get("order_id", 0),
            "status": posting.get("status", ""),
            "created_at": created_at,
            "in_process_at": in_process_at,
            "products_count": products_count,
            "total_price": round(total_price, 2),
            "total_commission": round(total_commission, 2),
            "total_payout": round(total_payout, 2),
            "city": city,
            "delivery_type": delivery_type,
            "is_premium": is_premium,
            "payment_type": payment_type,
            "warehouse_name": warehouse_name,
            "cluster_from": cluster_from,
            "cluster_to": cluster_to,
            "date": created_at,
            "raw_data": raw_data
        }
