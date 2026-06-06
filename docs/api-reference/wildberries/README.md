# Wildberries API – структурированная документация (FBS)

Документация разделена на **приоритетные отчёты** (для юнит-экономики и аналитики) и **операционные методы** (автоматизация FBS).

## 🔥 Приоритетные отчёты (аналитика)

| Раздел | Файл | Ключевые методы |
|--------|------|-----------------|
| Продажи и заказы | [sales_orders.md](analytics/sales_orders.md) | `/api/v1/supplier/sales`, `/api/v1/supplier/orders` |
| Финансовые отчёты | [finance.md](analytics/finance.md) | `/api/v5/supplier/reportDetailByPeriod` |
| Остатки на складах | [stocks.md](analytics/stocks.md) | `/api/v1/supplier/stocks`, `/api/v3/stocks/{warehouseId}` |
| Аналитика воронки продаж | [sales_funnel.md](analytics/sales_funnel.md) | `/api/analytics/v3/sales-funnel/*` |
| Отчёты по возвратам | [returns.md](analytics/returns.md) | `/api/v1/analytics/goods-return` |

## ⚙️ Автоматизация FBS

| Раздел | Файл | Ключевые методы |
|--------|------|-----------------|
| Сборочные задания | [orders_fbs.md](automation/orders_fbs.md) | `/api/v3/orders/new`, `/api/v3/orders/{orderId}/cancel`, `/api/v3/orders/status` |
| Поставки FBS | [supplies.md](automation/supplies.md) | `/api/v3/supplies`, `/api/v3/supplies/{supplyId}/orders` |
| Остатки на складах | [stocks_management.md](automation/stocks_management.md) | `/api/v3/stocks/{warehouseId}` (PUT, DELETE) |
| Склады продавца | [warehouses.md](automation/warehouses.md) | `/api/v3/warehouses` |
| Метаданные (маркировка) | [metadata.md](automation/metadata.md) | `/api/v3/orders/{orderId}/meta/*` |
| Цены и скидки | [prices.md](automation/prices.md) | `/api/v2/upload/task` |
| Товары и карточки | [products.md](automation/products.md) | `/content/v2/cards/*` |
| **Реклама** | [ads.md](automation/ads.md) | `/adv/v1/upd`, `/adv/v3/fullstats` |

## 📌 Примечание

- Все методы актуальны для схемы **FBS**.
- Для финансовой аналитики основной источник — `/api/v5/supplier/reportDetailByPeriod`.

## 📌 Общие принципы работы
См. [general.md](general.md) – авторизация, форматы дат, пагинация, лимиты, особенности FBS.
