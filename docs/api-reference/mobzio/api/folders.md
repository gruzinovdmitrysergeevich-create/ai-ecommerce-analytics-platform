
Управление папками
Папки используются для группировки ссылок (по проектам, каналам и т.д.).

Получение списка папок
GET /folders

Возвращает массив папок с их ID, названиями и типами.

Создание папки
POST /addfolder

Параметры:

name (обязательно) – название папки.

type (обязательно) – тип папки. Доступные значения:
instagram, whatsapp, vk, telegram, custom, facebook, twitter, snapchat, tiktok, pinterest, facebookmessenger, yandexmusic, applemusic, youtubemusic, soundcloud, wildberries, ozon, lamoda, yamarket, kazanexpress, rozetka, etsy, yandexeda, uzum, avito, kaspi, letual, megamarket, vkvideo, goldapple, detmir, leroymerlin, youtube, aliexpress, ozon_new, emall, dzen, teez, litres, twitch, hh, likee, wibes, samokat, browser, delivioby, max.

description – описание папки (опционально).

Пример ответа:

json
{
  "status": "success",
  "result": { "folder_id": 123 }
}
Редактирование папки
POST /editfolder

Параметры:

folder_id (обязательно)

name (обязательно) – новое название.

description – новое описание.

Удаление папки
POST /deletefolder

Параметр:

folder_id (обязательно)

Внимание: удаление папки не удаляет ссылки, они просто теряют привязку.
