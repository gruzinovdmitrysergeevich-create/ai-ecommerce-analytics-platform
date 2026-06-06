# Воронка продаж (FBS)

## `POST /api/analytics/v3/sales-funnel/products`

**Назначение:** статистика карточек товаров за период (сравнение с прошлым).  
**Параметры:** `selectedPeriod`, `pastPeriod`, `nmIds` (до 1000), `limit`, `offset`.  
**Поля ответа:** `openCount`, `cartCount`, `orderCount`, `buyoutCount`, `conversions`.

**Параметры для мета-таблицы:**  
- `pagination_type`: `offset`  
- `max_depth_days`: 365  
- `batch_size`: 1000  
- `is_async`: `false`

---

## `POST /api/analytics/v3/sales-funnel/products/history`

**Назначение:** статистика карточек товаров по дням (макс. 1 неделя).  
**Параметры:** `selectedPeriod`, `nmIds` (до 20), `aggregationLevel` (`day`/`week`).  
**Поля ответа:** `date`, `openCount`, `cartCount`, `orderCount`, `buyoutCount`.

---

## `POST /api/analytics/v3/sales-funnel/grouped/history`

**Назначение:** статистика групп товаров по дням (по предметам, брендам, ярлыкам).  
**Параметры:** `selectedPeriod`, `subjectIds`, `brandNames`, `tagIds`, `aggregationLevel`.  
**Поля ответа:** `history[].date`, `openCount`, `cartCount`, `orderCount`.
