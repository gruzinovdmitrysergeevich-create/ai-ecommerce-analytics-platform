
Статистика и конверсии
Статистика переходов по ссылке
GET /stats

Параметры:

Параметр	Обязательный	Описание
link_id	Да	ID ссылки.
page	Нет	Номер страницы (по 100 записей).
dateFrom	Нет	Timestamp начала периода (по умолч. 1640984404).
dateTo	Нет	Timestamp конца периода.
clean	Нет	1 – только уникальные клики.
Возвращает подробную историю переходов.

Конверсии (только для Wildberries)
GET /conversions

Параметры:

link_id (обязательно)

dateFrom, dateTo – timestamp (опционально)

attribution_mode – strict_link (по умолч., только указанный link_id) или all_artikuls (по всем артикулам из ссылки, включая дополнительные)

Пример ответа:

json
{
  "status": "success",
  "result": {
    "link_id": 10551,
    "type": "wildberries",
    "attribution_mode": "all_artikuls",
    "artikuls": ["236991705"],
    "dateFrom": 1735689600,
    "dateTo": 1738281600,
    "total_clicks": 158,
    "total_orders": 19,
    "conversions_count": 11,
    "conversion_click_to_order_percent": 6.96,
    "sales_share_percent": 57.89,
    "conversions": []
  }
}
Статистика WB через API ключ WB
Если у вас подключён API ключ Wildberries, доступны методы:

GET /wbapi/sales – данные о продажах.

GET /wbapi/orders – данные о заказах.

Обязательный параметр: link_id.

Ответы содержат сырые данные от WB API.
