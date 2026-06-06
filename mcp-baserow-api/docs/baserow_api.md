# Baserow Self-Hosted REST API Documentation

Версия: 1.29+ (актуально для локальной установки)

## Содержание

1. [Аутентификация](#аутентификация)
2. [Работа с Workspace](#работа-с-workspace)
3. [Работа с базами данных](#работа-с-базами-данных)
4. [Работа с таблицами](#работа-с-таблицами)
5. [Работа с полями](#работа-с-полями)
6. [Работа со строками](#работа-со-строками)
7. [Типы полей](#типы-полей)
8. [Поле link_row (связь между таблицами)](#поле-link_row-связь-между-таблицами)

---

## Аутентификация

### Получение JWT-токена

**POST** `/api/user/token-auth/`

Аутентифицирует пользователя по email и паролю, возвращает JWT-токен для последующих запросов.

**Request:**
```json
{
  "username": "user@example.com",
  "password": "your_password"
}
```

**Response (200):**
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Пример (curl):**
```bash
curl -X POST \
  http://localhost:8000/api/user/token-auth/ \
  -H 'Content-Type: application/json' \
  -d '{"username": "user@example.com", "password": "your_password"}'
```

### Использование токена

Для авторизации в запросах добавляйте заголовок:
```
Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

### Database Token (API Token)

Альтернативный способ — использование предварительно созданного токена базы данных:

```
Authorization: Token YOUR_API_TOKEN
```

**Пример:**
```bash
curl -X GET \
  http://localhost:8000/api/database/rows/table/1/ \
  -H 'Authorization: Token 9vZBOVFQG.a1d2f3g4h5i6j7k8l9m0n1o2p3q4r5s6t7u8v9w0x1y2z3'
```

---

## Работа с Workspace

### Получение списка workspaces

**GET** `/api/workspaces/`

Возвращает все workspaces, доступные авторизованному пользователю.

**Пример:**
```bash
curl -X GET \
  http://localhost:8000/api/workspaces/ \
  -H 'Content-Type: application/json' \
  -H 'Authorization: JWT {YOUR_TOKEN}'
```

**Response (200):**
```json
[
  {
    "id": 1,
    "name": "My Workspace",
    "users": [
      {
        "id": 1,
        "name": "John Doe",
        "email": "john@example.com",
        "permissions": "ADMIN"
      }
    ],
    "permissions": "ADMIN"
  }
]
```

### Создание workspace

**POST** `/api/workspaces/`

**Request:**
```json
{
  "name": "Marketing Team"
}
```

**Response (200):**
```json
{
  "id": 2,
  "name": "Marketing Team",
  "users": [
    {
      "id": 1,
      "name": "John Doe",
      "email": "john@example.com",
      "permissions": "ADMIN"
    }
  ],
  "permissions": "ADMIN"
}
```

**Пример:**
```bash
curl -X POST \
  http://localhost:8000/api/workspaces/ \
  -H 'Content-Type: application/json' \
  -H 'Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...' \
  -d '{"name": "Marketing Team"}'
```

---

## Работа с базами данных

### Создание базы данных (application)

**POST** `/api/applications/workspace/{workspace_id}/`

Создаёт новое приложение (базу данных) в указанном workspace.

**Request:**
```json
{
  "name": "My Database",
  "type": "database"
}
```

**Response (200):**
```json
{
  "id": 1,
  "name": "My Database",
  "order": 1,
  "type": "database",
  "workspace_id": 1
}
```

### Получение списка баз данных

**GET** `/api/applications/workspace/{workspace_id}/`

---

## Работа с таблицами

### Создание таблицы

**POST** `/api/database/tables/database/{database_id}/`

Создаёт новую таблицу в указанной базе данных. Можно сразу задать структуру полей и начальные данные.

**Request:**
```json
{
  "name": "Products",
  "data": [
    [
      {"name": "Name", "type": "text"},
      {"name": "Price", "type": "number"},
      {"name": "In Stock", "type": "boolean"}
    ],
    ["Laptop", 999.99, true],
    ["Mouse", 29.99, true],
    ["Keyboard", 79.99, false]
  ]
}
```

**Response (200):**
```json
{
  "id": 3,
  "name": "Products",
  "order": 3,
  "database_id": 1,
  "fields": [
    {
      "id": 1,
      "name": "Name",
      "type": "text",
      "order": 0
    },
    {
      "id": 2,
      "name": "Price",
      "type": "number",
      "order": 1,
      "number_decimal_places": 2
    },
    {
      "id": 3,
      "name": "In Stock",
      "type": "boolean",
      "order": 2
    }
  ]
}
```

**Пример:**
```bash
curl -X POST \
  http://localhost:8000/api/database/tables/database/1/ \
  -H 'Content-Type: application/json' \
  -H 'Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...' \
  -d '{
    "name": "Products",
    "data": [
      [{"name": "Name", "type": "text"}, {"name": "Price", "type": "number"}],
      ["Laptop", 999.99],
      ["Mouse", 29.99]
    ]
  }'
```

### Получение таблицы

**GET** `/api/database/tables/{table_id}/`

### Удаление таблицы

**DELETE** `/api/database/tables/{table_id}/`

**Response:** 204 No Content

---

## Работа с полями

### Создание поля

**POST** `/api/database/fields/table/{table_id}/`

**Request (текстовое поле):**
```json
{
  "name": "Description",
  "type": "text",
  "text_default": "No description"
}
```

**Response (200):**
```json
{
  "id": 10,
  "table_id": 1,
  "name": "Description",
  "order": 3,
  "type": "text",
  "primary": false,
  "text_default": "No description"
}
```

### Получение списка полей таблицы

**GET** `/api/database/fields/table/{table_id}/`

**Response (200):**
```json
[
  {
    "id": 1,
    "table_id": 1,
    "name": "Name",
    "type": "text",
    "order": 0,
    "primary": true
  },
  {
    "id": 2,
    "table_id": 1,
    "name": "Price",
    "type": "number",
    "order": 1,
    "primary": false,
    "number_decimal_places": 2,
    "number_negative": false
  }
]
```

---

## Работа со строками

### Получение строк

**GET** `/api/database/rows/table/{table_id}/`

**Query Parameters:**
- `user_field_names` (boolean) — если `true`, использует читаемые имена полей вместо `field_{id}`
- `page` (integer) — номер страницы
- `size` (integer) — количество строк на странице (до 100)

**Пример:**
```bash
curl -X GET \
  'http://localhost:8000/api/database/rows/table/1/?user_field_names=true' \
  -H 'Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...'
```

**Response (200):**
```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "order": "1.00000000000000000000",
      "Name": "Laptop",
      "Price": 999.99
    },
    {
      "id": 2,
      "order": "2.00000000000000000000",
      "Name": "Mouse",
      "Price": 29.99
    }
  ]
}
```

### Создание строки

**POST** `/api/database/rows/table/{table_id}/`

**Request:**
```json
{
  "Name": "Alice Johnson",
  "Email": "alice@example.com",
  "Active": true,
  "Age": 32
}
```

**Пример:**
```bash
curl -X POST \
  'http://localhost:8000/api/database/rows/table/1/?user_field_names=true' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...' \
  -d '{"Name": "Alice Johnson", "Email": "alice@example.com", "Active": true, "Age": 32}'
```

**Response (200):**
```json
{
  "id": 150,
  "order": "150.00000000000000000000",
  "Name": "Alice Johnson",
  "Email": "alice@example.com",
  "Active": true,
  "Age": 32
}
```

### Обновление строки

**PATCH** `/api/database/rows/table/{table_id}/{row_id}/`

**Request:**
```json
{
  "Email": "alice.johnson@newdomain.com",
  "Age": 33
}
```

**Response (200):**
```json
{
  "id": 150,
  "order": "150.00000000000000000000",
  "Name": "Alice Johnson",
  "Email": "alice.johnson@newdomain.com",
  "Active": true,
  "Age": 33
}
```

### Удаление строки

**DELETE** `/api/database/rows/table/{table_id}/{row_id}/`

**Response:** 204 No Content

**Пример:**
```bash
curl -X DELETE \
  http://localhost:8000/api/database/rows/table/1/150/ \
  -H 'Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...'
```

---

## Типы полей

Baserow поддерживает следующие типы полей:

| Тип | Описание | Специфичные параметры |
|-----|----------|----------------------|
| `text` | Короткий текст | `text_default` — значение по умолчанию |
| `long_text` | Длинный текст | — |
| `number` | Число | `number_decimal_places`, `number_negative` |
| `boolean` | Логическое значение | — |
| `date` | Дата | `date_format`, `date_include_time`, `date_time_format` |
| `link_row` | Связь с другой таблицей | `link_row_table_id`, `link_row_related_field_name` |
| `single_select` | Выбор одного варианта | `select_options` — массив `{value, color}` |
| `multiple_select` | Выбор нескольких вариантов | `select_options` |
| `file` | Файл | — |
| `phone_number` | Номер телефона | — |
| `email` | Email | — |
| `url` | URL-адрес | — |
| `formula` | Формула | `formula`, `formula_type` |
| `lookup` | Подстановка из связанной таблицы | — |
| `rollup` | Агрегация связанных данных | — |
| `rating` | Рейтинг (звёзды) | — |
| `count` | Количество связанных записей | — |
| `last_modified` | Время последнего изменения | — |
| `created_on` | Время создания | — |

### Примеры создания полей разных типов

**Текстовое поле:**
```json
{"name": "Description", "type": "text", "text_default": "N/A"}
```

**Числовое поле с десятичными знаками:**
```json
{
  "name": "Price",
  "type": "number",
  "number_decimal_places": 2,
  "number_negative": false
}
```

**Поле с выбором (single_select):**
```json
{
  "name": "Status",
  "type": "single_select",
  "select_options": [
    {"value": "Active", "color": "green"},
    {"value": "Pending", "color": "yellow"},
    {"value": "Inactive", "color": "red"}
  ]
}
```

---

## Поле link_row (связь между таблицами)

Поле `link_row` создаёт связь между двумя таблицами (аналог foreign key).

### Создание поля link_row

**POST** `/api/database/fields/table/{table_id}/`

**Request:**
```json
{
  "name": "Related Orders",
  "type": "link_row",
  "link_row_table_id": 2,
  "link_row_related_field_name": "Customer"
}
```

**Параметры:**
- `name` — имя поля в текущей таблице
- `link_row_table_id` — ID таблицы, на которую ссылаемся
- `link_row_related_field_name` — имя создаваемого обратного поля в связанной таблице

**Пример:**
```bash
curl -X POST \
  http://localhost:8000/api/database/fields/table/1/ \
  -H 'Content-Type: application/json' \
  -H 'Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...' \
  -d '{
    "name": "Related Orders",
    "type": "link_row",
    "link_row_table_id": 2,
    "link_row_related_field_name": "Customer"
  }'
```

**Response (200):**
```json
{
  "id": 10,
  "table_id": 1,
  "name": "Related Orders",
  "type": "link_row",
  "link_row_table_id": 2,
  "link_row_related_field_id": 11,
  "primary": false
}
```

### Работа со связанными данными

При создании/обновлении строки значение поля `link_row` — массив ID связанных записей:

```json
{
  "Name": "John Doe",
  "Orders": [1, 3, 5]
}
```

---

## Общие принципы

### Базовый URL

Для локальной установки Baserow:
```
http://localhost:8000/api/
```

### Формат данных

- Content-Type: `application/json`
- Поля в ответах именуются как `field_{id}` или по именам (с параметром `user_field_names=true`)

### Пагинация

GET-запросы возвращают результаты с пагинацией:
```json
{
  "count": 150,
  "next": "http://...?page=2",
  "previous": null,
  "results": [...]
}
```

### Ошибки

При ошибках возвращается JSON с деталями:
```json
{
  "error": "ERROR_INVALID_TOKEN",
  "detail": "Token is invalid or expired."
}
```

---

## Источники

- Официальная документация: https://api.baserow.io/api/docs/
- GitHub: https://github.com/baserow/baserow