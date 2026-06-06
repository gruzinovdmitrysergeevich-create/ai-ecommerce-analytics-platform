# Teams

## GET /api/teams/workspace/{workspace_id}/

****  
*operationId: `workspace_list_teams`*

**Параметры:**

- `search` (query) — Search for teams by their name.
- `sorts` (query) — Sort teams by name or subjects.
- `workspace_id` (path) — Lists all teams in a given workspace.

---

## POST /api/teams/workspace/{workspace_id}/

****  
*operationId: `workspace_create_team`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `workspace_id` (path) — 

**Тело запроса:**

- `name`: *string* (обязательно) — A human friendly name for this team.
- `default_role`: *string* — The uid of the role you want to assign to the team in the given workspace. You can omit this property if you want to remove the role.
- `subjects`: *array* — An array of subject ID/type objects to be used during team create and update.

---

## GET /api/teams/{team_id}/

****  
*operationId: `get_team`*

**Параметры:**

- `team_id` (path) — Returns the team related to the provided value.

---

## PUT /api/teams/{team_id}/

****  
*operationId: `update_team`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `team_id` (path) — 

**Тело запроса:**

- `name`: *string* (обязательно) — A human friendly name for this team.
- `default_role`: *string* — The uid of the role you want to assign to the team in the given workspace. You can omit this property if you want to remove the role.
- `subjects`: *array* — An array of subject ID/type objects to be used during team create and update.

---

## DELETE /api/teams/{team_id}/

****  
*operationId: `delete_team`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `team_id` (path) — Deletes the team related to the provided value.

---

## GET /api/teams/{team_id}/subjects/

****  
*operationId: `list_team_subjects`*

**Параметры:**

- `team_id` (path) — 

---

## POST /api/teams/{team_id}/subjects/

****  
*operationId: `create_subject`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `team_id` (path) — 

**Тело запроса:**

- `id`: *integer* (обязательно) — 
- `subject_id`: *integer* — The subject's unique identifier.
- `subject_user_email`: *string* — The user subject's email address.
- `subject_type`: ** (обязательно) — The type of subject that is being invited.

* `auth.User` - auth.User

---

## GET /api/teams/{team_id}/subjects/{subject_id}/

****  
*operationId: `get_subject`*

**Параметры:**

- `subject_id` (path) — Returns the subject related to the provided value.
- `team_id` (path) — 

---

## DELETE /api/teams/{team_id}/subjects/{subject_id}/

****  
*operationId: `delete_subject`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `subject_id` (path) — The subject id to remove from the team.
- `team_id` (path) — The team id which the subject will be removed from.

---
