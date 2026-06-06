
Аудитории и сегменты
Управление аудиторными сегментами, списками пользователей, счётчиками Top@Mail.ru и другими источниками данных для таргетинга.

Сегменты (Segments)
GET /api/v2/remarketing/segments.json – список сегментов.

POST /api/v2/remarketing/segments.json – создание сегмента (можно сразу передать relations).

GET/POST/DELETE /api/v2/remarketing/segments/{id}.json

POST/DELETE /api/v2/remarketing/segments/{id}/relations.json – добавить/удалить источники.

Списки пользователей (Users Lists)
GET /api/v3/remarketing/users_lists.json

POST /api/v3/remarketing/users_lists.json – загрузка файла (multipart/form-data, поле file, параметры name, type).

GET/POST/DELETE /api/v3/remarketing/users_lists/{id}.json

Счётчики Top@Mail.ru
GET /api/v2/remarketing/counters.json

POST /api/v2/remarketing/counters.json – добавить существующий или создать новый.

GET/POST/DELETE /api/v2/remarketing/counters/{counter_id}.json

Цели: /api/v2/remarketing/counters/{counter_id}/goals.json

Другие источники
Локальная география: /api/v2/remarketing/local_geo

Офлайн-конверсии: /api/v2/remarketing/offline_goals

События в приложениях: /api/v2/remarketing/inapp_events

Look-alike: добавляются в сегмент с object_type: "remarketing_lookalike_audience".

Ключи доступа (Sharing Keys)
GET/POST /api/v2/sharing_keys.json

POST/DELETE /api/v2/sharing_keys/{key}.json – активация/удаление.
