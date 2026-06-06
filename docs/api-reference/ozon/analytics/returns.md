# Возвраты FBO и FBS

## `POST /v1/returns/list`

**Назначение:** Информация о возвратах.

### Параметры запроса
| Параметр | Тип | Описание |
|----------|-----|----------|
| `filter.logistic_return_date` | object | `time_from`, `time_to` |
| `filter.visual_status_name` | string | Статус возврата |
| `filter.order_id` | string | ID заказа |
| `filter.posting_numbers` | array | Номера отправлений |
| `filter.offer_id` | string | Артикул |
| `filter.return_schema` | string | `FBO` / `FBS` |
| `limit` | int | До 500 |
| `last_id` | int | Для пагинации |

### Поля ответа
| Поле | Описание |
|------|----------|
| `returns[].id` | ID возврата |
| `returns[].product.sku` | SKU |
| `returns[].product.offer_id` | Артикул |
| `returns[].product.quantity` | Количество |
| `returns[].visual.status.display_name` | Статус |
| `returns[].logistic.return_date` | Дата возврата |

### Параметры для мета-таблицы
- `pagination_type`: `last_id`
- `max_depth_days`: 365
- `batch_size`: 500
- `is_async`: `false`

---

## `POST /v2/report/returns/create`

**Назначение:** Отчёт о возвратах (CSV).

### Параметры
| Параметр | Тип | Описание |
|----------|-----|----------|
| `filter.delivery_schema` | string | `fbo` / `fbs` |
| `filter.date_from` | string | `YYYY-MM-DD` |
| `filter.date_to` | string | |
| `filter.status` | string | Статус |

### Ответ
`code` – идентификатор отчёта.

### Параметры для мета-таблицы
- `pagination_type`: `none`
- `max_depth_days`: 365
- `batch_size`: 1
- `is_async`: `true`

[Документация](https://docs.ozon.ru/api/seller/#operation/ReturnsAPI_List)
