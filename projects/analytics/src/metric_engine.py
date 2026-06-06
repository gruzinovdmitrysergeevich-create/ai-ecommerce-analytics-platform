#!/usr/bin/env python3
"""
metric_engine.py — детерминированный расчёт метрик. Модель НЕ считает.

Все формулы — ЗДЕСЬ. Модель получает готовые цифры и только интерпретирует.

Метрики:
  - Финансовые: выручка, расходы, прибыль, маржа, ДРР, ROMI
  - Маркетинговые: CPC, CPM, CTR, конверсия, средний чек
  - Юнит-экономика: выручка/ед, расход/ед, прибыль/ед
  - Аномалии: сравнение периодов, поиск выбросов

Использование:
    from src.metric_engine import MetricEngine
    me = MetricEngine(dataframes)
    metrics = me.calculate("вопрос пользователя")
"""

import sys
from pathlib import Path
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

import json
import re
import pandas as pd
import numpy as np
from collections import defaultdict
from datetime import datetime, timedelta


class MetricEngine:
    def __init__(self, dataframes: dict, linker=None):
        """
        dataframes: {"df_имя": pd.DataFrame, ...}
        linker: DataLinker instance (опционально)
        """
        self.dfs = dataframes
        self.linker = linker
        self._results = {}

    # ════ Главный метод ════

    def calculate(self, question: str) -> dict:
        """Авто-определение нужных метрик по вопросу и расчёт."""
        q = question.lower()
        metrics = {}

        # Финансовые
        if any(w in q for w in ["доход", "расход", "прибыл", "убыток", "финанс", "итог"]):
            metrics.update(self._calc_financial())

        # Реклама + продажи
        if any(w in q for w in ["дрр", "romi", "реклам", "эффективност", "окупаемост"]):
            metrics.update(self._calc_ad_efficiency())

        # Маркетинг
        if any(w in q for w in ["cpc", "cpm", "ctr", "конверси", "воронк", "лид"]):
            metrics.update(self._calc_marketing())

        # Юнит-экономика
        if any(w in q for w in ["юнит", "единиц", "штук", "unit", "себестоимост", "маржа"]):
            metrics.update(self._calc_unit_economics())

        # Аномалии
        if any(w in q for w in ["аномал", "выброс", "отклонен", "сравн", "разниц"]):
            metrics.update(self._calc_anomalies())

        # Если ничего не нашли — считаем всё
        if not metrics:
            metrics.update(self._calc_financial())
            metrics.update(self._calc_ad_efficiency())

        self._results = metrics
        return metrics

    def format_for_model(self, metrics: dict = None) -> str:
        """Форматирует метрики для передачи модели."""
        if metrics is None:
            metrics = self._results
        lines = []
        for key, val in metrics.items():
            if isinstance(val, float):
                lines.append(f"  {key}: {val:,.2f}")
            elif isinstance(val, dict):
                lines.append(f"  {key}:")
                for k, v in val.items():
                    if isinstance(v, float):
                        lines.append(f"    {k}: {v:,.2f}")
                    else:
                        lines.append(f"    {k}: {v}")
            elif isinstance(val, list):
                lines.append(f"  {key}: {len(val)} записей")
            else:
                lines.append(f"  {key}: {val}")
        return "\n".join(lines)

    # ════ Финансовые метрики ════

    def _calc_financial(self) -> dict:
        """Расчёт финансовых метрик из банковской выписки."""
        result = {}

        bank_df = self._find_df(["выписк", "банк", "счёт"])
        if bank_df is None:
            return {"error": "Банковская выписка не найдена"}

        # Находим колонки
        credit_col = self._find_col(bank_df, ["кредит", "поступлен", "приход", "credit", "income"])
        debit_col = self._find_col(bank_df, ["дебет", "списан", "расход", "debit", "expense"])
        date_col = self._find_col(bank_df, ["дата", "date"])
        cp_col = self._find_col(bank_df, ["контрагент", "counterparty", "получател", "плательщик"])

        if credit_col and debit_col:
            # Конвертируем
            debit = pd.to_numeric(bank_df[debit_col], errors="coerce").fillna(0)
            credit = pd.to_numeric(bank_df[credit_col], errors="coerce").fillna(0)

            result["total_income"] = float(credit.sum())
            result["total_expense"] = float(debit.sum())
            result["operational_profit"] = float(credit.sum() - debit.sum())
            result["transaction_count"] = len(bank_df)

            # По годам если есть дата
            if date_col:
                bank_df["_year"] = pd.to_datetime(bank_df[date_col], errors="coerce").dt.year
                for year in sorted(bank_df["_year"].dropna().unique()):
                    ydf = bank_df[bank_df["_year"] == year]
                    y_credit = pd.to_numeric(ydf[credit_col], errors="coerce").fillna(0).sum()
                    y_debit = pd.to_numeric(ydf[debit_col], errors="coerce").fillna(0).sum()
                    result[f"income_{int(year)}"] = float(y_credit)
                    result[f"expense_{int(year)}"] = float(y_debit)
                    result[f"profit_{int(year)}"] = float(y_credit - y_debit)

        return result

    # ════ Эффективность рекламы ════

    def _calc_ad_efficiency(self) -> dict:
        """ДРР, ROMI, окупаемость рекламы."""
        result = {}

        # Ищем таблицу рекламных расходов
        ad_df = self._find_df(["traffic", "реклам", "посев", "attribution", "internal_advert"])
        sales_df = self._find_df(["продаж", "sales", "realization", "wb_aggregat", "ozon_aggregat"])

        # Альтернативно — из банка (Церебро)
        bank_df = self._find_df(["выписк", "банк", "счёт"])

        # Расходы на рекламу
        ad_spend = 0.0

        if ad_df is not None:
            spend_col = self._find_col(ad_df, ["cost", "spent", "стоимост", "трат", "бюджет", "расход", "sum", "сумм", "потрачено"])
            if spend_col:
                ad_spend = float(pd.to_numeric(ad_df[spend_col], errors="coerce").fillna(0).sum())
                result["ad_spend_source"] = "таблица рекламы"

        if ad_spend == 0 and bank_df is not None:
            cp_col = self._find_col(bank_df, ["контрагент", "counterparty"])
            debit_col = self._find_col(bank_df, ["дебет", "списан"])
            if cp_col and debit_col:
                cereb = bank_df[bank_df[cp_col].astype(str).str.lower().str.contains("церебро", na=False)]
                if len(cereb):
                    ad_spend = float(pd.to_numeric(cereb[debit_col], errors="coerce").fillna(0).sum())
                    result["ad_spend_source"] = "Церебро (банк)"

        result["ad_spend"] = ad_spend

        # Выручка
        revenue = 0.0
        if sales_df is not None:
            rev_col = self._find_col(sales_df, ["выручк", "revenue", "продаж", "sales", "total", "сумм", "price", "цена"])
            if rev_col:
                revenue = float(pd.to_numeric(sales_df[rev_col], errors="coerce").fillna(0).sum())
                result["revenue_source"] = "таблица продаж"

        # Из банка
        if revenue == 0 and bank_df is not None:
            cp_col = self._find_col(bank_df, ["контрагент"])
            credit_col = self._find_col(bank_df, ["кредит", "поступлен"])
            if cp_col and credit_col:
                wb = bank_df[bank_df[cp_col].astype(str).str.lower().str.contains("рвб|wildberries", na=False)]
                oz = bank_df[bank_df[cp_col].astype(str).str.lower().str.contains("интернет решен|ozon", na=False)]
                revenue = float(pd.to_numeric(pd.concat([wb, oz])[credit_col], errors="coerce").fillna(0).sum())
                result["revenue_source"] = "банк (WB+Ozon)"
                result["revenue_wb"] = float(pd.to_numeric(wb[credit_col], errors="coerce").fillna(0).sum()) if len(wb) else 0
                result["revenue_ozon"] = float(pd.to_numeric(oz[credit_col], errors="coerce").fillna(0).sum()) if len(oz) else 0

        result["revenue"] = revenue

        # ДРР
        if revenue > 0:
            result["DRR"] = ad_spend / revenue
            if result["DRR"] > 0.5:
                result["DRR_alert"] = "КРИТИЧЕСКИЙ — реклама съедает больше половины выручки"
            elif result["DRR"] > 0.3:
                result["DRR_alert"] = "ВЫСОКИЙ — требуется оптимизация"

        # ROMI
        if ad_spend > 0:
            result["ROMI"] = (revenue - ad_spend) / ad_spend

        return result

    # ════ Маркетинговые метрики ════

    def _calc_marketing(self) -> dict:
        """CPC, CPM, CTR, конверсия."""
        result = {}

        ad_df = self._find_df(["traffic", "реклам", "посев", "attribution"])

        if ad_df is not None:
            # CPC
            cost_col = self._find_col(ad_df, ["cost", "spent", "стоимост", "трат", "бюджет", "расход", "потрачено"])
            click_col = self._find_col(ad_df, ["click", "клик", "переход", "clicks", "клики"])
            if cost_col and click_col:
                cost = pd.to_numeric(ad_df[cost_col], errors="coerce").fillna(0)
                clicks = pd.to_numeric(ad_df[click_col], errors="coerce").fillna(0)
                if clicks.sum() > 0:
                    result["CPC"] = float(cost.sum() / clicks.sum())
                    result["total_clicks"] = int(clicks.sum())

            # CPM
            impr_col = self._find_col(ad_df, ["impress", "показ", "cpm", "reach", "охват", "impressions", "просмотр"])
            if cost_col and impr_col:
                cost = pd.to_numeric(ad_df[cost_col], errors="coerce").fillna(0)
                impr = pd.to_numeric(ad_df[impr_col], errors="coerce").fillna(0)
                if impr.sum() > 0:
                    result["CPM"] = float(cost.sum() / impr.sum() * 1000)
                    result["total_impressions"] = int(impr.sum())

            # CTR
            if click_col and impr_col:
                clicks = pd.to_numeric(ad_df[click_col], errors="coerce").fillna(0)
                impr = pd.to_numeric(ad_df[impr_col], errors="coerce").fillna(0)
                if impr.sum() > 0:
                    result["CTR"] = float(clicks.sum() / impr.sum())

        # Конверсия (из sales_funnel)
        funnel_df = self._find_df(["funnel", "воронк"])
        if funnel_df is not None:
            order_col = self._find_col(funnel_df, ["order", "заказ", "buyout"])
            view_col = self._find_col(funnel_df, ["view", "просмотр", "visit", "session", "сессия"])
            if order_col and view_col:
                orders = pd.to_numeric(funnel_df[order_col], errors="coerce").fillna(0)
                views = pd.to_numeric(funnel_df[view_col], errors="coerce").fillna(0)
                if views.sum() > 0:
                    result["conversion_rate"] = float(orders.sum() / views.sum())

        # Средний чек
        sales_df = self._find_df(["продаж", "sales", "aggregat"])
        if sales_df is not None:
            rev_col = self._find_col(sales_df, ["выручк", "revenue", "продаж", "sales", "total", "сумм"])
            order_col = self._find_col(sales_df, ["order", "заказ", "orders"])
            if rev_col and order_col:
                rev = pd.to_numeric(sales_df[rev_col], errors="coerce").fillna(0)
                orders = pd.to_numeric(sales_df[order_col], errors="coerce").fillna(0)
                if orders.sum() > 0:
                    result["avg_check"] = float(rev.sum() / orders.sum())

        return result

    # ════ Юнит-экономика ════

    def _calc_unit_economics(self) -> dict:
        """Прибыль на единицу, маржа."""
        result = {}

        sales_df = self._find_df(["продаж", "sales", "aggregat"])
        bank_df = self._find_df(["выписк", "банк"])

        if sales_df is not None:
            rev_col = self._find_col(sales_df, ["выручк", "revenue", "total", "сумм", "price"])
            qty_col = self._find_col(sales_df, ["количеств", "quantity", "qty", "шт", "order", "заказ", "units", "count"])

            if rev_col and qty_col:
                rev = pd.to_numeric(sales_df[rev_col], errors="coerce").fillna(0)
                qty = pd.to_numeric(sales_df[qty_col], errors="coerce").fillna(0)
                if qty.sum() > 0:
                    result["revenue_per_unit"] = float(rev.sum() / qty.sum())
                    result["total_units"] = int(qty.sum())
                    result["total_revenue"] = float(rev.sum())

                    # Комиссии
                    comm_col = self._find_col(sales_df, ["комисс", "commission", "fee", "удержан"])
                    if comm_col:
                        comm = pd.to_numeric(sales_df[comm_col], errors="coerce").fillna(0)
                        result["commission_per_unit"] = float(comm.sum() / qty.sum()) if qty.sum() > 0 else 0
                        result["total_commission"] = float(comm.sum())
                        # Маржа с учётом комиссий
                        net_rev = rev.sum() - comm.sum()
                        result["net_revenue"] = float(net_rev)
                        result["margin"] = float(net_rev / rev.sum()) if rev.sum() > 0 else 0

        return result

    # ════ Аномалии ════

    def _calc_anomalies(self) -> dict:
        """Сравнение периодов, поиск выбросов."""
        result = {}

        bank_df = self._find_df(["выписк", "банк", "счёт"])
        if bank_df is not None:
            date_col = self._find_col(bank_df, ["дата", "date"])
            debit_col = self._find_col(bank_df, ["дебет", "списан"])
            credit_col = self._find_col(bank_df, ["кредит", "поступлен"])

            if date_col and debit_col and credit_col:
                bank_df["_date"] = pd.to_datetime(bank_df[date_col], errors="coerce")
                bank_df["_month"] = bank_df["_date"].dt.to_period("M")
                bank_df["_debit"] = pd.to_numeric(bank_df[debit_col], errors="coerce").fillna(0)
                bank_df["_credit"] = pd.to_numeric(bank_df[credit_col], errors="coerce").fillna(0)

                monthly = bank_df.groupby("_month").agg(
                    income=("_credit", "sum"),
                    expense=("_debit", "sum"),
                    count=("_debit", "count"),
                ).reset_index()

                if len(monthly) >= 2:
                    # Сравниваем последние два месяца
                    monthly = monthly.sort_values("_month")
                    last = monthly.iloc[-1]
                    prev = monthly.iloc[-2]

                    result["compare_periods"] = f"{prev['_month']} → {last['_month']}"
                    result["income_change"] = float(last["income"] - prev["income"])
                    result["income_change_pct"] = float((last["income"] - prev["income"]) / prev["income"] * 100) if prev["income"] else 0
                    result["expense_change"] = float(last["expense"] - prev["expense"])
                    result["expense_change_pct"] = float((last["expense"] - prev["expense"]) / prev["expense"] * 100) if prev["expense"] else 0

                    # Аномалии: выбросы (> 2σ от среднего)
                    for col, name in [("income", "доход"), ("expense", "расход")]:
                        mean, std = monthly[col].mean(), monthly[col].std()
                        if std > 0:
                            outliers = monthly[abs(monthly[col] - mean) > 2 * std]
                            if len(outliers):
                                result[f"anomaly_{name}"] = [
                                    f"{r['_month']}: {r[col]:,.0f} (отклонение {abs(r[col]-mean)/std:.1f}σ)"
                                    for _, r in outliers.iterrows()
                                ]

        return result

    # ════ Вспомогательные методы ════

    def _find_df(self, keywords: list[str]):
        """Ищет DataFrame по ключевым словам в имени."""
        for name, df in self.dfs.items():
            name_lower = name.lower()
            if any(kw in name_lower for kw in keywords):
                return df
        return None

    def _find_col(self, df, keywords: list[str]) -> str | None:
        """Ищет колонку по ключевым словам."""
        for col in df.columns:
            col_lower = col.lower()
            if any(kw in col_lower for kw in keywords):
                return col
        return None
