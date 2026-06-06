
Управление ссылками
Создание, редактирование и получение информации о сокращённых ссылках.

Создание ссылки
POST /addlink

Параметры:

Поле	Обязательное	Описание
shortcode	Да	Желаемый короткий идентификатор (например, mylink).
type	Да	Тип ссылки: custom (обычная) или wildberries (для WB).
agree	Да	Всегда 2 (подтверждение условий).
wildberries	Для type=wildberries	Полная ссылка WB для сокращения.
url_ios	Нет	Отдельная ссылка для iOS.
url_android	Нет	Отдельная ссылка для Android.
folder_id	Нет	ID папки для привязки.
artikuls	Нет	Доп. артикулы WB через запятую (только для wildberries).
urlnote	Нет	Описание ссылки.
Пример запроса:

http
POST /addlink
Authorization: ваш_ключ
Content-Type: application/x-www-form-urlencoded

shortcode=test123&type=custom&agree=2&wildberries=https://www.wildberries.ru/catalog/123456/detail.aspx
Пример ответа:

json
{
  "status": "success",
  "result": "created",
  "message": "https://atlantm.mobz.link/test123",
  "info": { "link_id": 10551 }
}
Редактирование ссылки
POST /editlink

Обязательные параметры:

shortcode – существующий короткий код (можно с доменом или без).

Изменяемые поля (зависят от типа):

some_url – новая целевая ссылка (для всех типов, кроме custom).

urlnote – новое описание.

url_ios, url_android – новые OS‑специфичные ссылки.

folder_id – новый ID папки.

Пример ответа:

json
{
  "status": "success",
  "result": "updated",
  "message": "https://atlantm.mobz.link/test123",
  "info": { "link_id": 10551 }
}
Получение всех ссылок
GET /mylinks

Параметры:

stats=1 – добавить статистику по каждой ссылке (today, yesterday, all).

Пример ответа:

json
{
  "status": "success",
  "result": [],
  "message": [
    {
      "link_id": "10522",
      "link": "atlantm.mobz.link/h69z",
      "shortcode": "h69z",
      "description": "",
      "original_link": "https://...",
      "stats": { "today": "0", "yesterday": "0", "all": "0" }
    }
  ]
}
Получение одной ссылки
GET /onelink

Параметры:

link_id (обязательно)

stats=1 – добавить статистику

clean=1 – только уникальные клики

Ответ аналогичен элементу из mylinks.
