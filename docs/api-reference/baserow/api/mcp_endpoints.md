# MCP endpoints

## GET /api/mcp/endpoint/{endpoint_id}/

****  
*operationId: `get_mcp_endpoint`*

**Параметры:**

- `endpoint_id` (path) — 

---

## PATCH /api/mcp/endpoint/{endpoint_id}/

****  
*operationId: `update_mcp_endpoint`*

**Параметры:**

- `endpoint_id` (path) — 

**Тело запроса:**

- `name`: *string* — The human readable name of the MCP endpoint for the user.

---

## DELETE /api/mcp/endpoint/{endpoint_id}/

****  
*operationId: `delete_mcp_endpoint`*

**Параметры:**

- `endpoint_id` (path) — 

---

## GET /api/mcp/endpoints/

****  
*operationId: `list_mcp_endpoints`*


---

## POST /api/mcp/endpoints/

****  
*operationId: `create_mcp_endpoint`*


**Тело запроса:**

- `name`: *string* (обязательно) — The human readable name of the MCP endpoint for the user.
- `workspace_id`: *integer* (обязательно) — 

---
