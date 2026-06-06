#!/usr/bin/env python3
"""
Загрузчик для всех типов внутренней рекламы Ozon.
Использует поле unique_key для защиты от дубликатов на стороне Baserow.
"""

import requests
import time
import csv
import io
import logging
import json
from collections import defaultdict
from datetime import datetime, timedelta
from wb_base_loader import WBBaseLoader
from urllib.parse import urljoin

logger = logging.getLogger(__name__)

class OzonAdsLoader(WBBaseLoader):
    TABLE_ID = None
    BASE_URL = "https://api-performance.ozon.ru"

    CAMPAIGN_CONFIGS = {
        "CPO": {
            "endpoint": "/api/client/statistic/orders/generate",
            "needs_aggregation": True,
            "parser": "_parse_cpo_report",
            "aggregator": "_aggregate_cpo",
            "description": "Оплата за заказ"
        },
        "CPC": {
            "endpoint": "/api/client/statistics",
            "needs_aggregation": False,
            "parser": "_parse_cpc_report",
            "mapper": "_map_cpc_row",
            "description": "Оплата за клик"
        }
    }

    def __init__(self, auth_token, db_token, campaign_ids):
        from baserow_manager import BaserowManager
        bm = BaserowManager()
        table_id = bm.get_table_id_by_name("ozon_ads_stats")
        if not table_id:
            logger.info("Таблица ozon_ads_stats не найдена, создаю...")
            bm.ensure_table("ozon_ads_stats", bm.tables["ozon_ads_stats"])
            table_id = bm.get_table_id_by_name("ozon_ads_stats")
        
        super().__init__(table_id, "ozon_ads_stats", db_token)
        self.auth_token = auth_token
        self.campaign_ids = campaign_ids if campaign_ids else []
        self.ozon_headers = {
            "Authorization": f"Bearer {auth_token}",
            "Content-Type": "application/json"
        }

        if not self.campaign_ids:
            raise ValueError("Не указаны campaign_ids")

        self.campaign_types = self._fetch_campaign_types()
        self.campaign_type = self._determine_campaign_type()
        self.config = self.CAMPAIGN_CONFIGS[self.campaign_type]
        logger.info(f"✅ Тип кампании определён: {self.campaign_type} – {self.config['description']}")

    def _fetch_campaign_types(self):
        url = f"{self.BASE_URL}/api/client/campaign"
        try:
            resp = requests.get(url, headers=self.ozon_headers, timeout=30)
            if resp.status_code != 200:
                logger.error(f"Ошибка получения списка кампаний: {resp.text}")
                raise Exception("Не удалось получить список кампаний")
            data = resp.json()
            campaigns = data.get('list', [])
            types = {}
            for c in campaigns:
                cid = c['id']
                payment_type = c.get('PaymentType')
                if payment_type in self.CAMPAIGN_CONFIGS:
                    types[cid] = payment_type
                else:
                    logger.warning(f"Кампания {cid} имеет неизвестный тип {payment_type}, пропускаем")
            return types
        except Exception as e:
            logger.error(f"Ошибка при получении списка кампаний: {e}")
            raise

    def _determine_campaign_type(self):
        first_id = self.campaign_ids[0]
        ctype = self.campaign_types.get(first_id)
        if not ctype:
            raise Exception(f"Кампания {first_id} не найдена в списке кампаний или имеет неподдерживаемый тип")
        for cid in self.campaign_ids[1:]:
            if self.campaign_types.get(cid) != ctype:
                logger.warning(f"Кампания {cid} имеет другой тип, это может привести к ошибкам. Используем тип {ctype} для всех.")
        return ctype

    def fetch_data_for_date(self, date):
        if not self.campaign_ids:
            logger.error("Не указаны campaign_ids")
            return []

        if self.campaign_type == "CPO":
            payload = {
                "from": f"{date}T00:00:00Z",
                "to": f"{date}T23:59:59Z",
                "campaignId": self.campaign_ids[0]
            }
        else:
            payload = {
                "campaigns": self.campaign_ids,
                "from": f"{date}T00:00:00Z",
                "to": f"{date}T23:59:59Z",
                "groupBy": "DATE"
            }

        url = f"{self.BASE_URL}{self.config['endpoint']}"
        try:
            resp = requests.post(url, headers=self.ozon_headers, json=payload, timeout=30)
            if resp.status_code != 200:
                logger.error(f"Ошибка запуска отчёта ({self.campaign_type}): {resp.text}")
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
                    f"{self.BASE_URL}/api/client/statistics/{uuid}",
                    headers=self.ozon_headers,
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

            with open("/tmp/ozon_ads_report.csv", "w", encoding="utf-8") as f:
                f.write(resp.text)
            logger.info("Сырой отчёт сохранён в /tmp/ozon_ads_report.csv")

            parser_method = getattr(self, self.config['parser'])
            return parser_method(resp.text)

        except Exception as e:
            logger.error(f"Ошибка при скачивании/парсинге CSV: {e}")
            return []

    def _parse_cpo_report(self, content):
        lines = content.strip().splitlines()
        if len(lines) < 3:
            logger.error("Отчёт CPO слишком короткий")
            return []
        header = lines[1].split(';')
        data_lines = lines[2:]
        rows = []
        for line in data_lines:
            values = line.split(';')
            row = dict(zip(header, values))
            rows.append(row)
        logger.info(f"Скачано {len(rows)} строк из CPO-отчёта")
        return rows

    def _parse_cpc_report(self, content):
        lines = content.strip().splitlines()
        if len(lines) < 2:
            logger.error("Отчёт CPC слишком короткий")
            return []
        header_line = None
        data_start = 0
        for i, line in enumerate(lines):
            if 'Дата' in line or 'date' in line.lower():
                header_line = line
                data_start = i + 1
                break
        if not header_line:
            logger.error("Не удалось найти заголовки в CPC-отчёте")
            return []
        header = header_line.split(';')
        data_lines = lines[data_start:]
        rows = []
        for line in data_lines:
            if not line.strip():
                continue
            values = line.split(';')
            row = dict(zip(header, values))
            rows.append(row)
        logger.info(f"Скачано {len(rows)} строк из CPC-отчёта")
        return rows

    def _aggregate_cpo(self, rows, date):
        groups = defaultdict(lambda: {'orders': 0, 'revenue': 0.0, 'cost': 0.0})
        for r in rows:
            campaign = r.get('Источник заказов', '').strip()
            if not campaign:
                continue
            groups[campaign]['orders'] += 1
            rev = r.get('Стоимость продажи, ₽', '0').replace(',', '.').replace(' ', '')
            cost = r.get('Расход, ₽', '0').replace(',', '.').replace(' ', '')
            try:
                groups[campaign]['revenue'] += float(rev) if rev else 0.0
            except:
                pass
            try:
                groups[campaign]['cost'] += float(cost) if cost else 0.0
            except:
                pass

        records = []
        for campaign, agg in groups.items():
            # Нормализуем название кампании (убираем внешние кавычки)
            campaign_clean = campaign.strip('"')
            unique_key = f"{date}_{campaign_clean}"
            record = {
                'date': date,
                'campaign_name': campaign_clean,
                'unique_key': unique_key,
                'impressions': 0,
                'clicks': 0,
                'ctr': 0.0,
                'cost': round(agg['cost'], 2),
                'orders': agg['orders'],
                'revenue': round(agg['revenue'], 2),
                'drr': 0.0,
                'raw_data': ''
            }
            records.append(record)
        return records

    def _map_cpc_row(self, row, date):
        field_map = {
            'Дата': 'date',
            'Название кампании': 'campaign_name',
            'Показы': 'impressions',
            'Клики': 'clicks',
            'CTR, %': 'ctr',
            'Расход, Р, с НДС': 'cost',
            'Заказы': 'orders',
            'Выручка, Р': 'revenue',
            'ДРР, %': 'drr'
        }
        record = {'date': date}
        campaign_name = ''
        for csv_field, table_field in field_map.items():
            value = row.get(csv_field, '')
            if table_field == 'date':
                continue
            if table_field == 'campaign_name':
                campaign_name = value.strip().strip('"')
                record[table_field] = campaign_name
            elif table_field in ('impressions', 'clicks', 'orders'):
                try:
                    record[table_field] = int(float(value.replace(',', '.'))) if value else 0
                except:
                    record[table_field] = 0
            elif table_field in ('ctr', 'drr', 'cost', 'revenue'):
                try:
                    cleaned = value.replace(' ', '').replace(',', '.').replace('Р', '').strip()
                    record[table_field] = float(cleaned) if cleaned else 0.0
                except:
                    record[table_field] = 0.0
            else:
                record[table_field] = str(value) if value else ''
        for field in ['impressions', 'clicks', 'ctr', 'cost', 'orders', 'revenue', 'drr']:
            if field not in record:
                record[field] = 0
        if not record.get('campaign_name'):
            record['campaign_name'] = ''
        record['unique_key'] = f"{date}_{record['campaign_name']}"
        record['raw_data'] = ''
        return record

    def load_dates(self, date_list):
        all_records = []
        for date in date_list:
            logger.info(f"  📥 Загрузка {self.campaign_type} за {date}...")
            rows = self.fetch_data_for_date(date)
            if not rows:
                continue

            if self.config.get('needs_aggregation', False):
                new_records = self._aggregate_cpo(rows, date)
            else:
                new_records = []
                for r in rows:
                    rec = self._map_cpc_row(r, date)
                    if rec.get('campaign_name'):
                        new_records.append(rec)
                    else:
                        logger.warning("Пропущена строка без названия кампании")

            all_records.extend(new_records)
            time.sleep(1)

        if not all_records:
            logger.info("Нет новых записей для вставки")
            return 0

        # Вставка батчами с игнорированием ошибок уникальности
        inserted = 0
        for i in range(0, len(all_records), 200):
            batch = all_records[i:i+200]
            # Попробуем вставить batch
            try:
                result = self.upload_batch(batch)
                inserted += result
            except Exception as e:
                logger.error(f"Ошибка при вставке батча: {e}")
                # Возможно, часть записей не вставилась из-за дубликатов, но это нормально
        return inserted

    def transform_row(self, raw_row):
        return raw_row
