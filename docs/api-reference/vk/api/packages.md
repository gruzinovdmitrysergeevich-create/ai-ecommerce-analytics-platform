
Пакеты и площадки
Пакеты (Packages)
GET /api/v2/packages.json – список доступных форматов объявлений.

Каждый пакет содержит:

id, name, description

price – базовая ставка

priced_event_type – событие оптимизации (0 – показы, 1 – клики, 7 – конверсии)

paid_event_type – событие оплаты

max_price_per_unit – макс. ставка

objective – доступные цели (reach, traffic, appinstalls…)

options – доступные таргетинги и их значения.

Площадки (Pads)
GET /api/v2/packages_pads.json – площадки, используемые в таргетингах по умолчанию.

GET /api/v2/pads_trees.json – иерархические деревья площадок (для навигации).

Прогноз охвата
POST /api/v3/projection.json – возвращает прогноз охвата аудитории в зависимости от цены.

Тело запроса:

json
{
  "package_ids": [959],
  "targetings": {
    "pads": [5206],
    "age": {"age_list": [18,25]}
  }
}
Ответ содержит гистограмму price → uniqs (охват).
