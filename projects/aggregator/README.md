# Агрегатор данных (Aggregator)

Компактные агрегированные таблицы в Baserow на основе сырых данных из `universal-api-loader` (WB, Ozon) и `finance-loader` (финансы).

## Зачем нужен

Сырые таблицы содержат десятки тысяч строк (realization_detail — 24K, transactions — 21K). Для Metabase и AI-аналитики нужны сводные данные по дням. Агрегатор группирует и считает ключевые метрики.

## Какие агрегации считаются

| Таблица | Источник | Группировка | Метрики |
|---|---|---|---|
| `wb_aggregated` | `realization_detail` (WB) | День (`rrDate`) | Логистика, штрафы, хранение, приёмка, комиссия, розничная сумма, количество, к выплате, уникальные заказы |
| `ozon_aggregated` | `transactions` (Ozon) | День (`operation_date`) | Общая сумма, начисления за продажу, комиссия, доставка, обратная доставка, количество заказов |
| `finance_aggregated` | `Выписка по счёту` | День (`Дата`) | Дебет, кредит, дневной баланс |

## Запуск

```bash
cd /mnt/3E7ADD3C7ADCF19F/ai-projects/aggregator
python3 src/aggregator.py
```

## Конфигурация

`configs/aggregation_rules.json` — правила агрегации. Каждое правило описывает:
- `workspace` — имя рабочего пространства Baserow
- `source_table` — имя исходной таблицы
- `group_by` — поле группировки (дата)
- `metrics` — список метрик с типом агрегации (`sum`, `count_unique`, `first`)

## Требования

- Python 3.10+
- `requests`
- Baserow запущен на `localhost:8000`
- `.env` с `BASEROW_EMAIL` и `BASEROW_PASSWORD` (берётся из `~/my-ai-stack/analytics/.env`)

## Логи

`logs/run_YYYYMMDD_HHMMSS.log`

## Добавление новой метрики

1. Отредактировать `configs/aggregation_rules.json`
2. Добавить метрику в существующее правило или создать новое
3. Запустить `python3 src/aggregator.py`
