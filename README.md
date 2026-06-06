# AI-Powered E-commerce Analytics Platform

**Система сквозной аналитики для маркетплейсов Wildberries и Ozon.**

---

## Как это работает

```
WB API / Ozon API / Excel / Google Sheets
              │
              ▼
┌─────────────────────────────────────────┐
│       universal-api-loader              │
│  Универсальный загрузчик сырых данных   │
│  configs/ — JSON-конфиги для каждого    │
│  отчёта WB и Ozon                       │
└──────────────────┬──────────────────────┘
                   │
    ┌──────────────┼──────────────┐
    ▼              ▼              ▼
┌────────┐  ┌────────────┐  ┌──────────┐
│finance-│  │  loaders/  │  │ raw data │
│loader  │  │ 9 API-загр.│  │  (Excel) │
└───┬────┘  └─────┬──────┘  └────┬─────┘
    │             │              │
    └──────────┬──┘──────────────┘
               ▼
┌─────────────────────────────────────────┐
│              Baserow (PostgreSQL)        │
│         Единое хранилище данных          │
└──────────────────┬──────────────────────┘
                   │
         ┌─────────┼─────────┐
         ▼         ▼         ▼
   ┌──────────┐ ┌──────┐ ┌──────────┐
   │aggregator│ │Metab.│ │analytics │
   │агрегация │ │ :3001│ │AI-аналит.│
   └────┬─────┘ └──────┘ └────┬─────┘
        │                     │
        └──────────┬──────────┘
                   ▼
┌─────────────────────────────────────────┐
│            Streamlit Dashboard           │
│               localhost:8501             │
│   Обзор │ Аналитика │ Архитектура │ Дебаг │
└─────────────────────────────────────────┘
```

---

## Структура

```
├── universal-api-loader/         # Универсальный загрузчик API
│   ├── src/universal_loader.py   # Ядро (54KB)
│   ├── src/validate_config.py    # Валидатор JSON-конфигов
│   ├── configs/ozon/             # 5 JSON-конфигов отчётов Ozon
│   └── configs/wildberries/      # 4 JSON-конфига отчётов WB
│
├── finance-loader/               # Финансовый загрузчик
│   ├── src/finance_loader.py     # Ядро
│   └── configs/                  # 8 JSON-конфигов (банк, Ozon, WB, трафик)
│
├── aggregator/                   # Агрегатор данных
│   ├── src/aggregator.py
│   └── configs/aggregation_rules.json
│
├── analytics/                    # AI-аналитика
│   ├── analyst.py                # Оркестратор анализа
│   ├── src/                      # sandbox, metric_engine, data_discovery...
│   ├── wb_base_loader.py         # Базовый класс загрузчиков
│   └── wb_orchestrator.py        # Оркестратор WB-пайплайна
│
├── loaders/                      # 9 загрузчиков WB/Ozon API
│   ├── wb_sales_loader.py
│   ├── wb_realization_loader.py
│   ├── wb_ads_loader.py
│   ├── ozon_finance_v2_loader.py
│   ├── ozon_postings_loader.py
│   ├── ozon_realization_loader.py
│   ├── ozon_transactions_detail_loader.py
│   ├── ozon_vendor_loader.py
│   └── ozon_ads_loader.py
│
├── dashboard/                    # Streamlit UI
│   ├── app.py
│   └── modules/
│       ├── analytics_sandbox.py  # AI-аналитика (DeepSeek + Plotly)
│       ├── debug_agent.py        # AI-дебаг проекта
│       ├── finance_provider.py   # Финансовая сводка
│       ├── loader_runner.py      # Управление загрузчиками
│       ├── docker_manager.py     # Docker-контейнеры
│       ├── ollama_manager.py     # Ollama-станция
│       └── status_engine.py      # Статусы сервисов
│
├── docker-compose.yml            # Docker-инфраструктура
└── docs/screenshots/             # Скриншоты
```

---

## Стек

`Python` `Streamlit` `Docker` `PostgreSQL` `Baserow` `Metabase` `Qdrant` `DeepSeek API` `Ollama` `Tailscale`

---

## Скриншоты

![Обзор](docs/screenshots/overview.png)
![Аналитика](docs/screenshots/analytics.png)
![Архитектура](docs/screenshots/architecture.png)
![Дебаг](docs/screenshots/debug.png)

---

## Автор

**Дмитрий Грузинов** — основатель GEHLEN LANER.

📧 gruzinov.dmitry.sergeevich@gmail.com
