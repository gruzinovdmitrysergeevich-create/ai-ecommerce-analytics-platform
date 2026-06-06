# Performance API – рекламная аналитика (Ozon)

Базовый URL: `https://api-performance.ozon.ru`  
Авторизация: `Authorization: Bearer <API_KEY>`

## Общие лимиты
- Общий лимит: 100 000 запросов в сутки
- Лимит выгрузок: 2000 за 24 часа с аккаунта
- Максимальный период отчёта: 62 дня
- Одновременных выгрузок с аккаунта: 1

---

## `POST /api/client/statistics`

Статистика по кампаниям (CSV или JSON). Асинхронный метод.

### Параметры запроса
| Параметр | Тип | Описание |
|----------|-----|----------|
| `campaigns` | array | ID кампаний |
| `from` | string | Начало периода (RFC3339) |
| `to` | string | Конец периода |
| `dateFrom` | string | `YYYY-MM-DD` |
| `dateTo` | string | `YYYY-MM-DD` |
| `groupBy` | string | `DATE`, `START_OF_WEEK`, `START_OF_MONTH` |

### Параметры для мета-таблицы
- `pagination_type`: `none`
- `max_depth_days`: 62
- `batch_size`: 1
- `is_async`: `true`

---

## `POST /api/client/statistics/attribution`

Отчёт по заказам с атрибуцией (какие заказы пришли с рекламы).

### Параметры
Аналогично `/statistics`

### Параметры для мета-таблицы
- `pagination_type`: `none`
- `max_depth_days`: 62
- `batch_size`: 1
- `is_async`: `true`

---

## `POST /api/client/statistics/video`

Статистика по показам видеобаннеров.

### Параметры
| Параметр | Тип | Описание |
|----------|-----|----------|
| `campaigns` | array | ID кампаний |
| `dateFrom` | string | `YYYY-MM-DD` |
| `dateTo` | string | `YYYY-MM-DD` |
| `groupBy` | string | `DATE`, `START_OF_WEEK`, `START_OF_MONTH` |

### Параметры для мета-таблицы
- `pagination_type`: `none`
- `max_depth_days`: 62
- `batch_size`: 1
- `is_async`: `true`

---

## `GET /api/client/statistics/campaign/media`

Статистика по медийным кампаниям (JSON/CSV).

### Параметры
| Параметр | Тип | Описание |
|----------|-----|----------|
| `campaignIds` | array | ID кампаний |
| `dateFrom` | string | `YYYY-MM-DD` |
| `dateTo` | string | `YYYY-MM-DD` |

### Поля ответа
`campaignId`, `expense`, `impressions`, `clicks`, `orders`, `revenue`

### Параметры для мета-таблицы
- `pagination_type`: `none`
- `max_depth_days`: 62
- `batch_size`: 1
- `is_async`: `false`

---

## `GET /api/client/statistics/campaign/product`

Статистика по кампаниям «Оплата за клик».

### Параметры
| Параметр | Тип | Описание |
|----------|-----|----------|
| `campaignIds` | array | ID кампаний |
| `dateFrom` | string | `YYYY-MM-DD` |
| `dateTo` | string | `YYYY-MM-DD` |

### Параметры для мета-таблицы
- `pagination_type`: `none`
- `max_depth_days`: 62
- `batch_size`: 1
- `is_async`: `false`

---

## `GET /api/client/statistics/expense`

Расходы по кампаниям.

### Параметры
| Параметр | Тип | Описание |
|----------|-----|----------|
| `campaignIds` | array | ID кампаний |
| `dateFrom` | string | `YYYY-MM-DD` |
| `dateTo` | string | `YYYY-MM-DD` |

### Поля ответа
`campaignId`, `expense`, `bonusExpense`

### Параметры для мета-таблицы
- `pagination_type`: `none`
- `max_depth_days`: 62
- `batch_size`: 1
- `is_async`: `false`

---

## `GET /api/client/statistics/daily`

Дневная статистика по кампаниям.

### Параметры
| Параметр | Тип | Описание |
|----------|-----|----------|
| `campaignIds` | array | ID кампаний |
| `dateFrom` | string | `YYYY-MM-DD` |
| `dateTo` | string | `YYYY-MM-DD` |

### Поля ответа
`campaignId`, `date`, `impressions`, `clicks`, `expense`, `orders`, `revenue`

### Параметры для мета-таблицы
- `pagination_type`: `none`
- `max_depth_days`: 62
- `batch_size`: 1
- `is_async`: `false`

---

## `POST /api/client/statistic/orders/generate`

Отчёт по заказам в «Оплате за заказ» (выбранные товары).

### Параметры
| Параметр | Тип | Описание |
|----------|-----|----------|
| `from` | string | Начало периода (RFC3339) |
| `to` | string | Конец периода |

### Параметры для мета-таблицы
- `pagination_type`: `none`
- `max_depth_days`: 62
- `batch_size`: 1
- `is_async`: `true`

---

## `POST /api/client/statistic/products/generate`

Отчёт по товарам в «Оплате за заказ».

### Параметры
| Параметр | Тип | Описание |
|----------|-----|----------|
| `from` | string | Начало периода |
| `to` | string | Конец периода |

### Параметры для мета-таблицы
- `pagination_type`: `none`
- `max_depth_days`: 62
- `batch_size`: 1
- `is_async`: `true`

---

## `GET /api/client/statistics/all_sku_promo/orders/generate`

Отчёт по заказам в «Оплате за заказ» – все товары.

### Параметры
| Параметр | Тип | Описание |
|----------|-----|----------|
| `timeBounds.from` | string | Начало периода |
| `timeBounds.to` | string | Конец периода |

### Параметры для мета-таблицы
- `pagination_type`: `none`
- `max_depth_days`: 62
- `batch_size`: 1
- `is_async`: `true`

---

## `GET /api/client/statistics/all_sku_promo/products/generate`

Отчёт по товарам в «Оплате за заказ» – все товары.

### Параметры
| Параметр | Тип | Описание |
|----------|-----|----------|
| `timeBounds.from` | string | Начало периода |
| `timeBounds.to` | string | Конец периода |

### Параметры для мета-таблицы
- `pagination_type`: `none`
- `max_depth_days`: 62
- `batch_size`: 1
- `is_async`: `true`

---

## `POST /api/client/statistics/phrases`

Отчёт по поисковым запросам (только для кампаний с `placement = PLACEMENT_TOP_PROMOTION`).

### Параметры
| Параметр | Тип | Описание |
|----------|-----|----------|
| `campaigns` | array | ID кампаний |
| `from` | string | Начало периода |
| `to` | string | Конец периода |
| `groupBy` | string | `DATE`, `START_OF_WEEK`, `START_OF_MONTH` |

### Параметры для мета-таблицы
- `pagination_type`: `none`
- `max_depth_days`: 62
- `batch_size`: 1
- `is_async`: `true`

---

## `GET /api/client/statistics/{UUID}`

Проверка статуса асинхронного отчёта.

### Параметры
| Параметр | Тип | Описание |
|----------|-----|----------|
| `UUID` | string | Идентификатор задания |

### Поля ответа
| Поле | Описание |
|------|----------|
| `state` | `NOT_STARTED`, `IN_PROGRESS`, `ERROR`, `OK` |
| `link` | Ссылка на файл (если `OK`) |

---

## `GET /api/client/statistics/report`

Скачивание готового отчёта по UUID.

### Параметры
| Параметр | Тип | Описание |
|----------|-----|----------|
| `UUID` | string | Идентификатор задания |

[Документация Performance API](https://docs.ozon.ru/api/performance/)
