#!/usr/bin/env python3
"""
analyst.py — v5. Универсальный AI-аналитик. Без хардкора.

Архитектура:
  Pre-flight → DataDiscovery → DataLinker → MetricEngine → Sandbox → Вывод

Два режима:
  Простой: MetricEngine считает метрики → модель пишет вывод
  Глубокий: облако генерит код → песочница → локалка интерпретирует

Запуск:
  python3 analyst.py "вопрос"
"""

import sys, re, json
from pathlib import Path
from datetime import datetime
import pandas as pd
import numpy as np

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))

from src.model_provider import ModelProvider
from src.data_discovery import DataDiscovery
from src.data_linker import DataLinker
from src.metric_engine import MetricEngine
from src.sandbox import Sandbox


# ════ PRE-FLIGHT ════

def preflight(dd: DataDiscovery) -> dict:
    """Проверка окружения перед анализом. Возвращает статус."""
    status = {"ok": True, "warnings": []}

    # Baserow
    try:
        tables = dd.list_tables()
        status["tables_count"] = len(tables)
    except Exception as e:
        status["ok"] = False
        status["error"] = f"Baserow недоступен: {e}"
        return status

    if not tables:
        status["ok"] = False
        status["error"] = "В Baserow нет таблиц"
        return status

    # Проверка объёмов
    for t in tables:
        try:
            count = dd.get_row_count(t["table_id"])
            if count < 5:
                status["warnings"].append(f"⚠️ {t['table_name']}: всего {count} строк")
        except:
            pass

    return status


# ════ КЛАССИФИКАЦИЯ БАНКА (моделью, без хардкора) ════

BANK_CLASSIFICATION_CACHE = None  # глобальный кэш


def classify_bank_with_model(bank_df: pd.DataFrame, cp_col: str,
                             credit_col: str, debit_col: str,
                             provider: ModelProvider) -> dict:
    """
    Классифицирует контрагентов через модель.
    Возвращает словарь: {контрагент: {"category": ..., "is_income": bool, "is_personal": bool}}
    """
    global BANK_CLASSIFICATION_CACHE
    if BANK_CLASSIFICATION_CACHE is not None:
        return BANK_CLASSIFICATION_CACHE

    # Уникальные контрагенты с суммами
    cps = {}
    for _, row in bank_df.iterrows():
        cp = str(row.get(cp_col, "") or "").strip()
        if not cp or len(cp) < 3:
            continue
        credit = float(row.get(credit_col, 0) or 0)
        debit = float(row.get(debit_col, 0) or 0)
        if cp not in cps:
            cps[cp] = {"credit": 0.0, "debit": 0.0}
        cps[cp]["credit"] += credit
        cps[cp]["debit"] += debit

    if not cps:
        return {}

    # Топ-30 по объёму операций
    top = sorted(cps.items(), key=lambda x: x[1]["credit"] + x[1]["debit"], reverse=True)[:30]

    # Строим промпт для модели
    cp_list = "\n".join(
        f"  {cp[:60]} | поступления: {v['credit']:,.0f}₽ | списания: {v['debit']:,.0f}₽"
        for cp, v in top
    )

    prompt = f"""Ты бухгалтер. Классифицируй этих контрагентов.

Контрагенты из банковской выписки бизнеса СТМ LANER (торговля на Wildberries и Ozon):

{cp_list}

Для каждого контрагента дай ТОЛЬКО JSON в формате:
{{"контрагент": {{"category": "категория", "is_income": true/false, "is_personal": false}}}}

Где:
- category: одна из [wb_income, ozon_income, advertising, packaging, logistics, raw_materials, taxes, accounting, bank_fees, personal, other]
- is_income: true если это ПОСТУПЛЕНИЯ от бизнеса
- is_personal: true если это ЛИЧНЫЕ операции (переводы между своими счетами, депозиты, физлица по ФИО)

Правила:
- РВБ, Wildberries → wb_income, is_income=true
- Интернет Решения, Ozon → ozon_income, is_income=true
- Церебро, Cerebro → advertising, is_income=false
- Клинотек → packaging, is_income=false
- Гусейнов, Садам → logistics, is_income=false
- Скоромный → raw_materials, is_income=false
- Налоги, ФНС, казначейство → taxes
- Физлица (ФИО) с переводами → personal, is_personal=true
- Депозиты → personal, is_personal=true

Выведи ТОЛЬКО JSON, без <think>, без пояснений."""

    print("  🤖 Классифицирую контрагентов через модель...")
    resp = provider.classify(prompt)

    if not resp:
        print("  ⚠️ Модель не ответила — использую базовые правила")
        return _fallback_classification(cps)

    # Извлекаем JSON
    try:
        m = re.search(r'\{.*\}', resp, re.DOTALL)
        if m:
            classification = json.loads(m.group(0))
            print(f"  ✅ Классифицировано: {len(classification)} контрагентов")
            BANK_CLASSIFICATION_CACHE = classification
            return classification
    except json.JSONDecodeError:
        pass

    print("  ⚠️ Модель вернула не-JSON — использую базовые правила")
    return _fallback_classification(cps)


