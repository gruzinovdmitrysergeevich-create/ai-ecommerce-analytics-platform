# Управление остатками (FBO – только чтение)

Для FBO остатки обновляются автоматически. Методы только для получения информации.

## `POST /v4/product/info/stocks`

Информация о количестве товаров на складах FBS/rFBS/FBP.

### Параметры
| Параметр | Тип | Описание |
|----------|-----|----------|
| `filter.offer_id` | array | Артикулы |
| `filter.product_id` | array | ID товаров |
| `limit` | int | До 1000 |
| `cursor` | string | Пагинация |

### Поля ответа
| Поле | Описание |
|------|----------|
| `items[].stocks[].present` | В наличии |
| `items[].stocks[].reserved` | Зарезервировано |

---

## `POST /v1/analytics/stocks`

Аналитика остатков FBO (см. `analytics/stocks.md`).

---

## `POST /v2/products/stocks`

Обновление остатков (только для FBS/rFBS).

[Документация](https://docs.ozon.ru/api/seller/)
