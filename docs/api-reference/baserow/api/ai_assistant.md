# AI Assistant

## GET /assistant/chat/

****  
*operationId: `list_assistant_chats`*

**Параметры:**

- `limit` (query) — The number of results to return per page.
- `offset` (query) — The initial index from which to return the results.
- `workspace_id` (query) — The ID of the workspace.

---

## GET /assistant/chat/{chat_uuid}/cancel/

****  
*operationId: `list_assistant_chat_messages`*

**Параметры:**

- `chat_uuid` (path) — 

---

## POST /assistant/chat/{chat_uuid}/cancel/

****  
*operationId: `send_message_to_assistant_chat`*

**Параметры:**

- `chat_uuid` (path) — 

**Тело запроса:**

- `content`: *string* (обязательно) — The content of the message.
- `ui_context`: ** (обязательно) — The UI context related to what the user was looking at when the message was sent.

---

## DELETE /assistant/chat/{chat_uuid}/cancel/

****  
*operationId: `cancel_assistant_message`*

**Параметры:**

- `chat_uuid` (path) — 

---

## GET /assistant/chat/{chat_uuid}/messages/

****  
*operationId: `list_assistant_chat_messages_2`*

**Параметры:**

- `chat_uuid` (path) — 

---

## POST /assistant/chat/{chat_uuid}/messages/

****  
*operationId: `send_message_to_assistant_chat_2`*

**Параметры:**

- `chat_uuid` (path) — 

**Тело запроса:**

- `content`: *string* (обязательно) — The content of the message.
- `ui_context`: ** (обязательно) — The UI context related to what the user was looking at when the message was sent.

---

## DELETE /assistant/chat/{chat_uuid}/messages/

****  
*operationId: `cancel_assistant_message_2`*

**Параметры:**

- `chat_uuid` (path) — 

---

## PUT /assistant/messages/{message_id}/feedback/

****  
*operationId: `submit_assistant_message_feedback`*

**Параметры:**

- `message_id` (path) — 

---
