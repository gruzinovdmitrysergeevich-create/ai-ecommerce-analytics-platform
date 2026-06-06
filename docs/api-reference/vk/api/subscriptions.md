
Подписки на уведомления (Webhooks)
Позволяют получать уведомления об изменениях объектов в реальном времени.

Управление
GET /api/v3/subscription.json – список подписок.

POST /api/v3/subscription.json

json
{
  "resource": "BANNER",   // BANNER, AD_GROUP, LEAD, LEAD_FORM, SEGMENT, USER
  "callback_url": "https://your-server.com/callback"
}
DELETE /api/v3/subscription/{id}.json

Формат уведомления
На callback_url приходит POST с JSON:

json
{
  "id": "uuid",
  "resource_id": 123,
  "resource": "LEAD",
  "created": "2026-04-14 12:00:00",
  "data": { ... }   // объект ресурса
}
