
Лид-формы и опросы
Лид-формы (Lead Ads)
GET /api/v1/lead_ads/lead_forms.json – список форм.

POST /api/v1/lead_ads/lead_forms.json – создание (название, контактные поля, страницы вопросов, соглашение).

GET/POST /api/v1/lead_ads/lead_forms/{id}.json

POST /api/v1/lead_ads/lead_forms/archive / unarchive – архивация/восстановление.

GET /api/v1/lead_ads/lead_forms/{id}/leads.csv – экспорт лидов.

GET /api/v1/lead_ads/leads.json – список лидов.

POST /api/v1/lead_ads/upload_image/{role} – загрузка логотипа/обложки.

Опросы (Surveys)
Аналогичные эндпоинты с префиксом /api/v1/lead_ads/survey_forms:

GET/POST /survey_forms.json

GET/POST /survey_forms/{id}.json

archive / unarchive

GET .../respondents.xlsx – экспорт ответов.

GET /api/v1/lead_ads/respondents.json
