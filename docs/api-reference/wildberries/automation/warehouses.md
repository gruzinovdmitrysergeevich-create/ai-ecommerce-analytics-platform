# Склады продавца (FBS)

## `GET /api/v3/warehouses`

**Назначение:** список складов продавца.  
**Ответ:** `id`, `name`, `officeId`, `cargoType`, `deliveryType`.

## `POST /api/v3/warehouses`

**Назначение:** создать склад.  
**Тело:** `{"name": "Склад", "officeId": 123}`.

## `PUT /api/v3/warehouses/{warehouseId}`

**Назначение:** обновить склад.

## `DELETE /api/v3/warehouses/{warehouseId}`

**Назначение:** удалить склад.
