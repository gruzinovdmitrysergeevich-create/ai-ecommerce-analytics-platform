# Health

## GET /api/_health/celery-queue/

****  
*operationId: `celery_queue_size_check`*

**Параметры:**

- `queue` (query) — The name of the queues to check. Can be provided multiple times. Accepts either `celery` or `export`.

---

## POST /api/_health/email/

****  
*operationId: `email_tester`*


**Тело запроса:**

- `target_email`: *string* (обязательно) — 

---

## GET /api/_health/full/

****  
*operationId: `full_health_check`*


---
