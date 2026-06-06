#!/usr/bin/env python3
import requests
import os
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any

BASEROW_URL = os.getenv("BASEROW_URL", "http://localhost:8000")
DB_TOKEN = os.getenv("BASEROW_DB_TOKEN", os.getenv("BASEROW_TOKEN", ""))
ADMIN_USERNAME = os.getenv("BASEROW_ADMIN_USER", os.getenv("BASEROW_EMAIL", ""))
ADMIN_PASS = os.getenv("BASEROW_ADMIN_PASS", os.getenv("BASEROW_PASSWORD", ""))
DATABASE_ID = int(os.getenv("BASEROW_DATABASE_ID", "212"))

class BaserowManager:
    # Эталонное описание таблиц (доступно извне)
    tables = {
        "wb_sales": [
            {"name": "srid", "type": "text", "unique": True},
            {"name": "nmId", "type": "number"},
            {"name": "supplierArticle", "type": "text"},
            {"name": "barcode", "type": "text"},
            {"name": "date", "type": "date"},
            {"name": "quantity", "type": "number"},
            {"name": "totalPrice", "type": "number", "number_decimal_places": 2},
            {"name": "forPay", "type": "number", "number_decimal_places": 2},
            {"name": "finishedPrice", "type": "number", "number_decimal_places": 2},
            {"name": "subject", "type": "text"},
            {"name": "warehouseName", "type": "text"},
            {"name": "incomeID", "type": "number"},
            {"name": "docType", "type": "text"},
            {"name": "retailPrice", "type": "number", "number_decimal_places": 2},
            {"name": "wbSold", "type": "number", "number_decimal_places": 2},
            {"name": "sppPercent", "type": "number", "number_decimal_places": 2},
            {"name": "kvvPercent", "type": "number", "number_decimal_places": 2},
            {"name": "kvvFinalPercent", "type": "number", "number_decimal_places": 2},
            {"name": "reward", "type": "number", "number_decimal_places": 2},
            {"name": "acquiring", "type": "number", "number_decimal_places": 2},
            {"name": "vat", "type": "number", "number_decimal_places": 2},
            {"name": "bankName", "type": "text"},
            {"name": "officeNumber", "type": "text"},
            {"name": "deliveryCosts", "type": "number", "number_decimal_places": 2},
            {"name": "regionName", "type": "text"},
            {"name": "countryName", "type": "text"},
            {"name": "oblastOkrugName", "type": "text"},
            {"name": "isCancel", "type": "boolean"},
            {"name": "cancelDate", "type": "date"},
            {"name": "spp", "type": "number"},
            {"name": "paymentSaleAmount", "type": "number", "number_decimal_places": 2}
        ],
        "wb_tariffs_commissions": [
            {"name": "date", "type": "date"},
            {"name": "warehouseName", "type": "text"},
            {"name": "boxRate", "type": "number", "number_decimal_places": 2},
            {"name": "palletRate", "type": "number", "number_decimal_places": 2},
            {"name": "returnRate", "type": "number", "number_decimal_places": 2},
            {"name": "parentCategory", "type": "text"},
            {"name": "subjectId", "type": "number"},
            {"name": "subjectName", "type": "text"},
            {"name": "paidStorage", "type": "number", "number_decimal_places": 2},
            {"name": "paidAcceptance", "type": "number", "number_decimal_places": 2},
            {"name": "deliveryRub", "type": "number", "number_decimal_places": 2},
            {"name": "deliveryExpressRub", "type": "number", "number_decimal_places": 2}
        ],
        "wb_realization": [
            {"name": "realizationreport_id", "type": "number"},
            {"name": "date_from", "type": "date"},
            {"name": "date_to", "type": "date"},
            {"name": "create_dt", "type": "date"},
            {"name": "currency", "type": "text"},
            {"name": "suppliercontract_code", "type": "text"},
            {"name": "rrd_id", "type": "number", "unique": True},
            {"name": "gi_id", "type": "number"},
            {"name": "subject_name", "type": "text"},
            {"name": "nm_id", "type": "number"},
            {"name": "brand_name", "type": "text"},
            {"name": "sa_name", "type": "text"},
            {"name": "ts_name", "type": "text"},
            {"name": "barcode", "type": "text"},
            {"name": "doc_type_name", "type": "text"},
            {"name": "quantity", "type": "number"},
            {"name": "retail_price", "type": "number", "number_decimal_places": 2},
            {"name": "retail_amount", "type": "number", "number_decimal_places": 2},
            {"name": "sale_percent", "type": "number"},
            {"name": "commission_percent", "type": "number", "number_decimal_places": 2},
            {"name": "office_name", "type": "text"},
            {"name": "supplier_oper_name", "type": "text"},
            {"name": "order_dt", "type": "date"},
            {"name": "sale_dt", "type": "date"},
            {"name": "rr_dt", "type": "date"},
            {"name": "shk_id", "type": "number"},
            {"name": "retail_price_withdisc_rub", "type": "number", "number_decimal_places": 2},
            {"name": "delivery_amount", "type": "number", "number_decimal_places": 2},
            {"name": "return_amount", "type": "number", "number_decimal_places": 2},
            {"name": "delivery_cost", "type": "number", "number_decimal_places": 2},
            {"name": "return_count", "type": "number"},
            {"name": "ppvz_for_pay", "type": "number", "number_decimal_places": 2},
            {"name": "ppvz_supplier", "type": "number", "number_decimal_places": 2},
            {"name": "ppvz_kvw_percent", "type": "number", "number_decimal_places": 2},
            {"name": "ppvz_vw", "type": "number", "number_decimal_places": 2},
            {"name": "ppvz_vw_nds", "type": "number", "number_decimal_places": 2},
            {"name": "ppvz_commission", "type": "number", "number_decimal_places": 2},
            {"name": "ppvz_commission_percent", "type": "number", "number_decimal_places": 2},
            {"name": "ppvz_commission_plus", "type": "number", "number_decimal_places": 2},
            {"name": "ppvz_commission_plus_percent", "type": "number", "number_decimal_places": 2},
            {"name": "ppvz_commission_minus", "type": "number", "number_decimal_places": 2},
            {"name": "ppvz_commission_minus_percent", "type": "number", "number_decimal_places": 2},
            {"name": "ppvz_commission_extra", "type": "number", "number_decimal_places": 2},
            {"name": "ppvz_commission_extra_percent", "type": "number", "number_decimal_places": 2},
            {"name": "ppvz_commission_extra_minus", "type": "number", "number_decimal_places": 2},
            {"name": "ppvz_commission_extra_minus_percent", "type": "number", "number_decimal_places": 2},
            {"name": "ppvz_commission_extra_plus", "type": "number", "number_decimal_places": 2},
            {"name": "ppvz_commission_extra_plus_percent", "type": "number", "number_decimal_places": 2},
            {"name": "ppvz_commission_extra_plus_minus", "type": "number", "number_decimal_places": 2},
            {"name": "ppvz_commission_extra_plus_minus_percent", "type": "number", "number_decimal_places": 2}
        ],
        "ozon_ads_stats": [
            {"name": "date", "type": "date"},
            {"name": "campaign_id", "type": "number"},
            {"name": "campaign_name", "type": "text"},
            {"name": "campaign_type", "type": "text"},
            {"name": "impressions", "type": "number"},
            {"name": "clicks", "type": "number"},
            {"name": "ctr", "type": "number", "number_decimal_places": 2},
            {"name": "cpc", "type": "number", "number_decimal_places": 2},
            {"name": "spent", "type": "number", "number_decimal_places": 2},
            {"name": "orders", "type": "number"},
            {"name": "revenue", "type": "number", "number_decimal_places": 2},
            {"name": "roas", "type": "number", "number_decimal_places": 2},
            {"name": "unique_key", "type": "text", "unique": True}
        ],
        "ozon_finance_realization": [
            {"name": "month", "type": "date"},
            {"name": "product_id", "type": "number"},
            {"name": "product_name", "type": "text"},
            {"name": "sku", "type": "text"},
            {"name": "quantity", "type": "number"},
            {"name": "price", "type": "number", "number_decimal_places": 2},
            {"name": "commission", "type": "number", "number_decimal_places": 2},
            {"name": "delivery_cost", "type": "number", "number_decimal_places": 2},
            {"name": "return_cost", "type": "number", "number_decimal_places": 2},
            {"name": "total", "type": "number", "number_decimal_places": 2},
            {"name": "unique_key", "type": "text", "unique": True}
        ],
        "ozon_postings": [
            {"name": "posting_number", "type": "text", "unique": True},
            {"name": "created_at", "type": "date"},
            {"name": "status", "type": "text"},
            {"name": "sku", "type": "text"},
            {"name": "product_name", "type": "text"},
            {"name": "quantity", "type": "number"},
            {"name": "price", "type": "number", "number_decimal_places": 2},
            {"name": "commission", "type": "number", "number_decimal_places": 2},
            {"name": "delivery_cost", "type": "number", "number_decimal_places": 2},
            {"name": "total", "type": "number", "number_decimal_places": 2}
        ]
    }

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Token {DB_TOKEN}",
            "Content-Type": "application/json"
        })

    def get_table_id_by_name(self, table_name: str) -> Optional[int]:
        """Получить ID таблицы по имени."""
        url = f"{BASEROW_URL}/api/database/tables/database/{DATABASE_ID}/"
        try:
            resp = self.session.get(url, timeout=30)
            resp.raise_for_status()
            tables = resp.json()
            for table in tables:
                if table["name"] == table_name:
                    return table["id"]
            return None
        except Exception as e:
            print(f"Ошибка получения ID таблицы {table_name}: {e}")
            return None

    def ensure_table(self, table_name: str, fields: List[Dict[str, Any]]) -> int:
        """Создать таблицу, если её нет, и вернуть ID."""
        existing_id = self.get_table_id_by_name(table_name)
        if existing_id:
            return existing_id

        # Создаём таблицу
        url = f"{BASEROW_URL}/api/database/tables/database/{DATABASE_ID}/"
        payload = {"name": table_name, "data": []}
        try:
            resp = self.session.post(url, json=payload, timeout=30)
            resp.raise_for_status()
            table_data = resp.json()
            table_id = table_data["id"]
        except Exception as e:
            raise Exception(f"Не удалось создать таблицу {table_name}: {e}")

        # Создаём поля
        for field in fields:
            field_url = f"{BASEROW_URL}/api/database/fields/table/{table_id}/"
            field_payload = {
                "name": field["name"],
                "