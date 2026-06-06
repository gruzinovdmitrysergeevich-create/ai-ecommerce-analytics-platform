#!/usr/bin/env python3
"""Аналитика: AI-генерирует pandas-код, выполняет, визуализирует результат."""
import os, sys, io, re, json, base64
import requests
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional

ANALYTICS_DIR = os.path.expanduser("~/my-ai-stack/analytics")
sys.path.insert(0, ANALYTICS_DIR)

BASEROW_URL = "http://localhost:8000"
JWT_EMAIL = os.getenv("BASEROW_EMAIL", "")
JWT_PASS = os.getenv("BASEROW_PASSWORD", "")
_jwt_cache = {"token": None, "expires_at": 0}

MAX_ATTEMPTS = 3

# ============================================================
#  JWT / DATA
# ============================================================
def _get_jwt():
    import time
    now = time.time()
    if _jwt_cache["token"] and now < _jwt_cache["expires_at"]:
        return _jwt_cache["token"]
    try:
        resp = requests.post(f"{BASEROW_URL}/api/user/token-auth/",
            json={"email": JWT_EMAIL, "password": JWT_PASS}, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            token = data.get("access_token") or data.get("access")
            if token:
                _jwt_cache["token"] = token
                _jwt_cache["expires_at"] = now + 3000
                return token
    except Exception:
        pass
    return None

def _load_api_key(env_var):
    key = os.environ.get(env_var)
    if key: return key
    env_file = os.path.expanduser("~/.hermes/.env")
    if os.path.exists(env_file):
        with open(env_file) as f:
            for line in f:
                if line.startswith(f"{env_var}="):
                    return line.strip().split("=",1)[1].strip().strip('"').strip("'")
    return None

def _load_data() -> pd.DataFrame:
    jwt = _get_jwt()
    if not jwt: raise RuntimeError("Не удалось получить JWT-токен Baserow")
    headers = {"Authorization": f"JWT {jwt}"}
    rows = []; page = 1
    while True:
        resp = requests.get(f"{BASEROW_URL}/api/database/rows/table/1463/?user_field_names=true&size=200&page={page}",
            headers=headers, timeout=30)
        if resp.status_code == 401:
            _jwt_cache["token"] = None; _jwt_cache["expires_at"] = 0
            jwt = _get_jwt()
            if not jwt: raise RuntimeError("JWT-токен недействителен")
            headers = {"Authorization": f"JWT {jwt}"}
            resp = requests.get(f"{BASEROW_URL}/api/database/rows/table/1463/?user_field_names=true&size=200&page={page}",
                headers=headers, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        rows.extend(data["results"])
        if not data.get("next"): break
        page += 1
    df = pd.DataFrame(rows)
    skip = {'id','order','Name','Notes','Active','date','Дата','month'}
    for col in df.columns:
        if col in skip: continue
        try:
            df[col] = pd.to_numeric(df[col].astype(str).str.replace(',','.',regex=False), errors='coerce').fillna(0)
        except: pass
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
    return df

def _load_traffic() -> pd.DataFrame:
    """Загрузить рекламные данные (трафик) из Baserow таблицы 1448."""
    jwt = _get_jwt()
    if not jwt: return pd.DataFrame()
    headers = {"Authorization": f"JWT {jwt}"}
    rows = []; page = 1
    while True:
        resp = requests.get(f"{BASEROW_URL}/api/database/rows/table/1448/?user_field_names=true&size=200&page={page}",
            headers=headers, timeout=30)
        if resp.status_code == 401:
            _jwt_cache["token"] = None; _jwt_cache["expires_at"] = 0
            jwt = _get_jwt()
            if not jwt: break
            headers = {"Authorization": f"JWT {jwt}"}
            continue
        resp.raise_for_status()
        data = resp.json()
        rows.extend(data["results"])
        if not data.get("next"): break
        page += 1
    df = pd.DataFrame(rows)
    # Конвертируем числовые поля
    num_fields = ['spent','impressions','clicks']
    for col in num_fields:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
    # Рассчитываем производные метрики
    if 'spent' in df.columns and 'impressions' in df.columns:
        df['CPM'] = ((df['spent'] / df['impressions'].replace(0, np.nan)) * 1000).round(2)
    if 'spent' in df.columns and 'clicks' in df.columns:
        df['CPC'] = (df['spent'] / df['clicks'].replace(0, np.nan)).round(2)
    return df

# ============================================================
#  ИНТЕРАКТИВНЫЕ ГРАФИКИ (Plotly — hover, zoom, данные)
# ============================================================
PLOTLY_CDN = '<script src="https://cdn.plot.ly/plotly-2.32.0.min.js"></script>'

def _df_to_plotly(df, title, chart_type="bar"):
    """Создать интерактивный Plotly-график из DataFrame."""
    import plotly.graph_objects as go
    import plotly.io as pio
    
    cols = df.columns.tolist()
    num_cols = [c for c in cols if df[c].dtype in ('float64','int64','int32')]
    x_col = cols[0]
    x_vals = df[x_col].astype(str).tolist()
    
    fig = go.Figure()
    colors = ['#6B3FA0', '#9B6FC0', '#C4A4E0', '#2D1B4E', '#8B5FBF', '#4A90D9', '#E8744A']
    
    if chart_type == "pie":
        vals = df[num_cols[0]].tolist() if num_cols else df.iloc[:,1].tolist()
        fig.add_trace(go.Pie(labels=x_vals, values=vals, 
            marker_colors=colors[:len(x_vals)],
            textinfo='label+percent', hole=0.3))
    elif chart_type == "line":
        for i, c in enumerate(num_cols[:3]):
            fig.add_trace(go.Scatter(x=x_vals, y=df[c].tolist(), 
                mode='lines+markers', name=c, line=dict(width=2.5, color=colors[i]),
                hovertemplate=f'{c}: %{{y:,.0f}}<extra></extra>'))
    else:  # bar
        for i, c in enumerate(num_cols[:3]):
            fig.add_trace(go.Bar(x=x_vals, y=df[c].tolist(), 
                name=c, marker_color=colors[i],
                hovertemplate=f'{c}: %{{y:,.0f}}<extra></extra>'))
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=14, color='#2D1B4E', family='Inter,sans-serif')),
        plot_bgcolor='#FFFFFF', paper_bgcolor='#FFFFFF',
        margin=dict(l=20, r=20, t=50, b=20),
        legend=dict(font=dict(size=11, color='#2D1B4E')),
        xaxis=dict(tickfont=dict(size=10, color='#7B6B8D')),
        yaxis=dict(tickfont=dict(size=10, color='#7B6B8D'), gridcolor='rgba(107,63,160,0.1)'),
        hovermode='x unified', height=420,
    )
    
    html = pio.to_html(fig, include_plotlyjs=False, full_html=False, 
                       config={'displayModeBar': True, 'displaylogo': False,
                               'modeBarButtonsToRemove': ['lasso2d','select2d']})
    return PLOTLY_CDN + html

