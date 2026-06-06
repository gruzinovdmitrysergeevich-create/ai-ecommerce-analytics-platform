# Товары и атрибуты (Ozon FBO)

## `POST /v1/description-category/tree`

Дерево категорий и типов товаров. Используется для получения `description_category_id` и `type_id`.

### Параметры
| Параметр | Тип | Описание |
|----------|-----|----------|
| `language` | string | `DEFAULT`, `RU`, `EN` |

---

## `POST /v1/description-category/attribute`

Список характеристик для категории и типа.

### Параметры
| Параметр | Тип | Описание |
|----------|-----|----------|
| `description_category_id` | int | ID категории |
| `type_id` | int | ID типа |

---

## `POST /v1/description-category/attribute/values`

Справочник значений характеристики.

### Параметры
| Параметр | Тип | Описание |
|----------|-----|----------|
| `attribute_id` | int | ID характеристики |
| `description_category_id` | int | |
| `type_id` | int | |
| `limit` | int | Количество (до 2000) |

---

## `POST /v3/product/import`

Создание или обновление товаров. До 100 товаров за запрос.

### Параметры (элемент массива `items`)
| Параметр | Тип | Описание |
|----------|-----|----------|
| `offer_id` | string | Артикул |
| `name` | string | Название |
| `price` | string | Цена |
| `old_price` | string | Цена до скидки |
| `vat` | string | НДС |
| `barcode` | string | Штрихкод |
| `description_category_id` | int | ID категории |
| `type_id` | int | ID типа |
| `attributes` | array | Характеристики |
| `images` | array | Ссылки на изображения |
| `depth`, `width`, `height` | int | Габариты |
| `weight` | int | Вес |
| `dimension_unit` | string | `mm`, `cm`, `in` |
| `weight_unit` | string | `g`, `kg`, `lb` |

### Ответ
`task_id` – для проверки статуса через `/v1/product/import/info`.

---

## `POST /v1/product/import/info`

Статус загрузки товара.

### Параметры
| Параметр | Тип | Описание |
|----------|-----|----------|
| `task_id` | int | ID задачи |

---

## `POST /v3/product/list`

Список товаров с пагинацией.

### Параметры
| Параметр | Тип | Описание |
|----------|-----|----------|
| `filter.offer_id` | array | Артикулы |
| `filter.product_id` | array | ID товаров |
| `filter.visibility` | string | `ALL`, `IN_SALE`, `ARCHIVED` |
| `limit` | int | До 1000 |
| `last_id` | string | Для пагинации |

---

## `POST /v3/product/info/list`

Информация о товарах по идентификаторам (до 1000).

### Параметры
| Параметр | Тип | Описание |
|----------|-----|----------|
| `offer_id` | array | |
| `product_id` | array | |
| `sku` | array | |

---

## `POST /v4/product/info/attributes`

Описание характеристик товара.

### Параметры
| Параметр | Тип | Описание |
|----------|-----|----------|
| `filter.offer_id` | array | |
| `filter.product_id` | array | |
| `filter.sku` | array | |
| `limit` | int | До 1000 |

---

## `POST /v1/product/archive` / `POST /v1/product/unarchive`

Перенос в архив и восстановление.

### Параметры
| Параметр | Тип | Описание |
|----------|-----|----------|
| `product_id` | array | ID товаров (до 100) |

---

## `POST /v2/products/delete`

Удаление товара без SKU из архива.

### Параметры
| Параметр | Тип | Описание |
|----------|-----|----------|
| `products[].offer_id` | string | Артикул |

[Документация](https://docs.ozon.ru/api/seller/)
