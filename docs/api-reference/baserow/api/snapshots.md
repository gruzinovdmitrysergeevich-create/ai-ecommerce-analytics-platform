# Snapshots

## GET /api/snapshots/application/{application_id}/

****  
*operationId: `list_snapshots`*

**Параметры:**

- `application_id` (path) — Application ID for which to list snapshots.

---

## POST /api/snapshots/application/{application_id}/

****  
*operationId: `create_snapshot`*

**Параметры:**

- `application_id` (path) — Application ID for which to list snapshots.

**Тело запроса:**

- `id`: *integer* (обязательно) — 
- `name`: *string* (обязательно) — 
- `snapshot_from_application`: *integer* (обязательно) — 
- `created_at`: *string* (обязательно) — 
- `created_by`: ** (обязательно) — 

---

## DELETE /api/snapshots/{snapshot_id}/

****  
*operationId: `delete_snapshot`*

**Параметры:**

- `snapshot_id` (path) — Id of the snapshot to delete.

---

## POST /api/snapshots/{snapshot_id}/restore/

****  
*operationId: `restore_snapshot`*

**Параметры:**

- `snapshot_id` (path) — Id of the snapshot to restore.

---
