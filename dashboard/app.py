#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎨 GEHLEN — Единый центр управления
"""

import streamlit as st
import os
import sys
import subprocess

print("[DEBUG] app.py started, sys.path[0]=" + sys.path[0])

from modules.finance_provider import get_finance_summary
print("[DEBUG] finance_provider imported")
import json
import time
import webbrowser
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Автообновление каждые 120 сек (статус-блоки)
st_autorefresh(interval=120000, key="status_refresh")

from modules.status_engine import (
    get_overview_status, get_docker_status, get_ollama_local_status,
    get_ollama_station_status, get_vllm_status, get_tailscale_status,
    get_metabase_status, get_baserow_status, get_qdrant_status,
)
from modules.finance_provider import get_finance_summary
from modules.docker_manager import docker_action
from modules.ollama_manager import ollama_action, vllm_action
from modules.loader_runner import list_loaders, run_loader, get_loader_logs, get_loader_status
import sys as _sys
_analytics_path = os.path.expanduser("~/my-ai-stack/analytics")
if _analytics_path not in _sys.path:
    _sys.path.insert(0, _analytics_path)
# Добавляем src/ для импорта модулей аналитики
_src_path = os.path.join(_analytics_path, "src")
if _src_path not in _sys.path:
    _sys.path.insert(0, _src_path)
try:
    from analyst import run_question as run_analytics_question
except ImportError:
    # Fallback: если analyst.py не найден — используем старый sandbox
    from modules.analytics_sandbox import run_analytics_question
from modules.debug_agent import debug_script_with_model as debug_script
# get_overview_status imported above (line 18-22)
from arch_block import ARCH_BLOCK

# ═══════════════════════════════════════════════════
# УТИЛИТЫ
# ═══════════════════════════════════════════════════
BASEROW_URL = "http://localhost:8000"
BASEROW_TOKEN = "5iIBoYZ579mQMRYnJpx12nFKESISiB9w"
METABASE_URL = "http://localhost:3001"
QDRANT_URL = "http://localhost:6333/dashboard"
WB_PRODUCT_URL = "https://www.wildberries.ru/catalog/239789919/detail.aspx?targetUrl=GP"
ARCHITECTURE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mockups/architecture.html")

LOG_DIR = os.path.expanduser("~/my-ai-stack/ui-dashboard/logs")
os.makedirs(LOG_DIR, exist_ok=True)

def write_log(module: str, message: str, level="INFO"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] [{level}] [{module}] {message}\n"
    log_file = os.path.join(LOG_DIR, f"{datetime.now():%Y-%m-%d}.log")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(line)

def render_comp_row(name, svg, detail, is_ok, status_text):
    cls = "ok" if is_ok else "err"
    dot = "g" if is_ok else "r"
    color = "#4ade80" if is_ok else "#f87171"
    st.markdown(f'''<div class="comp-row {cls}">
        <div class="comp-icon">{svg}</div>
        <div class="comp-info"><div class="comp-name">{name}</div><div class="comp-detail">{detail}</div></div>
        <div class="comp-stat" style="color:{color};"><span class="comp-dot {dot}"></span>{status_text}</div>
    </div>''', unsafe_allow_html=True)

# SVG логотипы
docker_icon = '<svg width="28" height="28" viewBox="0 0 32 32"><path d="M4.3 12.3h3.5v3.5H4.3v-3.5zm3.7 0h3.5v3.5H8v-3.5zm3.7 0h3.5v3.5h-3.5v-3.5zm-3.7-3.8H8v3.5H4.3V8.5zm3.7 0h3.5v3.5H8V8.5zm3.7 0h3.5v3.5h-3.5V8.5zm3.7-3.8h3.5v3.5h-3.5V4.7zm-15 0h3.5v3.5H4.3V4.7z" fill="#0db7ed"/><path d="M25.5 10.5c-1 0-1.9.4-2.5 1-.5-.4-1.3-.6-2.1-.6l-.4.1.1.4c.3.5.4 1.1.1 1.6-.3.5-.8.9-1.3 1h6.6v-1.6c0-1.9-1.3-3.4-2.9-3.6-.1.6-.5 1.1-.9 1.5-.4.4-.7.6-.7.9z" fill="#0db7ed"/><path d="M1 18h28.5c-.3 1.5-1.7 2.5-3.3 2.5H4.3c-1.6 0-3-1-3.3-2.5z" fill="#0db7ed"/><ellipse cx="8" cy="21" rx="2" ry="1.5" fill="#0db7ed"/><ellipse cx="15" cy="21" rx="2" ry="1.5" fill="#0db7ed"/><ellipse cx="22" cy="21" rx="2" ry="1.5" fill="#0db7ed"/></svg>'
ollama_icon = '<svg width="28" height="28" viewBox="0 0 24 24"><ellipse cx="12" cy="8" rx="6" ry="4" fill="#D0C0E8"/><ellipse cx="10" cy="6" rx="1" ry="1.2" fill="#2D1B4E"/><ellipse cx="14" cy="6" rx="1" ry="1.2" fill="#2D1B4E"/><path d="M6 10c0 3 2.7 5 6 5s6-2 6-5" stroke="#D0C0E8" stroke-width="1.5" fill="none"/></svg>'
baserow_icon = '<svg width="28" height="28" viewBox="0 0 24 24"><rect x="2" y="4" width="8" height="6" rx="1.5" fill="#4FC3F7"/><rect x="13" y="4" width="8" height="6" rx="1.5" fill="#1565C0"/><rect x="2" y="13" width="8" height="6" rx="1.5" fill="#0D47A1"/><rect x="13" y="13" width="8" height="6" rx="1.5" fill="#2196F3"/></svg>'
metabase_icon = '<svg width="28" height="28" viewBox="0 0 24 24"><circle cx="5" cy="6" r="2.5" fill="#42A5F5"/><circle cx="15" cy="6" r="2.5" fill="#1565C0"/><circle cx="10" cy="15" r="2.5" fill="#1E88E5"/><circle cx="5" cy="19" r="2" fill="#1565C0"/><circle cx="15" cy="19" r="2" fill="#0D47A1"/></svg>'
qdrant_icon = '<svg width="28" height="28" viewBox="0 0 24 24"><polygon points="12,1 18,5 18,12 12,16 6,12 6,5" fill="none" stroke="#E91E63" stroke-width="2"/><polygon points="12,5 15,7 15,10 12,12 9,10 9,7" fill="#E91E63" opacity="0.6"/></svg>'
vllm_icon = '<svg width="28" height="28" viewBox="0 0 24 24"><polygon points="13,2 4,13 11,13 10,22 20,10 12,10" fill="#FFD54F" stroke="#FFA000" stroke-width="0.5"/></svg>'
tailscale_icon = '<svg width="28" height="28" viewBox="0 0 24 24"><polygon points="12,2 18,5 18,11 12,14 6,11 6,5" fill="none" stroke="#9B8AB8" stroke-width="1.5"/><polygon points="12,14 18,11 18,17 12,20 6,17 6,11" fill="none" stroke="#9B8AB8" stroke-width="1"/></svg>'
loaders_icon = '<svg width="28" height="28" viewBox="0 0 24 24"><path d="M4 4h6l2 3h7a1 1 0 011 1v9a1 1 0 01-1 1H4a1 1 0 01-1-1V5a1 1 0 011-1z" fill="#FFB74D" stroke="#F57C00" stroke-width="0.5"/><path d="M2 8h20v1H2V8z" fill="#FFF3E0"/></svg>'
postgres_icon = '<svg width="28" height="28" viewBox="0 0 24 24"><ellipse cx="12" cy="14" rx="7" ry="5" fill="#336791"/><ellipse cx="9" cy="12" rx="1.2" ry="1.5" fill="white"/><ellipse cx="15" cy="12" rx="1.2" ry="1.5" fill="white"/><circle cx="9" cy="11.5" r="0.5" fill="#336791"/><circle cx="15" cy="11.5" r="0.5" fill="#336791"/></svg>'
woman_svg = '<svg width="28" height="28" viewBox="0 0 28 28" fill="none"><circle cx="14" cy="7" r="4" fill="#6B3FA0"/><path d="M8 13C8 13 10 18 14 18C18 18 20 13 20 13" stroke="#6B3FA0" stroke-width="2" stroke-linecap="round"/><rect x="6" y="20" width="16" height="5" rx="2" fill="#8B5FC0" opacity="0.6"/><path d="M10 25L9 27M18 25L19 27" stroke="#6B3FA0" stroke-width="1.5" stroke-linecap="round"/></svg>'
# Картинка из меню (женщина с тазиком) — та же что в сайдбаре
import re
with open(__file__, 'r', encoding='utf-8') as _f:
    _m = re.search(r'data:image/png;base64,([A-Za-z0-9+/=]+)', _f.read())
sidebar_img = f'<img src="data:image/png;base64,{_m.group(1)}" width="28" height="28" style="border-radius:4px;object-fit:cover;" />' if _m else woman_svg

def render_status_card(title, status_text, is_ok=True, is_warn=False, details=""):
    cls = "ok" if is_ok else ("warn" if is_warn else "err")
    icon = "✅" if is_ok else ("⚠️" if is_warn else "❌")
    st.markdown(f"""
    <div class="status-card {cls}">
        <h4>{icon} {title}</h4>
        <p><strong>{status_text}</strong></p>
        <p style="opacity:0.85; font-size:0.82rem;">{details}</p>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════
