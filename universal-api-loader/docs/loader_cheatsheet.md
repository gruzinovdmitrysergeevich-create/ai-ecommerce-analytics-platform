# Шпаргалка для загрузчика

## Baserow: нормализация типов
- `text` → строка, обрезается, пустое → null
- `number` → float(2 знака), запятая → точка, валютные символы удаляются
- `integer` → int, из строки через float()
- `date` → YYYY-MM-DD, поддерживаются ISO, DD.MM.YYYY, DD/MM/YYYY
- `boolean` → true/false из строк "true","1","yes","да"
- Зарезервированные имена: `id`→`row_id`, `order`→`row_order`, `created_on`→`row_created_on`, `updated_on`→`row_updated_on`
- Точки в именах полей заменяются на подчёркивания

## Wildberries API
- Авторизация: `Authorization: Bearer <токен>`
- Пагинация: rrdid (reportDetailByPeriod), dateFrom (sales), offset (sales_funnel), none (goods_return)
- Даты: `YYYY-MM-DD`
- Rate limit: 300/мин

## Ozon API
- Авторизация: `Client-Id` + `Api-Key`
- Пагинация: page_number (transactions, realization), offset (turnover_stocks, analytics_data), last_id (returns_list), none (stock_on_warehouses)
- Даты: `YYYY-MM-DD` + `T00:00:00Z` для POST body
- Rate limit: 50/сек

## Структура JSON-конфига
```json
{
  "report_name": "sales",
  "api_endpoint": "/api/v1/supplier/sales",
  "method": "GET",
  "pagination_type": "dateFrom",
  "field_mapping": {"srid": "text", "nmId": "integer", "finishedPrice": "number", "forPay": "number"},
  "unique_key": "srid",
  "max_depth_days": 90,
  "batch_size": 80000,
  "is_async": false,
  "rate_limit_per_sec": 5,
  "response_data_path": "",
  "date_params": {"from_param": "dateFrom", "to_param": ""},
  "pagination_config": {},
  "request_body_template": ""
}
Отладка
Валидатор: python validators/validate_report_config.py --report-id <ID>

Логи загрузчика: logs/status.md

Логи валидатора: validators/logs/validate.log

Тестовый запуск: cd ~/my-ai-stack/analytics && ./runner.py /mnt/3E7ADD3C7ADCF19F/ai-projects/universal-api-loader/src/universal_loader.py
