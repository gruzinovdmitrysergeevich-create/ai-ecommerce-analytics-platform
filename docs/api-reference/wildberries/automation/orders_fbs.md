# Сборочные задания FBS

## `GET /api/v3/orders/new`

**Назначение:** список новых сборочных заданий.  
**Ответ:** `orders[].id`, `nmId`, `article`, `createdAt`, `requiredMeta`.

---

## `POST /api/v3/orders/status`

**Назначение:** получить статусы заданий по ID.  
**Тело:** `{"orders": [123, 456]}`.  
**Ответ:** `supplierStatus` (`new`, `confirm`, `complete`, `cancel`), `wbStatus`.

---

## `PATCH /api/v3/orders/{orderId}/cancel`

**Назначение:** отменить сборочное задание.  
**Статус после:** `cancel`.

---

## `POST /api/v3/orders/stickers`

**Назначение:** получить стикеры для заданий (SVG, PNG, ZPL).  
**Параметры:** `type`, `width`, `height`.  
**Тело:** `{"orders": [id1, id2]}` (до 100).