# НАСТРОЙКИ СТРАНИЦЫ
# ═══════════════════════════════════════════════════
st.set_page_config(
    page_title="Gehlen Laner",
    page_icon="assets/favicon.png",
    layout="wide",
    initial_sidebar_state="expanded",
)



# ═══════════════════════════════════════════════════
# КАСТОМНЫЕ СТИЛИ
# ═══════════════════════════════════════════════════
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    :root {
        --g-purple-deep: #2D1B4E;
        --g-purple-main: #4A306D;
        --g-purple-light: #6B3FA0;
        --g-purple-bright: #8B5FC0;
        --g-purple-pale: #B8A0D8;
        --g-white: #FFFFFF;
        --g-text-muted: #A890C8;
        --g-hover-bg: rgba(107, 63, 160, 0.25);
        --g-active-bg: rgba(107, 63, 160, 0.45);
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--g-purple-deep) 0%, #1a0f2e 100%) !important;
    }
    [data-testid="stSidebar"] > div:first-child { padding-top: 0 !important; }
    [data-testid="stSidebar"] * { color-scheme: dark !important; }

    [data-testid="stAppViewContainer"] { background: #EDE4F5 !important; }
    [data-testid="stAppViewContainer"] > .main { background: #EDE4F5 !important; }

    [data-testid="stSidebar"] [data-testid="stRadio"] > div[role="radiogroup"] { gap: 0 !important; }
    /* УБИРАЕМ РАДИО-КРУЖКИ */
    [data-testid="stSidebar"] [data-testid="stRadio"] input[type="radio"] { display: none !important; }
    [data-testid="stSidebar"] [data-baseweb="radio"] > div:first-child { display: none !important; visibility: hidden !important; width: 0 !important; height: 0 !important; }
    [data-testid="stSidebar"] [data-testid="stRadio"] label > div:first-of-type { display: none !important; }
    /* Пункты меню */
    [data-testid="stSidebar"] [data-testid="stRadio"] label {
        display: flex !important; align-items: center; padding: 10px 16px !important;
        margin: 2px 10px !important; border-radius: 8px !important; cursor: pointer;
        transition: background 0.15s ease, color 0.15s ease, transform 0.15s ease !important;
        background: transparent !important; color: var(--g-text-muted) !important;
        font-weight: 500 !important; font-size: 0.9rem !important; border: none !important;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
        background: rgba(107,63,160,0.25) !important; color: #FFFFFF !important;
        transform: translateX(3px) !important;
    }
    /* Активный пункт */
    [data-testid="stSidebar"] [data-testid="stRadio"] label[aria-checked="true"],
    [data-testid="stSidebar"] [data-testid="stRadio"] label[data-checked="true"] {
        background: rgba(107,63,160,0.45) !important; color: #FFFFFF !important; font-weight: 600 !important;
    }

    h1 { font-size: 2rem !important; font-weight: 800 !important; color: var(--g-purple-deep) !important; }
    h2 { font-size: 1.4rem !important; font-weight: 700 !important; color: var(--g-purple-deep) !important;
         border-bottom: 3px solid var(--g-purple-light); padding-bottom: 6px; margin-top: 1.5rem !important; }
    h3 { font-size: 1.1rem !important; font-weight: 600 !important; color: var(--g-purple-main) !important; }

    .status-card {
        background: linear-gradient(135deg, var(--g-purple-main) 0%, var(--g-purple-light) 100%);
        border-radius: 14px; padding: 18px; color: white;
        box-shadow: 0 6px 24px rgba(74,48,109,0.25); margin-bottom: 14px;
        border-left: 4px solid var(--g-purple-bright);
    }
    .status-card.ok { background: linear-gradient(135deg, #1a5c3a 0%, #27ae60 100%); box-shadow: 0 6px 24px rgba(39,174,96,0.25); border-left-color: #4ade80; }
    .status-card.warn { background: linear-gradient(135deg, #8B6914 0%, #D4A017 100%); box-shadow: 0 6px 24px rgba(212,160,23,0.25); border-left-color: #fbbf24; }
    .status-card.err { background: linear-gradient(135deg, #6b1c1c 0%, #c0392b 100%); box-shadow: 0 6px 24px rgba(192,57,43,0.25); border-left-color: #f87171; }
    .status-card h4 { margin: 0 0 6px 0; font-size: 1.05rem; font-weight: 700; }
    .status-card p { margin: 0; opacity: 0.95; font-size: 0.9rem; }

    
    
    .metric-value { font-size: 1.8rem; font-weight: 800; color: var(--g-purple-main); }
    .metric-value.neg { color: #c0392b; }
    .metric-value.pos { color: #27ae60; }
    .metric-label { font-size: 0.85rem; color: #64748b; margin-top: 4px; font-weight: 500; }

        .log-box { background:rgba(45,27,78,0.4); border-radius:10px; padding:12px 16px; 
        font-family:'Courier New',monospace; font-size:0.78rem; line-height:1.6; max-height:200px; overflow-y:auto; }
        background: #0f172a; color: #94a3b8; border-radius: 12px; padding: 16px;
        font-family: monospace; font-size: 0.82rem;
        max-height: 360px; overflow-y: auto; white-space: pre-wrap; line-height: 1.6;
        border: 1px solid #1e293b;
    }

    div[data-testid="stButton"] > button {
        border-radius: 10px !important; font-weight: 700 !important;
        transition: all 0.2s ease !important; border: none !important;
    }
    div[data-testid="stButton"] > button:hover {
        transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0,0,0,0.15) !important;
    }
    div[data-testid="stButton"] > button[kind="primary"] {
        background: var(--g-purple-main) !important;
    }

    .sidebar-subtitle {
        color: var(--g-text-muted); text-align: center;
        font-size: 0.78rem; font-weight: 500; margin: 8px 0 20px 0;
        letter-spacing: 1px; text-transform: uppercase;
    }

    .badge { display: inline-block; padding: 2px 10px; border-radius: 12px; font-size: 0.75rem; font-weight: 700; }
    .badge.on { background: #dcfce7; color: #166534; }
    .badge.off { background: #fee2e2; color: #991b1b; }
    .badge.warn { background: #fef3c7; color: #92400e; }

    /* Ссылки в сайдбаре — белые, 0.9rem как меню */
    /* Сервисы — с анимацией */
    [data-testid="stSidebar"] a:not([href*="wildberries"]) {
        color: #FFFFFF !important;
        font-size: 0.9rem !important;
        font-family: "Inter", sans-serif !important;
        font-weight: 500 !important;
        text-decoration: none !important;
        transition: all 0.15s ease !important;
    }
    [data-testid="stSidebar"] a:not([href*="wildberries"]):hover {
        color: #FFFFFF !important;
        text-decoration: none !important;
        background: rgba(107,63,160,0.25) !important;
        border-radius: 8px !important;
        padding-left: 4px !important;
    }
    /* Картинка — без анимации */
    [data-testid="stSidebar"] a[href*="wildberries"] {
        display: block !important;
        text-align: center !important;
    }
    [data-testid="stSidebar"] a[href*="wildberries"]:hover {
        background: transparent !important;
    }



    /* Ховер метрик */
    
    
    
    
    
    
    
    
    
    
    
    .comp-icon { width:34px; text-align:center; flex-shrink:0; display:flex; align-items:center; justify-content:center; }
    .comp-icon svg { width:24px; height:24px; }
    .comp-icon img { width:28px; height:28px; border-radius:5px; object-fit:cover; }
    .comp-info { flex:1; }
    .comp-name { font-weight:700; font-size:0.95rem; color:#2D1B4E; font-family:Inter,sans-serif; }
    .comp-detail, .comp-desc { font-size:0.78rem; color:#7B6B8D; margin-top:-2px; line-height:1.15; font-family:Inter,sans-serif; font-weight:400; }
    .comp-stat { font-size:0.9rem; font-weight:600; white-space:nowrap; font-family:Inter,sans-serif; text-align:right; min-width:100px; }
    .comp-dot { display:inline-block; width:8px; height:8px; border-radius:50%; margin-right:6px; }
    .comp-dot.g { background:#4ade80; box-shadow:0 0 6px #4ade80; }
    .comp-dot.r { background:#f87171; box-shadow:0 0 6px #f87171; }
    
    

    .fin-num { font-size:1.5rem; font-weight:700; color:#7B6B8D; font-family:Inter,sans-serif; }
    .fin-num small { font-size:1.1rem; font-weight:600; color:#7B6B8D; }
    .fin-neg { color:#dc2626 !important; }
    .fin-neg small { color:#dc2626 !important; }
    .fin-label { font-size:0.85rem; color:#7B6B8D; margin-top:4px; font-family:Inter,sans-serif; font-weight:600; }

    .pl-block { position:relative; overflow:hidden; }
    .pl-detail { display:none; }
    .pl-block:hover .pl-main { display:none; }
    .pl-block:hover .pl-detail { display:block; }
    .drr-block:hover .drr-num { transform:scale(1.2) !important; }


    .mp-block { position:relative; overflow:hidden; }
    .mp-detail { display:none; }
    .mp-block:hover .mp-total { display:none; }
    .mp-block:hover .mp-detail { display:block; }


    .metric-box {
        background: rgba(255,255,255,0.12) !important;
        border: 1px solid rgba(200,190,220,0.3) !important;
        border-radius: 12px !important;
        padding: 14px 10px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.12);
        transition: all 0.2s ease;
        font-family: Inter, sans-serif !important;
        text-align: center !important;
    }
    /* Selectbox — корпоративный тёмно-фиолетовый */
    div[data-baseweb="select"] > div {
        background: rgba(45,27,78,0.06) !important;
        border-color: rgba(107,63,160,0.4) !important;
        border-radius: 8px !important;
    }
    div[data-baseweb="select"] span, div[data-baseweb="select"] div[value] {
        color: #2D1B4E !important;
        font-family: Inter, sans-serif !important;
    }
    /* Дропдаун selectbox — popover (НЕ внутри select!) */
    div[data-baseweb="popover"],
    div[data-baseweb="popover"] > div:first-child { background: transparent !important; }
    div[data-baseweb="popover"] ul {
        background: rgba(45,27,78,0.06) !important;
        border: 1px solid rgba(107,63,160,0.4) !important;
    }
    li[role="option"] {
        color: #2D1B4E !important;
        font-family: Inter, sans-serif !important;
    }
    li[role="option"]:hover {
        background: rgba(107,63,160,0.2) !important;
    }
    /* Стрелка selectbox — тёмная */
    div[data-baseweb="select"] svg, div[data-baseweb="select"] path {
        fill: #2D1B4E !important;
    }
    /* Textarea — как панели */
    div[data-testid="stTextArea"] textarea, textarea[aria-label="Запрос"] {
        background: rgba(45,27,78,0.06) !important;
        border: 1px solid rgba(107,63,160,0.4) !important;
        border-radius: 12px !important;
        color: #2D1B4E !important;
        font-family: Inter, sans-serif !important;
        font-size: 0.8rem !important;
        line-height: 1.5 !important;
    }
    div[data-testid="stTextArea"] textarea:focus, textarea[aria-label="Запрос"]:focus {
        border-color: #6B3FA0 !important;
    }
    div[data-testid="stTextArea"] textarea::placeholder, textarea[aria-label="Запрос"]::placeholder {
        color: #9B8AB8 !important;
        text-align: center !important;
        font-size: 0.78rem !important;
    }
    /* Убираем тёмный фон и рамку у внутренних div'ов textarea */
    [data-testid="stTextAreaRootElement"],
    [data-testid="stTextAreaRootElement"] > div {
        background: transparent !important;
        border: none !important;
    }
    /* Календарь — белый шрифт в дропдаунах месяца/года */
    div[data-baseweb="calendar"] div[data-baseweb="menu"] li,
    div[data-baseweb="calendar"] div[data-baseweb="menu"] span {
        color: #FFFFFF !important;
    }
    /* Календарь — фон дропдаунов */
    div[data-baseweb="calendar"] div[data-baseweb="menu"] {
        background: #2D1B4E !important;
    }
    .metric-box:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.22);
    }
        .metric-box[data-status="ok"]:hover {
        background: rgba(74,222,128,0.18) !important;
        border-color: rgba(74,222,128,0.5) !important;
    }
    .metric-box[data-status="err"]:hover {
        background: rgba(248,113,113,0.15) !important;
        border-color: rgba(248,113,113,0.45) !important;
    }

    .fin-block { background:rgba(255,255,255,0.12); border:1px solid rgba(200,190,220,0.3);
        border-radius:12px; padding:14px 10px; flex:1; min-width:100px; text-align:center;
        box-shadow:0 2px 8px rgba(0,0,0,0.12); transition:all 0.2s ease; cursor:pointer; 
        min-height:130px; display:flex; flex-direction:column; justify-content:center; }
    .fin-block:hover { transform:translateY(-3px); box-shadow:0 6px 20px rgba(0,0,0,0.22); }

    .comp-section { background:transparent !important; border:none !important; 
        border-radius:0 !important; padding:0 !important; margin:0 !important; }
    .comp-row { display:flex; align-items:center; gap:12px; padding:0;
        border-bottom:1px solid rgba(107,63,160,0.10); }
    .comp-row:last-child { border-bottom:none; }
    /* Ховер на всю строку компонента */
    [data-testid="stHorizontalBlock"]:has(.comp-name) {
        transition: all 0.25s ease; border-radius: 10px; padding: 4px 16px; margin: -2px -16px; cursor: pointer;
        align-items: center !important; gap: 4px !important;
    }
    [data-testid="stHorizontalBlock"]:has(.comp-name) > [data-testid="stColumn"] {
        display: flex !important; align-items: center !important;
    }
    [data-testid="stHorizontalBlock"]:has(.comp-row[data-status="ok"]):hover {
        background: rgba(107,63,160,0.15) !important; transform: translateY(-2px);
        box-shadow: 0 2px 12px rgba(107,63,160,0.12);
    }
    [data-testid="stHorizontalBlock"]:has(.comp-row[data-status="err"]):hover {
        background: rgba(248,113,113,0.15) !important; transform: translateY(-2px);
        box-shadow: 0 2px 12px rgba(248,113,113,0.12);
    }
    /* Выключенный компонент — тусклее */
    [data-testid="stHorizontalBlock"]:has(.comp-row[data-status="err"]) {
        opacity: 0.55;
    }
    [data-testid="stHorizontalBlock"]:has(.comp-row[data-status="err"]):hover {
        opacity: 1;
    }
    /* Рубильник норм, только текст toggle чуть меньше */
    [data-testid="stWidgetLabel"] { font-size:0.9rem !important; }
    [data-testid="stWidgetLabel"] p { color:#6B3FA0 !important; font-family:Inter,sans-serif !important; font-weight:600 !important; font-size:0.78rem !important; }
    .comp-log-btn { background:rgba(45,27,78,0.85); color:#FFFFFF; border-radius:6px; padding:8px 14px; 
        font-size:0.78rem; font-weight:600; cursor:pointer; text-align:center; font-family:Inter,sans-serif; }
    .comp-log-popup { background:rgba(45,27,78,0.95); border-radius:8px; padding:14px 18px; color:#FFFFFF; 
        font-size:0.82rem; font-family:monospace; line-height:1.6; position:fixed; top:50%; left:50%;
        transform:translate(-50%,-50%); z-index:9999; width:max-content; max-width:600px;
        box-shadow:0 8px 40px rgba(0,0,0,0.6); }
    /* Календарь: анимация при наведении */
    [data-testid="stDateInput"]:hover { transform: translateY(-2px) !important; transition: all 0.2s ease !important; }
    [data-testid="stDateInput"] input { transition: all 0.2s ease !important; }
    [data-testid="stDateInput"]:hover input { border-color: rgba(45,27,78,0.65) !important; }

        [data-testid="stDateInput"] {
        border: none !important;
        box-shadow: none !important;
        outline: none !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    [data-testid="stDateInput"] > div {
        border: none !important;
        box-shadow: none !important;
        outline: none !important;
        background: transparent !important;
    }
    [data-testid="stDateInput"] > div > div {
        border: none !important;
        box-shadow: none !important;
        outline: none !important;
        background: transparent !important;
    }
    [data-testid="stDateInput"] input {
        background: rgba(255,255,255,0.10) !important;
        border: 1.5px solid rgba(45,27,78,0.45) !important;
        border-radius: 8px !important;
        color: #2D1B4E !important;
        font-family: Inter,sans-serif !important;
        font-size: 0.78rem !important;
        font-weight: 600 !important;
        padding: 5px 8px !important;
        text-align: center !important;
        box-shadow: none !important;
        outline: none !important;
        -webkit-appearance: none !important;
        appearance: none !important;
        width: 115px !important;
        caret-color: transparent !important;
        border-left-width: 1.5px !important;
        border-right-width: 1.5px !important;
        border-top-width: 1.5px !important;
        border-bottom-width: 1.5px !important;
        border-left-style: solid !important;
        border-right-style: solid !important;
        border-top-style: solid !important;
        border-bottom-style: solid !important;
        border-left-color: rgba(45,27,78,0.45) !important;
        border-right-color: rgba(45,27,78,0.45) !important;
        border-top-color: rgba(45,27,78,0.45) !important;
        border-bottom-color: rgba(45,27,78,0.45) !important;
    }
    [data-testid="stDateInput"] input:focus {
        border-color: rgba(45,27,78,0.55) !important;
        box-shadow: none !important;
        outline: none !important;
    }

    .wb-block { border-color: transparent !important; }
    .wb-block:hover { border-color: rgba(203,17,171,0.5) !important; }
    .oz-block { border-color: transparent !important; }
    .oz-block:hover { border-color: rgba(0,91,255,0.5) !important; }
    /* Календарь: белый шрифт в дропдаунах месяца/года, непрозрачный фон */
    /* react-datepicker dropdown month/year */
    .react-datepicker__month-select, .react-datepicker__year-select { background: #2D1B4E !important; color: #FFFFFF !important; border: 1px solid rgba(255,255,255,0.2) !important; }
    .react-datepicker__month-select option, .react-datepicker__year-select option { background: #2D1B4E !important; color: #FFFFFF !important; }
    /* Streamlit month/year dropdown listbox items */
    [role="application"] [role="listbox"] li[role="option"] { background: #2D1B4E !important; color: #FFFFFF !important; }
    [role="application"] [role="listbox"] li[role="option"][aria-selected="true"] { background: #6B3FA0 !important; color: #FFFFFF !important; }
    [role="application"] [role="listbox"] { background: #2D1B4E !important; border: 1px solid rgba(107,63,160,0.4) !important; }
    /* Calendar dropdown — глобальные селекторы для popover (портал) */
    ul[role="listbox"] { background: #2D1B4E !important; border: 1px solid rgba(107,63,160,0.5) !important; }
    ul[role="listbox"] li[role="option"] { background: #2D1B4E !important; color: #FFFFFF !important; font-family: Inter, sans-serif !important; }
    ul[role="listbox"] li[role="option"]:hover { background: #4A306D !important; }
    ul[role="listbox"] li[role="option"][aria-selected="true"] { background: #6B3FA0 !important; color: #FFFFFF !important; }
    /* BaseWeb menu (календарь месяц/год) */
    [data-baseweb="menu"] { background: #2D1B4E !important; }
    [data-baseweb="menu"] li { background: #2D1B4E !important; color: #FFFFFF !important; }
    [data-baseweb="menu"] li:hover { background: #4A306D !important; }
    [data-baseweb="menu"] [aria-selected="true"] { background: #6B3FA0 !important; }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════
# БОКОВАЯ ПАНЕЛЬ
# ═══════════════════════════════════════════════════
with st.sidebar:
    st.markdown('''
    <div style="text-align:center; margin:20px 0 0;">
        <svg width="180" height="46" viewBox="0 0 180 46" xmlns="http://www.w3.org/2000/svg">
            <text x="90" y="36" text-anchor="middle" font-family="Inter,sans-serif" font-weight="800" 
                  font-size="36" fill="#FFFFFF" letter-spacing="0">Gehlen</text>
        </svg>
    </div>
    <div class="sidebar-subtitle" style="letter-spacing:2px;">Единый центр управления</div>
    ''', unsafe_allow_html=True)
    st.markdown("<hr style='margin: 10px 16px; border-color: rgba(107,63,160,0.4);'>", unsafe_allow_html=True)

    page = st.radio(
        "",
        [
            "Обзор системы",
            "Аналитика",
            "Архитектура",
            "⚙ Дебаг",
        ],
        label_visibility="collapsed",
    )

    st.markdown('<div style="height:40px;"></div>', unsafe_allow_html=True)
    st.markdown("<hr style='margin: 12px 16px; border-color: rgba(107,63,160,0.4);'>", unsafe_allow_html=True)
    st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
    st.markdown("<p style='color: var(--g-text-muted); font-size: 0.78rem; margin: 0 16px 8px; font-weight: 600; text-align:center; text-transform:uppercase; letter-spacing:1px;'>СЕРВИСЫ</p>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="display:flex;flex-direction:column;gap:6px;padding:0 12px;">
        <a href="{BASEROW_URL}/?start_register=0" target="_blank" style="text-decoration:none;">
            <div style="padding:8px 12px;color:#FFFFFF!important;font-weight:500;font-size:0.9rem;display:flex;align-items:center;gap:8px;border-radius:8px;transition:all 0.15s;" onmouseover="this.style.background='rgba(107,63,160,0.25)';this.style.color='#FFFFFF';this.style.transform='translateX(3px)'" onmouseout="this.style.background='transparent';this.style.color='rgba(255,255,255,0.75)';this.style.transform='translateX(0)'">
                <svg width="16" height="16" viewBox="0 0 16 16"><rect x="0" y="1" width="16" height="4" rx="1" fill="#4FC3F7"/><rect x="0" y="6" width="16" height="4" rx="1" fill="#1565C0"/><rect x="0" y="11" width="16" height="4" rx="1" fill="#0D47A1"/></svg>
                Baserow
            </div>
        </a>
        <a href="{METABASE_URL}" target="_blank" style="text-decoration:none;">
            <div style="padding:8px 12px;color:#FFFFFF!important;font-weight:500;font-size:0.9rem;display:flex;align-items:center;gap:8px;border-radius:8px;transition:all 0.15s;" onmouseover="this.style.background='rgba(107,63,160,0.25)';this.style.color='#FFFFFF';this.style.transform='translateX(3px)'" onmouseout="this.style.background='transparent';this.style.color='rgba(255,255,255,0.75)';this.style.transform='translateX(0)'">
                <svg width="16" height="16" viewBox="0 0 16 16"><circle cx="4" cy="3" r="2" fill="#42A5F5"/><circle cx="12" cy="3" r="2" fill="#1565C0"/><circle cx="8" cy="8" r="2" fill="#1E88E5"/><circle cx="4" cy="13" r="2" fill="#1565C0"/><circle cx="12" cy="13" r="2" fill="#0D47A1"/></svg>
                Metabase
            </div>
        </a>
        <a href="{QDRANT_URL}" target="_blank" style="text-decoration:none;">
            <div style="padding:8px 12px;color:#FFFFFF!important;font-weight:500;font-size:0.9rem;display:flex;align-items:center;gap:8px;border-radius:8px;transition:all 0.15s;" onmouseover="this.style.background='rgba(107,63,160,0.25)';this.style.color='#FFFFFF';this.style.transform='translateX(3px)'" onmouseout="this.style.background='transparent';this.style.color='rgba(255,255,255,0.75)';this.style.transform='translateX(0)'">
                <svg width="16" height="16" viewBox="0 0 16 16"><polygon points="8,0 14,3.5 14,10.5 8,14 2,10.5 2,3.5" fill="#E91E63" stroke="#C2185B" stroke-width="0.5"/></svg>
                Qdrant
            </div>
        </a>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
    st.markdown("<hr style='margin: 12px 16px; border-color: rgba(107,63,160,0.4);'>", unsafe_allow_html=True)
    st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
    total_in = st.session_state.get("total_tokens_in", 0)
    total_out = st.session_state.get("total_tokens_out", 0)
    pct = min(100, int((total_in + total_out) / 128000 * 100)) if (total_in + total_out) > 0 else 0
    st.markdown(f"""
    <div style="padding:8px 16px;">
        <div style="text-align:center;font-family:Inter,sans-serif;font-size:0.75rem;color:#9B8AB8;margin-bottom:5px;text-transform:uppercase;letter-spacing:1px;">context</div>
        <div style="display:flex;justify-content:space-between;font-family:Inter,sans-serif;font-size:0.7rem;color:#9B8AB8;margin-bottom:4px;">
            <span>Вход: {total_in:,}</span><span>Выход: {total_out:,}</span>
        </div>
        <div style="background:rgba(255,255,255,0.15);border-radius:4px;height:4px;overflow:hidden;">
            <div style="background:rgba(255,140,0,0.8);height:4px;width:{pct}%;border-radius:4px;transition:width 0.5s;"></div>
        </div>
        <div style="text-align:center;font-family:Inter,sans-serif;font-size:0.72rem;color:#9B8AB8;margin-top:4px;">DeepSeek v4 Pro</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
    st.markdown("<hr style='margin: 12px 16px; border-color: rgba(107,63,160,0.4);'>", unsafe_allow_html=True)
    st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
    st.markdown(f"""<div style="text-align:center;padding:0 16px 24px;">
        <a href="{WB_PRODUCT_URL}" target="_blank">
            <img src="data:image/png;base64,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" style="width:66px;height:66px;border-radius:6px;object-fit:cover;display:block;margin:0 auto;opacity:0.95;" onmouseover="this.style.opacity='1'" onmouseout="this.style.opacity='0.95'">
        </a>
    </div>""", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#7B6B8D;font-size:0.7rem;margin:2px 0 24px;'>Gehlen Laner v1.0</p>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════
# СТРАНИЦА: ОБЗОР
# ═══════════════════════════════════════════════════

# ═══════════════════════════════════════════════════
# СХЕМА АРХИТЕКТУРЫ
# ═══════════════════════════════════════════════════
if page == "Архитектура":
    s = get_overview_status()
    dg, dr = "#4ade80", "#f87171"
    D = lambda ok: dg if ok else dr
    T = lambda ok: "Работает" if ok else "Остановлен"

    st.markdown('''<style>
    [data-testid="stAppViewContainer"]:has(.a2) { background: #1a0f2e !important; }
    .a2 { max-width:1100px; margin:0 auto; padding:30px 20px; font-family:Inter,sans-serif; }
    .a2 h1 { text-align:center; font-size:1.6rem; font-weight:700; color:#FFFFFF !important; margin-bottom:6px; }
    .a2 .sub { text-align:center; font-size:0.78rem; color:#7B6B8D; margin-bottom:36px; }
    .a2 .r { display:flex; gap:14px; justify-content:center; margin-bottom:12px; flex-wrap:wrap; }
    .a2 .b { background:rgba(107,63,160,0.2); border:1px solid rgba(107,63,160,0.35); border-radius:12px; padding:16px 20px; min-width:140px; text-align:center; }
    .a2 .bn { font-weight:600; font-size:0.9rem; color:#D0C0E8; margin-bottom:4px; }
    .a2 .bd { font-size:0.72rem; color:#9B8AB8; }
    .a2 .bs { margin-top:10px; font-size:0.78rem; color:#C0B0D8; }
    .a2 .dot { width:10px; height:10px; border-radius:50%; display:inline-block; margin-right:6px; }
    .a2 .ar { text-align:center; color:#6B3FA0; font-size:2rem; margin:0; line-height:1; }
    .a2 .sec { text-align:center; font-size:0.75rem; font-weight:600; color:#6B3FA0; margin-bottom:10px; letter-spacing:2px; text-transform:uppercase; }
    .a2 .ln { border:none; border-top:1px solid rgba(107,63,160,0.3); margin:20px 0 16px; }
    .a2 .ic { font-size:1.1rem; }

</style>''', unsafe_allow_html=True)

    bs = s.get("baserow_ready", False)
    mb = s.get("metabase_ready", False)
    qd = s.get("qdrant_ready", False)
    dk = s.get("docker_running", False)
    ol = s.get("ollama_local", False)
    vl = s.get("vllm_running", False)
    ts = s.get("tailscale_ok", False)
    cnt = s.get("containers_running", 0)
    stinfo = s.get("ollama_station", {})
    st_ok = stinfo.get("running", False) if isinstance(stinfo, dict) else False
    tip = s.get("tailscale_ip", "N/A")
    lc = s.get("loader_count", 0)

    h = '<div class="a2">'
    h += '<h1 style="color:#FFFFFF;">Gehlen Laner ' + chr(8212) + ' Архитектура системы</h1>'
    h += '<p class="sub">Обновляется в реальном времени · <span style="color:#4ade80;">Зелёный</span> — работает · <span style="color:#f87171;">Красный</span> — остановлен</p>'

    h += '<div class="sec">Источники данных</div><div class="r">'
    for name, desc in [("Wildberries API", "Продажи · Реализация · Реклама"),
                        ("Ozon API", "Postings · Ads · Finance"),
                        ("Банк / Excel", "Выписки · Управлёнка · Трафик")]:
        h += f'<div class="b"><div class="bn">{name}</div><div class="bd">{desc}</div><div class="bs"><span class="dot" style="background:{D(bs)};box-shadow:0 0 8px {D(bs)}"></span>{"Активен" if bs else "Остановлен"}</div></div>'
    h += '</div><div class="ar">⬇</div>'

    h += '<div class="sec">Загрузчики</div><div class="r">'
    for name, desc in [("Universal API Loader", f"WB + Ozon → Baserow"),
                        ("Finance Loader", "14 источников → Baserow"),
                        ("Агрегатор", "Сырые → 3 агрегата")]:
        h += f'<div class="b"><div class="bn">{name}</div><div class="bd">{desc}</div><div class="bs"><span class="dot" style="background:{dg};box-shadow:0 0 8px {dg}"></span>{lc if "Universal" in name else "Готов"}</div></div>'
    h += '</div><div class="ar">⬇</div>'

    h += '<div class="sec">Хранилище & Аналитика</div><div class="r">'
    for name, desc, ok in [("Baserow", ":8000 — 15+ таблиц", bs),
                            ("Metabase", ":3001 — Визуализация", mb),
                            ("Qdrant", ":6333 — Векторная БД", qd),
                            ("Analyst v5", "MetricEngine + DeepSeek", True)]:
        h += f'<div class="b"><div class="bn">{name}</div><div class="bd">{desc}</div><div class="bs"><span class="dot" style="background:{D(ok)};box-shadow:0 0 8px {D(ok)}"></span>{"Доступен" if ok else "Остановлен"}</div></div>'
    h += '</div><hr class="ln">'

    h += '<div class="sec">AI Инфраструктура</div><div class="r">'
    items = [
        (f'<span class="ic">🐳</span> Docker', f'{cnt} контейнеров', dk),
        (f'<span class="ic">🦙</span> Ollama Station', 'Стационар · RTX 3090', st_ok),
        (f'<span class="ic">⬡</span> Tailscale', f'{tip}', ts),
    ]
    for name, desc, ok in items:
        stxt = "Работает" if (ok is True) else ("Доступен" if name.endswith("Station>") or "Tailscale" in name else ("Подключён" if "Tailscale" in name else "Остановлен"))
        if ok is False: stxt = "Остановлен"
        if ok is True: stxt = "Работает" if "Docker" in name or "Ollama" in name else ("Подключён" if "Tailscale" in name else "Доступен")
        h += f'<div class="b"><div class="bn">{name}</div><div class="bd">{desc}</div><div class="bs"><span class="dot" style="background:{D(ok)};box-shadow:0 0 8px {D(ok)}"></span>{T(ok)}</div></div>'
    h += '</div></div>'

    st.markdown(h, unsafe_allow_html=True)

if page == "Обзор системы":
    status = get_overview_status()
    cols = st.columns(4)
    cnt = min(status.get("containers_running", 0), 3)
    metrics = [
        ("Docker", "🐳", status.get("docker_running", False), 
         f"Работает · {cnt}/3" if status.get("docker_running") else "Остановлен"),
        ("Ollama", "🦙", status.get("ollama_station", {}).get("running", False), 
         "Работает" if status.get("ollama_station", {}).get("running") else "Остановлен"),
        ("PostgreSQL", "🐘", status.get("db_ready", False), 
         "Работает" if status.get("db_ready") else "Остановлен"),
        ("Tailscale", "⬡", status.get("tailscale_ok", False), 
         "Подключён" if status.get("tailscale_ok") else "Отключён"),
    ]
    for i, (label, icon, ok, text) in enumerate(metrics):
        with cols[i]:
            color = "#4ade80" if ok else "#f87171"
            st.markdown(f"""
            <div class="metric-box" data-status="{'ok' if ok else 'err'}">
                <div class="metric-value" style="color:#2D1B4E;font-size:1.1rem;font-weight:700;font-family:Inter,sans-serif;">{icon} {label}</div>
                <div class="metric-label" style="color:{color};font-family:Inter,sans-serif;font-weight:600;font-size:0.85rem;">{text}</div>
            </div>
            """, unsafe_allow_html=True)

    # Заголовок + датапикер в одну строку
    st.markdown("<div style='height:24px;'></div>", unsafe_allow_html=True)
    hc1, hc2 = st.columns([5, 1])
    with hc1:
        st.markdown("<span class='fin-title' style='display:inline-flex;align-items:center;font-family:Inter,sans-serif;font-weight:800;font-size:1.1rem;padding:2px 0 6px;white-space:nowrap;'><span style='color:#2D1B4E;font-weight:800;font-size:1.15rem;margin-right:6px;'>$</span><span style='color:#2D1B4E;font-weight:800;'>Финансовая сводка</span></span>", unsafe_allow_html=True)
    with hc2:
        # Авто-определение последней даты с данными (кэш 5 мин в session_state)
        if "last_data_date" not in st.session_state:
            st.session_state.last_data_date = None
        default_date = st.session_state.get("last_data_date") or datetime.now().date()
        selected_date = st.date_input("", value=default_date, label_visibility="collapsed")
    
    date_str = selected_date.strftime("%Y-%m-%d")
    if "finance_cache" not in st.session_state:
        st.session_state.finance_cache = {}
    if date_str not in st.session_state.finance_cache:
        with st.spinner("Загружаю финансы..."):
            st.session_state.finance_cache[date_str] = get_finance_summary(date_str)
            # Авто-сохраняем последнюю успешную дату
            fin_check = st.session_state.finance_cache[date_str]
            if (fin_check.get("wb_sold", 0) > 0 or fin_check.get("ozon_sold", 0) > 0) and not fin_check.get("error"):
                st.session_state.last_data_date = selected_date
    fin = st.session_state.finance_cache[date_str]
    if fin.get("error"):
        st.caption(f"⚠ {fin['error']}")
    wb_sold, wb_mono, wb_double, wb_triple = fin.get("wb_sold",0), fin.get("wb_mono",0), fin.get("wb_double",0), fin.get("wb_triple",0)
    ozon_sold = fin.get("ozon_sold", 0)
    income, expense = fin.get("income",0), fin.get("expense",0)
    profit, drr = fin.get("profit",0), fin.get("drr",0)
    wb_rev_est = fin.get("wb_revenue_estimated", False)  # оценка по средним ценам
    if fin.get("error"):
        st.error(f"Ошибка загрузки финансовых данных: {fin['error']}")
    # Предупреждение если данных нет
    no_data = (wb_sold == 0 and ozon_sold == 0)
    if no_data and date_str == datetime.now().strftime("%Y-%m-%d"):
        st.info("💡 Нет данных за сегодня. Выберите дату с данными в календаре (например, 2025-04-22). Последняя дата с данными будет запомнена автоматически.")
    elif no_data:
        st.warning(f"⚠️ Нет данных за {date_str}. Попробуйте другую дату.")
    
    fm1, fm2 = st.columns(2)
    with fm1:
        st.markdown(f'''<div class="fin-block mp-block wb-block">
            <div style="display:flex;align-items:center;justify-content:center;gap:8px;margin-bottom:10px;">
                <svg width="26" height="26" viewBox="0 0 24 24"><rect x="2" y="2" width="20" height="20" rx="4" fill="#CB11AB"/><text x="12" y="16" text-anchor="middle" font-size="11" font-weight="800" fill="white">WB</text></svg>
                <span style="font-size:1.05rem;color:#CB11AB;font-weight:700;">Wildberries</span>
            </div>
            <div class="mp-total"><div class="fin-num">{wb_sold}<small> шт.</small></div></div>
            <div class="mp-detail">
                <div style="display:flex;gap:6px;justify-content:center;flex-wrap:wrap;">
                    <span style="background:rgba(203,17,171,0.5);padding:4px 10px;border-radius:6px;font-size:0.9rem;color:#FFB3E5;font-weight:700;">Моно: {wb_mono}</span>
                    <span style="background:rgba(203,17,171,0.5);padding:4px 10px;border-radius:6px;font-size:0.9rem;color:#FFB3E5;font-weight:700;">Дубли: {wb_double}</span>
                    <span style="background:rgba(203,17,171,0.5);padding:4px 10px;border-radius:6px;font-size:0.9rem;color:#FFB3E5;font-weight:700;">Тройки: {wb_triple}</span>
                </div>
            </div>
            <div class="fin-label">Продано</div>
        </div>''', unsafe_allow_html=True)
    with fm2:
        ozon_mono, ozon_double, ozon_triple = fin.get("ozon_mono",0), fin.get("ozon_double",0), fin.get("ozon_triple",0)
        st.markdown(f'''<div class="fin-block mp-block oz-block">
            <div style="display:flex;align-items:center;justify-content:center;gap:8px;margin-bottom:10px;">
                <svg width="26" height="26" viewBox="0 0 24 24"><rect x="2" y="2" width="20" height="20" rx="4" fill="#005BFF"/><text x="12" y="16" text-anchor="middle" font-size="8" font-weight="800" fill="white">OZON</text></svg>
                <span style="font-size:1.05rem;color:#005BFF;font-weight:700;">Ozon</span>
            </div>
            <div class="mp-total"><div class="fin-num">{ozon_sold}<small> шт.</small></div></div>
            <div class="mp-detail">
                <div style="display:flex;gap:6px;justify-content:center;flex-wrap:wrap;">
                    <span style="background:rgba(0,91,255,0.45);padding:4px 10px;border-radius:6px;font-size:0.9rem;color:#B3D4FF;font-weight:700;">Моно: {ozon_mono}</span>
                    <span style="background:rgba(0,91,255,0.45);padding:4px 10px;border-radius:6px;font-size:0.9rem;color:#B3D4FF;font-weight:700;">Дубли: {ozon_double}</span>
                    <span style="background:rgba(0,91,255,0.45);padding:4px 10px;border-radius:6px;font-size:0.9rem;color:#B3D4FF;font-weight:700;">Тройки: {ozon_triple}</span>
                </div>
            </div>
            <div class="fin-label">Продано</div>
        </div>''', unsafe_allow_html=True)

    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
    fp1, fp2 = st.columns(2)
    with fp1:
        profit_class = "fin-neg" if profit < 0 else ""
        profit_fmt = f"{int(profit):,}".replace(",", " ")
        income_prefix = "≈" if wb_rev_est else ""
        income_fmt = f"{income_prefix}{int(income):,}".replace(",", " ")
        expense_fmt = f"{int(expense):,}".replace(",", " ")
        income_note = '<div style="font-size:0.6rem;color:#9B8AB8;margin-top:-2px;">WB: оценка по ср. ценам</div>' if wb_rev_est else ""
        st.markdown(f'''<div class="fin-block pl-block">
            <div class="pl-main"><div class="fin-num {profit_class}">{profit_fmt}<small> ₽</small></div><div class="fin-label">Прибыль / Убыток</div></div>
            <div class="pl-detail">
                <div style="display:flex;justify-content:center;gap:16px;">
                    <div style="text-align:center;"><span style="color:#22c55e;font-weight:700;font-size:1.2rem;">{income_fmt}<small> ₽</small></span><br><span style="font-size:0.75rem;color:#7B6B8D;font-weight:600;">Доход</span>{income_note}</div>
                    <div style="text-align:center;"><span style="color:#ef4444;font-weight:700;font-size:1.2rem;">{expense_fmt}<small> ₽</small></span><br><span style="font-size:0.75rem;color:#7B6B8D;font-weight:600;">Расход</span></div>
                </div>
            </div>
        </div>''', unsafe_allow_html=True)
    with fp2:
        if drr == -1:
            drr_display = "∞"
        elif drr > 0:
            drr_display = f"{drr}%"
        elif wb_sold == 0 and ozon_sold == 0:
            drr_display = "—"
        else:
            drr_display = "0%"
        st.markdown(f'''<div class="fin-block drr-block" >
            <div class="fin-num drr-num" style="color:#2D1B4E;transition:transform 0.3s ease;">{drr_display}</div>
            <div class="fin-label">ДРР</div>
        </div>''', unsafe_allow_html=True)

    st.markdown("<p style='font-family:Inter,sans-serif;font-weight:700;font-size:1.1rem;color:#2D1B4E;margin:24px 0 0 0;'>Components</p>", unsafe_allow_html=True)
    st.markdown('<div class="comp-section" style="border-top:none !important;margin-top:4px !important;">', unsafe_allow_html=True)

    # Хелпер: рабочий toggle (session_state + инициализация из реального статуса)
    def _toggle_init(key, real_ok):
        if key not in st.session_state:
            st.session_state[key] = real_ok
            st.session_state[f"prev_{key}"] = real_ok
            write_log("TOGGLE", f"INIT {key} = {real_ok}")
        else:
            write_log("TOGGLE", f"INIT {key} already exists = {st.session_state[key]}")
        return st.session_state[key]
    def _toggle_changed(key, cname):
        curr = st.session_state.get(key, False)
        prev = st.session_state.get(f"prev_{key}", curr)
        write_log("TOGGLE", f"CHANGED {key}: curr={curr}, prev={prev}")
        if curr != prev:
            st.session_state[f"prev_{key}"] = curr
            write_log("TOGGLE", f"ACTION {key} → {cname} {'start' if curr else 'stop'}")
            if cname == "ollama_station":
                ollama_action("station", "start" if curr else "stop")
            elif cname in ("api_loader", "fin_loader", "aggregator"):
                if curr:
                    run_loader(cname)
            elif cname:
                docker_action("start" if curr else "stop", cname)
            st.rerun()

    # ─── Baserow ───
    baserow_ok = _toggle_init("toggle_baserow", status.get("baserow_ready", False))
    st.markdown(f'<div class="comp-wrapper {"ok" if baserow_ok else "err"}">', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns([17, 0.9, 0.7, 0.8])
    with c1:
        st.markdown('<div class="comp-row" data-status="' + ('ok' if baserow_ok else 'err') + '"><div class="comp-icon">' + baserow_icon + '</div><div class="comp-info"><div class="comp-name">Baserow</div><div class="comp-desc">База данных · Порт 8000</div></div></div>', unsafe_allow_html=True)
    with c2:
        st.toggle("", key=r"toggle_baserow", label_visibility="collapsed")
        _toggle_changed("toggle_baserow", "baserow")
    with c3:
        if st.button("↻", key="restart_baserow", help="Перезапустить"):
            docker_action("restart", "baserow")
    with c4:
        if st.button("log", key="log_baserow_btn"):
            st.session_state["log_baserow"] = not st.session_state.get("log_baserow", False)
        if st.session_state.get("log_baserow", False):
            st.markdown('<div class="comp-log-popup">🕐 ' + datetime.now().strftime("%H:%M") + ' · Статус: ' + ("Работает" if baserow_ok else "Остановлен") + ' · Порт 8000</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ─── Metabase ───
    metabase_ok = _toggle_init("toggle_metabase", status.get("metabase_ready", False))
    st.markdown(f'<div class="comp-wrapper {"ok" if metabase_ok else "err"}">', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns([17, 0.9, 0.7, 0.8])
    with c1:
        st.markdown('<div class="comp-row" data-status="' + ('ok' if metabase_ok else 'err') + '"><div class="comp-icon">' + metabase_icon + '</div><div class="comp-info"><div class="comp-name">Metabase</div><div class="comp-desc">Визуализация · Порт 3001</div></div></div>', unsafe_allow_html=True)
    with c2:
        st.toggle("", key=r"toggle_metabase", label_visibility="collapsed")
        _toggle_changed("toggle_metabase", "metabase")
    with c3:
        if st.button("↻", key="restart_metabase", help="Перезапустить"):
            docker_action("restart", "metabase")
    with c4:
        if st.button("log", key="log_metabase_btn"):
            st.session_state["log_metabase"] = not st.session_state.get("log_metabase", False)
        if st.session_state.get("log_metabase", False):
            st.markdown('<div class="comp-log-popup">🕐 ' + datetime.now().strftime("%H:%M") + ' · Статус: ' + ("Работает" if metabase_ok else "Остановлен") + ' · Порт 3001</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ─── Qdrant ───
    qdrant_ok = _toggle_init("toggle_qdrant", status.get("qdrant_ready", False))
    st.markdown(f'<div class="comp-wrapper {"ok" if qdrant_ok else "err"}">', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns([17, 0.9, 0.7, 0.8])
    with c1:
        st.markdown('<div class="comp-row" data-status="' + ('ok' if qdrant_ok else 'err') + '"><div class="comp-icon">' + qdrant_icon + '</div><div class="comp-info"><div class="comp-name">Qdrant</div><div class="comp-desc">Векторная БД · Порт 6333</div></div></div>', unsafe_allow_html=True)
    with c2:
        st.toggle("", key=r"toggle_qdrant", label_visibility="collapsed")
        _toggle_changed("toggle_qdrant", "qdrant")
    with c3:
        if st.button("↻", key="restart_qdrant", help="Перезапустить"):
            docker_action("restart", "qdrant")
    with c4:
        if st.button("log", key="log_qdrant_btn"):
            st.session_state["log_qdrant"] = not st.session_state.get("log_qdrant", False)
        if st.session_state.get("log_qdrant", False):
            st.markdown('<div class="comp-log-popup">🕐 ' + datetime.now().strftime("%H:%M") + ' · Статус: ' + ("Работает" if qdrant_ok else "Остановлен") + ' · Порт 6333</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ─── Ollama (стационар) ───
    station = status.get("ollama_station", {})
    ollama_ok = _toggle_init("toggle_ollama_st", station.get("running", False))
    st.markdown(f'<div class="comp-wrapper {"ok" if ollama_ok else "err"}">', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns([17, 0.9, 0.7, 0.8])
    with c1:
        st.markdown('<div class="comp-row" data-status="' + ('ok' if ollama_ok else 'err') + '"><div class="comp-icon">🦙</div><div class="comp-info"><div class="comp-name">Ollama (стационар)</div><div class="comp-desc">Tailscale: ' + status.get('tailscale_ip', 'N/A') + '</div></div></div>', unsafe_allow_html=True)
    with c2:
        st.toggle("", key=r"toggle_ollama_st", label_visibility="collapsed")
        _toggle_changed("toggle_ollama_st", "ollama_station")
    with c3:
        if st.button("↻", key="restart_ollama_st", help="Перезапустить"):
            ollama_action("station", "restart")
    with c4:
        if st.button("log", key="log_ollama_btn"):
            st.session_state["log_ollama"] = not st.session_state.get("log_ollama", False)
        if st.session_state.get("log_ollama", False):
            ollama_log_info = (str(len(station.get('models', []))) + " моделей") if ollama_ok else "Остановлен"
            st.markdown('<div class="comp-log-popup">🕐 ' + datetime.now().strftime("%H:%M") + ' · Статус: ' + ollama_log_info + '</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ─── Универсальный загрузчик API ───
    api_ok = _toggle_init("toggle_api_loader", True)
    st.markdown(f'<div class="comp-wrapper {"ok" if api_ok else "err"}">', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns([17, 0.9, 0.7, 0.8])
    with c1:
        st.markdown('<div class="comp-row" data-status="' + ('ok' if api_ok else 'err') + '"><div class="comp-icon">' + sidebar_img + '</div><div class="comp-info"><div class="comp-name">Универсальный загрузчик API</div><div class="comp-desc">WB + Ozon · Сырые данные</div></div></div>', unsafe_allow_html=True)
    with c2:
        st.toggle("", key=r"toggle_api_loader", label_visibility="collapsed")
        _toggle_changed("toggle_api_loader", "api_loader")
    with c3:
        if st.button("↻", key="restart_api_loader", help="Перезапустить"):
            run_loader("api_loader")
    with c4:
        if st.button("log", key="log_api_btn"):
            st.session_state["log_api"] = not st.session_state.get("log_api", False)
        if st.session_state.get("log_api", False):
            sts = get_loader_status("api_loader")
            last = sts.get("last_run", "Никогда")
            loaded = sts.get("loaded", 0)
            dups = sts.get("duplicates", 0)
            runtime = sts.get("runtime", "")
            st.markdown(f'<div class="comp-log-popup">🕐 {last}<br>📥 Загружено: {loaded} · 🔃 Дубли: {dups}<br>⏱ {runtime}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ─── Загрузчик финансовых документов ───
    fin_ok = _toggle_init("toggle_fin_loader", True)
    st.markdown(f'<div class="comp-wrapper {"ok" if fin_ok else "err"}">', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns([17, 0.9, 0.7, 0.8])
    with c1:
        st.markdown('<div class="comp-row" data-status="' + ('ok' if fin_ok else 'err') + '"><div class="comp-icon">' + sidebar_img + '</div><div class="comp-info"><div class="comp-name">Загрузчик фин. документов</div><div class="comp-desc">Банк + Выгрузки + Счета</div></div></div>', unsafe_allow_html=True)
    with c2:
        st.toggle("", key=r"toggle_fin_loader", label_visibility="collapsed")
        _toggle_changed("toggle_fin_loader", "fin_loader")
    with c3:
        if st.button("↻", key="restart_fin_loader", help="Перезапустить"):
            run_loader("fin_loader")
    with c4:
        if st.button("log", key="log_fin_btn"):
            st.session_state["log_fin"] = not st.session_state.get("log_fin", False)
        if st.session_state.get("log_fin", False):
            sts = get_loader_status("fin_loader")
            last = sts.get("last_run", "Никогда")
            loaded = sts.get("loaded", 0)
            dups = sts.get("duplicates", 0)
            runtime = sts.get("runtime", "")
            st.markdown(f'<div class="comp-log-popup">🕐 {last}<br>📥 Загружено: {loaded} · 🔃 Дубли: {dups}<br>⏱ {runtime}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ─── Агрегатор ───
    agg_ok = _toggle_init("toggle_aggregator", True)
    st.markdown(f'<div class="comp-wrapper {"ok" if agg_ok else "err"}">', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns([17, 0.9, 0.7, 0.8])
    with c1:
        st.markdown('<div class="comp-row" data-status="' + ('ok' if agg_ok else 'err') + '"><div class="comp-icon">' + sidebar_img + '</div><div class="comp-info"><div class="comp-name">Агрегатор</div><div class="comp-desc">WB + Ozon + Finance → Baserow</div></div></div>', unsafe_allow_html=True)
    with c2:
        st.toggle("", key=r"toggle_aggregator", label_visibility="collapsed")
        _toggle_changed("toggle_aggregator", "aggregator")
    with c3:
        if st.button("↻", key="restart_aggregator", help="Перезапустить"):
            run_loader("aggregator")
    with c4:
        if st.button("log", key="log_agg_btn"):
            st.session_state["log_agg"] = not st.session_state.get("log_agg", False)
        if st.session_state.get("log_agg", False):
            sts = get_loader_status("aggregator")
            last = sts.get("last_run", "Никогда")
            loaded = sts.get("loaded", 0)
            aggs = sts.get("aggregations", [])
            agg_text = " · ".join([f"{a['table']}: {a['rows']}" for a in aggs]) if aggs else ""
            st.markdown(f'<div class="comp-log-popup">🕐 {last}<br>📥 Агрегировано: {loaded} строк<br>{agg_text}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Закрытие попапа по клику в любое место
    st.markdown("""<script>
    document.addEventListener('click',function(e){
        if(!e.target.closest('.comp-log-popup')){
            document.querySelectorAll('.comp-log-popup').forEach(function(p){p.remove();});
        }
    });
    </script>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════
# СТРАНИЦА: AI ИНФРАСТРУКТУРА
# ═══════════════════════════════════════════════════
elif page == "Аналитика":

    # Маркер для скопинга CSS (аналитика: светлый дропдаун)
    st.markdown('<div class="analytics-page-marker" style="display:none;"></div>', unsafe_allow_html=True)
    st.markdown('''<style>
    /* Аналитика: светлый selectbox — как панели Аналитика/Запрос */
    [data-testid="stAppViewContainer"]:has(.analytics-page-marker) div[data-baseweb="select"] > div {
        background: rgba(45,27,78,0.06) !important;
        border: 1px solid rgba(107,63,160,0.4) !important;
        border-radius: 12px !important;
    }
    [data-testid="stAppViewContainer"]:has(.analytics-page-marker) div[data-baseweb="select"] div[value] {
        color: #2D1B4E !important;
        font-family: Inter, sans-serif !important;
    }
    [data-testid="stAppViewContainer"]:has(.analytics-page-marker) div[data-baseweb="select"] svg,
    [data-testid="stAppViewContainer"]:has(.analytics-page-marker) div[data-baseweb="select"] path {
        fill: #2D1B4E !important;
    }
    /* Дропдаун: светло-фиолетовый */
    [data-testid="stAppViewContainer"]:has(.analytics-page-marker) div[data-baseweb="popover"],
    [data-testid="stAppViewContainer"]:has(.analytics-page-marker) div[data-baseweb="popover"] > div:first-child {
        background: transparent !important;
    }
    [data-testid="stAppViewContainer"]:has(.analytics-page-marker) div[data-baseweb="popover"] ul {
        background: rgba(237,228,245,0.97) !important;
        border: 1px solid rgba(107,63,160,0.4) !important;
        border-radius: 10px !important;
    }
    [data-testid="stAppViewContainer"]:has(.analytics-page-marker) li[role="option"] {
        color: #2D1B4E !important;
        font-family: Inter, sans-serif !important;
        background: transparent !important;
    }
    [data-testid="stAppViewContainer"]:has(.analytics-page-marker) li[role="option"]:hover {
        background: rgba(107,63,160,0.2) !important;
    }
    [data-testid="stAppViewContainer"]:has(.analytics-page-marker) li[role="option"][aria-selected="true"] {
        background: rgba(107,63,160,0.15) !important;
        color: #2D1B4E !important;
    }
    </style>''', unsafe_allow_html=True)

    # ─── Выбор агента ───
    st.markdown('<p style="font-family:Inter,sans-serif;font-size:0.9rem;font-weight:600;color:#2D1B4E;margin:0 0 4px;">Агент</p>', unsafe_allow_html=True)
    agent = st.selectbox("Агент", ["Hermes (DeepSeek v4 Pro)", "DeepSeek Fin (локальная)"], key="analytics_agent",
        label_visibility="collapsed",
        help="Hermes — DeepSeek v4 Pro через OpenCode API. DeepSeek Fin — локальная модель через Ollama на стационаре.")

    # ─── Окно аналитики (наверху, над запросом) ───
    st.markdown('<p style="font-family:Inter,sans-serif;font-size:0.9rem;font-weight:600;color:#2D1B4E;margin:90px 0 4px;">Аналитика</p>', unsafe_allow_html=True)
    output_area = st.empty()
    # Плейсхолдер только если нет сохранённого результата
    if not st.session_state.get("analytics_result"):
        output_area.markdown("""
        <div style="background:rgba(45,27,78,0.06);border:1px solid rgba(107,63,160,0.4);
            border-radius:12px;padding:20px;min-height:400px;overflow-y:auto;
            font-family:Inter,sans-serif;color:#2D1B4E;">
            <p style="color:#2D1B4E;font-size:0.85rem;text-align:center;margin-top:170px;opacity:0.5;">
            Здесь появится аналитическая интерпретация агента</p>
        </div>
        """, unsafe_allow_html=True)

    # ─── Поле запроса ───
    st.markdown('<p style="font-family:Inter,sans-serif;font-size:0.9rem;font-weight:600;color:#2D1B4E;margin:10px 0 4px;">Запрос</p>', unsafe_allow_html=True)
    question = st.text_area("Запрос", placeholder="Пример: Посчитай ДРР за последние 7 дней по WB и сравни с прошлой неделей", height=100, key="analytics_q", label_visibility="collapsed")

    # ─── Кнопка выполнения ───
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        execute = st.button("Выполнить", use_container_width=True, type="primary", key="analytics_run")

    if execute and question:
        output_area.markdown("""
        <div style="background:rgba(45,27,78,0.06);border:1px solid rgba(107,63,160,0.4);
            border-radius:12px;padding:20px;min-height:400px;text-align:center;
            font-family:Inter,sans-serif;color:#2D1B4E;">
            <p style="margin-top:170px;font-size:1rem;">Анализирую...</p>
        </div>
        """, unsafe_allow_html=True)
        try:
            result = run_analytics_question(question)
            write_log("Аналитика", f"[{agent}] {question[:60]}...")
            st.session_state.analytics_result = result
            st.session_state.analytics_last_agent = agent
            # Накапливаем токены для счётчика
            st.session_state.total_tokens_in = st.session_state.get("total_tokens_in", 0) + result.get("usage_input", 0)
            st.session_state.total_tokens_out = st.session_state.get("total_tokens_out", 0) + result.get("usage_output", 0)
        except Exception as e:
            st.session_state.analytics_result = {
                "status": "error", "error": f"Ошибка: {e}", "output": None
            }
        st.rerun()

    # ─── Наполнение окна аналитики ───
    saved_result = st.session_state.get("analytics_result")
    if saved_result:
        output = saved_result.get("output") or ""
        error = saved_result.get("error") or ""
        
        if output:
            # Clean output: remove markdown code blocks, normalize whitespace
            import re
            clean = re.sub(r'```.*?```', '', output, flags=re.DOTALL)
            clean = re.sub(r'`([^`]+)`', r'\1', clean)
            clean = clean.strip()
            result_html = f"""
            <div style="background:rgba(45,27,78,0.06);border:1px solid rgba(107,63,160,0.4);
                border-radius:12px;padding:24px;min-height:400px;max-height:680px;overflow-y:auto;
                font-family:Inter,sans-serif;color:#2D1B4E !important;font-size:0.85rem;line-height:1.7;
                white-space:pre-wrap;word-wrap:break-word;">
{clean}
            </div>"""
        elif error:
            result_html = f"""
            <div style="background:rgba(45,27,78,0.06);border:1px solid rgba(107,63,160,0.4);
                border-radius:12px;padding:20px;min-height:400px;overflow-y:auto;
                font-family:Inter,sans-serif;color:#2D1B4E !important;">
            <p style="color:#c0392b;">Ошибка: {error}</p>
            </div>"""
        else:
            result_html = """
            <div style="background:rgba(45,27,78,0.06);border:1px solid rgba(107,63,160,0.4);
                border-radius:12px;padding:20px;min-height:400px;overflow-y:auto;
                font-family:Inter,sans-serif;color:#2D1B4E;">
            <p style="color:#2D1B4E;text-align:center;margin-top:170px;">Пустой результат</p>
            </div>"""
        
        output_area.markdown(result_html, unsafe_allow_html=True)

        # --- Таблица данных (чистый st.dataframe) ---
        result_df_data = saved_result.get("result_df_data")
        if result_df_data:
            import pandas as pd
            df_table = pd.DataFrame(result_df_data)
            st.markdown('<p style="font-family:Inter,sans-serif;font-size:0.85rem;font-weight:600;color:#2D1B4E;margin:16px 0 6px;">📋 Данные</p>', unsafe_allow_html=True)
            st.dataframe(df_table, use_container_width=True, hide_index=True,
                        column_config={c: st.column_config.NumberColumn(format="%.0f") 
                                      for c in df_table.select_dtypes('number').columns})

        # --- График Plotly ---
        chart_html = saved_result.get("chart_html", "")
        if chart_html and len(chart_html) > 100:
            st.markdown('<p style="font-family:Inter,sans-serif;font-size:0.85rem;font-weight:600;color:#2D1B4E;margin:10px 0 6px;">📊 Визуализация</p>', unsafe_allow_html=True)
            # Оборачиваем в светлый контейнер чтобы не было чёрного фона
            wrapped = f'''<div style="background:#fff;border-radius:10px;padding:8px;">
            {chart_html}
            </div>'''
            st.components.v1.html(wrapped, height=580, scrolling=False)

        if st.button("🗑 Очистить", key="clear_analytics"):
            st.session_state.pop("analytics_result", None)
            st.session_state.pop("analytics_last_agent", None)
            st.rerun()

# ═══════════════════════════════════════════════════
# СТРАНИЦА: ДЕБАГ
# ═══════════════════════════════════════════════════
elif page == "⚙ Дебаг":

    # ─── Окно результата ───
    st.markdown('<p style="font-family:Inter,sans-serif;font-size:0.9rem;font-weight:600;color:#2D1B4E;margin:0 0 4px;">Результат</p>', unsafe_allow_html=True)
    debug_output = st.empty()
    if not st.session_state.get("debug_result"):
        debug_output.markdown("""
        <div style="background:rgba(45,27,78,0.06);border:1px solid rgba(107,63,160,0.4);border-radius:12px;padding:20px;min-height:680px;overflow-y:auto;font-family:Inter,sans-serif;color:#2D1B4E;">
            <p style="color:#2D1B4E;font-size:0.85rem;text-align:center;margin-top:310px;opacity:0.5;">Здесь появится результат дебага</p>
        </div>
        """, unsafe_allow_html=True)

    # ─── Поле описания проблемы ───
    st.markdown('<p style="font-family:Inter,sans-serif;font-size:0.9rem;font-weight:600;color:#2D1B4E;margin:10px 0 4px;">Описание проблемы</p>', unsafe_allow_html=True)
    problem = st.text_area("Описание проблемы", placeholder="Опиши что проверить: загрузчики, API, конфигурации, endpoints...", height=100, key="debug_problem", label_visibility="collapsed")

    # ─── Кнопка выполнения ───
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        execute = st.button("Выполнить", use_container_width=True, type="primary", key="debug_run")

    if execute and problem:
        debug_output.markdown("""
        <div style="background:rgba(45,27,78,0.06);border:1px solid rgba(107,63,160,0.4);border-radius:12px;padding:20px;min-height:680px;text-align:center;font-family:Inter,sans-serif;color:#2D1B4E;">
            <p style="margin-top:310px;font-size:1rem;">Анализирую проект...</p>
        </div>
        """, unsafe_allow_html=True)
        try:
            result = debug_script("", problem)
            write_log("Дебаг", f"Статус: {result.get('status')}")
            st.session_state.debug_result = result
        except Exception as e:
            st.session_state.debug_result = {"status":"error", "error": str(e)}
        st.rerun()

    # ─── Наполнение окна ───
    saved = st.session_state.get("debug_result")
    if saved:
        analysis = saved.get("analysis") or ""
        error = saved.get("error") or ""
        
        if analysis:
            debug_output.markdown(f"""
            <div style="background:rgba(45,27,78,0.06);border:1px solid rgba(107,63,160,0.4);border-radius:12px;padding:24px;min-height:400px;max-height:600px;overflow-y:auto;font-family:Inter,sans-serif;color:#2D1B4E !important;font-size:0.85rem;line-height:1.7;white-space:pre-wrap;word-wrap:break-word;">
{analysis}
            </div>
            """, unsafe_allow_html=True)
        
        fixed_code = saved.get("fixed_code") or ""
        changes = saved.get("changes") or []
        
        # Отчёт об изменениях
        if changes:
            st.markdown('<p style="font-family:Inter,sans-serif;font-size:0.85rem;font-weight:600;color:#2D1B4E;margin:16px 0 6px;">Статус</p>', unsafe_allow_html=True)
            for ch in changes:
                if "info" in ch:
                    st.info(ch["info"])
                elif "error" in ch:
                    st.warning(f"❌ {ch['file']}: {ch['error']}")
                else:
                    st.success(f"✅ {ch['file']} ({ch['size']}B) — бэкап: {ch['backup']}")
        
        if fixed_code:
            with st.expander("📝 Исправленный код", expanded=False):
                st.code(fixed_code, language="python")
        
        if error:
            debug_output.markdown(f"""
            <div style="background:rgba(45,27,78,0.06);border:1px solid rgba(107,63,160,0.4);border-radius:12px;padding:20px;min-height:400px;font-family:Inter,sans-serif;color:#2D1B4E;">
            <p style="color:#c0392b;">Ошибка: {error}</p>
            </div>
            """, unsafe_allow_html=True)
        
        if st.button("🗑 Очистить", key="clear_debug"):
            st.session_state.pop("debug_result", None)
            st.rerun()
