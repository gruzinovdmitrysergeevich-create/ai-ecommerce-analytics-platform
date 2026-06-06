# Trash

## GET /api/trash/

****  
*operationId: `get_trash_structure`*


---

## PATCH /api/trash/restore/

****  
*operationId: `restore`*


**Тело запроса:**

- `trash_item_id`: *integer* — 
- `parent_trash_item_id`: *integer* — 
- `trash_item_type`: ** — 

---

## GET /api/trash/workspace/{workspace_id}/

****  
*operationId: `workspace_get_contents`*

**Параметры:**

- `application_id` (query) — Optionally filters down the trash to only items for this application in the workspace.
- `page` (query) — Selects which page of trash contents should be returned.
- `workspace_id` (path) — Returns the trash for the workspace with this id.

---

## DELETE /api/trash/workspace/{workspace_id}/

****  
*operationId: `workspace_empty_contents`*

**Параметры:**

- `application_id` (query) — Optionally filters down the trash to delete to only items for this application in the workspace.
- `workspace_id` (path) — The workspace whose trash contents to empty, including the workspace itself if it is also trashed.

---