def chart_bar(df, title="", x_col=None, y_col=None, color=None):
    return _df_to_plotly(df, title, "bar")

def chart_pie(df, title="", labels_col=None, values_col=None):
    return _df_to_plotly(df, title, "pie")

def chart_line(df, title="", x_col=None, y_col=None):
    return _df_to_plotly(df, title, "line")

# ============================================================
#  API CALLS
# ============================================================
def _extract_code(text):
    text = text.strip()
    m = re.search(r'```(?:python)?\s*\n(.*?)```', text, re.DOTALL)
    if m: return m.group(1).strip()
    lines = text.split('\n')
    if lines[0].startswith('```'): lines = lines[1:]
    if lines and lines[-1].startswith('```'): lines = lines[:-1]
    return '\n'.join(lines).strip()

def _call_ollama(prompt, model="qwq-marketing-v08:latest"):
    """Вызов локальной Ollama. Использует chat API с коротким num_predict."""
    base = "http://100.64.243.115:11434"
    
    # Урезаем промпт для слабой локальной модели — только суть
    short_prompt = prompt.split("Ответь ТОЛЬКО Python-кодом")[0]
    if len(short_prompt) > 1500:
        short_prompt = short_prompt[:1500] + "\nОтветь ТОЛЬКО Python-кодом в ```python```."
    else:
        short_prompt = prompt
    
    try:
        resp = requests.post(f"{base}/api/chat",
            json={"model": model, "messages": [{"role":"user","content":short_prompt}],
                  "stream": False,
                  "options": {"temperature": 0.1, "num_predict": 400}},
            timeout=90)
        if resp.status_code == 200:
            data = resp.json()
            response_text = data.get("message", {}).get("content", "")
            if response_text and len(response_text) > 30:
                code = _extract_code(response_text)
                if code and len(code) > 20:
                    usage = {"prompt_tokens": len(short_prompt)//4, "completion_tokens": len(response_text)//4}
                    return code, usage
    except Exception:
        pass
    
    return None, None

def _call_deepseek(prompt, model="deepseek-v4-pro"):
    """Вызов DeepSeek API."""
    api_key = _load_api_key("DEEPSEEK_API_KEY")
    if not api_key: return None, None
    resp = requests.post("https://api.deepseek.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={"model": model, "messages": [{"role":"user","content":prompt}],
              "temperature":0.1, "max_tokens":2500}, timeout=180)
    resp.raise_for_status()
    data = resp.json()
    code = _extract_code(data["choices"][0]["message"]["content"].strip())
    usage = data.get("usage", {})
    return code, usage

