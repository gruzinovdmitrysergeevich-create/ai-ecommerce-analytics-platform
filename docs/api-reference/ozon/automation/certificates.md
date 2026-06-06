# Сертификаты

## `POST /v1/product/certificate/create`

Добавить сертификат.

### Параметры
| Параметр | Тип | Описание |
|----------|-----|----------|
| `name` | string | Название |
| `number` | string | Номер |
| `type_code` | string | Тип сертификата |
| `issue_date` | string | Дата начала действия |
| `expire_date` | string | Дата окончания |
| `files` | array | Файлы (multipart) |

---

## `POST /v1/product/certificate/bind`

Привязать сертификат к товару.

### Параметры
| Параметр | Тип | Описание |
|----------|-----|----------|
| `certificate_id` | int | ID сертификата |
| `product_id` | array | ID товаров |

---

## `POST /v1/product/certificate/list`

Список сертификатов.

### Параметры
| Параметр | Тип | Описание |
|----------|-----|----------|
| `status` | string | Статус |
| `type` | string | Тип |
| `page` | int | |
| `page_size` | int | |

[Документация](https://docs.ozon.ru/api/seller/)