def _fallback_classification(cps: dict) -> dict:
    """Запасная классификация по ключевым словам (если модель не смогла)."""
    rules = {
        "wb_income": ["рвб", "wildberries"],
        "ozon_income": ["интернет решен", "ozon"],
        "advertising": ["церебро", "cerebro", "digital"],
        "packaging": ["клинотек"],
        "logistics": ["гусейнов", "садам"],
        "raw_materials": ["скоромный"],
        "taxes": ["фнс", "казначей", "налог"],
        "accounting": ["иско", "бухгалтер"],
        "personal": ["кучмин", "грузинов", "депозит", "депп"],
    }
    result = {}
    for cp in cps:
        cp_lower = cp.lower()
        classified = False
        for cat, keywords in rules.items():
            if any(kw in cp_lower for kw in keywords):
                result[cp] = {
                    "category": cat,
                    "is_income": cat.endswith("_income"),
                    "is_personal": cat == "personal",
                }
                classified = True
                break
        if not classified:
            result[cp] = {"category": "other", "is_income": False, "is_personal": False}
    return result


# ════ ГЛАВНЫЙ ЦИКЛ ════

def run_question(question: str) -> dict:
    """Вызов из кода (Streamlit, API). Возвращает {output, error, status}."""
    import io, sys as _sys
    old_stdout = _sys.stdout
    _sys.stdout = io.StringIO()
    try:
        # Эмулируем CLI-вызов: подменяем argv и вызываем main
        old_argv = _sys.argv
        _sys.argv = ["analyst.py", question]
        main()
        output = _sys.stdout.getvalue()
        return {"output": output, "status": "ok"}
    except Exception as e:
        return {"error": str(e), "status": "error"}
    finally:
        _sys.stdout = old_stdout
        _sys.argv = old_argv


