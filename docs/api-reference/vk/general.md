# Общая информация о VK Ads API

## Базовый URL
https://ads.vk.com/api/v2/

text
Некоторые ресурсы доступны по `/api/v1/` (лид-формы) и `/api/v3/` (опросы, пользователи).

## Авторизация
Используется OAuth2. Основные схемы:
- **Client Credentials Grant** – для собственного аккаунта.
- **Agency Client Credentials Grant** – для клиентов агентства.
- **Authorization Code Grant** – для доступа к сторонним аккаунтам.

Токен передаётся в заголовке:
Authorization: Bearer {access_token}

text
Токен живёт 24 часа, обновляется через `refresh_token`.

## Формат запросов и ответов
- Все данные в JSON (`application/json`).
- Пагинация: `limit` (по умолч. 20, макс. 50–100), `offset`.
- Фильтры: `_<field>__<lookup>=value` (например, `_status__in=active,blocked`).
- Сортировка: `sorting=field,-field2`.

## Базовые типы данных
| Тип | JSON-пример |
|-----|-------------|
| Строка | `"value"` |
| Целое | `123` |
| Десятичная дробь | `"1.23"` |
| Булево | `true` / `false` |
| Дата | `"YYYY-MM-DD"` |
| Дата и время | `"YYYY-MM-DD HH:MM:SS"` (Europe/Moscow) |
| Список | `["a","b"]` |
| Объект | `{"id":1}` |

## HTTP-статусы
- `200` – успех.
- `201` – создано.
- `204` – успех без тела.
- `400` – ошибка валидации.
- `401` – неверный токен.
- `403` – доступ запрещён.
- `404` – не найдено.
- `429` – превышен лимит.

## Лимиты запросов
Возвращаются в заголовках:
- `X-RateLimit-RPS-Limit` / `Remaining`
- `X-RateLimit-Hourly-Limit` / `Remaining`
- `X-RateLimit-Daily-Limit` / `Remaining`

Детальные лимиты: `GET /api/v2/throttling.json`.

## Ошибки авторизации
| Код | Описание |
|-----|----------|
| `invalid_token` | Токен не существует или удалён (>1 месяца). |
| `expired_token` | Токен истёк (можно обновить). |
| `invalid_client` | Неверные client_id или client_secret. |
| `revoked_token` | Доступ отозван пользователем. |

## Ссылки
- Инструкция по получению доступа: https://ads.vk.com/help/features/help_api
- Полная документация методов: https://target.vk.ru/partners/help/management_api
