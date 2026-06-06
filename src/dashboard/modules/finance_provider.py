#!/usr/bin/env python3
"""finance_provider.py — быстрая загрузка с дисковым кешем."""
import urllib.request, json, time, os

print("[DEBUG] finance_provider.py LOADED v2026-05-31")

BASEROW_URL = "http://localhost:8000"
JWT_EMAIL = "gruzinov.dmitry.sergeevich@gmail.com"
JWT_PASS = "1I9N59!_09&"
CACHE_FILE = "/tmp/finance_cache.json"

_DEBUG_LOG = "/tmp/finance_debug.log"

def _log(msg):
    with open(_DEBUG_LOG, "a") as f:
        f.write(f"{time.strftime('%H:%M:%S')} {msg}\n")

_log(f"MODULE LOADED {__file__}")

_jwt_cache = {"token": None, "ts": 0}
_meta_cache = None
_rows_cache = {}

def _get_jwt():
    now = time.time()
    if _jwt_cache["token"] and (now - _jwt_cache["ts"]) < 3600:
        return _jwt_cache["token"]
    data = json.dumps({"email": JWT_EMAIL, "password": JWT_PASS}).encode()
    req = urllib.request.Request(f"{BASEROW_URL}/api/user/token-auth/", data=data,
                                  headers={"Content-Type": "application/json"})
    jwt = json.loads(urllib.request.urlopen(req, timeout=15).read())["token"]
    _jwt_cache["token"] = jwt
    _jwt_cache["ts"] = now
    return jwt

def _api(path, timeout=20):
    jwt = _get_jwt()
    req = urllib.request.Request(f"{BASEROW_URL}{path}")
    req.add_header("Authorization", f"JWT {jwt}")
    return json.loads(urllib.request.urlopen(req, timeout=timeout).read())

def _discover():
    global _meta_cache
    if _meta_cache:
        return _meta_cache
    try:
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE) as f:
                cached = json.load(f)
                if time.time() - cached.get("ts", 0) < 3600:
                    _meta_cache = cached["tables"]
                    return _meta_cache
    except:
        pass
    _meta_cache = []
    try:
        for app in _api("/api/applications/", 15):
            if app.get("type") == "database":
                db_id = app["id"]
                try:
                    for t in _api(f"/api/database/tables/database/{db_id}/", 15):
                        _meta_cache.append({"name": t["name"], "id": t["id"], "db": db_id})
                except:
                    pass
    except:
        pass
    try:
        with open(CACHE_FILE, "w") as f:
            json.dump({"tables": _meta_cache, "ts": time.time()}, f)
    except:
        pass
    return _meta_cache

def _load_rows(tid, table_name):
    """Загружает все строки таблицы (с кешем 5 минут)."""
    cache_key = f"{tid}_{table_name}"
    now = time.time()
    if cache_key in _rows_cache:
        cached, ts = _rows_cache[cache_key]
        if now - ts < 3600:
            return cached
    rows = []
    page = 1
    while True:
        try:
            data = _api(f"/api/database/rows/table/{tid}/?page={page}&size=200&user_field_names=true", 20)
            rows.extend(data["results"])
            if not data.get("next"):
                break
            page += 1
        except:
            break
    _rows_cache[cache_key] = (rows, now)
    return rows

def _sumf(rows, field):
    return round(sum(float(r.get(field, 0) or 0) for r in rows), 2)

def _sumf_abs(rows, field):
    return round(sum(abs(float(r.get(field, 0) or 0)) for r in rows), 2)

def _extract_date(r):
    """Извлекает дату из записи в формате YYYY-MM-DD."""
    for key in ["date", "saleDt", "rrDate", "orderDt", "operation_date", "month", "created_at", "Дата", "updTime"]:
        val = r.get(key)
        if val:
            s = str(val)
            return s[:10]
    return ""

def _classify_wb_article(article):
    """Классифицирует WB артикул по комплектам: 800g=mono, 1600g=double, 2400g=triple."""
    import re
    a = str(article).upper()
    # Приоритет: 2400 > 1600 > 800 (избегаем ложных срабатываний)
    if re.search(r'2400', a):
        return "triple"
    elif re.search(r'1600', a) or re.search(r'_2\b', a):
        return "double"
    elif re.search(r'800', a):
        return "mono"
    return None

def _classify_ozon_offer(offer_id):
    """Классифицирует Ozon offer_id по комплектам."""
    o = str(offer_id).upper()
    if "1600" in o or "2" in o:
        return "double"
    elif "2400" in o or "3" in o:
        return "triple"
    elif "800" in o:
        return "mono"
    return None

