# User sources

## GET /api/application/{application_id}/list-user-source-users/

****  
*operationId: `list_application_user_source_users`*

**Параметры:**

- `application_id` (path) — The application we want the users for.

---

## GET /api/application/{application_id}/user-sources/

****  
*operationId: `list_application_user_sources`*

**Параметры:**

- `application_id` (path) — Returns only the user_sources of the application related to the provided Id.

---

## POST /api/application/{application_id}/user-sources/

****  
*operationId: `create_application_user_source`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `application_id` (path) — Creates an user_source for the application related to the provided value.

**Тело запроса:**


---

## POST /api/user-source-auth-refresh/

****  
*operationId: `user_source_token_refresh`*


---

## POST /api/user-source-token-blacklist/

****  
*operationId: `user_source_token_blacklist`*


**Тело запроса:**

- `refresh`: *string* (обязательно) — 

---

## POST /api/user-source/sso/saml/acs/

****  
*operationId: `auth_provider_saml_acs_url_2`*


**Тело запроса:**

- `SAMLResponse`: *string* (обязательно) — The encoded SAML response from the IdP.
- `RelayState`: *string* (обязательно) — The frontend URL where redirect the authenticated user.

---

## PATCH /api/user-source/{user_source_id}/

****  
*operationId: `update_application_user_source`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `user_source_id` (path) — The id of the user_source

**Тело запроса:**


---

## DELETE /api/user-source/{user_source_id}/

****  
*operationId: `delete_application_user_source`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `user_source_id` (path) — The id of the user_source

---

## POST /api/user-source/{user_source_id}/force-token-auth

****  
*operationId: `user_source_force_token_auth`*

**Параметры:**

- `user_source_id` (path) — The user source to use to authenticate the user.

---

## PATCH /api/user-source/{user_source_id}/move/

****  
*operationId: `move_application_user_source`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `user_source_id` (path) — The id of the user_source to move

**Тело запроса:**

- `before_id`: *integer* — If provided, the user_source is moved before the user_source with this Id. Otherwise the user_source is placed at the end of the page.

---

## POST /api/user-source/{user_source_id}/token-auth

****  
*operationId: `user_source_token_auth`*

**Параметры:**

- `user_source_id` (path) — The id of the user_source to move

**Тело запроса:**

- `username`: *string* (обязательно) — 
- `password`: *string* (обязательно) — 
- `access`: *string* (обязательно) — 
- `refresh`: *string* (обязательно) — 

---

## GET /api/user-source/{user_source_uid}/sso/oauth2/openid_connect/callback/

****  
*operationId: `app_auth_oidc_login_callback`*

**Параметры:**

- `code` (query) — The code returned by the IDP.
- `state` (query) — The oauth state returned by the IDP.
- `user_source_uid` (path) — The uid of the user source for which to process the callback.

---

## GET /api/user-source/{user_source_uid}/sso/oauth2/openid_connect/login/

****  
*operationId: `app_auth_oidc_login_redirect`*

**Параметры:**

- `iss` (query) — The issuer of the authentication.
- `original` (query) — The URL that the user wants to access.
- `user_source_uid` (path) — The uid of the user source to use for authentication.

---

## GET /api/user-source/{user_source_uid}/sso/saml/login/

****  
*operationId: `app_auth_provider_saml_sp_login`*

**Параметры:**

- `email` (query) — The email address of the user that want to sign in using SAML.
- `original` (query) — The url to which the user should be redirected after a successful login or sign up.
- `user_source_uid` (path) — 

---
