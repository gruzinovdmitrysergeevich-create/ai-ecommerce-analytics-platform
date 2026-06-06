# Чаты с покупателями

## `POST /v3/chat/list`

Список чатов.

### Параметры
| Параметр | Тип | Описание |
|----------|-----|----------|
| `filter.chat_status` | string | `OPENED` |
| `filter.unread_only` | bool | |
| `limit` | int | До 100 |
| `cursor` | string | Пагинация |

---

## `POST /v3/chat/history`

История сообщений чата.

### Параметры
| Параметр | Тип | Описание |
|----------|-----|----------|
| `chat_id` | string | ID чата |
| `direction` | string | `Forward` / `Backward` |
| `limit` | int | До 1000 |

---

## `POST /v1/chat/send/message`

Отправить сообщение (Premium).

### Параметры
| Параметр | Тип | Описание |
|----------|-----|----------|
| `chat_id` | string | |
| `text` | string | Текст (1-1000 символов) |

---

## `POST /v1/chat/send/file`

Отправить файл.

### Параметры
| Параметр | Тип | Описание |
|----------|-----|----------|
| `chat_id` | string | |
| `name` | string | Имя файла |
| `base64_content` | string | Файл в base64 |

---

## `POST /v1/chat/start`

Создать новый чат по отправлению.

### Параметры
| Параметр | Тип | Описание |
|----------|-----|----------|
| `posting_number` | string | Номер отправления |

---

## `POST /v2/chat/read`

Отметить сообщения прочитанными.

### Параметры
| Параметр | Тип | Описание |
|----------|-----|----------|
| `chat_id` | string | |
| `from_message_id` | int | ID сообщения |

[Документация](https://docs.ozon.ru/api/seller/)