def _classify_ozon_accruals(accruals):
    """Эвристика: определяет комплект по сумме accruals_for_sale (реализация: 800г ≈ 402₽, 1600г ≈ 691₽)."""
    if accruals <= 550:
        return "mono"
    elif accruals <= 1000:
        return "double"
    else:
        return "triple"

def get_finance_summary(date_str):
    _log(f"get_finance_summary({date_str}) CALLED")
    result = {
        "wb_sold": 0, "wb_mono": 0, "wb_double": 0, "wb_triple": 0, "wb_revenue": 0,
        "ozon_sold": 0, "ozon_mono": 0, "ozon_double": 0, "ozon_triple": 0, "ozon_revenue": 0,
        "income": 0, "expense": 0, "profit": 0, "drr": 0,
        "ad_expense": 0, "wb_ad_expense": 0, "traffic_ad_expense": 0
    }
    has_wb_raw = False
    has_ozon_raw = False
    has_wb_agg = False
    has_ozon_agg = False
    
    try:
        tables = _discover()
        # ── Первый проход: найдём realization_detail для комплектов ──
        # (он самый полный — 14K строк с vendorCode)
        for t in tables:
            rows = _load_rows(t["id"], t["name"])
            if not rows:
                continue
            keys = list(rows[0].keys())
            kset = set(keys)
            filtered = [r for r in rows if _extract_date(r) == date_str]
            
            # === WB REALIZATION DETAIL (комплекты + расходы) ===
            if {"deliveryService","ppvzSalesCommission","rrDate"}.issubset(kset):
                if filtered:
                    # Расходы
                    for col in ["deliveryService","penalty","acquiringFee","ppvzSalesCommission",
                               "paidStorage","paidAcceptance","deduction","rebillLogisticCost"]:
                        if col in kset:
                            result["expense"] += _sumf(filtered, col)
                    
                    # КОМПЛЕКТЫ из vendorCode (самый глубокий источник)
                    if "vendorCode" in kset:
                        _log(f"realization_detail: {len(filtered)} rows, classifying by vendorCode")
                        for r in filtered:
                            vc = r.get("vendorCode", "") or ""
                            if not vc:
                                continue
                            kit = _classify_wb_article(vc)
                            if kit == "mono": result["wb_mono"] += 1
                            elif kit == "double": result["wb_double"] += 1
                            elif kit == "triple": result["wb_triple"] += 1
                        # wb_sold = сумма всех классифицированных комплектов
                        result["wb_sold"] = result["wb_mono"] + result["wb_double"] + result["wb_triple"]
                        has_wb_raw = True  # Блокируем wb_aggregated от двойного счёта
                        _log(f"realization_detail kits: mono={result['wb_mono']} double={result['wb_double']} triple={result['wb_triple']} total={result['wb_sold']}")
                        
                        # Выручка из forPay realization_detail
                        rev = _sumf(filtered, "forPay")
                        if rev > 0:
                            result["wb_revenue"] += rev
                        _log(f"realization_detail forPay revenue: {rev}")
        
        # ── Второй проход: остальные таблицы ──
        for t in tables:
            rows = _load_rows(t["id"], t["name"])
            if not rows:
                continue
            keys = list(rows[0].keys())
            kset = set(keys)
            filtered = [r for r in rows if _extract_date(r) == date_str]
            
            # === WB ПРОДАЖИ (raw) — выручка если realization_detail не дал ===
            if {"forPay","supplierArticle","nmId","incomeID"}.issubset(kset):
                if filtered:
                    has_wb_raw = True
                    rev = _sumf(filtered, "forPay")
                    # Добавляем выручку (если realization_detail уже дал — суммируем)
                    if result["wb_revenue"] == 0:
                        result["wb_revenue"] += rev
                    # Если realization_detail не дал комплектов — берём из sales
                    if result["wb_sold"] == 0:
                        result["wb_sold"] += len(filtered)
                        for r in filtered:
                            article = r.get("supplierArticle", "")
                            kit = _classify_wb_article(article)
                            if kit == "mono": result["wb_mono"] += 1
                            elif kit == "double": result["wb_double"] += 1
                            elif kit == "triple": result["wb_triple"] += 1
                        _log(f"sales fallback: sold={len(filtered)} rev={rev}")
            
            # === OZON ТРАНЗАКЦИИ (raw) ===
            elif "sale_commission" in kset and "operation_type" in kset:
                if filtered:
                    has_ozon_raw = True
                    sales_rows = [r for r in filtered if float(r.get("accruals_for_sale", 0) or 0) > 0]
                    result["ozon_sold"] += len(sales_rows)
                    rev = _sumf(sales_rows, "accruals_for_sale")
                    result["ozon_revenue"] += rev
                    # Комиссия и доставка в Ozon часто отрицательные в таблице — берём abs
                    result["expense"] += _sumf_abs(filtered, "sale_commission")
                    result["expense"] += _sumf_abs(filtered, "delivery_charge")
                    # Разбивка по комплектам (эвристика по accruals — в transactions нет offer_id)
                    for r in sales_rows:
                        acc = float(r.get("accruals_for_sale", 0) or 0)
                        kit = _classify_ozon_accruals(acc)
                        if kit == "mono": result["ozon_mono"] += 1
                        elif kit == "double": result["ozon_double"] += 1
                        elif kit == "triple": result["ozon_triple"] += 1
            
            # === OZON АГРЕГИРОВАННЫЕ (с date) ===
            elif "order_count" in kset and "total_amount" in kset and "total_sales" in kset:
                has_ozon_agg = True
                if not has_ozon_raw and filtered:
                    result["ozon_sold"] += int(_sumf(filtered, "order_count"))
                    rev = _sumf(filtered, "total_sales")
                    if rev <= 0:
                        rev = abs(_sumf(filtered, "total_amount"))
                    result["ozon_revenue"] += rev
                    result["expense"] += _sumf_abs(filtered, "total_commission")
                    result["expense"] += _sumf_abs(filtered, "total_delivery")
                    result["expense"] += _sumf_abs(filtered, "total_return_delivery")
            
            # === OZON legacy (posting_number) ===
            elif {"posting_number","total_payout"}.issubset(kset):
                if filtered:
                    result["ozon_sold"] += len(filtered)
                    rev = _sumf(filtered, "total_payout")
                    result["ozon_revenue"] += rev
                    result["expense"] += _sumf(filtered, "total_commission")
            
            # === WB АГРЕГИРОВАННЫЕ (только revenue, не sold — sold из realization_detail) ===
            elif "total_forPay" in kset and "total_quantity" in kset:
                has_wb_agg = True
                if filtered:
                    # Не трогаем wb_sold — он уже из realization_detail
                    # Только revenue и расходы
                    if result["wb_revenue"] == 0:
                        rev = _sumf(filtered, "total_forPay")
                        if rev == 0 and "total_retail_amount" in kset:
                            rev = _sumf(filtered, "total_retail_amount")
                        result["wb_revenue"] += rev
                    result["expense"] += _sumf(filtered, "total_commission")
                    result["expense"] += _sumf(filtered, "total_logistics")
                    result["expense"] += _sumf(filtered, "total_penalties")
            
            # === РЕКЛАМА WB (ads_upd) ===
            elif "updSum" in kset and "updTime" in kset:
                if filtered:
                    s = _sumf(filtered, "updSum")
                    result["wb_ad_expense"] += s
                    result["ad_expense"] += s
            
            # === ТРАФИК (traffic_purchase) ===
            elif "spent" in kset and "date" in kset:
                if filtered:
                    s = _sumf(filtered, "spent")
                    result["traffic_ad_expense"] += s
                    result["ad_expense"] += s
            elif "Потрачено_руб" in kset and "Дата" in kset:
                if filtered:
                    s = _sumf(filtered, "Потрачено_руб")
                    result["traffic_ad_expense"] += s
                    result["ad_expense"] += s
            
            # Generic cost+impressions (legacy fallback — не добавляем в ad_expense, чтобы не дублировать)
            elif {"cost","impressions","clicks"}.issubset(kset):
                if filtered:
                    s = _sumf(filtered, "cost")
                    result["ad_expense"] += s
            
            # === ФИНАНС АГРЕГИРОВАННЫЕ ===
            elif {"total_debit","total_credit"}.issubset(kset):
                if not has_wb_raw and not has_ozon_raw and filtered:
                    result["income"] += _sumf(filtered, "total_debit")
                    result["expense"] += _sumf(filtered, "total_credit")
            
            # === ФИНАНСОВАЯ ВЫПИСКА (Дебет/Кредит) ===
            elif "Дебет,_RUR" in kset and "Кредит,_RUR" in kset:
                if filtered:
                    for r in filtered:
                        debit = float(r.get("Дебет,_RUR", 0) or 0)
                        credit = float(r.get("Кредит,_RUR", 0) or 0)
                        if credit > 0:
                            result["income"] += credit
                        if debit > 0:
                            result["expense"] += debit
            
            # === УПРАВЛЕНКА (ДЕБЕТ/КРЕДИТ) ===
            elif "ДЕБЕТ_(списания)" in kset and "КРЕДИТ_(поступления)" in kset:
                if filtered:
                    for r in filtered:
                        debit = float(r.get("ДЕБЕТ_(списания)", 0) or 0)
                        credit = float(r.get("КРЕДИТ_(поступления)", 0) or 0)
                        if credit > 0:
                            result["income"] += credit
                        if debit > 0:
                            result["expense"] += debit
            
            # === legacy amount (fallback) ===
            elif "amount" in kset and "Сумма" not in kset and "total_amount" not in kset:
                if filtered:
                    for r in filtered:
                        amt = float(r.get("amount", 0) or 0)
                        if amt < 0:
                            result["expense"] += abs(amt)
                        elif amt > 0 and not has_wb_raw and not has_ozon_raw:
                            result["income"] += amt
        
        # Итоговый доход: продажи WB + Ozon (primary source)
        result["income"] = round(result["wb_revenue"] + result["ozon_revenue"], 2)
        
        # Fallback: если wb_revenue=0, оцениваем по средним ценам из sales-таблицы
        if result["wb_revenue"] == 0 and result["wb_sold"] > 0:
            _log("wb_revenue=0, estimating from average sales prices")
            # Ищем таблицу sales для средних цен
            avg_prices = {"mono": 0, "double": 0, "triple": 0}
            for t in tables:
                rows = _load_rows(t["id"], t["name"])
                if not rows:
                    continue
                kset = set(rows[0].keys())
                if {"forPay","supplierArticle","nmId","incomeID"}.issubset(kset):
                    from collections import defaultdict
                    kit_prices = defaultdict(list)
                    for r in rows:
                        fp = float(r.get("forPay", 0) or 0)
                        if fp > 0:
                            kit = _classify_wb_article(r.get("supplierArticle", ""))
                            if kit:
                                kit_prices[kit].append(fp)
                    for kit, prices in kit_prices.items():
                        if prices:
                            avg_prices[kit] = round(sum(prices) / len(prices), 2)
                    _log(f"avg prices from sales: {dict(avg_prices)}")
                    break
            
            if avg_prices["mono"] > 0 or avg_prices["double"] > 0 or avg_prices["triple"] > 0:
                est_rev = 0.0
                if avg_prices["mono"] > 0:
                    est_rev += result["wb_mono"] * avg_prices["mono"]
                if avg_prices["double"] > 0:
                    est_rev += result["wb_double"] * avg_prices["double"]
                if avg_prices["triple"] > 0:
                    est_rev += result["wb_triple"] * avg_prices["triple"]
                result["wb_revenue"] = round(est_rev, 2)
                result["income"] = round(result["wb_revenue"] + result["ozon_revenue"], 2)
                result["wb_revenue_estimated"] = True
                _log(f"estimated wb_revenue: {result['wb_revenue']} (mono={result['wb_mono']}×{avg_prices['mono']} + double={result['wb_double']}×{avg_prices['double']} + triple={result['wb_triple']}×{avg_prices['triple']})")
        
        result["expense"] = round(result["expense"], 2)
        # Добавляем рекламные расходы в общие расходы (для profit)
        result["expense"] = round(result["expense"] + result["ad_expense"], 2)
        result["profit"] = round(result["income"] - result["expense"], 2)
        result["wb_revenue"] = round(result["wb_revenue"], 2)
        result["ozon_revenue"] = round(result["ozon_revenue"], 2)
        
        # Суммарный ad-расход
        total_ad = round(result["wb_ad_expense"] + result["traffic_ad_expense"], 2)
        
        _log(f"RESULT wb_sold={result['wb_sold']} wb_rev={result['wb_revenue']} ozon={result['ozon_sold']} profit={result['profit']} total_ad={total_ad}")
        
        # ДРР = (вся реклама) / (выручка с ненулевых маркетплейсов) × 100
        effective_revenue = 0.0
        if result["wb_revenue"] > 0:
            effective_revenue += result["wb_revenue"]
        if result["ozon_revenue"] > 0:
            effective_revenue += result["ozon_revenue"]
        
        if effective_revenue > 0:
            result["drr"] = round((total_ad / effective_revenue) * 100, 1)
        elif total_ad > 0:
            result["drr"] = -1  # «∞» — реклама есть, выручки нет
        else:
            result["drr"] = 0
        
    except Exception as e:
        result["error"] = str(e)
    return result
