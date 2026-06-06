#!/usr/bin/env python3
"""
Модульный загрузчик продаж Wildberries для оркестратора.
Использует базовый класс BaseLoader.
"""

import requests
import time
import logging
from datetime import datetime
from wb_base_loader import WBBaseLoader

logger = logging.getLogger(__name__)

class WBSalesLoader(WBBaseLoader):
    """Загрузчик продаж Wildberries (метод /api/v1/supplier/sales)"""
    
    TABLE_ID = 863
    WB_API_URL = "https://statistics-api.wildberries.ru/api/v1/supplier/sales"

    def __init__(self, wb_token, db_token):
        super().__init__(self.TABLE_ID, "wb_sales", db_token)
        self.wb_token = wb_token

    def fetch_data_for_date(self, date):
        """Загружает данные за конкретную дату с обработкой 429"""
        headers = {"Authorization": self.wb_token}
        params = {"dateFrom": f"{date}T00:00:00", "flag": 1}
        
        for attempt in range(3):
            try:
                resp = requests.get(self.WB_API_URL, headers=headers, params=params, timeout=30)
                if resp.status_code == 200:
                    return resp.json()
                elif resp.status_code == 429:
                    retry_after = int(resp.headers.get('Retry-After', 60))
                    wait = retry_after * (2 ** attempt)
                    logger.warning(f"⚠️ 429, жду {wait} сек...")
                    time.sleep(wait)
                else:
                    logger.error(f"❌ Ошибка WB {resp.status_code}: {resp.text[:200]}")
                    return []
            except Exception as e:
                logger.error(f"❌ Ошибка запроса WB: {e}")
                return []
        return []

    def transform_row(self, sale):
        """Преобразует сырую запись WB в формат Baserow (таблица 863)"""
        def round2(v):
            try:
                return round(float(v), 2) if v else 0.0
            except:
                return 0.0

        # Нормализация cancelDate
        cancel_date = sale.get("cancelDate", "")
        if cancel_date in (None, "", "0001-01-01T00:00:00", "0001-01-01"):
            cancel_date = None
        elif isinstance(cancel_date, str) and "T" in cancel_date:
            cancel_date = cancel_date.split("T")[0]

        return {
            "srid": str(sale.get("srid", "")),
            "nmId": sale.get("nmId"),
            "supplierArticle": sale.get("supplierArticle", ""),
            "barcode": sale.get("barcode", ""),
            "date": (sale.get("date") or "")[:10],
            "quantity": sale.get("quantity", 0),
            "totalPrice": round2(sale.get("totalPrice")),
            "forPay": round2(sale.get("forPay")),
            "finishedPrice": round2(sale.get("finishedPrice")),
            "subject": sale.get("subject", ""),
            "warehouseName": sale.get("warehouseName", ""),
            "incomeID": sale.get("incomeID"),
            "docType": sale.get("docType", ""),
            "retailPrice": round2(sale.get("retailPrice")),
            "wbSold": round2(sale.get("wbSold")),
            "sppPercent": round2(sale.get("spp")),
            "kvvPercent": round2(sale.get("kvv")),
            "kvvFinalPercent": round2(sale.get("kvvFinal")),
            "reward": round2(sale.get("reward")),
            "acquiring": round2(sale.get("acquiring")),
            "vat": round2(sale.get("vat")),
            "bankName": sale.get("bankName", ""),
            "officeNumber": sale.get("officeNumber", ""),
            "deliveryCosts": round2(sale.get("deliveryCosts")),
            "regionName": sale.get("regionName", ""),
            "countryName": sale.get("countryName", ""),
            "oblastOkrugName": sale.get("oblastOkrugName", ""),
            "isCancel": sale.get("isCancel", False),
            "cancelDate": cancel_date,
            "spp": round2(sale.get("spp")),
            "paymentSaleAmount": round2(sale.get("paymentSaleAmount")),
        }
