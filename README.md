# AI-Powered E-commerce Analytics Platform

**Система сквозной аналитики для маркетплейсов Wildberries и Ozon.**

---

## Как это работает

```
WB API / Ozon API                Google Sheets / Excel
       │                                 │
       ▼                                 ▼
┌──────────────────┐          ┌──────────────────┐
│ universal-api-   │          │  finance-loader  │
│ loader           │          │  банк, реклама,  │
│ сырые данные     │          │  управленка      │
└────────┬─────────┘          └────────┬─────────┘
         │                             │
         └──────────────┬──────────────┘
                        ▼
              ┌──────────────────┐
              │     Baserow      │
              │  (PostgreSQL)    │
              │ единое хранилище │
              └────────┬─────────┘
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
┌────────────┐  ┌────────────┐  ┌──────────────┐
│ aggregator │  │  Metabase  │  │  analytics   │
│ агрегация  │  │ визуализац.│  │ DeepSeek API │
│ по дням    │  │            │  │ + Ollama     │
└─────┬──────┘  └────────────┘  └──────┬───────┘
      │                               │
      └───────────────┬───────────────┘
                      ▼
           ┌──────────────────┐
           │    Dashboard     │
           │    Streamlit     │
           │   4 страницы     │
           └──────────────────┘
```

**Qdrant** (векторная база данных) поднимается через Docker и хранит неструктурированные данные (договоры, документацию). Участвует в аналитике как дополнительный источник данных.

---

## Структура

```
├── universal-api-loader/         # Универсальный загрузчик WB/Ozon API
│   ├── src/universal_loader.py   # Ядро: чтение JSON-конфигов, загрузка в Baserow
│   ├── src/validate_config.py    # Валидатор конфигов перед запуском
│   ├── configs/ozon/             # 5 JSON-конфигов отчётов Ozon
│   └── configs/wildberries/      # 4 JSON-конфига отчётов WB
│
├── finance-loader/               # Финансовый загрузчик (Google Sheets, Excel)
│   ├── src/finance_loader.py     # Ядро: загрузка из таблиц и файлов
│   └── configs/                  # 8 JSON-конфигов (банк, Ozon, WB, трафик)
│
├── aggregator/                   # Агрегация сырых данных в ежедневные сводки
│   ├── src/aggregator.py         # Группировка по дням, расчёт метрик
│   └── configs/aggregation_rules.json  # Правила агрегации
│
├── analytics/                    # AI-аналитика
│   ├── analyst.py                # Оркестратор: получает вопрос → запускает цепочку
│   ├── config.yaml               # Адреса сервисов, модели AI
│   └── src/
│       ├── data_discovery.py     # Авто-обнаружение всех таблиц Baserow
│       ├── data_linker.py        # Поиск связей между таблицами
│       ├── metric_engine.py      # Детерминированный расчёт метрик (ДРР, ROMI, маржа)
│       ├── model_provider.py     # Работа с AI-моделями (DeepSeek API + Ollama)
│       └── sandbox.py            # Безопасное выполнение сгенерированного кода
│
├── dashboard/                    # Streamlit UI — единый центр управления
│   ├── app.py                    # Главный дашборд (4 страницы)
│   └── modules/
│       ├── debug_agent.py        # AI-дебаг: сканирует проект, ищет ошибки
│       ├── finance_provider.py   # Финансовая сводка из Baserow
│       ├── loader_runner.py      # Управление загрузчиками (вкл/выкл/логи)
│       ├── docker_manager.py     # Управление Docker-контейнерами
│       ├── ollama_manager.py     # Управление Ollama на стационаре
│       └── status_engine.py      # Проверка статусов всех сервисов
│
├── docs/screenshots/             # Скриншоты интерфейса
├── docker-compose.yml            # Docker-инфраструктура (Baserow, Metabase, Qdrant)
├── .env.example                  # Шаблон переменных окружения
├── .gitignore
└── README.md
```

---

## Стек

`Python` `Streamlit` `Docker` `PostgreSQL` `Baserow` `Metabase` `Qdrant` `DeepSeek API` `Ollama` `Tailscale`

---

## Скриншоты

![Обзор системы](docs/screenshots/overview.png)

![Архитектура](docs/screenshots/architecture.png)

![Аналитика](docs/screenshots/analytics1.png)

![Аналитика](docs/screenshots/analytics2.png)

---

## Автор

**Дмитрий Грузинов** — Gehlen LANER

📧 gruzinov.dmitry.sergeevich@gmail.com
