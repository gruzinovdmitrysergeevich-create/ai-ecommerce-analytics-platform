
Мобильные приложения
Доступные приложения
GET /api/v1/mobile_app_users.json – список приложений пользователя с информацией о доступе и SkAdNetwork ID.

Данные из магазинов
GET/POST /api/v2/apple_apps/{app_id}.json

GET/POST /api/v2/google_apps/{app_id}.json

Категории событий
GET /api/v1/inapp_event_categories.json – список категорий (purchase, addToCart…).

SkAdNetwork (iOS)
POST /api/v2/apple_apps/{app_id}/sk_ad_network_ids/share.json – выдать идентификаторы агенту.

POST .../withdraw.json – забрать обратно.
