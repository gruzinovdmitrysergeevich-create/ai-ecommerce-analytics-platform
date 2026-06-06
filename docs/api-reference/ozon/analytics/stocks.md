# Аналитика остатков и оборачиваемости (Ozon FBO)

## `POST /v1/analytics/stocks`

**Назначение:** Аналитика по остаткам товаров на складах FBO.

### Параметры запроса
| Параметр | Тип | Описание |
|----------|-----|----------|
| `skus` | array | Список SKU (до 100) |
| `cluster_ids` | array | Идентификаторы кластеров |
| `macrolocal_cluster_ids` | array | Идентификаторы макролокальных кластеров |
| `item_tags` | array | Теги товара: `ECONOM`, `NOVEL`, `DISCOUNT`, `FBS_RETURN`, `SUPER` |
| `turnover_grades` | array | Статус ликвидности |
| `warehouse_ids` | array | Идентификаторы складов |

### Поля ответа
| Поле | Описание |
|------|----------|
| `items[].sku` | SKU |
| `items[].offer_id` | Артикул |
| `items[].available_stock_count` | Доступно к продаже |
| `items[].transit_stock_count` | В поставках в пути |
| `items[].ads` | Среднесуточные продажи за 28 дней |
| `items[].idc` | На сколько дней хватит остатка |
| `items[].turnover_grade` | Статус ликвидности |

### Особенности
- Обновление дважды в день (07:00 и 16:00 UTC).

### Параметры для мета-таблицы
- `pagination_type`: `none`
- `max_depth_days`: 90
- `batch_size`: 100
- `is_async`: `false`

---

## `POST /v1/analytics/turnover/stocks`

**Назначение:** Оборачиваемость товара и количество дней, на которое хватит остатка.

### Параметры запроса
| Параметр | Тип | Описание |
|----------|-----|----------|
| `sku` | array | Список SKU |
| `limit` | int | Количество значений (1-1000) |
| `offset` | int | Смещение |

### Поля ответа
| Поле | Описание |
|------|----------|
| `items[].sku` | SKU |
| `items[].ads` | Среднесуточные продажи за 60 дней |
| `items[].current_stock` | Остаток |
| `items[].idc` | На сколько дней хватит |
| `items[].turnover` | Оборачиваемость в днях |
| `items[].idc_grade` | Уровень остатка |
| `items[].turnover_grade` | Уровень оборачиваемости |

### Параметры для мета-таблицы
- `pagination_type`: `offset`
- `max_depth_days`: 90
- `batch_size`: 1000
- `is_async`: `false`

[Документация](https://docs.ozon.ru/api/seller/#operation/AnalyticsAPI_Stocks)
