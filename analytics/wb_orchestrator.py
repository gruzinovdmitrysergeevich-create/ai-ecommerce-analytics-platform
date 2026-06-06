#!/usr/bin/env python3
import os
import sys
import logging
import argparse
import time
import requests
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from loaders.wb_sales_loader import WBSalesLoader
from loaders.wb_realization_loader import WBRealizationLoader
from loaders.wb_ads_loader import WBAdsLoader
from loaders.ozon_postings_loader import OzonPostingsLoader
from loaders.ozon_realization_loader import OzonRealizationLoader
from loaders.ozon_ads_loader import OzonAdsLoader
from loaders.ozon_vendor_loader import OzonVendorLoader
from loaders.ozon_finance_v2_loader import OzonFinanceV2Loader
from loaders.ozon_transactions_detail_loader import OzonTransactionsDetailLoader

from baserow_manager import BaserowManager, DB_TOKEN
from ozon_auth import OzonPerformanceAuth

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('orchestrator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('orchestrator')

WB_TOKEN = os.environ.get('WB_TOKEN', '')
OZON_CLIENT_ID = os.environ.get('OZON_CLIENT_ID', '')
OZON_API_KEY = os.environ.get('OZON_API_KEY', '')
OZON_PERF_CLIENT_ID = os.environ.get('OZON_PERF_CLIENT_ID', '')
OZON_PERF_CLIENT_SECRET = os.environ.get('OZON_PERF_CLIENT_SECRET', '')

if not WB_TOKEN:
    logger.error("❌ Не задан WB_TOKEN")
    sys.exit(1)

if not OZON_PERF_CLIENT_ID or not OZON_PERF_CLIENT_SECRET:
    logger.error("❌ Не заданы OZON_PERF_CLIENT_ID и OZON_PERF_CLIENT_SECRET")
    sys.exit(1)

if not OZON_CLIENT_ID or not OZON_API_KEY:
    logger.error("❌ Не заданы OZON_CLIENT_ID и OZON_API_KEY")
    sys.exit(1)

ozon_auth = OzonPerformanceAuth(OZON_PERF_CLIENT_ID, OZON_PERF_CLIENT_SECRET)
ozon_token = ozon_auth.get_token()
if not ozon_token:
    logger.error("❌ Не удалось получить токен Ozon")
    sys.exit(1)
logger.info("✅ Токен Ozon получен")

def is_baserow_ready():
    try:
        headers = {"Authorization": f"Token {DB_TOKEN}"}
        r = requests.get(f"http://localhost:8000/api/database/rows/table/863/",
                         headers=headers, params={"size": 1}, timeout=5)
        return r.status_code == 200
    except Exception as e:
        logger.error(f"Ошибка подключения к Baserow: {e}")
        return False

def get_ozon_campaigns():
    """Получает список всех ID кампаний Ozon Performance"""
    try:
        url = "https://api-performance.ozon.ru/api/client/campaign"
        headers = {"Authorization": f"Bearer {ozon_token}"}
        resp = requests.get(url, headers=headers, timeout=30)
        if resp.status_code != 200:
            logger.error(f"Ошибка получения списка кампаний Ozon: {resp.text}")
            return []
        data = resp.json()
        campaigns = data.get('list', [])
        ids = [c['id'] for c in campaigns]
        logger.info(f"📋 Получено {len(ids)} кампаний Ozon")
        return ids
    except Exception as e:
        logger.error(f"Ошибка при получении списка кампаний Ozon: {e}")
        return []

def run_loader(loader_class, *args, **kwargs):
    force_start = kwargs.pop('force_start', None) if kwargs else None
    force_end = kwargs.pop('force_end', None) if kwargs else None

    try:
        loader = loader_class(*args, **kwargs)
        if force_start and force_end:
            start = datetime.strptime(force_start, '%Y-%m-%d')
            end = datetime.strptime(force_end, '%Y-%m-%d')
            dates = [(start + timedelta(days=i)).strftime('%Y-%m-%d')
                     for i in range((end - start).days + 1)]
            logger.info(f"📅 {loader_class.__name__}: принудительный период {force_start} - {force_end} (всего {len(dates)} дней)")
            return loader.load_dates(dates)
        else:
            last_date = loader.get_last_date()
            start = datetime.strptime(last_date, '%Y-%m-%d') + timedelta(days=1)
            end = datetime.now()
            if start.date() > end.date():
                logger.info(f"⏭️ {loader_class.__name__}: нет новых данных (последняя дата {last_date})")
                return 0
            dates = []
            current = start
            while current.date() <= end.date():
                dates.append(current.strftime('%Y-%m-%d'))
                current += timedelta(days=1)
            logger.info(f"📅 {loader_class.__name__}: загрузка с {dates[0]} по {dates[-1]} (всего {len(dates)} дней)")
            return loader.load_dates(dates)
    except Exception as e:
        logger.error(f"❌ Ошибка в {loader_class.__name__}: {e}", exc_info=True)
        return 0

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--force-period', nargs=2, metavar=('START', 'END'),
                        help='Принудительный период YYYY-MM-DD YYYY-MM-DD')
    args = parser.parse_args()

    logger.info("=" * 60)
    logger.info("🚀 Оркестратор загрузки данных Wildberries и Ozon")
    logger.info("=" * 60)

    if not is_baserow_ready():
        logger.error("❌ Baserow недоступен. Завершение.")
        sys.exit(1)
    logger.info("✅ Baserow доступен")

    bm = BaserowManager()

    ozon_campaigns = get_ozon_campaigns()
    if not ozon_campaigns:
        logger.warning("⚠️ Не удалось получить список кампаний Ozon, рекламный загрузчик может не работать")

    loaders_config = [
        {'class': WBSalesLoader, 'args': (WB_TOKEN, DB_TOKEN), 'kwargs': {}},
        {'class': WBRealizationLoader, 'args': (WB_TOKEN, DB_TOKEN), 'kwargs': {}},
        {'class': WBAdsLoader, 'args': (WB_TOKEN, DB_TOKEN), 'kwargs': {}},
        {'class': OzonPostingsLoader, 'args': (OZON_CLIENT_ID, OZON_API_KEY, DB_TOKEN), 'kwargs': {}},
        {'class': OzonRealizationLoader, 'args': (OZON_CLIENT_ID, OZON_API_KEY, DB_TOKEN), 'kwargs': {}},
        {'class': OzonAdsLoader, 'args': (ozon_token, DB_TOKEN, ozon_campaigns), 'kwargs': {}},
        {'class': OzonVendorLoader, 'args': (ozon_token, DB_TOKEN), 'kwargs': {}},
        {'class': OzonFinanceV2Loader, 'args': (OZON_CLIENT_ID, OZON_API_KEY, DB_TOKEN), 'kwargs': {}},
        {'class': OzonTransactionsDetailLoader, 'args': (OZON_CLIENT_ID, OZON_API_KEY, DB_TOKEN), 'kwargs': {}},
    ]

    if args.force_period:
        force_start, force_end = args.force_period
        for cfg in loaders_config:
            cfg['kwargs']['force_start'] = force_start
            cfg['kwargs']['force_end'] = force_end
        logger.info(f"📅 Принудительный период: {force_start} → {force_end}")
    else:
        logger.info("📅 Автоматический режим (загрузка новых данных)")

    total_uploaded = 0
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {}
        for cfg in loaders_config:
            future = executor.submit(run_loader, cfg['class'], *cfg['args'], **cfg['kwargs'])
            futures[future] = cfg['class'].__name__

        logger.info(f"📋 Запущено {len(futures)} загрузчиков")
        for future in as_completed(futures):
            name = futures[future]
            try:
                result = future.result()  # без таймаута
                logger.info(f"✅ {name} загружено {result} записей")
                total_uploaded += result
            except Exception as e:
                logger.error(f"❌ {name} завершился ошибкой: {e}")

        logger.info("🏁 Все загрузчики завершили работу, завершаем...")
        executor.shutdown(wait=False)

    logger.info(f"🏁 Оркестратор завершён. Всего загружено записей: {total_uploaded}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("🛑 Прервано пользователем")
        sys.exit(0)
    except Exception as e:
        logger.exception(f"💥 Непредвиденная ошибка: {e}")
        sys.exit(1)
