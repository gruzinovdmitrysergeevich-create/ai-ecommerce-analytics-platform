#!/usr/bin/env python3
"""
Загрузчик рекламной статистики Wildberries.
Таблица: wb_ads_stats (создаётся автоматически)
Использует POST /adv/v2/fullstats для получения статистики по всем кампаниям.
"""

import os
import requests
import logging
import time
from datetime import datetime, timedelta
from wb_base_loader import WBBaseLoader
from baserow_manager import BaserowManager

logger = logging.getLogger(__name__)

class WBAdsLoader(WBBaseLoader):
    """Загружает данные по рекламе Wildberries за указанные даты."""

    API_URL = "https://advert-api.wildberries.ru/adv/v2/fullstats"
    LIST_URL = "https://advert-api.wildberries.ru/adv/v1/promotion/count"
    DATE_FIELD = "date"

    def __init__(self, wb_token, db_token):
        # Получаем или создаём таблицу
        bm = BaserowManager()
        table_id = bm.get_table_id_by_name("wb_ads_stats")
        if table_id is None:
            logger.info("📦 Создаю таблицу wb_ads_stats...")
            table_id = bm.ensure_table("wb_ads_stats", bm.tables["wb_ads_stats"])
        else:
            logger.info(f"✅ Таблица wb_ads_stats уже существует, ID = {table_id}")

        super().__init__(table_id=table_id, table_name="wb_ads_stats", db_token=db_token, baserow_manager=bm)

        self.wb_token = wb_token
        self.headers = {
            "Authorization": wb_token,
            "Content-Type": "application/json"
        }

        # Получаем список ВСЕХ кампаний автоматически
        self.campaign_ids = self._fetch_all_campaign_ids()
        logger.info(f"📋 Загружено {len(self.campaign_ids)} кампаний")

    def _fetch_all_campaign_ids(self):
        """Получает список всех ID кампаний через API."""
        try:
            resp = requests.get(self.LIST_URL, headers=self.headers, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            ids = []
            for group in data.get("adverts", []):
                for item in group.get("advert_list", []):
                    ids.append(item["advertId"])
            return ids
        except Exception as e:
            logger.error(f"❌ Ошибка получения списка кампаний: {e}")
            return []

    def fetch_data_for_date(self, date):
        """
        Получает статистику за конкретную дату для всех кампаний.
        date: строка "YYYY-MM-DD"
        """
        if not self.campaign_ids:
            return []

        # Формируем тело запроса для всех кампаний
        request_body = [
            {"id": cid, "interval": {"begin": date, "end": date}}
            for cid in self.campaign_ids
        ]

        try:
            resp = requests.post(self.API_URL, headers=self.headers, json=request_body, timeout=60)

            if resp.status_code == 429:
                logger.warning("⏳ Rate limit, жду 65 секунд...")
                time.sleep(65)
                return self.fetch_data_for_date(date)

            if resp.status_code == 400:
                # Часто 400 означает, что за этот день вообще нет данных
                logger.debug(f"API вернул 400 (нет данных) за {date}")
                return []

            resp.raise_for_status()
            data = resp.json()

            if not isinstance(data, list):
                logger.warning(f"Неожиданный формат ответа: {type(data)}")
                return []

            all_rows = []
            for campaign_data in data:
                campaign_id = campaign_data.get("advertId")
                if not campaign_id:
                    continue

                days = campaign_data.get("days", [])
                for day_data in days:
                    day_date = day_data.get("date")
                    if day_date and "T" in day_date:
                        day_date = day_date.split("T")[0]

                    # Суммируем по всем приложениям (apps) и товарам (nms)
                    total_orders = 0
                    total_revenue = 0.0
                    impressions = day_data.get("views", 0)
                    clicks = day_data.get("clicks", 0)
                    cost = day_data.get("sum", 0.0)

                    for app in day_data.get("apps", []):
                        total_orders += app.get("orders", 0)
                        total_revenue += app.get("sum_price", 0.0)

                    all_rows.append({
                        "campaign_id": campaign_id,
                        "date": day_date,
                        "impressions": impressions,
                        "clicks": clicks,
                        "cost": cost,
                        "orders": total_orders,
                        "revenue": total_revenue,
                        "raw_data": str(day_data)
                    })

            logger.info(f"  Получено {len(all_rows)} записей за {date}")
            return all_rows

        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Ошибка запроса: {e}")
            return []
        except Exception as e:
            logger.error(f"❌ Непредвиденная ошибка: {e}")
            return []

    def transform_row(self, raw_row):
        """Преобразует запись для вставки в Baserow."""
        return {
            "unique_key": f"{raw_row['date']}_{raw_row['campaign_id']}",
            "date": raw_row["date"],
            "campaign_name": raw_row.get("campaign_name", ""),
            "impressions": raw_row["impressions"],
            "clicks": raw_row["clicks"],
            "cost": raw_row["cost"],
            "orders": raw_row["orders"],
            "revenue": raw_row["revenue"],
            "raw_data": raw_row["raw_data"]
        }
