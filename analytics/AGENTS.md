# AGENTS.md — Hermes: универсальный аналитик

## Что делает

`analyst.py` — универсальный AI-аналитик. Авто-обнаруживает ВСЕ таблицы Baserow,
сам находит связи между ними, считает метрики детерминированно, 
модель — только интерпретирует.

**БЕЗ ХАРДКОРА.** Никаких списков контрагентов, названий колонок, таблиц в коде.

## Архитектура (v5)

```
analyst.py (оркестратор)
    │
    ├── Pre-flight: проверка Baserow, моделей, полноты данных
    │
    ├── DataDiscovery: авто-обнаружение ВСЕХ таблиц
    │
    ├── DataLinker: поиск связей между таблицами (по датам, колонкам, ID)
    │
    ├── MetricEngine: детерминированный расчёт метрик (ДРР, ROMI, CPC, маржа)
    │       │
    │       └── Модель НЕ считает! Только интерпретирует готовые цифры.
    │
    ├── Банк: классификация контрагентов через модель (один раз, кэшируется)
    │
    └── Анализ:
          ├── Простой вопрос → MetricEngine → цифры → модель (deepseek-fin) → вывод
          └── Сложный вопрос → облако (DeepSeek) → код → Sandbox (retry 3x) → модель → вывод
```

## Модели

| Роль | Модель | Где |
|------|--------|-----|
| **Генерация кода** | DeepSeek API (deepseek-chat = v4 Pro) | Облако |
| **Интерпретация** | deepseek-fin:latest | Локально, Ollama |
| **Классификация** | deepseek-fin | Локально (однократно) |
| **Fallback** | DeepSeek API | Если локальная не ответила |

## Запуск

```bash
cd /mnt/3E7ADD3C7ADCF19F/ai-projects/analytics
python3 analyst.py "вопрос"

# Примеры
python3 analyst.py "Доходы и расходы за всё время"
python3 analyst.py "Свяжи рекламу с продажами по месяцам"
python3 analyst.py "Почему упала прибыль?"
python3 analyst.py "Посчитай ДРР и ROMI за 2025"
```

## Структура

```
analytics/
├── analyst.py              ← точка входа
├── config.yaml             ← ТОЛЬКО техническое (адреса, ключи, пороги)
├── AGENTS.md               ← этот файл
├── src/
│   ├── model_provider.py   ← code (облако) + interpret (локально)
│   ├── data_discovery.py   ← авто-обнаружение таблиц Baserow
│   ├── data_linker.py      ← авто-поиск связей между таблицами
│   ├── metric_engine.py    ← детерминированный расчёт метрик
│   └── sandbox.py          ← умная песочница (retry + анализ ошибок)
└── memory-bank/            ← проектная документация
```

## config.yaml

ТОЛЬКО ТЕХНИЧЕСКОЕ. Никаких фамилий/контрагентов/правил классификации.

Содержит:
- baserow (url, логин, пароль)
- models (code: DeepSeek API, interpret: Ollama, fallback)
- business (название, маркетплейсы)
- analysis (период по умолчанию, пороги аномалий)
- validation (мин. строк, макс. разрыв в днях)

## Конвейер данных

```
marketplace API → universal-api-loader → Baserow (сырые)
Excel/Google → finance-loader → Baserow (сырые)
                                    │
                              aggregator → Baserow (агрегаты)
                                    │
                              analyst.py ← модели
```

## Если что-то сломалось

```bash
# Baserow
cd ~/my-ai-stack && docker compose up -d baserow

# Ollama
curl http://100.64.243.115:11434/api/tags

# Перезапустить загрузчики
cd /mnt/3E7ADD3C7ADCF19F/ai-projects/universal-api-loader && python3 loader.py &
cd /mnt/3E7ADD3C7ADCF19F/ai-projects/finance-loader && python3 src/finance_loader.py
cd /mnt/3E7ADD3C7ADCF19F/ai-projects/aggregator && python3 src/aggregator.py
```

## Правила для Hermes

1. НЕ хардкодить названия таблиц, колонок, контрагентов. ВСЁ через авто-обнаружение или модель.
2. Модель НЕ считает. Скрипт считает (MetricEngine). Модель интерпретирует.
3. Для кода — облако DeepSeek. Для выводов — локально deepseek-fin.
4. При ошибках — Sandbox сам анализирует и даёт модели подсказки.
5. Если локальная модель молчит — fallback на облако.
6. Новые контрагенты — модель классифицирует сама, не лезть в config.yaml.
7. После каждого изменения — запустить тест.