def main():
    question = " ".join(a for a in sys.argv[1:] if not a.startswith("--"))
    if not question:
        question = "Дай полный финансовый анализ за всё время"

    print("=" * 60)
    print(f"📊 АНАЛИТИК v5 | {datetime.now().strftime('%H:%M')}")
    print(f"   Вопрос: {question[:100]}")
    print("=" * 60)

    # 1. Pre-flight
    print("\n🔍 Pre-flight проверка...")
    dd = DataDiscovery()
    status = preflight(dd)
    if not status["ok"]:
        print(f"❌ {status['error']}")
        return
    for w in status.get("warnings", []):
        print(f"  {w}")

    # 2. Модели
    provider = ModelProvider()

    # 3. Загружаем все данные
    print(f"\n📥 Загружаю {status['tables_count']} таблиц...")
    dataframes = {}
    all_schemas = []

    for t in dd.list_tables():
        # Загружаем ВСЕ строки для маленьких таблиц, до 5000 для больших
        count = dd.get_row_count(t["table_id"])
        if count < 5:
            print(f"  ⏭️ {t['table_name']}: {count} строк (пропущено)")
            continue
        max_rows = 5000 if count > 5000 else count + 100
        sample_rows = dd.get_all_rows(t["table_id"], max_rows=max_rows)
        if not sample_rows:
            print(f"  ⏭️ {t['table_name']}: пусто")
            continue

        df_sample = pd.DataFrame(sample_rows)  # семпл для схемы
        
        # Конвертируем русские числа: "3,848,324.00" → 3848324.00
        for col in df_sample.columns:
            try:
                # Если колонка содержит строки с запятыми и числами
                sample_vals = df_sample[col].dropna().astype(str).head(5)
                if any("," in str(v) and any(c.isdigit() for c in str(v)) for v in sample_vals):
                    df_sample[col] = df_sample[col].astype(str).str.replace(",", "").str.replace(" ", "")
                    df_sample[col] = pd.to_numeric(df_sample[col], errors="coerce")
            except:
                pass
        
        name = t["table_name"]
        safe_name = re.sub(r'[^a-zA-Zа-яА-Я0-9_]', '_', name).lower()
        dataframes[f"df_{safe_name}"] = df_sample
        all_schemas.append({"name": safe_name, "rows": len(df_sample), "sample": sample_rows[:1], "workspace": t["workspace_name"]})

        print(f"  ✅ {name}: {len(df_sample)} строк, {len(df_sample.columns)} колонок")

    if not dataframes:
        print("❌ Нет данных для анализа")
        return

    # 4. DataLinker — связи между таблицами
    print(f"\n🔗 Ищу связи между таблицами...")
    linker = DataLinker()
    join_hints = linker.get_join_hints()
    print(f"   Найдено связей: {len(linker.build_graph()['links'])}")

    # 5. MetricEngine — детерминированные метрики
    print(f"\n📐 Считаю метрики...")
    me = MetricEngine(dataframes, linker)
    metrics = me.calculate(question)

    # 6. Определяем режим
    deep_keywords = ["свяжи", "корреляци", "зависи", "причин",
                     "разниц", "расхожден", "аномал",
                     "воронк", "реклама и продаж",
                     "join", "merge", "объедини", "построй график"]
    is_deep = any(re.search(kw, question.lower()) for kw in deep_keywords)

    # 7. Банк: классификация моделью
    bank_df = None
    for key in dataframes:
        if any(kw in key for kw in ["выписк", "банк", "счёт"]):
            bank_df = dataframes[key]
            break

    bank_classification = {}
    if bank_df is not None:
        cp_col = _find_col(bank_df, ["контрагент", "counterparty"])
        credit_col = _find_col(bank_df, ["кредит", "поступлен", "приход"])
        debit_col = _find_col(bank_df, ["дебет", "списан", "расход"])

        if cp_col and credit_col and debit_col:
            bank_classification = classify_bank_with_model(
                bank_df, cp_col, credit_col, debit_col, provider
            )

            # Считаем bank summary по классификации
            bank_summary = _summarize_bank(bank_df, cp_col, credit_col, debit_col, bank_classification)
            for k, v in bank_summary.items():
                if k not in metrics:
                    metrics[k] = v

    # 8. Анализ
    if is_deep:
        _run_deep_analysis(question, dataframes, all_schemas, join_hints, metrics, provider)
    else:
        _run_simple_analysis(question, metrics, provider)

    print("\n✅ ГОТОВО")


# ════ ПРОСТОЙ РЕЖИМ ════

