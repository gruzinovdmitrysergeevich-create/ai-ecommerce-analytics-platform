# Admin

## GET /api/admin/dashboard/

****  
*operationId: `admin_dashboard`*


---

## GET /api/admin/users/

****  
*operationId: `admin_list_users`*

**Параметры:**

- `ids` (query) — A comma-separated list of users IDs to filter by. When provided, only users with those IDs are returned.
- `page` (query) — Defines which page should be returned.
- `search` (query) — If provided only users with id or username or first_name that match the query will be returned.
- `size` (query) — Defines how many users should be returned per page.
- `sorts` (query) — A comma separated string of attributes to sort by, each attribute must be prefixed with `+` for a descending sort or a `-` for an ascending sort. The accepted attribute names are: `id, is_active, name, username, date_joined, last_login`. For example `sorts=-id,-is_active` will sort the users first by descending id and then ascending is_active. A sortparameter with multiple instances of the same sort attribute will respond with the ERROR_INVALID_SORT_ATTRIBUTE error.

---

## POST /api/admin/users/

****  
*operationId: `admin_create_user`*


**Тело запроса:**

- `username`: *string* (обязательно) — 
- `name`: *string* (обязательно) — 
- `is_active`: *boolean* — Designates whether this user should be treated as active. Set this to false instead of deleting accounts.
- `is_staff`: *boolean* — Designates whether this user is an admin and has access to all workspaces and Baserow's admin areas. 
- `password`: *string* (обязательно) — 

---

## POST /api/admin/users/impersonate/

****  
*operationId: `admin_impersonate_user`*


**Тело запроса:**

- `user`: *integer* (обязательно) — 

---

## PATCH /api/admin/users/{user_id}/

****  
*operationId: `admin_edit_user`*

**Параметры:**

- `user_id` (path) — The id of the user to edit

**Тело запроса:**

- `username`: *string* — 
- `name`: *string* — 
- `is_active`: *boolean* — Designates whether this user should be treated as active. Set this to false instead of deleting accounts.
- `is_staff`: *boolean* — Designates whether this user is an admin and has access to all workspaces and Baserow's admin areas. 
- `password`: *string* — 

---

## DELETE /api/admin/users/{user_id}/

****  
*operationId: `admin_delete_user`*

**Параметры:**

- `user_id` (path) — The id of the user to delete

---

## GET /api/admin/workspaces/

****  
*operationId: `admin_list_workspaces`*

**Параметры:**

- `ids` (query) — A comma-separated list of workspaces IDs to filter by. When provided, only workspaces with those IDs are returned.
- `page` (query) — Defines which page should be returned.
- `search` (query) — If provided only workspaces with id or name that match the query will be returned.
- `size` (query) — Defines how many workspaces should be returned per page.
- `sorts` (query) — A comma separated string of attributes to sort by, each attribute must be prefixed with `+` for a descending sort or a `-` for an ascending sort. The accepted attribute names are: `id, name, application_count, created_on, row_count, storage_usage`. For example `sorts=-id,-name` will sort the workspaces first by descending id and then ascending name. A sortparameter with multiple instances of the same sort attribute will respond with the ERROR_INVALID_SORT_ATTRIBUTE error.

---

## GET /api/admin/workspaces/options/

****  
*operationId: `admin_list_workspaces_as_options`*

**Параметры:**

- `ids` (query) — A comma-separated list of workspaces IDs to filter by. When provided, only workspaces with those IDs are returned.
- `page` (query) — Defines which page should be returned.
- `search` (query) — If provided only workspaces with name that match the query will be returned.
- `size` (query) — Defines how many workspaces should be returned per page.

---

## DELETE /api/admin/workspaces/{workspace_id}/

****  
*operationId: `admin_delete_workspace`*

**Параметры:**

- `workspace_id` (path) — The id of the workspace to delete

---

## GET /api/licenses/

****  
*operationId: `admin_licenses`*


---

## POST /api/licenses/

****  
*operationId: `admin_register_license`*


**Тело запроса:**

- `license`: *string* (обязательно) — The license that you want to register.

---

## GET /api/licenses/{id}/

****  
*operationId: `admin_get_license`*

**Параметры:**

- `id` (path) — The internal identifier of the license.

---

## DELETE /api/licenses/{id}/

****  
*operationId: `admin_remove_license`*

**Параметры:**

- `id` (path) — The internal identifier of the license, this is `id` and not `license_id`.

---

## GET /api/licenses/{id}/check/

****  
*operationId: `admin_license_check`*

**Параметры:**

- `id` (path) — The internal identifier of the license, this is `id` and not `license_id`.

---

## POST /api/licenses/{id}/fill-seats/

****  
*operationId: `admin_fill_remaining_seats_of_license`*

**Параметры:**

- `id` (path) — The internal identifier of the license, this is `id` and not `license_id`.

---

## GET /api/licenses/{id}/lookup-users/

****  
*operationId: `admin_license_lookup_users`*

**Параметры:**

- `id` (path) — The internal identifier of the license, this is `id` and not `license_id`.
- `page` (query) — Defines which page of users should be returned.
- `search` (query) — If provided, only users where the name or email contains the value are returned.
- `size` (query) — Defines how many users should be returned per page.

---

## POST /api/licenses/{id}/remove-all-users/

****  
*operationId: `admin_remove_all_users_from_license`*

**Параметры:**

- `id` (path) — The internal identifier of the license, this is `id` and not `license_id`.

---

## POST /api/licenses/{id}/{user_id}/

****  
*operationId: `admin_add_user_to_license`*

**Параметры:**

- `id` (path) — The internal identifier of the license, this is `id` and not `license_id`.
- `user_id` (path) — The ID of the user that must be added to the license.

---

## DELETE /api/licenses/{id}/{user_id}/

****  
*operationId: `admin_remove_user_from_license`*

**Параметры:**

- `id` (path) — The internal identifier of the license, this is `id` and not `license_id`.
- `user_id` (path) — The ID of the user that must be removed from the license.

---
