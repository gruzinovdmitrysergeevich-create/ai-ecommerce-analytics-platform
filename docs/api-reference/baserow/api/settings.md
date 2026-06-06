# Settings

## GET /api/settings/

****  
*operationId: `get_settings`*


---

## GET /api/settings/instance-id/

****  
*operationId: `get_instance_id`*


---

## PATCH /api/settings/update/

****  
*operationId: `update_settings`*


**Тело запроса:**

- `allow_new_signups`: *boolean* — Indicates whether new users can create a new account when signing up.
- `allow_signups_via_workspace_invitations`: *boolean* — Indicates whether invited users can create an account when signing up, even if allow_new_signups is disabled.
- `allow_reset_password`: *boolean* — Indicates whether users can request a password reset link.
- `allow_global_workspace_creation`: *boolean* — Indicates whether all users can create workspaces, or just staff.
- `account_deletion_grace_delay`: *integer* — Number of days after the last login for an account pending deletion to be deleted
- `show_admin_signup_page`: *boolean* — Indicates that there are no admin users in the database yet, so in the frontend the signup form will be shown instead of the login page.
- `track_workspace_usage`: *boolean* — Runs a job once per day which calculates per workspace row counts and file storage usage, displayed on the admin workspace page.
- `show_baserow_help_request`: *boolean* — Indicates whether the `We need your help!` message will be shown on the dashboard
- `co_branding_logo`: ** — Co-branding logo that's placed next to the Baserow logo (176x29).
- `email_verification`: ** — Controls whether user email addresses have to be verified.

* `no_verification` - no_verification
* `recommended` - recommended
* `enforced` - enforced
- `verify_import_signature`: *boolean* — Indicates whether the signature of imported files should be verified.

---
