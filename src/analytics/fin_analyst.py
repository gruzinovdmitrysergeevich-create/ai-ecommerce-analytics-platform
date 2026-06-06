#!/usr/bin/env python3
"""
fin_analyst.py - Полная версия с очисткой числовых колонок и преобразованием даты.
"""

import sys
import requests
import json
import pandas as pd
import numpy as np
import scipy
import lifetimes
import uncertainties
import numpy_financial as npf
import io
from datetime import datetime

MODEL_NAME = "deepseek-fin:latest"
MODEL_URL = "http://100.64.243.115:11434/api/generate"
MAX_ATTEMPTS = 3

BASEROW_TOKEN = "5iIBoYZ579mQMRYnJpx12nFKESISiB9w"
BASEROW_URL = "http://localhost:8000"
TABLE_ID = 773

# Список колонок, которые нужно привести к числовому типу
NUMERIC_COLUMNS = ['spent', 'clicks', 'impressions']

def load_and_clean_data():
    """Загружает данные из Baserow, приводит числовые колонки к float и дату к datetime."""
    headers = {"Authorization": f"Token {BASEROW_TOKEN}"}
    rows = []
    page = 1
    while True:
        resp = requests.get(
            f"{BASEROW_URL}/api/database/rows/table/{TABLE_ID}/",
            headers=headers,
            params={"page": page, "size": 200, "user_field_names": "true"}
        )
        resp.raise_for_status()
        data = resp.json()
        rows.extend(data["results"])
        if not data["next"]:
            break
        page += 1
    
    df = pd.DataFrame(rows)
    
    # Преобразование числовых колонок
    for col in NUMERIC_COLUMNS:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace(',', '.', regex=False)
            df[col] = df[col].replace('', '0')
            df[col] = pd.to_numeric(df[col], errors='coerce')
            df[col] = df[col].fillna(0)
    
    # Преобразование даты
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        # Можно оставить как есть, или заполнить NaT, если критично
    
    return df

def generate_prompt(question, data_df):
    sample = data_df.head(3).to_csv(index=False)
    cols = list(data_df.columns)
    prompt = f"""
Ты финансовый аналитик, который пишет Python-код для решения задач.
Вопрос пользователя: {question}

Данные уже загружены в переменную `df` (pandas DataFrame).
Пример данных (первые 3 строки):
{sample}

Все числовые колонки приведены к типу float и не содержат пропусков.
Колонка 'date' преобразована в тип datetime (если присутствует).
Библиотеки, которые можно использовать: pandas, numpy, scipy, lifetimes, uncertainties, numpy_financial.
Код должен работать с существующей переменной `df`.
НЕ пытайся загружать данные из внешних источников, не используй read_csv, read_excel и т.п.
Код должен быть самодостаточным и заканчиваться print() с результатом.
Выведи только код, без пояснений и markdown-форматирования.
"""
    return prompt

def call_model(prompt):
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "temperature": 0.1,
        "options": {"num_predict": 1000}
    }
    try:
        resp = requests.post(MODEL_URL, json=payload, timeout=120)
        resp.raise_for_status()
        code = resp.json()["response"].strip()
        if code.startswith("```python"):
            code = code[9:]
        elif code.startswith("```"):
            code = code[3:]
        if code.endswith("```"):
            code = code[:-3]
        return code.strip()
    except Exception as e:
        print(f"Ошибка вызова модели: {e}")
        return None

def run_code_with_exec(code, data_df):
    globals_dict = {
        "df": data_df,
        "pd": pd,
        "np": np,
        "scipy": scipy,
        "lifetimes": lifetimes,
        "uncertainties": uncertainties,
        "npf": npf
    }
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        exec(code, globals_dict)
        output = sys.stdout.getvalue()
        return True, output
    except Exception as e:
        return False, str(e)
    finally:
        sys.stdout = old_stdout

def main():
    if len(sys.argv) < 2:
        print("Использование: python fin_analyst.py \"вопрос\"")
        sys.exit(1)
    question = sys.argv[1]
    print(f"Вопрос: {question}\n")

    print("📥 Загрузка и очистка данных из таблицы ID 773...")
    try:
        data_df = load_and_clean_data()
        print(f"✅ Загружено {len(data_df)} строк")
        print(f"Колонки: {list(data_df.columns)}")
        print("Статистика по числовым колонкам после очистки:")
        numeric_cols = [c for c in NUMERIC_COLUMNS if c in data_df.columns]
        if numeric_cols:
            print(data_df[numeric_cols].describe())
    except Exception as e:
        print(f"❌ Ошибка загрузки: {e}")
        sys.exit(1)

    prompt = generate_prompt(question, data_df)
    print("📤 Промпт отправлен модели...")

    for attempt in range(1, MAX_ATTEMPTS+1):
        print(f"\n🔄 Попытка {attempt}")
        code = call_model(prompt)
        if not code:
            break
        print("📜 Код:\n", code)
        success, output = run_code_with_exec(code, data_df)
        if success:
            print("✅ Успех!\n📊 Результат:\n", output)
            return
        else:
            print(f"❌ Ошибка: {output}")
            if attempt < MAX_ATTEMPTS:
                prompt += f"\n\nПредыдущий код упал с ошибкой:\n{output}\nИсправь."
    print("❌ Не удалось выполнить после всех попыток.")

if __name__ == "__main__":
    main()
