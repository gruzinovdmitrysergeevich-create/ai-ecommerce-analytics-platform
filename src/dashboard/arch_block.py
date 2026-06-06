# -*- coding: utf-8 -*-
# Архитектура — вставка в app.py
ARCH_BLOCK = """
# ═══════════════════════════════════════════════════
# СХЕМА АРХИТЕКТУРЫ
# ═══════════════════════════════════════════════════
if st.session_state.get("show_arch"):
    from modules.status_engine import get_overview_status
    s = get_overview_status()
    dg, dr = "#4ade80", "#f87171"
    D = lambda ok: dg if ok else dr
    T = lambda ok: "Работает" if ok else "Остановлен"

    st.markdown('''<style>
    .a2 { max-width:1100px; margin:0 auto; padding:30px 20px; font-family:Inter,sans-serif; }
    .a2 h1 { text-align:center; font-size:1.6rem; font-weight:700; color:#FFFFFF; margin-bottom:6px; }
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
    h += '<h1>Gehlen Laner ' + chr(8212) + ' Архитектура системы</h1>'
    h += '<p class="sub">Обновляется в реальном времени · <span style="color:#4ade80;">Зелёный</span> — работает · <span style="color:#f87171;">Красный</span> — остановлен</p>'

    h += '<div class="sec">Источники данных</div><div class="r">'
    for name, desc in [("Wildberries API", "Продажи · Реализация · Реклама"),
                        ("Ozon API", "Postings · Ads · Finance"),
                        ("Банк / Excel", "Выписки · Управлёнка · Трафик")]:
        h += f'<div class="b"><div class="bn">{name}</div><div class="bd">{desc}</div><div class="bs"><span class="dot" style="background:{D(bs)};box-shadow:0 0 8px {D(bs)}"></span>{"Активен" if bs else "Недоступен"}</div></div>'
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
        h += f'<div class="b"><div class="bn">{name}</div><div class="bd">{desc}</div><div class="bs"><span class="dot" style="background:{D(ok)};box-shadow:0 0 8px {D(ok)}"></span>{"Доступен" if ok else "Недоступен"}</div></div>'
    h += '</div><hr class="ln">'

    h += '<div class="sec">AI Инфраструктура</div><div class="r">'
    items = [
        (f'<span class="ic">🐳</span> Docker', f'{cnt} контейнеров', dk),
        (f'<span class="ic">🦙</span> Ollama Local', 'Ноутбук · iGPU', ol),
        (f'<span class="ic">🦙</span> Ollama Station', 'Стационар · RTX 3090', st_ok),
        ('vLLM', 'Qwen3-Reranker-4B', vl),
        (f'<span class="ic">⬡</span> Tailscale', f'VPN · {tip}', ts),
    ]
    for name, desc, ok in items:
        stxt = "Работает" if (ok is True) else ("Доступен" if name.endswith("Station>") or "Tailscale" in name else ("Подключён" if "Tailscale" in name else "Остановлен"))
        if ok is False: stxt = "Остановлен"
        if ok is True: stxt = "Работает" if "Docker" in name or "Ollama" in name else ("Подключён" if "Tailscale" in name else "Доступен")
        h += f'<div class="b"><div class="bn">{name}</div><div class="bd">{desc}</div><div class="bs"><span class="dot" style="background:{D(ok)};box-shadow:0 0 8px {D(ok)}"></span>{T(ok)}</div></div>'
    h += '</div></div>'

    st.markdown(h, unsafe_allow_html=True)

    _, c, _ = st.columns([2, 2, 2])
    with c:
        if st.button("← Вернуться к обзору", use_container_width=True, type="primary"):
            st.session_state.show_arch = False
            st.rerun()
    st.stop()
"""
