
Рекламные кампании (AdPlans)
Ресурс: /api/v2/ad_plans

Получение списка
GET /api/v2/ad_plans.json

limit, offset

_id, _id__in

_status, _status__in (active, blocked, deleted)

sorting (id, name, status, -created)

Получение одной
GET /api/v2/ad_plans/{id}.json?fields=...

Создание
POST /api/v2/ad_plans.json

json
{
  "name": "Название",
  "status": "active",
  "date_start": "2026-04-01",
  "date_end": "2026-04-30",
  "budget_limit_day": "1000.00",
  "budget_limit": "5000.00",
  "autobidding_mode": "max_goals",
  "objective": "traffic"
}
Обязательно: name, status.

Редактирование
POST /api/v2/ad_plans/{id}.json – передаются только изменяемые поля.

Массовое обновление
POST /api/v2/ad_plans/mass_action.json – массив до 200 объектов с полями id, status, budget_limit_day, budget_limit, date_start, date_end, max_price.
