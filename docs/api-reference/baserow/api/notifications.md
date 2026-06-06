# Notifications

## GET /api/notifications/{workspace_id}/

****  
*operationId: `list_workspace_notifications`*

**Параметры:**

- `limit` (query) — Defines how many notifications should be returned.
- `offset` (query) — Defines the offset of the notifications that should be returned.
- `workspace_id` (path) — The workspace id that the notifications belong to.

---

## DELETE /api/notifications/{workspace_id}/

****  
*operationId: `clear_workspace_notifications`*

**Параметры:**

- `workspace_id` (path) — The workspace the notifications are in.

---

## POST /api/notifications/{workspace_id}/mark-all-as-read/

****  
*operationId: `mark_all_workspace_notifications_as_read`*

**Параметры:**

- `workspace_id` (path) — The workspace the notifications are in.

---

## PATCH /api/notifications/{workspace_id}/{notification_id}/

****  
*operationId: `mark_notification_as_read`*

**Параметры:**

- `notification_id` (path) — The notification id to update.
- `workspace_id` (path) — The workspace the notification is in.

---
