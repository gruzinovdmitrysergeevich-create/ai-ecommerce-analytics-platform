# Baserow API: автоматический onboarding

## Создание workspace
`POST /api/workspaces/` with `{"name": "..."}`

## Создание database (application)
`POST /api/applications/workspace/{workspace_id}/` with `{"type": "database", "name": "..."}`

## Создание таблицы
`POST /api/database/tables/database/{database_id}/` (can pass `data` for batch creation)

## Создание поля
`POST /api/database/fields/table/{table_id}/` (required: `name`, `type`)

## Создание database token
`POST /api/database/tokens/` with `{"name": "...", "workspace": <id>}`

## Загрузка/обновление строк
- `POST /api/database/rows/table/{table_id}/batch/`
- `PATCH /api/database/rows/table/{table_id}/{row_id}/?user_field_names=true`

## Фильтрация
`GET .../rows/table/{table_id}/?user_field_names=true&filter__field_{id}=value`