def _run_simple_analysis(question: str, metrics: dict, provider: ModelProvider):
    """MetricEngine считает → модель интерпретирует."""
    print(f"\n📊 РЕЖИМ: базовый анализ")

    metrics_text = MetricEngine(dataframes={}, linker=None).format_for_model(metrics)

    prompt = f"""Ты старший финансовый аналитик. Без <think>. Отвечай на русском.

Контекст: бизнес СТМ LANER, торговля на Wildberries (FBS) и Ozon (FBO).

Вопрос: {question}

РАССЧИТАННЫЕ МЕТРИКИ (скрипт посчитал, проверять не надо):
{metrics_text}

СТРУКТУРА ОТВЕТА (обязательно):
## Краткий ответ (1-2 предложения)
## Ключевые метрики (таблица: метрика | значение)
## Анализ (почему такие цифры, что на них повлияло)
## Рекомендации (что делать, на что обратить внимание)

В метриках расшифровывай аббревиатуры: ДРР = доля рекламных расходов (сколько копеек рекламы на рубль выручки), ROMI = окупаемость инвестиций в рекламу, CPC = цена клика.
"""

    print(f"  🧠 Модель анализирует...")
    result = provider.interpret(prompt)

    if metrics:
        # Выводим ключевые метрики
        for key in ["total_income", "total_expense", "operational_profit",
                     "revenue", "ad_spend", "DRR", "ROMI", "margin"]:
            if key in metrics:
                val = metrics[key]
                if isinstance(val, float):
                    if key in ("DRR", "margin", "CTR", "conversion_rate"):
                        print(f"  {key}: {val:.1%}")
                    elif abs(val) >= 1000:
                        print(f"  {key}: {val:,.0f} ₽")
                    else:
                        print(f"  {key}: {val:.2f}")

    if result:
        print(f"\n{'='*60}")
        print(result)
    else:
        print("\n❌ Модель не ответила")


# ════ ГЛУБОКИЙ РЕЖИМ ════

