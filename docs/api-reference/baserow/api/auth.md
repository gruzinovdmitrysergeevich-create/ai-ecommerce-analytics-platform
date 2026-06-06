# Auth

## GET /api/admin/auth-provider/

****  
*operationId: `list_auth_providers`*


---

## POST /api/admin/auth-provider/

****  
*operationId: `create_auth_provider`*


---

## GET /api/admin/auth-provider/{auth_provider_id}/

****  
*operationId: `get_auth_provider`*

**Параметры:**

- `auth_provider_id` (path) — The authentication provider id to fetch.

---

## PATCH /api/admin/auth-provider/{auth_provider_id}/

****  
*operationId: `update_auth_provider`*

**Параметры:**

- `auth_provider_id` (path) — The authentication provider id to update.

---

## DELETE /api/admin/auth-provider/{auth_provider_id}/

****  
*operationId: `delete_auth_provider`*

**Параметры:**

- `auth_provider_id` (path) — The authentication provider id to delete.

---

## GET /api/auth-provider/login-options/

****  
*operationId: `list_auth_providers_login_options`*


---

## GET /api/sso/oauth2/callback/{provider_id}/

****  
*operationId: `oauth_provider_login_callback`*

**Параметры:**

- `code` (query) — The code returned by the IDP.
- `provider_id` (path) — The id of the provider for which to process the callback.

---

## GET /api/sso/oauth2/login/{provider_id}/

****  
*operationId: `oauth_provider_login_redirect`*

**Параметры:**

- `original` (query) — The relative part of URL that the user wanted to access.
- `provider_id` (path) — The id of the provider for redirect.
- `workspace_invitation_token` (query) — The invitation token sent to the user to join a specific workspace.

---

## POST /api/sso/saml/acs/

****  
*operationId: `auth_provider_saml_acs_url`*


**Тело запроса:**

- `SAMLResponse`: *string* (обязательно) — The encoded SAML response from the IdP.
- `RelayState`: *string* (обязательно) — The frontend URL where redirect the authenticated user.

---

## GET /api/sso/saml/login-url/

****  
*operationId: `auth_provider_login_url`*

**Параметры:**

- `email` (query) — The email address of the user that want to sign in using SAML.
- `language` (query) — An ISO 639 language code (with optional variant) selected by the user. Ex: en-GB.
- `original` (query) — The url to which the user should be redirected after a successful login.
- `workspace_invitation_token` (query) — If provided and valid, the user accepts the workspace invitation and will have access to the workspace after login or signing up.

---

## GET /api/sso/saml/login/

****  
*operationId: `auth_provider_saml_sp_login`*

**Параметры:**

- `email` (query) — The email address of the user that want to sign in using SAML.
- `language` (query) — An ISO 639 language code (with optional variant) selected by the user. Ex: en-GB.
- `original` (query) — The url to which the user should be redirected after a successful login or sign up.
- `workspace_invitation_token` (query) — If provided and valid, the user accepts the workspace invitation and will have access to the workspace after login or signing up.

---

## GET /api/two-factor-auth/configuration/

****  
*operationId: `two_factor_auth_configuration`*


---

## POST /api/two-factor-auth/configuration/

****  
*operationId: `configure_two_factor_auth`*


**Тело запроса:**


---

## POST /api/two-factor-auth/disable/

****  
*operationId: `disable_two_factor_auth`*


**Тело запроса:**

- `password`: *string* (обязательно) — 

---

## POST /api/two-factor-auth/verify/

****  
*operationId: `verify_totp_auth`*


**Тело запроса:**

- `email`: *string* (обязательно) — 
- `code`: *string* — 
- `backup_code`: *string* — 

---
