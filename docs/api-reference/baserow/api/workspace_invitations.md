# Workspace invitations

## GET /api/workspaces/invitations/token/{token}/

****  
*operationId: `get_workspace_invitation_by_token`*

**Параметры:**

- `token` (path) — Returns the workspace invitation related to the provided token.

---

## GET /api/workspaces/invitations/workspace/{workspace_id}/

****  
*operationId: `list_workspace_invitations`*

**Параметры:**

- `workspace_id` (path) — Returns only invitations that are in the workspace related to the provided value.

---

## POST /api/workspaces/invitations/workspace/{workspace_id}/

****  
*operationId: `create_workspace_invitation`*

**Параметры:**

- `workspace_id` (path) — Creates a workspace invitation to the workspace related to the provided value.

**Тело запроса:**

- `email`: *string* (обязательно) — The email address of the user that the invitation is meant for. Only a user with that email address can accept it.
- `permissions`: *string* — The permissions that the user is going to get within the workspace after accepting the invitation.
- `message`: *string* — An optional message that the invitor can provide. This will be visible to the receiver of the invitation.
- `base_url`: *string* (обязательно) — The base URL where the user can publicly accept his invitation.The accept token is going to be appended to the base_url (base_url '/token').

---

## GET /api/workspaces/invitations/{workspace_invitation_id}/

****  
*operationId: `get_workspace_invitation`*

**Параметры:**

- `workspace_invitation_id` (path) — Returns the workspace invitation related to the provided value.

---

## PATCH /api/workspaces/invitations/{workspace_invitation_id}/

****  
*operationId: `update_workspace_invitation`*

**Параметры:**

- `workspace_invitation_id` (path) — Updates the workspace invitation related to the provided value.

**Тело запроса:**

- `permissions`: *string* — The permissions that the user is going to get within the workspace after accepting the invitation.

---

## DELETE /api/workspaces/invitations/{workspace_invitation_id}/

****  
*operationId: `delete_workspace_invitation`*

**Параметры:**

- `workspace_invitation_id` (path) — Deletes the workspace invitation related to the provided value.

---

## POST /api/workspaces/invitations/{workspace_invitation_id}/accept/

****  
*operationId: `accept_workspace_invitation`*

**Параметры:**

- `workspace_invitation_id` (path) — Accepts the workspace invitation related to the provided value.

---

## POST /api/workspaces/invitations/{workspace_invitation_id}/reject/

****  
*operationId: `reject_workspace_invitation`*

**Параметры:**

- `workspace_invitation_id` (path) — Rejects the workspace invitation related to the provided value.

---
