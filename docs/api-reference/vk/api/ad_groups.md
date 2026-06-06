
Группы объявлений (AdGroups)
Ресурс: /api/v2/ad_groups

Группа определяет таргетинги, бюджет и ставки. Входит в состав кампании.

Получение списка
GET /api/v2/ad_groups.json

Фильтры: _ad_plan_id, _status, _last_updated__gt.

Создание
POST /api/v2/ad_groups.json

json
{
  "name": "Группа",
  "ad_plan_id": 123,
  "package_id": 83,
  "status": "active",
  "budget_limit_day": "500.00",
  "max_price": "120.00",
  "targetings": {
    "age": {"age_list": [18,25,35]},
    "sex": ["male"],
    "regions": [188],
    "pads": [5206]
  }
}
package_id – обязателен (формат объявлений).

Таргетинги (основные)
age – список возрастов (0 – возраст не определён).

sex – ["male", "female"].

regions – ID регионов (можно отрицательные для исключения).

pads – ID площадок.

interests, interests_soc_dem, interests_stable – ID интересов.

fulltime – дни и часы показа.

mobile_operation_systems, mobile_operators, mobile_types, mobile_vendors.

segments – ID аудиторных сегментов.

geo – общий объект с regions или local_geo.

Редактирование
POST /api/v2/ad_groups/{id}.json

Массовое действие
POST /api/v2/ad_groups/mass_action.json – до 200 групп.

Удаление
DELETE /api/v2/ad_groups/{id}.json
