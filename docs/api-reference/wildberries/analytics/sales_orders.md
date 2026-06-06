# Продажи и заказы (FBS)

## `GET /api/v1/supplier/sales`

**Назначение:** информация о продажах и возвратах.  
**Особенности:** данные обновляются раз в 30 минут, хранятся 90 дней.  
**Параметры:** `dateFrom` (обязательно), `flag` (0/1).  
**Поля ответа:** `srid`, `nmId`, `finishedPrice`, `forPay`, `saleID` (S* — продажа, R* — возврат).  

**Параметры для мета-таблицы:**  
- `pagination_type`: `dateFrom` (последовательная подгрузка по `lastChangeDate`)  
- `max_depth_days`: 90  
- `batch_size`: ~80000  
- `is_async`: `false`

---

## `GET /api/v1/supplier/orders`

**Назначение:** информация о заказах (сборочных заданиях).  
**Параметры:** `dateFrom`, `flag`.  
**Поля ответа:** `srid`, `nmId`, `isCancel`, `cancelDate`.  

**Параметры для мета-таблицы:**  
- `pagination_type`: `dateFrom`  
- `max_depth_days`: 90  
- `batch_size`: ~80000  
- `is_async`: `false`
