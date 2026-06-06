# Финансовые отчёты (FBS)

## `GET /api/v5/supplier/reportDetailByPeriod`

**Назначение:** детализация к отчётам реализации (основной источник для юнит-экономики).  
**Параметры:** `dateFrom`, `dateTo`, `limit` (до 100000), `rrdid` (пагинация), `period` (`daily`/`weekly`).  
**Ключевые поля:**  
- `realizationreport_id`, `gi_id` (поставка)  
- `retail_price_withdisc_rub`, `ppvz_for_pay` (к перечислению)  
- `commission_percent`, `delivery_rub`, `storage_fee`  
- `srid` (ID заказа), `nmId`, `barcode`  

**Параметры для мета-таблицы:**  
- `pagination_type`: `rrdid`  
- `max_depth_days`: 365+  
- `batch_size`: 100000  
- `is_async`: `false`
