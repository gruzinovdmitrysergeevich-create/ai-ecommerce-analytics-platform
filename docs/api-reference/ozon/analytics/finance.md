# Финансовые отчёты и транзакции (Ozon FBO)

## `POST /v3/finance/transaction/list`

Список всех транзакций (начисления, комиссии, услуги) за период. Максимальный период в одном запросе — 1 месяц.

### Параметры запроса
| Параметр | Тип | Описание |
|----------|-----|----------|
| `filter.date.from` | string | Начало периода (ISO 8601) |
| `filter.date.to` | string | Конец периода |
| `filter.transaction_type` | string | `all`, `orders`, `returns`, `services`, `compensation`, `transferDelivery`, `other` |
| `filter.operation_type` | array | Фильтр по типам операций |
| `filter.posting_number` | string | Номер отправления |
| `page` | int | Номер страницы |
| `page_size` | int | Размер страницы (макс. 1000) |

### Поля ответа
| Поле | Описание |
|------|----------|
| `operations[].operation_id` | ID операции |
| `operations[].operation_type_name` | Тип операции |
| `operations[].amount` | Сумма |
| `operations[].posting.posting_number` | Номер отправления |
| `operations[].items` | Товары в операции |

### Параметры для мета-таблицы
- `pagination_type`: `page_number`
- `max_depth_days`: 1095
- `batch_size`: 1000
- `is_async`: false

---

## `POST /v3/finance/transaction/totals`

Итоговые суммы по транзакциям за указанный период.

### Параметры запроса
| Параметр | Тип | Описание |
|----------|-----|----------|
| `date.from` | string | Начало периода |
| `date.to` | string | Конец периода |
| `posting_number` | string | Номер отправления (опционально) |
| `transaction_type` | string | Тип транзакции |

### Поля ответа
| Поле | Описание |
|------|----------|
| `accruals_for_sale` | Общая стоимость товаров и возвратов |
| `sale_commission` | Комиссия за продажу |
| `processing_and_delivery` | Обработка и доставка |
| `refunds_and_cancellations` | Возвраты и отмены |
| `services_amount` | Услуги |
| `compensation_amount` | Компенсации |

### Параметры для мета-таблицы
- `pagination_type`: `none`
- `max_depth_days`: 365
- `batch_size`: 1
- `is_async`: false

---

## `POST /v1/finance/cash-flow-statement/list`

Финансовый отчёт за периоды с 01 по 15 и с 16 по 31 число.

### Параметры
| Параметр | Тип | Описание |
|----------|-----|----------|
| `date.from` | string | Начало периода |
| `date.to` | string | Конец периода |
| `with_details` | bool | Детализация |
| `page` | int | Страница |
| `page_size` | int | Размер страницы |

### Поля ответа
| Поле | Описание |
|------|----------|
| `cash_flows[].orders_amount` | Сумма заказов |
| `cash_flows[].returns_amount` | Сумма возвратов |
| `cash_flows[].services_amount` | Сумма услуг |
| `details.payments` | Выплаты |

### Параметры для мета-таблицы
- `pagination_type`: `page_number`
- `max_depth_days`: 365
- `batch_size`: 100
- `is_async`: false

---

## `POST /v2/finance/realization`

Отчёт о реализации товаров за месяц (доставленные и возвращённые). Отмены и невыкупы не включаются. Доступен не позднее 5-го числа следующего месяца.

### Параметры
| Параметр | Тип | Описание |
|----------|-----|----------|
| `month` | int | Месяц (1-12) |
| `year` | int | Год |

### Поля ответа
| Поле | Описание |
|------|----------|
| `header.contract_number` | Номер договора |
| `rows[].item.sku` | SKU |
| `rows[].item.offer_id` | Артикул |
| `rows[].seller_price_per_instance` | Цена продавца |
| `rows[].delivery_commission.total` | Комиссия за доставку |
| `rows[].return_commission.total` | Комиссия за возврат |

### Параметры для мета-таблицы
- `pagination_type`: `none`
- `max_depth_days`: 365
- `batch_size`: 1
- `is_async`: false

---

## `POST /v1/finance/realization/posting`

Позаказный отчёт о реализации товаров с детализацией по каждому заказу.

### Параметры
| Параметр | Тип | Описание |
|----------|-----|----------|
| `month` | int | Месяц |
| `year` | int | Год |

### Поля ответа
| Поле | Описание |
|------|----------|
| `rows[].order.posting_number` | Номер отправления |
| `rows[].order.created_date` | Дата создания |
| `rows[].item.offer_id` | Артикул |

### Параметры для мета-таблицы
- `pagination_type`: `none`
- `max_depth_days`: 365
- `batch_size`: 1
- `is_async`: false

---

## `POST /v1/finance/compensation`

Отчёт о компенсациях. Возвращает код для получения файла через `/v1/report/info`.

### Параметры
| Параметр | Тип | Описание |
|----------|-----|----------|
| `date` | string | `YYYY-MM` |
| `language` | string | `RU` / `EN` |

### Параметры для мета-таблицы
- `pagination_type`: `none`
- `max_depth_days`: 365
- `batch_size`: 1
- `is_async`: true

---

## `POST /v1/finance/decompensation`

Отчёт о декомпенсациях.

### Параметры
| Параметр | Тип | Описание |
|----------|-----|----------|
| `date` | string | `YYYY-MM` |
| `language` | string | `RU` / `EN` |

### Параметры для мета-таблицы
- `pagination_type`: `none`
- `max_depth_days`: 365
- `batch_size`: 1
- `is_async`: true

---

## `POST /v1/finance/document-b2b-sales`

Реестр продаж юридическим лицам (CSV).

### Параметры
| Параметр | Тип | Описание |
|----------|-----|----------|
| `date` | string | `YYYY-MM` |
| `language` | string | `RU` / `EN` |

### Параметры для мета-таблицы
- `pagination_type`: `none`
- `max_depth_days`: 365
- `batch_size`: 1
- `is_async`: true

---

## `POST /v1/finance/document-b2b-sales/json`

Реестр продаж юридическим лицам в JSON.

### Параметры
| Параметр | Тип | Описание |
|----------|-----|----------|
| `date` | string | `YYYY-MM` |

### Поля ответа
| Поле | Описание |
|------|----------|
| `invoices[].buyer_info` | Данные покупателя |
| `invoices[].operations[].amount` | Сумма |
| `invoices[].operations[].posting_number` | Номер отправления |

### Параметры для мета-таблицы
- `pagination_type`: `none`
- `max_depth_days`: 365
- `batch_size`: 1
- `is_async`: false

---

## `POST /v1/finance/products/buyout`

Отчёт о выкупленных товарах Ozon для продажи в ЕАЭС и другие страны.

### Параметры
| Параметр | Тип | Описание |
|----------|-----|----------|
| `date_from` | string | `YYYY-MM-DD` |
| `date_to` | string | `YYYY-MM-DD` (макс. 31 день) |

### Поля ответа
| Поле | Описание |
|------|----------|
| `products[].sku` | SKU |
| `products[].offer_id` | Артикул |
| `products[].buyout_price` | Цена выкупа |
| `products[].amount` | Сумма к начислению |

### Параметры для мета-таблицы
- `pagination_type`: `none`
- `max_depth_days`: 365
- `batch_size`: 1
- `is_async`: false

[Официальная документация](https://docs.ozon.ru/api/seller/)
