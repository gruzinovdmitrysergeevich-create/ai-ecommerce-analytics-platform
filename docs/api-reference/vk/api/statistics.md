
Статистика
Основной метод для получения ретроспективных данных по откруткам.

Статистика по группам объявлений (по дням)
GET /api/v2/statistics/ad_groups/day.json

Обязательные параметры:

ids – ID групп через запятую.

period=day

date_from – YYYY-MM-DD

date_to – YYYY-MM-DD

Пример запроса:

text
GET /api/v2/statistics/ad_groups/day.json?ids=9367343,9367344&period=day&date_from=2026-04-01&date_to=2026-04-10
Основные метрики в ответе:

impressions – показы

clicks – клики

spent – потрачено (в валюте аккаунта)

reach – охват

cpm – цена за 1000 показов

ctr – кликабельность (%)

Статистика по объявлениям
GET /api/v2/statistics/banners/day.json – аналогично, параметр ids – ID баннеров.

Статистика по кампаниям
GET /api/v2/statistics/ad_plans/day.json
