# AI-Powered E-commerce Analytics Platform

**Система сквозной аналитики для маркетплейсов Wildberries и Ozon с AI-ассистентом.**

---

## Архитектура

```
WB API / Ozon API
       │
       ▼
┌──────────────────────────────────────────────┐
│              Универсальные загрузчики         │
│  loaders/ — 9 загрузчиков сырых данных       │
│  (wb_sales, wb_realization, wb_ads,          │
│   ozon_finance_v2, ozon_postings, ...)       │
└──────────────────┬───────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────┐
│              Оркестратор + Baserow            │
│  analytics/wb_orchestrator.py                │
│  analytics/baserow_manager.py                │
│         ↓ PostgreSQL (Baserow) ↓             │
└──────────────────┬───────────────────────────┘
                   │
     ┌─────────────┼─────────────┐
     ▼             ▼             ▼
┌──────────┐ ┌──────────┐ ┌──────────┐
│Проекты   │ │ Дашборд  │ │ Metabase │
│          │ │          │ │          │
│aggregator│ │Streamlit │ │ :3001    │
│finance-  │ │ :8501    │ │ (BI)     │
│loader    │ │          │ │          │
│analytics │ │  4 стр:  │ └──────────┘
│          │ │  Обзор   │
└──────────┘ │  Аналит. │
             │  Архитект│
             │  Дебаг   │
             └──────────┘
```

---

## Структура

```
├── loaders/                       # API-загрузчики (9 шт.)
│   ├── wb_sales_loader.py         # WB — продажи
│   ├── wb_realization_loader.py   # WB — реализация
│   ├── wb_ads_loader.py           # WB — реклама
│   ├── ozon_finance_v2_loader.py  # Ozon — финансы v2
│   ├── ozon_postings_loader.py    # Ozon — отправления
│   ├── ozon_realization_loader.py # Ozon — реализация
│   ├── ozon_transactions_detail_loader.py  # Ozon — детал. транзакции
│   ├── ozon_vendor_loader.py      # Ozon — внешний трафик
│   └── ozon_ads_loader.py         # Ozon — реклама
│
├── analytics/                     # Ядро
│   ├── wb_base_loader.py          # Базовый класс для загрузчиков
│   ├── wb_orchestrator.py         # Оркестратор пайплайна
│   ├── baserow_manager.py         # Клиент Baserow API
│   └── runner.py                  # Запускатор
│
├── projects/                      # Независимые проекты
│   ├── aggregator/                # Агрегация данных
│   │   ├── src/aggregator.py
│   │   └── configs/aggregation_rules.json
│   ├── finance-loader/            # Финансовый загрузчик
│   │   ├── src/finance_loader.py
│   │   └── configs/ (7 JSON-конфигов)
│   └── analytics/                 # AI-аналитика
│       ├── analyst.py
│       └── src/ (sandbox, metric_engine, data_discovery...)
│
├── dashboard/                     # Streamlit UI
│   ├── app.py                     # Главный дашборд
│   └── modules/
│       ├── analytics_sandbox.py   # AI-аналитика (DeepSeek + Plotly)
│       ├── debug_agent.py         # AI-дебаг проекта
│       ├── finance_provider.py    # Финансовая сводка
│       ├── loader_runner.py       # Управление загрузчиками
│       ├── docker_manager.py      # Docker-контейнеры
│       ├── ollama_manager.py      # Ollama-станция
│       └── status_engine.py       # Статусы сервисов
│
├── docker-compose.yml             # Инфраструктура
└── docs/screenshots/              # Скриншоты
```

---

## Стек

`Python` `Streamlit` `Docker` `PostgreSQL` `Baserow` `Metabase` `Qdrant` `DeepSeek API` `Ollama` `Tailscale`

---

## Скриншоты

![Обзор системы](docs/screenshots/overview.png)
![AI-аналитика](docs/screenshots/analytics.png)
![Дебаг](docs/screenshots/debug.png)

---

## Автор

**Дмитрий Грузинов** — основатель GEHLEN LANER.

📧 gruzinov.dmitry.sergeevich@gmail.com
