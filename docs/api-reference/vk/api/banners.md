
Объявления (Banners)
Ресурс: /api/v2/banners

Креативы, которые показываются пользователям. Принадлежат группе объявлений.

Получение списка
GET /api/v2/banners.json

Фильтры: _ad_group_id, _status, _updated__gt, _url, _textblock.

Получение одного
GET /api/v2/banners/{id}.json

Создание
Обычно создаются вместе с группой (поле banners в запросе POST /ad_groups).

Редактирование
POST /api/v2/banners/{id}.json
Важно: секции urls, textblocks, content замещаются полностью. Передавайте всю структуру.

Массовое действие
POST /api/v2/banners/mass_action.json – изменение статусов (до 200 баннеров).

Удаление
DELETE /api/v2/banners/{id}.json
