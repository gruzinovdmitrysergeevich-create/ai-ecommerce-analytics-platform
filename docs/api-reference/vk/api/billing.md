
Финансы (Billing)
Группы транзакций
GET /api/v2/billing/transaction_groups.json – история пополнений и списаний, сгруппированная по месяцам.

Поля ответа: amount, date, description, type (deposit / charge), receipt (ссылка на чек).

Переводы между агентством и клиентом
POST /api/v2/billing/transactions/{to|from}/{user_id}.json

Тело запроса:

json
{"amount": "1000.00"}
Ответ содержит новые балансы агентства и клиента.