def _run_deep_analysis(question: str, dataframes: dict, schemas: list,
                       join_hints: str, metrics: dict, provider: ModelProvider):
    """Облако генерит код → песочница → локалка интерпретирует."""
    print(f"\n🔬 РЕЖИМ: глубокий анализ")
    print(f"   (облако → код → песочница → локалка → интерпретация)")

    # Схемы для модели — только РЕЛЕВАНТНЫЕ таблицы
    schemas_text = ""
    q_lower = question.lower()

    for s in schemas:
        df_key = f"df_{s['name']}"
        df = dataframes.get(df_key)
        if df is None or df.empty:
            continue

        # Пропускаем таблицы без данных и явно нерелевантные
        name_lower = df_key.lower()
        skip = {"stock_on_warehouses", "turnover_stocks", "sales_funnel", "internal_advertising"}
        if any(s in name_lower for s in skip):
            continue

        # ВСЕ колонки
        all_cols = list(df.columns)
        schemas_text += f"\nDataFrame: {df_key} ({len(df)} строк, {len(all_cols)} колонок)\n"
        schemas_text += f"  Источник: {s.get('workspace', '?')}\n"
        schemas_text += f"  ВСЕ колонки: {', '.join(all_cols)}\n"

        # Ищем НЕПУСТУЮ строку для примера
        sample_row = None
        skip_cols = {"id", "order", "Name", "Notes", "Active"}
        for _, row in df.iterrows():
            non_empty = {k: v for k, v in row.items()
                        if k not in skip_cols and v is not None and v != "" and v != "None"}
            if len(non_empty) >= 3:
                sample_row = non_empty
                break
        if sample_row:
            schemas_text += f"  Пример строки: {json.dumps(sample_row, ensure_ascii=False, default=str)[:400]}\n"

        # Диапазон дат
        date_cols = [c for c in all_cols if "date" in c.lower() or "дата" in c.lower()]
        if date_cols:
            try:
                dates = pd.to_datetime(df[date_cols[0]], errors="coerce").dropna()
                if len(dates):
                    schemas_text += f"  Период: {dates.min().date()} — {dates.max().date()}\n"
            except:
                pass

    # Метрики (уже посчитаны)
    metrics_text = MetricEngine(dataframes={}).format_for_model(metrics) if metrics else ""

    if join_hints:
        schemas_text += f"\n\n🔗 СВЯЗИ МЕЖДУ ТАБЛИЦАМИ (используй для JOIN):\n{join_hints[:2000]}"

    if metrics_text:
        schemas_text += f"\n\n📐 ГОТОВЫЕ МЕТРИКИ (уже посчитаны скриптом, используй для проверки):\n{metrics_text[:1000]}"

    # Запускаем Sandbox
    sb = Sandbox(dataframes)

    def generate_code(prompt: str) -> str | None:
        return provider.code(prompt)

    print(f"  🔄 Генерация кода → песочница → retry...")
    ok, output, history = sb.execute_with_retry(generate_code, question, schemas_text)

    # Статистика retry
    attempts = len([h for h in history if "attempt" in h])
    errors = len([h for h in history if not h.get("ok", False)])
    print(f"  📊 Попыток: {attempts}, ошибок: {errors}")

    if ok:
        print(f"  ✅ Код выполнен!")
        print(f"\n{'='*60}")
        print("📊 РЕЗУЛЬТАТ ВЫПОЛНЕНИЯ КОДА")
        print(f"{'='*60}")
        print(output[:3000])

        # Интерпретация
        print(f"\n  🧠 Локальная модель интерпретирует...")
        interp_prompt = f"""Ты финансовый аналитик. Без <think>. На русском.

Контекст: СТМ LANER, Wildberries + Ozon.

Вопрос пользователя: {question}

ГОТОВЫЕ МЕТРИКИ (скрипт посчитал):
{metrics_text[:1500]}

РЕЗУЛЬТАТ АНАЛИЗА (из кода):
{output[:3000]}

Дай:
## Что показал анализ (1-2 предложения сути)
## Причины (почему так произошло)
## Рекомендации (что делать)

Расшифровывай аббревиатуры. Говори по-русски понятно."""
        interp = provider.interpret(interp_prompt)
        if interp:
            print(f"\n{'='*60}")
            print("🧠 ЗАКЛЮЧЕНИЕ")
            print(f"{'='*60}")
            print(interp)
    else:
        print(f"  ❌ Код не выполнен после {attempts} попыток")
        print(f"\n{output[:2000]}")


# ════ ВСПОМОГАТЕЛЬНЫЕ ════

def _find_col(df: pd.DataFrame, keywords: list[str]) -> str | None:
    """Ищет колонку по ключевым словам."""
    for col in df.columns:
        cl = col.lower()
        if any(kw in cl for kw in keywords):
            return col
    return None


def _summarize_bank(bank_df: pd.DataFrame, cp_col: str,
                    credit_col: str, debit_col: str,
                    classification: dict) -> dict:
    """Суммирует банк по классифицированным категориям."""
    result = {"income": {}, "expense": {}, "personal_in": 0.0, "personal_out": 0.0}

    for _, row in bank_df.iterrows():
        cp = str(row.get(cp_col, "") or "").strip()
        credit = float(row.get(credit_col, 0) or 0)
        debit = float(row.get(debit_col, 0) or 0)

        cat = classification.get(cp, {})

        if cat.get("is_personal"):
            result["personal_in"] += credit
            result["personal_out"] += debit
            continue

        if credit > 0:
            cat_name = cat.get("category", "other_income")
            result["income"][cat_name] = result["income"].get(cat_name, 0) + credit

        if debit > 0:
            cat_name = cat.get("category", "other_expense")
            result["expense"][cat_name] = result["expense"].get(cat_name, 0) + debit

    # Итоги
    result["total_income"] = sum(result["income"].values())
    result["total_expense"] = sum(result["expense"].values())
    result["operational_profit"] = result["total_income"] - result["total_expense"]

    return result


if __name__ == "__main__":
    main()
