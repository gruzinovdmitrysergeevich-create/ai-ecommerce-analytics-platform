# Отправления FBO

## `POST /v2/posting/fbo/list`

**Назначение:** Список отправлений FBO за период (макс. 1 год).

### Параметры запроса
| Параметр | Тип | Описание |
|----------|-----|----------|
| `filter.since` | string | Начало периода |
| `filter.to` | string | Конец периода |
| `filter.status` | string | Статус отправления |
| `limit` | int | Количество (макс. 1000) |
| `offset` | int | Смещение (макс. 20000) |
| `with.analytics_data` | bool | Добавить аналитику |
| `with.financial_data` | bool | Добавить финансы |

### Поля ответа
| Поле | Описание |
|------|----------|
| `result[].posting_number` | Номер отправления |
| `result[].order_number` | Номер заказа |
| `result[].status` | Статус |
| `result[].products[].sku` | SKU |
| `result[].financial_data.products[].commission_amount` | Комиссия |
| `result[].financial_data.products[].payout` | Выплата |

### Параметры для мета-таблицы
- `pagination_type`: `offset`
- `max_depth_days`: 365
- `batch_size`: 1000
- `is_async`: `false`

---

## `POST /v2/posting/fbo/get`

**Назначение:** Информация о конкретном отправлении.

### Параметры
| Параметр | Тип | Описание |
|----------|-----|----------|
| `posting_number` | string | Номер отправления |
| `with.analytics_data` | bool | |
| `with.financial_data` | bool | |

### Параметры для мета-таблицы
- `pagination_type`: `none`
- `max_depth_days`: 365
- `batch_size`: 1
- `is_async`: `false`

---

## `POST /v1/report/postings/create`

**Назначение:** Расширенный отчёт об отправлениях (CSV).

### Параметры
| Параметр | Тип | Описание |
|----------|-----|----------|
| `filter.processed_at_from` | string | Начало периода обработки |
| `filter.processed_at_to` | string | Конец периода |
| `filter.delivery_schema` | array | `fbo`, `fbs`, `rfbs` |
| `filter.statuses` | array | Статусы |
| `filter.offer_id` | string | Артикул |
| `filter.sku` | array | SKU |

### Ответ
`code` – идентификатор для `/v1/report/info`.

### Параметры для мета-таблицы
- `pagination_type`: `none`
- `max_depth_days`: 365
- `batch_size`: 1
- `is_async`: `true`

[Документация](https://docs.ozon.ru/api/seller/#operation/PostingAPI_FboListV2)
