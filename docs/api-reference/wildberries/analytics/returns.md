# Возвраты (FBS)

## `GET /api/v1/analytics/goods-return`

**Назначение:** отчёт о возвратах товаров продавцу.  
**Параметры:** `dateFrom`, `dateTo` (макс. 31 день).  
**Поля ответа:** `nmId`, `srid`, `orderId`, `status`, `reason`, `completedDt`.

**Параметры для мета-таблицы:**  
- `pagination_type`: `none`  
- `max_depth_days`: 31  
- `batch_size`: 1  
- `is_async`: `false`
