# Метаданные FBS (маркировка)

## `GET /api/marketplace/v3/orders/meta`

**Назначение:** получить метаданные сборочных заданий (IMEI, УИН, GTIN, SGTIN, ГТД).  
**Тело:** `{"orders": [123, 456]}`.

## `PUT /api/v3/orders/{orderId}/meta/sgtin`

**Назначение:** закрепить код маркировки (до 100).  
**Тело:** `{"sgtins": ["010290...", "010460..."]}`.

## `PUT /api/v3/orders/{orderId}/meta/imei`

**Назначение:** закрепить IMEI (один).  
**Тело:** `{"imei": "123456789012345"}`.

## `PUT /api/v3/orders/{orderId}/meta/uin`

**Назначение:** закрепить УИН.  
**Тело:** `{"uin": "1234567890123456"}`.

## `DELETE /api/v3/orders/{orderId}/meta?key=sgtin`

**Назначение:** удалить метаданные по ключу.
