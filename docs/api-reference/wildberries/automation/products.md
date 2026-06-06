# Товары и карточки (FBS)

## `POST /content/v2/cards/upload`

**Назначение:** создание карточек товаров.  
**Тело:** массив объектов с `subjectID`, `variants` (до 100 карточек).  
**Ответ:** `task_id` для проверки статуса.

## `POST /content/v2/cards/update`

**Назначение:** редактирование карточек.  
**Тело:** массив с `nmID`, `vendorCode`, `characteristics`, `sizes`.

## `POST /content/v2/get/cards/list`

**Назначение:** список карточек товаров с пагинацией.  
**Параметры:** `settings.cursor.limit`, `filter.textSearch`.

## `GET /content/v2/object/all`

**Назначение:** список предметов (категорий) для создания карточек.
