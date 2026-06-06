# Пуш-уведомления

## `POST /v1/notification/set`

Подключить URL для уведомлений.

### Параметры
| Параметр | Тип | Описание |
|----------|-----|----------|
| `url` | string | URL-адрес |
| `types` | array | Типы уведомлений |

### Типы уведомлений
- `TYPE_NEW_POSTING` – новое отправление
- `TYPE_POSTING_CANCELLED` – отмена
- `TYPE_STATE_CHANGED` – изменение статуса
- `TYPE_DELIVERY_DATE_CHANGED` – изменение даты доставки
- `TYPE_CUTOFF_DATE_CHANGED` – изменение даты отгрузки
- `TYPE_NEW_MESSAGE` – новое сообщение в чате
- `TYPE_STOCKS_CHANGED` – изменение остатков

---

## `POST /v1/notification/list`

Список подключённых URL-адресов.

## `POST /v1/notification/update`

Изменить URL или типы.

## `POST /v1/notification/delete`

Удалить URL.

## `POST /v1/notification/enable`

Включить/выключить уведомления.

[Документация](https://docs.ozon.ru/api/seller/)
