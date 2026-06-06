
Отчётность в ОРД
Методы для передачи данных в Единый реестр интернет-рекламы (ОРД).

Для партнёров (площадки)
GET /api/v1/ord/partner/pads.json – список площадок отчётности.

POST /api/v1/ord/partner/pads/{id}.json – обновление данных площадки и цепочки контрагентов.

GET/POST /api/v1/ord/partner/acts/{month}.json – акты за месяц.

GET/POST /api/v1/ord/partner/acts/{month}/{pad_id}.json – акты по конкретной площадке.

GET/POST /api/v1/ord/partner/subagents.json – управление контрагентами.

Важно: месяц указывается как YYYY-MM-01. Создавать/изменять акты можно только до 20-го числа текущего месяца.

Для агентств
GET /api/v2/ord/agency/acts.json – акты клиентов за месяц.

GET/POST /api/v2/ord/agency/{client_id}/acts.json – акты конкретного клиента.

GET /api/v2/ord/agency/report.json – сводный отчёт.

GET/POST /api/v2/ord/agency/status.json – статус отправки актов в ОРД.

Данные пользователя
GET/POST /api/v2/ord_user.json – ОРД-данные физического лица (имя, телефон, ИНН).
