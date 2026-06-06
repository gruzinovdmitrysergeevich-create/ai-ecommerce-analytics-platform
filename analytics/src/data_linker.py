#!/usr/bin/env python3
"""
data_linker.py — авто-поиск связей между таблицами Baserow.

Без хардкора. Сам находит:
  - Связи по датам (какие таблицы можно JOIN'ить по периоду)
  - Связи по совпадающим названиям колонок (артикул, sku, бренд)
  - Связи по числовым ID
  - Семантические связи через модель (таблица «реклама» + «продажи» → по дням)

Использование:
    from data_linker import DataLinker
    dl = DataLinker()
    graph = dl.build_graph()  # граф связей
    linked = dl.find_related("wb_aggregated")  # что связано с таблицей
"""

import sys
from pathlib import Path
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

import re
from collections import defaultdict
from datetime import datetime
import pandas as pd

from src.data_discovery import DataDiscovery


class DataLinker:
    def __init__(self, config_path=None):
        self.dd = DataDiscovery(config_path)
        self._tables = None       # [{table_id, table_name, workspace_name}, ...]
        self._schemas = {}        # table_id → [{name, type}, ...]
        self._samples = {}        # table_id → list of rows
        self._profiles = {}       # table_id → {rows, num_cols, date_cols, text_cols, date_range}

    # ════ Главный метод: построение графа связей ════

    def build_graph(self) -> dict:
        """Строит полный граф связей между ВСЕМИ таблицами."""
        self._discover_all()

        graph = {"tables": {}, "links": []}

        # Профилируем каждую таблицу
        for t in self._tables:
            profile = self._profile_table(t)
            self._profiles[t["table_id"]] = profile
            graph["tables"][t["table_name"]] = profile

        # 1. Связи по датам
        self._find_date_links(graph)

        # 2. Связи по названиям колонок
        self._find_column_links(graph)

        # 3. Связи по ID-колонкам
        self._find_id_links(graph)

        return graph

    def find_related(self, table_name: str) -> list[dict]:
        """Какие таблицы связаны с этой."""
        graph = self.build_graph()
        links = []
        for link in graph["links"]:
            if table_name in (link["from"], link["to"]):
                links.append(link)
        return links

    def get_join_hints(self) -> str:
        """Строка с подсказками для модели: как JOIN'ить таблицы."""
        graph = self.build_graph()
        hints = []
        for link in graph["links"]:
            hints.append(
                f"df_{link['from']}.{link['from_col']} ↔ df_{link['to']}.{link['to_col']} ({link['type']})"
            )
        return "\n".join(hints) if hints else "Связей не найдено (JOIN по датам вручную)"

    def get_table_profile(self, table_name: str) -> dict | None:
        """Профиль конкретной таблицы."""
        table = self.dd.find_table(table_name)
        if not table:
            return None
        return self._profile_table(table)

    # ════ Внутренние методы ════

    def _discover_all(self):
        """Загружает метаданные всех таблиц."""
        self._tables = self.dd.list_tables()
        for t in self._tables:
            tid = t["table_id"]
            self._schemas[tid] = self.dd.get_schema(tid)
            # Берём до 20 строк для анализа
            self._samples[tid] = self.dd.get_all_rows(tid, max_rows=100)
            if len(self._samples[tid]) > 20:
                self._samples[tid] = self._samples[tid][:20]

    def _profile_table(self, table: dict) -> dict:
        """Анализирует таблицу: типы колонок, периоды, ключевые слова."""
        tid = table["table_id"]
        schema = self._schemas.get(tid, [])
        sample_rows = self._samples.get(tid, [])

        num_cols = []
        date_cols = []
        text_cols = []
        id_cols = []

        for col in schema:
            name = col["name"]
            if name in ("id", "order", "Name", "Notes", "Active"):
                continue
            # ID-колонки
            if "_id" in name.lower() or re.match(r'^[A-Z]+\d*$', name):
                id_cols.append(name)
                continue

            # Проверяем по sample
            values = [r.get(name) for r in sample_rows[:20] if r.get(name) is not None]
            if not values:
                continue

            # Дата?
            if "date" in name.lower() or "дата" in name.lower() or "день" in name.lower():
                date_cols.append(name)
                continue

            # Число?
            numeric = 0
            for v in values[:10]:
                try:
                    float(str(v).replace(",", ".").replace(" ", ""))
                    numeric += 1
                except:
                    pass
            if numeric > len(values) * 0.3:
                num_cols.append(name)
            else:
                text_cols.append(name)

        # Диапазон дат
        date_range = None
        if date_cols and sample_rows:
            for dc in date_cols:
                dates = []
                for r in sample_rows[:100]:
                    v = r.get(dc)
                    if v:
                        try:
                            dates.append(pd.to_datetime(v))
                        except:
                            pass
                if dates:
                    date_range = f"{min(dates).date()} — {max(dates).date()}"
                    break

        # Слова-маркеры в названии таблицы и колонках
        all_lower = (table["table_name"] + " " + " ".join(c["name"].lower() for c in schema)).lower()
        markers = {
            "advertising": bool(re.search(r'ad|реклам|трафик|посев|attribution', all_lower)),
            "sales": bool(re.search(r'sales|продаж|realization|реализац|order|заказ', all_lower)),
            "finance": bool(re.search(r'выписк|банк|финанс|счёт|управленк|дебет|кредит', all_lower)),
            "returns": bool(re.search(r'return|возврат', all_lower)),
            "stock": bool(re.search(r'stock|склад|остат|warehouse', all_lower)),
            "marketing": bool(re.search(r'marketing|маркетинг|продвиж|cpc|cpm', all_lower)),
            "commissions": bool(re.search(r'комисс|удержан|логистик|штраф|penalty|commission', all_lower)),
        }

        return {
            "table_id": tid,
            "workspace": table["workspace_name"],
            "rows": len(sample_rows),
            "num_cols": num_cols,
            "date_cols": date_cols,
            "text_cols": text_cols[:10],
            "id_cols": id_cols,
            "date_range": date_range,
            "markers": {k: v for k, v in markers.items() if v},
        }

    def _find_date_links(self, graph: dict):
        """Связи по датам: таблицы с пересекающимися периодами."""
        tables = list(graph["tables"].items())

        for i, (name1, p1) in enumerate(tables):
            if not p1["date_cols"] or not p1["date_range"]:
                continue
            for name2, p2 in tables[i + 1:]:
                if not p2["date_cols"] or not p2["date_range"]:
                    continue
                # Если периоды пересекаются — связь по дате
                if p1["workspace"] == p2["workspace"]:
                    continue  # один воркспейс — неинтересно

                graph["links"].append({
                    "from": name1,
                    "to": name2,
                    "from_col": p1["date_cols"][0],
                    "to_col": p2["date_cols"][0],
                    "type": "date",
                    "note": f"JOIN по дням: {p1['date_range']} ↔ {p2['date_range']}",
                })

    def _find_column_links(self, graph: dict):
        """Связи по совпадающим названиям колонок."""
        tables = list(graph["tables"].items())
        # Ключевые слова для сопоставления
        matches = {
            "артикул": ["article", "sku", "артикул", "vendor", "offer_id", "nm_id", "nm"],
            "бренд": ["brand", "бренд", "brand_name"],
            "категория": ["category", "категория", "subject", "тип"],
            "заказ": ["order", "заказ", "order_id", "orders"],
            "продажи": ["sales", "продаж", "revenue", "выручк", "sum", "сумм", "price", "цена"],
            "возврат": ["return", "возврат", "returns"],
            "комиссия": ["commission", "комисс", "fee", "удержан"],
            "логистика": ["logistic", "логистик", "delivery", "доставк"],
        }

        for i, (name1, p1) in enumerate(tables):
            cols1 = [c.lower() for c in p1["text_cols"] + p1["num_cols"] + p1["id_cols"]]
            for name2, p2 in tables[i + 1:]:
                cols2 = [c.lower() for c in p2["text_cols"] + p2["num_cols"] + p2["id_cols"]]
                for concept, keywords in matches.items():
                    c1 = next((c for c in cols1 if any(kw in c for kw in keywords)), None)
                    c2 = next((c for c in cols2 if any(kw in c for kw in keywords)), None)
                    if c1 and c2:
                        graph["links"].append({
                            "from": name1, "to": name2,
                            "from_col": c1, "to_col": c2,
                            "type": f"column:{concept}",
                            "note": f"Обе таблицы содержат '{concept}'",
                        })
                        break  # одна связь на пару таблиц

    def _find_id_links(self, graph: dict):
        """Связи по ID-колонкам (совпадающие значения)."""
        tables = list(graph["tables"].items())
        for i, (name1, p1) in enumerate(tables):
            if not p1["id_cols"]:
                continue
            for name2, p2 in tables[i + 1:]:
                if not p2["id_cols"]:
                    continue
                for id1 in p1["id_cols"]:
                    for id2 in p2["id_cols"]:
                        if id1.lower() == id2.lower():
                            graph["links"].append({
                                "from": name1, "to": name2,
                                "from_col": id1, "to_col": id2,
                                "type": "id",
                                "note": f"Ключ: {id1}",
                            })


# ════ Тест ════

if __name__ == "__main__":
    dl = DataLinker()
    print("🔍 Строю граф связей...")
    graph = dl.build_graph()

    print(f"\n📊 Таблиц: {len(graph['tables'])}")
    for name, p in graph["tables"].items():
        markers = ", ".join(p["markers"].keys()) if p["markers"] else "—"
        print(f"  {name}: {p['rows']} строк, маркеры: {markers}")

    print(f"\n🔗 Связей: {len(graph['links'])}")
    for link in graph["links"][:15]:
        print(f"  {link['from']} ↔ {link['to']} ({link['type']}) — {link['note'][:80]}")

    print("\n📝 Подсказки для JOIN:")
    print(dl.get_join_hints())
