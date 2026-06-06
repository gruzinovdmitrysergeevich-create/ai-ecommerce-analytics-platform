
Управление клиентами агентства
Клиенты агентства
GET /api/v2/agency/clients.json – список клиентов.

POST /api/v2/agency/clients/{client_id}.json – редактирование (access_type, user.additional_info).

DELETE /api/v2/agency/clients/{client_id}.json – вывести клиента (только при нулевом балансе).

Менеджеры и их клиенты
GET /api/v3/manager/clients.json (для менеджеров).

POST /api/v2/agency/managers/{manager_id}/clients/{client_id}.json – изменить доступ менеджера.

DELETE – удалить клиента из ведения менеджера.

Информация о пользователе
GET /api/v3/user.json – данные текущего пользователя (тип, валюта, email, регионы).

POST /api/v3/user.json – обновить настройки (язык, валюта, рассылки, ОРД).
