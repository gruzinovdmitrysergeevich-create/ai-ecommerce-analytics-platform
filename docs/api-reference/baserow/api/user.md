# User

## POST /api/user/

****  
*operationId: `create_user`*


**Тело запроса:**

- `name`: *string* (обязательно) — 
- `email`: *string* (обязательно) — The email address is also going to be the username.
- `password`: *string* (обязательно) — 
- `language`: *string* — An ISO 639 language code (with optional variant) selected by the user. Ex: en-GB.
- `authenticate`: *boolean* — Indicates whether an authentication JWT should be generated and be included in the response.
- `workspace_invitation_token`: *string* — If provided and valid, the user accepts the workspace invitation and will have access to the workspace after signing up.
- `template_id`: *integer* — The id of the template that must be installed after creating the account. This only works if the `workspace_invitation_token` param is not provided.
- `captcha_token`: *string* — The captcha response token, required when captcha is enabled.

---

## PATCH /api/user/account/

****  
*operationId: `update_account`*


**Тело запроса:**

- `first_name`: *string* — 
- `language`: *string* — An ISO 639 language code (with optional variant) selected by the user. Ex: en-GB.
- `email_notification_frequency`: ** — The maximum frequency at which the user wants to receive email notifications.

* `instant` - instant
* `daily` - daily
* `weekly` - weekly
* `never` - never
- `completed_onboarding`: *boolean* — Indicates whether the user has completed the onboarding.
- `completed_guided_tours`: *array* — Indicates which guided tour types have been completed.

---

## POST /api/user/change-email/

****  
*operationId: `change_email`*


**Тело запроса:**

- `token`: *string* (обязательно) — The confirmation token.

---

## POST /api/user/change-password/

****  
*operationId: `change_password`*


**Тело запроса:**

- `old_password`: *string* (обязательно) — 
- `new_password`: *string* (обязательно) — 

---

## GET /api/user/dashboard/

****  
*operationId: `dashboard`*


---

## PATCH /api/user/redo/

****  
*operationId: `redo`*

**Параметры:**

- `ClientSessionId` (header) — The particular client session to redo actions for. The actions must have been performed with this same header set with the same value for them to be redoable by this endpoint.

**Тело запроса:**

- `scopes`: ** — A JSON object with keys and values representing the various action scopes to include when undoing or redoing. Every action in Baserow will be associated with a action scope, when undoing/redoing only actions which match any of the provided scope key:value pairs will included when this endpoint picks the next action to undo/redo. If no scopes are provided then all actions performed in the client session will be included when undoing/redoing.

---

## POST /api/user/reset-password/

****  
*operationId: `reset_password`*


**Тело запроса:**

- `token`: *string* (обязательно) — 
- `password`: *string* (обязательно) — 

---

## POST /api/user/schedule-account-deletion/

****  
*operationId: `schedule_account_deletion`*


---

## POST /api/user/send-change-email-confirmation/

****  
*operationId: `send_change_email_confirmation`*


**Тело запроса:**

- `new_email`: *string* (обязательно) — The new email address to change to.
- `password`: *string* (обязательно) — The current password of the user for verification.
- `base_url`: *string* (обязательно) — The base URL where the user can confirm the email change. The confirmation token is going to be appended to the base_url (base_url '/token').

---

## POST /api/user/send-reset-password-email/

****  
*operationId: `send_password_reset_email`*


**Тело запроса:**

- `email`: *string* (обязательно) — The email address of the user that has requested a password reset.
- `base_url`: *string* (обязательно) — The base URL where the user can reset his password. The reset token is going to be appended to the base_url (base_url '/token').

---

## POST /api/user/send-verify-email/

****  
*operationId: `send_verify_email`*


---

## POST /api/user/token-auth/

****  
*operationId: `token_auth`*


**Тело запроса:**

- `email`: *string* — 
- `username`: *string* — Deprecated. Use `email` instead.
- `password`: *string* (обязательно) — 

---

## POST /api/user/token-blacklist/

****  
*operationId: `token_blacklist`*


**Тело запроса:**

- `refresh`: *string* (обязательно) — 

---

## POST /api/user/token-refresh/

****  
*operationId: `token_refresh`*


**Тело запроса:**

- `access`: *string* (обязательно) — 
- `refresh_token`: *string* — 
- `token`: *string* — Deprecated. Use `refresh_token` instead.

---

## POST /api/user/token-verify/

****  
*operationId: `token_verify`*


**Тело запроса:**

- `token`: *string* — Deprecated. Use `refresh_token` instead.
- `refresh_token`: *string* (обязательно) — 

---

## PATCH /api/user/undo/

****  
*operationId: `undo`*

**Параметры:**

- `ClientSessionId` (header) — The particular client session to undo actions for. The actions must have been performed with this same header set with the same value for them to be undoable by this endpoint.

**Тело запроса:**

- `scopes`: ** — A JSON object with keys and values representing the various action scopes to include when undoing or redoing. Every action in Baserow will be associated with a action scope, when undoing/redoing only actions which match any of the provided scope key:value pairs will included when this endpoint picks the next action to undo/redo. If no scopes are provided then all actions performed in the client session will be included when undoing/redoing.

---

## POST /api/user/verify-email/

****  
*operationId: `verify_email`*


**Тело запроса:**

- `token`: *string* (обязательно) — 

---
