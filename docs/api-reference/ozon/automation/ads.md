# Реклама Ozon (Performance API)

Базовый URL: `https://api-performance.ozon.ru`

## Авторизация
Заголовок `Authorization: Bearer <API_KEY>`

## `POST /api/client/statistics`
Статистика по кампаниям (CSV или JSON). Асинхронный метод.

### Параметры
- `campaigns` – массив ID
- `from`, `to` – RFC3339
- `groupBy` – `DATE`, `START_OF_WEEK`, `START_OF_MONTH`

### Процесс
1. POST → получаем `UUID` задачи.
2. GET `/api/client/statistics/{UUID}` – статус.
3. При готовности – ссылка на файл.

## `POST /api/client/statistics/attribution`
Отчёт по заказам с атрибуцией.

## Лимиты
- 100 000 запросов в сутки
- Максимальный период отчёта: 62 дня
- Одновременных выгрузок: 1

[Документация](https://docs.ozon.ru/api/performance/)
