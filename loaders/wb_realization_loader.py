#!/usr/bin/env python3
"""
Модульный загрузчик отчётов реализации Wildberries для оркестратора.
Добавлены поля для FBS: delivery_method, seller_promo_id, seller_promo_discount,
loyalty_id, loyalty_discount, uuid_promocode, sale_price_promocode_discount_prc.
"""

import requests
import time
import logging
from datetime import datetime, timedelta
from wb_base_loader import WBBaseLoader

logger = logging.getLogger(__name__)

class WBRealizationLoader(WBBaseLoader):
    DATE_FIELD = "rr_dt"
    TABLE_ID = 867
    WB_API_URL = "https://statistics-api.wildberries.ru/api/v5/supplier/reportDetailByPeriod"

    def __init__(self, wb_token, db_token):
        super().__init__(self.TABLE_ID, "wb_realization", db_token)
        self.wb_token = wb_token

    def fetch_data_for_date(self, date):
        headers = {"Authorization": self.wb_token}
        all_data = []
        rrdid = 0
        limit = 100000

        while True:
            params = {
                "dateFrom": date,
                "dateTo": date,
                "limit": limit,
                "rrdid": rrdid
            }
            try:
                resp = requests.get(self.WB_API_URL, headers=headers, params=params, timeout=60)
                if resp.status_code == 200:
                    data = resp.json()
                    if not data:
                        break
                    all_data.extend(data)
                    if len(data) < limit:
                        break
                    rrdid = data[-1].get("rrd_id", 0)
                    time.sleep(0.5)
                elif resp.status_code == 204:
                    logger.info(f"   Нет данных за {date} (204 No Content)")
                    return []
                elif resp.status_code == 429:
                    retry_after = int(resp.headers.get('Retry-After', 60))
                    wait = retry_after
                    logger.warning(f"⚠️ 429, жду {wait} сек...")
                    time.sleep(wait)
                else:
                    logger.error(f"❌ Ошибка WB {resp.status_code}: {resp.text[:200]}")
                    break
            except Exception as e:
                logger.error(f"❌ Исключение при загрузке: {e}")
                break
        return all_data

    def transform_row(self, item):
        def safe_float(v):
            try:
                return float(v) if v is not None else 0.0
            except:
                return 0.0

        def safe_int(v):
            try:
                return int(v) if v is not None else 0
            except:
                return 0

        def non_negative_float(v):
            val = safe_float(v)
            return max(val, 0.0)

        # Новые поля для FBS и скидок
        delivery_method = item.get("delivery_method", "")
        seller_promo_id = safe_int(item.get("seller_promo_id"))
        seller_promo_discount = safe_float(item.get("seller_promo_discount"))
        loyalty_id = safe_int(item.get("loyalty_id"))
        loyalty_discount = safe_float(item.get("loyalty_discount"))
        uuid_promocode = item.get("uuid_promocode", "")
        sale_price_promocode_discount_prc = safe_float(item.get("sale_price_promocode_discount_prc"))

        return {
            "realizationreport_id": safe_int(item.get("realizationreport_id")),
            "date_from": item.get("date_from"),
            "date_to": item.get("date_to"),
            "create_dt": item.get("create_dt"),
            "currency": item.get("currency_name"),
            "suppliercontract_code": item.get("suppliercontract_code", ""),
            "rrd_id": safe_int(item.get("rrd_id")),
            "gi_id": safe_int(item.get("gi_id")),
            "subject_name": item.get("subject_name", ""),
            "nm_id": safe_int(item.get("nm_id")),
            "brand_name": item.get("brand_name", ""),
            "sa_name": item.get("sa_name", ""),
            "ts_name": item.get("ts_name", ""),
            "barcode": item.get("barcode", ""),
            "doc_type_name": item.get("doc_type_name", ""),
            "quantity": safe_int(item.get("quantity")),
            "retail_price": safe_float(item.get("retail_price")),
            "retail_amount": safe_float(item.get("retail_amount")),
            "sale_percent": safe_int(item.get("sale_percent")),
            "commission_percent": safe_float(item.get("commission_percent")),
            "office_name": item.get("office_name", ""),
            "supplier_oper_name": item.get("supplier_oper_name", ""),
            "order_dt": item.get("order_dt"),
            "sale_dt": item.get("sale_dt"),
            "rr_dt": item.get("rr_dt"),
            "shk_id": safe_int(item.get("shk_id")),
            "retail_price_withdisc_rub": safe_float(item.get("retail_price_withdisc_rub")),
            "delivery_amount": safe_float(item.get("delivery_amount")),
            "return_amount": safe_float(item.get("return_amount")),
            "delivery_rub": safe_float(item.get("delivery_rub")),
            "gi_box_type_name": item.get("gi_box_type_name", ""),
            "product_discount_for_rep": safe_float(item.get("product_discount_for_report")),
            "supplier_promo": safe_float(item.get("supplier_promo")),
            "rid": safe_int(item.get("rid")),
            "ppvz_spp_prc": safe_float(item.get("ppvz_spp_prc")),
            "ppvz_kvw_prc_base": safe_float(item.get("ppvz_kvw_prc_base")),
            "ppvz_kvw_prc": non_negative_float(item.get("ppvz_kvw_prc")),
            "ppvz_sales_commission": non_negative_float(item.get("ppvz_sales_commission")),
            "ppvz_for_pay": safe_float(item.get("ppvz_for_pay")),
            "ppvz_reward": safe_float(item.get("ppvz_reward")),
            "ppvz_vat": safe_float(item.get("ppvz_vat")),
            "ppvz_office_id": safe_int(item.get("ppvz_office_id")),
            "ppvz_office_name": item.get("ppvz_office_name", ""),
            "ppvz_supplier_id": safe_int(item.get("ppvz_supplier_id")),
            "ppvz_supplier_name": item.get("ppvz_supplier_name", ""),
            "ppvz_inn": item.get("ppvz_inn", ""),
            "declaration_number": item.get("declaration_number", ""),
            "bonus_type_name": item.get("bonus_type_name", ""),
            "sticker_id": item.get("sticker_id", ""),
            "site_country": item.get("site_country", ""),
            "penalty": safe_float(item.get("penalty")),
            "additional_payment": safe_float(item.get("additional_payment")),
            "rebill_logistic_cost": safe_float(item.get("rebill_logistic_cost")),
            "rebill_storage_cost": safe_float(item.get("rebill_storage_cost")),
            "acquiring_bank": item.get("acquiring_bank", ""),
            "acquiring_fee": safe_float(item.get("acquiring_fee")),
            "kiz": item.get("kiz", ""),
            "storage_fee": safe_float(item.get("storage_fee")),
            "deduction": safe_float(item.get("deduction")),
            "acceptance": safe_float(item.get("acceptance")),
            "assembly_cost": safe_float(item.get("assembly_cost")),
            "dropoff_cost": safe_float(item.get("dropoff_cost")),
            "sorting_cost": safe_float(item.get("sorting_cost")),
            # Новые поля
            "delivery_method": delivery_method,
            "seller_promo_id": seller_promo_id,
            "seller_promo_discount": seller_promo_discount,
            "loyalty_id": loyalty_id,
            "loyalty_discount": loyalty_discount,
            "uuid_promocode": uuid_promocode,
            "sale_price_promocode_discount_prc": sale_price_promocode_discount_prc
        }

    def get_last_date(self):
        """Возвращает максимальную дату из поля rr_dt (дата отчёта) в таблице."""
        url = f"{self.baserow_url}/api/database/rows/table/{self.table_id}/"
        params = {"order_by": "-rr_dt", "size": 1, "user_field_names": "true"}
        try:
            resp = requests.get(url, headers=self.headers, params=params, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                if data.get("results"):
                    dt = data["results"][0].get("rr_dt")
                    if dt and isinstance(dt, str) and len(dt) >= 10:
                        return dt[:10]
            return "2026-01-01"
        except Exception as e:
            logger.error(f"Ошибка получения последней даты в реализации: {e}")
            return "2026-01-01"
