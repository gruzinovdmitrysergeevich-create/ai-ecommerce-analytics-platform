# Основная аналитика – /v1/analytics/data

## `POST /v1/analytics/data`

**Назначение:** получение аналитических данных с группировкой по измерениям (день, SKU, категория и т.д.).

### Параметры запроса

| Параметр | Тип | Описание |
|----------|-----|----------|
| `date_from` | string | Начало периода (YYYY-MM-DD) |
| `date_to` | string | Конец периода |
| `dimension` | array | Группировка: `sku`, `day`, `week`, `month`, `category1`..`category4`, `brand`, `modelID` |
| `metrics` | array | До 14 метрик |
| `filters` | array | Фильтры по SKU, категориям |
| `limit` | int | Размер страницы (макс. 1000) |
| `offset` | int | Смещение |
| `sort` | array | Сортировка по метрике |

### Основные метрики

| Метрика | Описание |
|---------|----------|
| `revenue` | Заказано на сумму |
| `ordered_units` | Заказано товаров |
| `hits_view_search` | Показы в поиске и категории |
| `hits_view_pdp` | Показы на карточке товара |
| `hits_tocart` | Добавлено в корзину |
| `conv_tocart` | Конверсия в корзину |
| `returns` | Возвращено товаров |
| `cancellations` | Отменено товаров |
| `delivered_units` | Доставлено товаров |

### Особенности

- Без Premium-подписки: данные за последние 3 месяца, ограниченный набор группировок.
- Лимит: 1 запрос в минуту.

### Параметры для мета-таблицы

- `pagination_type`: `offset`
- `max_depth_days`: 1095 (с Premium) / 90 (без)
- `batch_size`: 1000
- `is_async`: `false`

[Документация](https://docs.ozon.ru/api/seller/#operation/AnalyticsAPI_Data)