# ============================================================
#  MAIN ANALYTICS
# ============================================================
_CHART_RESULT = ""  # глобально для песочницы

def run_analytics_question(question, model="Hermes"):
    global _CHART_RESULT
    _CHART_RESULT = ""
    
    result = {"code":None,"output":None,"chart_html":"","result_df_data":None,"error":None,"status":"unknown",
              "agent":model,"usage_input":0,"usage_output":0}
    try:
        df = _load_data()
        result["rows_loaded"] = len(df)
    except Exception as e:
        result["error"] = f"Ошибка данных: {e}"; result["status"]="error"; return result

    # Загружаем рекламные данные если запрос про рекламу
    q_lower = question.lower()
    is_ad_query = any(w in q_lower for w in ['cpm','cpc','epc','drr','реклам','трафик','посев','посевах',
                                               'cpv','ctr','конверси','клик','показ','охват','таргет',
                                               'креатив','баннер','аукцион','списани','advert','updsum'])
    
    df_ads = None
    if is_ad_query:
        try:
            df_ads = _load_traffic()
        except Exception:
            pass
    
    # Колонки для промпта
    numeric_cols = [c for c in df.columns if df[c].dtype in ('float64','int64')]
    empty_cols = [c for c in numeric_cols if df[c].sum() == 0]
    data_cols = [c for c in numeric_cols if df[c].sum() > 0]
    
    col_map = {
        'total_quantity': 'продажи (шт)',
        'total_logistics': 'логистика (руб)',
        'total_penalties': 'штрафы (руб)',
        'total_acceptance': 'приёмка (руб)',
        'total_storage': 'хранение (руб)',
    }
    col_desc = ', '.join(f'{k} = {col_map.get(k, k)}' for k in data_cols)
    
    # Авто-определение типа графика по запросу (расширенный набор ключевых слов)
    q_lower = question.lower()
    if any(w in q_lower for w in ['структур','дол','процент','пирог','распредел','состав','разбивк',
                                    'категори','сегмент','часть','удельн','вклад']):
        chart_hint = "chart_pie"
    elif any(w in q_lower for w in ['динамик','тренд','рост','падени','линия','график','изменен',
                                     'помесяч','понедель','квартал','истори','год','месяц']):
        chart_hint = "chart_line"
    else:
        chart_hint = "chart_bar"
    
    # Если есть рекламные данные — добавляем в промпт
    ad_section = ""
    if df_ads is not None and len(df_ads) > 0:
        ad_cols = [c for c in df_ads.columns if c in ('spent','impressions','clicks','CPM','CPC',
                     'community_name','campaign_name','source','date')]
        ad_section = f"""
ДОПОЛНИТЕЛЬНО загружен DataFrame df_ads с рекламными данными ({len(df_ads)} строк):
колонки: {', '.join(ad_cols)}
- df_ads['community_name'] — название площадки/сообщества
- df_ads['campaign_name'] — название кампании
- df_ads['spent'] — потрачено (руб)
- df_ads['impressions'] — показы
- df_ads['clicks'] — клики
- df_ads['CPM'] и df_ads['CPC'] уже рассчитаны
- df_ads['date'] — дата (datetime) или df_ads['Дата_и_время_публикации']
"""

    prompt = f"""Ты — финансовый аналитик GEHLEN LANER. Напиши Python-код для pandas.
Вопрос: {question}
ПЕРЕМЕННАЯ df УЖЕ ЗАГРУЖЕНА. НЕ используй pd.read_csv().
df имеет столбцы: {col_desc}
Пустые (всегда 0): {empty_cols} — НЕ ИСПОЛЬЗУЙ их.
Дата в df['date'] формата datetime.
{ad_section}

ТРЕБОВАНИЯ к коду — СТРОГО:
1. ВСЕ данные (цифры, месяцы, метрики) положи в ИТОГОВЫЙ DataFrame result_df (2+ колонок).
   НЕ печатай построчную разбивку — она будет показана в таблице автоматически.
2. print() используй ТОЛЬКО для 2-4 фраз делового вывода и рекомендации.
   Пример хорошего print(): «Средний ДРР 45%. Самый убыточный месяц — июнь (ДРР 200%).
   Рекомендация: сократить рекламный бюджет на 30% в летние месяцы.»
   Пример ПЛОХОГО print() — НЕ ДЕЛАЙ ТАК: «2025-04: доход 0, логистика 29918...»
   Это данные, они должны быть в result_df и таблице, а не в тексте.
3. Числа в print(): f'{{val:,.0f}}' для рублей, f'{{val:,}}' для штук.
4. НЕ импортируй pandas (pd уже есть).
5. После print() вызови визуализацию. Для этого запроса — {chart_hint}():
   result_chart = {chart_hint}(result_df, title="...")
   (для pie: первый столбец — названия, второй — значения)

Ответь ТОЛЬКО Python-кодом в ```python```."""

    # Маршрутизация: оба агента → DeepSeek API (локальная Ollama не тянет генерацию)
    # TODO: когда стационар будет мощнее — включить _call_ollama()
    model_lower = model.lower()
    use_ollama = any(w in model_lower for w in ['deepseek','fin','локаль','ollama','local'])
    
    for attempt in range(1, MAX_ATTEMPTS+1):
        if use_ollama:
            # Стационар слишком слабый — сразу DeepSeek API
            code, usage = _call_deepseek(prompt, model="deepseek-chat")
            if code:
                result["agent"] = model + " (через DeepSeek API — стационар не тянет)"
        else:
            code, usage = _call_deepseek(prompt, model="deepseek-chat")
        if not code:
            if attempt < MAX_ATTEMPTS:
                prompt += "\n\nОшибка: ответ пустой. Сгенерируй код заново."
                continue
            result["error"] = "Модель не ответила после 3 попыток"; result["status"]="error"; return result
        if usage:
            result["usage_input"] += usage.get("prompt_tokens",0)
            result["usage_output"] += usage.get("completion_tokens",0)
        result["code"] = code
        
        old_stdout = sys.stdout; sys.stdout = io.StringIO()
        sandbox_vars = {"df":df, "pd":pd, "np":np, "__builtins__":__builtins__,
                        "chart_bar": chart_bar, "chart_pie": chart_pie, "chart_line": chart_line,
                        "result_chart": ""}
        if df_ads is not None and len(df_ads) > 0:
            sandbox_vars["df_ads"] = df_ads
        try:
            exec(code, sandbox_vars)
            output = sys.stdout.getvalue()
            
            # График: приоритет — model-generated chart_html, затем авто-выбор
            chart_output = ""
            
            # Сначала ищем все DataFrame'ы в песочнице
            dataframes = [(vn, vv) for vn, vv in sandbox_vars.items() 
                         if isinstance(vv, pd.DataFrame) and not vv.empty and len(vv.columns) >= 2
                         and vn not in ('df','df_ads')]
            priority_names = ['result_df','итоговый','итог','result','summary','agg','группировка']
            
            # 1. Сначала результат из переменной result_chart (модель может вызвать chart_*())
            model_chart = sandbox_vars.get("result_chart", "")
            if isinstance(model_chart, str) and 'Plotly' in model_chart and len(model_chart) > 500:
                chart_output = model_chart
            
            # 2. Если нет готового графика — строим из DataFrame
            chart_func = {"chart_pie": chart_pie, "chart_line": chart_line}.get(chart_hint, chart_bar)
            
            # Ищем лучший DataFrame для графика и таблицы
            best_df = None
            for pname in priority_names:
                for vn, vv in dataframes:
                    if pname in vn.lower():
                        best_df = vv
                        break
                if best_df is not None: break
            # Fallback: последний DataFrame
            if best_df is None and dataframes:
                best_df = dataframes[-1][1]
            
            if not chart_output and best_df is not None:
                try:
                    chart_output = chart_func(best_df, title=question[:80])
                except: pass
            # Последний fallback: df
            if not chart_output and 'df' in sandbox_vars:
                df_orig = sandbox_vars['df']
                try:
                    if len(df_orig.columns) >= 2:
                        chart_output = chart_func(df_orig, title=question[:80])
                        if best_df is None: best_df = df_orig
                except: pass
            
            # Строим таблицу: возвращаем как JSON-совместимый dict для st.dataframe()
            result_df_data = None
            if best_df is not None and not best_df.empty:
                try:
                    df_display = best_df.copy()
                    # Переименовываем колонки на русский
                    rename_map = {c: col_map.get(c, c) for c in df_display.columns if c in col_map}
                    df_display.rename(columns=rename_map, inplace=True)
                    # Оставляем числа как есть (не форматируем — st.dataframe сам покажет)
                    result_df_data = df_display.to_dict(orient='records')
                except:
                    pass
            
            result["output"] = output.strip()
            result["chart_html"] = chart_output if chart_output else ""
            result["result_df_data"] = result_df_data
            result["status"] = "ok"
            return result
        except Exception as e:
            if attempt < MAX_ATTEMPTS:
                prompt += f"\n\nОшибка выполнения: {e}\nИсправь код."
            else:
                result["error"] = f"Ошибка выполнения: {e}"; result["status"]="error"
        finally:
            sys.stdout = old_stdout
    return result

def get_quick_metrics():
    try:
        df = _load_data()
        return {"rows": len(df), "total_qty": int(df['total_quantity'].sum()) if 'total_quantity' in df.columns else 0}
    except: return None
