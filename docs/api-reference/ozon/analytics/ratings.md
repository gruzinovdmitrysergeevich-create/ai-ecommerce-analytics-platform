# Рейтинги продавца

## `POST /v1/rating/summary`

**Назначение:** Текущие рейтинги продавца.

### Параметры
Без параметров.

### Поля ответа
| Поле | Описание |
|------|----------|
| `groups[].group_name` | Группа рейтингов |
| `groups[].items[].name` | Название |
| `groups[].items[].current_value` | Текущее значение |
| `groups[].items[].status` | Статус |
| `premium` | Наличие Premium |
| `penalty_score_exceeded` | Превышение штрафных баллов |

### Параметры для мета-таблицы
- `pagination_type`: `none`
- `max_depth_days`: 30
- `batch_size`: 1
- `is_async`: `false`

---

## `POST /v1/rating/history`

**Назначение:** История рейтингов за период.

### Параметры
| Параметр | Тип | Описание |
|----------|-----|----------|
| `date_from` | string | Начало периода |
| `date_to` | string | Конец периода |
| `ratings` | array | Список рейтингов |
| `with_premium_scores` | bool | Штрафные баллы Premium |

### Параметры для мета-таблицы
- `pagination_type`: `none`
- `max_depth_days`: 365
- `batch_size`: 1
- `is_async`: `false`

[Документация](https://docs.ozon.ru/api/seller/#operation/RatingAPI_Summary)
