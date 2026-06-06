# Field permissions

## GET /api/field-permissions/{field_id}/

****  
*operationId: `get_field_permissions`*

**Параметры:**

- `field_id` (path) — The ID of the field to get the permissions for.

---

## PATCH /api/field-permissions/{field_id}/

****  
*operationId: `update_field_permissions`*

**Параметры:**

- `field_id` (path) — The ID of the field to update the permissions for.

**Тело запроса:**

- `role`: ** — The role required to update the data for this field.

* `ADMIN` - Admin
* `BUILDER` - Builder
* `EDITOR` - Editor
* `NOBODY` - Nobody
- `allow_in_forms`: *boolean* — Whether to allow this field to be shown in forms. Default is False. This setting is only relevant if the role is not 'EDITOR'. 

---
