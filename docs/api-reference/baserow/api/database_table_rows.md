# Database table rows

## GET /api/database/rows/names/

****  
*operationId: `list_database_table_row_names`*

**Параметры:**

- `table__{id}` (query) — A list of comma separated row ids to query from the table with id {id}. For example, if you want the name of row `42` and `43` from table `28` this parameter will be `table__28=42,43`. You can specify multiple rows for different tables but every tables must be in the same database. You need at least read permission on all specified tables.

---

## GET /api/database/rows/table/{table_id}/

****  
*operationId: `list_database_table_rows`*

**Параметры:**

- `exclude` (query) — All the fields are included in the response by default. You can select a subset of fields by providing the exclude query parameter. If you for example provide the following GET parameter `exclude=field_1,field_2` then the fields with id `1` and id `2` are going to be excluded from the selection and response. If the `user_field_names` parameter is provided then instead exclude should be a comma separated list of the actual field names. For field names with commas you should surround the name with quotes like so: `exclude=My Field,"Field With , "`. A backslash can be used to escape field names which contain double quotes like so: `exclude=My Field,Field with \"`.
- `filter__{field}__{filter}` (query) — The rows can optionally be filtered by the same view filters available for the views. Multiple filters can be provided if they follow the same format. The field and filter variable indicate how to filter and the value indicates where to filter on.

For example if you provide the following GET parameter `filter__field_1__equal=test` then only rows where the value of field_1 is equal to test are going to be returned.

The following filters are available: equal, not_equal, filename_contains, files_lower_than, has_file_type, contains, contains_not, contains_word, doesnt_contain_word, length_is_lower_than, higher_than, higher_than_or_equal, lower_than, lower_than_or_equal, is_even_and_whole, date_equal, date_before, date_before_or_equal, date_after_days_ago, date_after, date_after_or_equal, date_not_equal, date_equals_today, date_before_today, date_after_today, date_within_days, date_within_weeks, date_within_months, date_equals_days_ago, date_equals_months_ago, date_equals_years_ago, date_equals_week, date_equals_month, date_equals_day_of_month, date_equals_year, date_is, date_is_not, date_is_before, date_is_on_or_before, date_is_after, date_is_on_or_after, date_is_within, single_select_equal, single_select_not_equal, single_select_is_any_of, single_select_is_none_of, link_row_has, link_row_has_not, link_row_contains, link_row_not_contains, boolean, empty, not_empty, multiple_select_has, multiple_select_has_not, multiple_collaborators_has, multiple_collaborators_has_not, user_is, user_is_not, has_value_equal, has_not_value_equal, has_value_contains, has_not_value_contains, has_value_contains_word, has_not_value_contains_word, has_value_length_is_lower_than, has_all_values_equal, has_empty_value, has_not_empty_value, has_any_select_option_equal, has_none_select_option_equal, has_value_lower, has_value_lower_or_equal, has_value_higher, has_value_higher_or_equal, has_not_value_higher_or_equal, has_not_value_higher, has_not_value_lower_or_equal, has_not_value_lower, has_date_equal, has_not_date_equal, has_date_before, has_not_date_before, has_date_on_or_before, has_not_date_on_or_before, has_date_on_or_after, has_not_date_on_or_after, has_date_after, has_not_date_after, has_date_within, has_not_date_within.

**Please note that if the `filters` parameter is provided, this parameter will be ignored.** 


- `filter_type` (query) — `AND`: Indicates that the rows must match all the provided filters.

`OR`: Indicates that the rows only have to match one of the filters.

This works only if two or more filters are provided.

**Please note that if the `filters` parameter is provided, this parameter will be ignored.**
- `filters` (query) — A JSON serialized string containing the filter tree to apply to this view. The filter tree is a nested structure containing the filters that need to be applied. 

An example of a valid filter tree is the following:`{"filter_type": "AND", "filters": [{"field": 1, "type": "equal", "value": "test"}]}`. The `field` value must be the ID of the field to filter on, or the name of the field if `user_field_names` is true.

The following filters are available: equal, not_equal, filename_contains, files_lower_than, has_file_type, contains, contains_not, contains_word, doesnt_contain_word, length_is_lower_than, higher_than, higher_than_or_equal, lower_than, lower_than_or_equal, is_even_and_whole, date_equal, date_before, date_before_or_equal, date_after_days_ago, date_after, date_after_or_equal, date_not_equal, date_equals_today, date_before_today, date_after_today, date_within_days, date_within_weeks, date_within_months, date_equals_days_ago, date_equals_months_ago, date_equals_years_ago, date_equals_week, date_equals_month, date_equals_day_of_month, date_equals_year, date_is, date_is_not, date_is_before, date_is_on_or_before, date_is_after, date_is_on_or_after, date_is_within, single_select_equal, single_select_not_equal, single_select_is_any_of, single_select_is_none_of, link_row_has, link_row_has_not, link_row_contains, link_row_not_contains, boolean, empty, not_empty, multiple_select_has, multiple_select_has_not, multiple_collaborators_has, multiple_collaborators_has_not, user_is, user_is_not, has_value_equal, has_not_value_equal, has_value_contains, has_not_value_contains, has_value_contains_word, has_not_value_contains_word, has_value_length_is_lower_than, has_all_values_equal, has_empty_value, has_not_empty_value, has_any_select_option_equal, has_none_select_option_equal, has_value_lower, has_value_lower_or_equal, has_value_higher, has_value_higher_or_equal, has_not_value_higher_or_equal, has_not_value_higher, has_not_value_lower_or_equal, has_not_value_lower, has_date_equal, has_not_date_equal, has_date_before, has_not_date_before, has_date_on_or_before, has_not_date_on_or_before, has_date_on_or_after, has_not_date_on_or_after, has_date_after, has_not_date_after, has_date_within, has_not_date_within.

**Please note that if this parameter is provided, all other `filter__{field}__{filter}` will be ignored, as well as the `filter_type` parameter.**
- `include` (query) — All the fields are included in the response by default. You can select a subset of fields by providing the include query parameter. If you for example provide the following GET parameter `include=field_1,field_2` then only the fields withid `1` and id `2` are going to be selected and included in the response. If the `user_field_names` parameter is provided then instead include should be a comma separated list of the actual field names. For field names with commas you should surround the name with quotes like so: `include=My Field,"Field With , "`. A backslash can be used to escape field names which contain double quotes like so: `include=My Field,Field with \"`.
- `order_by` (query) — Optionally the rows can be ordered by provided field ids separated by comma. By default a field is ordered in ascending (A-Z) order, but by prepending the field with a '-' it can be ordered descending (Z-A). If the `user_field_names` parameter is provided then instead order_by should be a comma separated list of the actual field names. For field names with commas you should surround the name with quotes like so: `order_by=My Field,"Field With , "`. A backslash can be used to escape field names which contain double quotes like so: `order_by=My Field,Field with \"`.
- `page` (query) — Defines which page of rows should be returned.
- `search` (query) — If provided only rows with data that matches the search query are going to be returned.
- `search_mode` (query) — If provided, allows API consumers to determine what kind of search experience they wish to have. If the default `SearchMode.FT_WITH_COUNT` is used, then Postgres full-text search is used. If `SearchMode.COMPAT` is provided then the search term will be exactly searched for including whitespace on each cell. This is the Baserow legacy search behaviour.
- `size` (query) — Defines how many rows should be returned per page.
- `table_id` (path) — Returns the rows of the table related to the provided value.
- `user_field_names` (query) — A flag query parameter that, if provided with one of the following values: `y`, `yes`, `true`, `t`, `on`, `1`, or an empty value, will cause the returned JSON to use the user-specified field names instead of the internal Baserow field names (e.g., field_123).
- `view_id` (query) — Includes all the filters and sorts of the provided view.
- `{link_row_field}__join={target_field},{target_field2}` (query) — This parameter allows you to request a lookup of field values from a target table through existing link row fields. The parameter name has to be the name of an existing link row field, followed by `__join`. The value should be a list of field names for which we want to lookup additional values. You can provide one or multiple target fields. It is not possible to lookup a value of a link row field in the target table. If `user_field_names` parameter is set, the names of the fields should be user field names. In this case the resulting field names in the output will also be user field names. The used link row field has to be among the requested fields if using the `include` or `exclude` parameters.

---

## POST /api/database/rows/table/{table_id}/

****  
*operationId: `create_database_table_row`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `ClientUndoRedoActionGroupId` (header) — An optional header that marks the action performed by this request as having occurred in a particular action group.Then calling the undo/redo endpoint with the same ClientSessionId header, all the actions belonging to the same action group can be undone/redone together in a single API call.
- `before` (query) — If provided then the newly created row will be positioned before the row with the provided id.
- `send_webhook_events` (query) — A flag query parameter that triggers webhooks after the operation, if set to `y`, `yes`, `true`, `t`, `on`, `1`, or left empty. Defaults to `true`
- `table_id` (path) — Creates a row in the table related to the provided value.
- `user_field_names` (query) — A flag query parameter that, if provided with one of the following values: `y`, `yes`, `true`, `t`, `on`, `1`, or an empty value, will cause this endpoint to expect and return the user-specified field names instead of the internal Baserow field names (e.g., field_123).
- `view` (query) — Provide if the row is created in a view. This can result in different permission checking and default values.

**Тело запроса:**

- `field_1`: *string* — This field represents the `text` field. The number in field_1 is in a normal request or response the id of the field. If the GET parameter user_field_names is provided and its value is one of the following: `y`, `yes`, `true`, `t`, `on`, `1`, or empty, then the key will instead be the actual name of the field. 
- `field_2`: *string* — This field represents the `long_text` field. The number in field_2 is in a normal request or response the id of the field. If the GET parameter user_field_names is provided and its value is one of the following: `y`, `yes`, `true`, `t`, `on`, `1`, or empty, then the key will instead be the actual name of the field. 
- `field_3`: *string* — This field represents the `url` field. The number in field_3 is in a normal request or response the id of the field. If the GET parameter user_field_names is provided and its value is one of the following: `y`, `yes`, `true`, `t`, `on`, `1`, or empty, then the key will instead be the actual name of the field. 
- `field_4`: *string* — This field represents the `email` field. The number in field_4 is in a normal request or response the id of the field. If the GET parameter user_field_names is provided and its value is one of the following: `y`, `yes`, `true`, `t`, `on`, `1`, or empty, then the key will instead be the actual name of the field. 
- `field_5`: *string* — This field represents the `number` field. The number in field_5 is in a normal request or response the id of the field. If the GET parameter user_field_names is provided and its value is one of the following: `y`, `yes`, `true`, `t`, `on`, `1`, or empty, then the key will instead be the actual name of the field. 
- `field_6`: *integer* — This field represents the `rating` field. The number in field_6 is in a normal request or response the id of the field. If the GET parameter user_field_names is provided and its value is one of the following: `y`, `yes`, `true`, `t`, `on`, `1`, or empty, then the key will instead be the actual name of the field. 
- `field_7`: *boolean* — This field represents the `boolean` field. The number in field_7 is in a normal request or response the id of the field. If the GET parameter user_field_names is provided and its value is one of the following: `y`, `yes`, `true`, `t`, `on`, `1`, or empty, then the key will instead be the actual name of the field. 
- `field_8`: *string* — This field represents the `date` field. The number in field_8 is in a normal request or response the id of the field. If the GET parameter user_field_names is provided and its value is one of the following: `y`, `yes`, `true`, `t`, `on`, `1`, or empty, then the key will instead be the actual name of the field. 
- `field_13`: *number* — This field represents the `duration` field. The number in field_13 is in a normal request or response the id of the field. If the GET parameter user_field_names is provided and its value is one of the following: `y`, `yes`, `true`, `t`, `on`, `1`, or empty, then the key will instead be the actual name of the field. The provided value can be a string in one of the available formats or a number representing the duration in seconds. In any case, the value will be rounded to match the field's duration format.
- `field_14`: *array* — This field represents the `link_row` field. The number in field_14 is in a normal request or response the id of the field. If the GET parameter user_field_names is provided and its value is one of the following: `y`, `yes`, `true`, `t`, `on`, `1`, or empty, then the key will instead be the actual name of the field. This field accepts an `array` containing the ids or the names of the related rows. A name is the value of the primary key of the related row. This field also accepts a string with names separated by a comma or an array of row names. You can also provide a unique row Id.The response contains a list of objects containing the `id` and the primary field's `value` as a string for display purposes.
- `field_15`: *array* — This field represents the `file` field. The number in field_15 is in a normal request or response the id of the field. If the GET parameter user_field_names is provided and its value is one of the following: `y`, `yes`, `true`, `t`, `on`, `1`, or empty, then the key will instead be the actual name of the field. This field accepts an `array` containing objects with the name of the file. The response contains an `array` of more detailed objects related to the files.
- `field_16`: *integer* — Accepts one of the following option ids as integer value This field accepts an `integer` representing the chosen select option id related to the field. Available ids can be found when getting or listing the field. The response represents chosen field, but also the value and color is exposed..
- `field_17`: *array* — This field represents the `multiple_select` field. The number in field_17 is in a normal request or response the id of the field. If the GET parameter user_field_names is provided and its value is one of the following: `y`, `yes`, `true`, `t`, `on`, `1`, or empty, then the key will instead be the actual name of the field. This field accepts a list of `integer` each of which representing the chosen select option id related to the field. Available ids can be foundwhen getting or listing the field. You can also send a list of option names in which case the option are searched by name. The first one that matches is used. This field also accepts a string with names separated by a comma or an array of file names. The response represents chosen field, but also the value and color is exposed.
- `field_18`: *string* — This field represents the `phone_number` field. The number in field_18 is in a normal request or response the id of the field. If the GET parameter user_field_names is provided and its value is one of the following: `y`, `yes`, `true`, `t`, `on`, `1`, or empty, then the key will instead be the actual name of the field. 
- `field_23`: *array* — This field represents the `multiple_collaborators` field. The number in field_23 is in a normal request or response the id of the field. If the GET parameter user_field_names is provided and its value is one of the following: `y`, `yes`, `true`, `t`, `on`, `1`, or empty, then the key will instead be the actual name of the field. This field accepts a list of objects representing the chosen collaborators through the object's `id` property. The id is Baserow user id. The response objects also contains the collaborator name directly along with its id.
- `field_26`: *string* — This field represents the `password` field. The number in field_26 is in a normal request or response the id of the field. If the GET parameter user_field_names is provided and its value is one of the following: `y`, `yes`, `true`, `t`, `on`, `1`, or empty, then the key will instead be the actual name of the field. Allows setting a write only password value. Providing a string will set the password, `null` will unset it, `true` will be ignored. The response will respond with `true` is a password is set, but will never expose the password itself.
- `field_28`: *string* — This field represents the `ai` field. The number in field_28 is in a normal request or response the id of the field. If the GET parameter user_field_names is provided and its value is one of the following: `y`, `yes`, `true`, `t`, `on`, `1`, or empty, then the key will instead be the actual name of the field. Holds a value that is generated by a generative AI model using a dynamic prompt.

---

## POST /api/database/rows/table/{table_id}/batch-delete/

****  
*operationId: `batch_delete_database_table_rows`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `ClientUndoRedoActionGroupId` (header) — An optional header that marks the action performed by this request as having occurred in a particular action group.Then calling the undo/redo endpoint with the same ClientSessionId header, all the actions belonging to the same action group can be undone/redone together in a single API call.
- `send_webhook_events` (query) — A flag query parameter that triggers webhooks after the operation, if set to `y`, `yes`, `true`, `t`, `on`, `1`, or left empty. Defaults to `true`
- `table_id` (path) — Deletes the rows in the table related to the value.
- `view` (query) — Provide if the rows are deleted in a view. This can result in different permission checking and default values.

**Тело запроса:**

- `items`: *array* (обязательно) — 

---

## POST /api/database/rows/table/{table_id}/batch/

****  
*operationId: `batch_create_database_table_rows`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `ClientUndoRedoActionGroupId` (header) — An optional header that marks the action performed by this request as having occurred in a particular action group.Then calling the undo/redo endpoint with the same ClientSessionId header, all the actions belonging to the same action group can be undone/redone together in a single API call.
- `before` (query) — If provided then the newly created rows will be positioned before the row with the provided id.
- `include_metadata` (query) — if provided, this will include `metadata` key containing operation metadata information in the response. Metadata will include a list of field ids, that were changed during the operation. The list will be stored in `update_field_ids` key in `metadata` object. Also, metadata object will include `cascade_update` key with a list of rows updated in cascade, and a list of field ids that were updated in cascade update.
- `send_webhook_events` (query) — A flag query parameter that triggers webhooks after the operation, if set to `y`, `yes`, `true`, `t`, `on`, `1`, or left empty. Defaults to `true`
- `table_id` (path) — Creates the rows in the table.
- `user_field_names` (query) — A flag query parameter that, if provided with one of the following values: `y`, `yes`, `true`, `t`, `on`, `1`, or an empty value, will cause this endpoint to expect and return the user-specified field names instead of the internal Baserow field names (e.g., field_123).
- `view` (query) — Provide if the rows are created in a view. This can result in different permission checking and default values.

**Тело запроса:**

- `items`: *array* (обязательно) — 

---

## PATCH /api/database/rows/table/{table_id}/batch/

****  
*operationId: `batch_update_database_table_rows`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `ClientUndoRedoActionGroupId` (header) — An optional header that marks the action performed by this request as having occurred in a particular action group.Then calling the undo/redo endpoint with the same ClientSessionId header, all the actions belonging to the same action group can be undone/redone together in a single API call.
- `include_metadata` (query) — if provided, this will include `metadata` key containing operation metadata information in the response. Metadata will include a list of field ids, that were changed during the operation. The list will be stored in `update_field_ids` key in `metadata` object. Also, metadata object will include `cascade_update` key with a list of rows updated in cascade, and a list of field ids that were updated in cascade update.
- `send_webhook_events` (query) — A flag query parameter that triggers webhooks after the operation, if set to `y`, `yes`, `true`, `t`, `on`, `1`, or left empty. Defaults to `true`
- `table_id` (path) — Updates the rows in the table.
- `user_field_names` (query) — A flag query parameter that, if provided with one of the following values: `y`, `yes`, `true`, `t`, `on`, `1`, or an empty value, will cause this endpoint to expect and return the user-specified field names instead of the internal Baserow field names (e.g., field_123).
- `view` (query) — Provide if the rows are updated in a view. This can result in different permission checking and default values.

**Тело запроса:**

- `items`: *array* — 

---

## GET /api/database/rows/table/{table_id}/{row_id}/

****  
*operationId: `get_database_table_row`*

**Параметры:**

- `include` (query) — Optionally include row's `metadata` in the response. The `metadata` object includes extra row specific data like the 'row_comments_notification_mode' settings, if available.
- `row_id` (path) — Returns the row related the provided value.
- `table_id` (path) — Returns the row of the table related to the provided value.
- `user_field_names` (query) — A flag query parameter that, if provided with one of the following values: `y`, `yes`, `true`, `t`, `on`, `1`, or an empty value, will cause the returned JSON to use the user-specified field names instead of the internal Baserow field names (e.g., field_123).
- `view` (query) — Provide if the row if fetched in a view. This can result in different permission checking and default values.

---

## PATCH /api/database/rows/table/{table_id}/{row_id}/

****  
*operationId: `update_database_table_row`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `ClientUndoRedoActionGroupId` (header) — An optional header that marks the action performed by this request as having occurred in a particular action group.Then calling the undo/redo endpoint with the same ClientSessionId header, all the actions belonging to the same action group can be undone/redone together in a single API call.
- `row_id` (path) — Updates the row related to the value.
- `send_webhook_events` (query) — A flag query parameter that triggers webhooks after the operation, if set to `y`, `yes`, `true`, `t`, `on`, `1`, or left empty. Defaults to `true`
- `table_id` (path) — Updates the row in the table related to the value.
- `user_field_names` (query) — A flag query parameter that, if provided with one of the following values: `y`, `yes`, `true`, `t`, `on`, `1`, or an empty value, will cause this endpoint to expect and return the user-specified field names instead of the internal Baserow field names (e.g., field_123).
- `view` (query) — Provide if the row is updated in a view. This can result in different permission checking and default values.

**Тело запроса:**

- `field_1`: *string* — This field represents the `text` field. The number in field_1 is in a normal request or response the id of the field. If the GET parameter user_field_names is provided and its value is one of the following: `y`, `yes`, `true`, `t`, `on`, `1`, or empty, then the key will instead be the actual name of the field. 
- `field_2`: *string* — This field represents the `long_text` field. The number in field_2 is in a normal request or response the id of the field. If the GET parameter user_field_names is provided and its value is one of the following: `y`, `yes`, `true`, `t`, `on`, `1`, or empty, then the key will instead be the actual name of the field. 
- `field_3`: *string* — This field represents the `url` field. The number in field_3 is in a normal request or response the id of the field. If the GET parameter user_field_names is provided and its value is one of the following: `y`, `yes`, `true`, `t`, `on`, `1`, or empty, then the key will instead be the actual name of the field. 
- `field_4`: *string* — This field represents the `email` field. The number in field_4 is in a normal request or response the id of the field. If the GET parameter user_field_names is provided and its value is one of the following: `y`, `yes`, `true`, `t`, `on`, `1`, or empty, then the key will instead be the actual name of the field. 
- `field_5`: *string* — This field represents the `number` field. The number in field_5 is in a normal request or response the id of the field. If the GET parameter user_field_names is provided and its value is one of the following: `y`, `yes`, `true`, `t`, `on`, `1`, or empty, then the key will instead be the actual name of the field. 
- `field_6`: *integer* — This field represents the `rating` field. The number in field_6 is in a normal request or response the id of the field. If the GET parameter user_field_names is provided and its value is one of the following: `y`, `yes`, `true`, `t`, `on`, `1`, or empty, then the key will instead be the actual name of the field. 
- `field_7`: *boolean* — This field represents the `boolean` field. The number in field_7 is in a normal request or response the id of the field. If the GET parameter user_field_names is provided and its value is one of the following: `y`, `yes`, `true`, `t`, `on`, `1`, or empty, then the key will instead be the actual name of the field. 
- `field_8`: *string* — This field represents the `date` field. The number in field_8 is in a normal request or response the id of the field. If the GET parameter user_field_names is provided and its value is one of the following: `y`, `yes`, `true`, `t`, `on`, `1`, or empty, then the key will instead be the actual name of the field. 
- `field_13`: *number* — This field represents the `duration` field. The number in field_13 is in a normal request or response the id of the field. If the GET parameter user_field_names is provided and its value is one of the following: `y`, `yes`, `true`, `t`, `on`, `1`, or empty, then the key will instead be the actual name of the field. The provided value can be a string in one of the available formats or a number representing the duration in seconds. In any case, the value will be rounded to match the field's duration format.
- `field_14`: *array* — This field represents the `link_row` field. The number in field_14 is in a normal request or response the id of the field. If the GET parameter user_field_names is provided and its value is one of the following: `y`, `yes`, `true`, `t`, `on`, `1`, or empty, then the key will instead be the actual name of the field. This field accepts an `array` containing the ids or the names of the related rows. A name is the value of the primary key of the related row. This field also accepts a string with names separated by a comma or an array of row names. You can also provide a unique row Id.The response contains a list of objects containing the `id` and the primary field's `value` as a string for display purposes.
- `field_15`: *array* — This field represents the `file` field. The number in field_15 is in a normal request or response the id of the field. If the GET parameter user_field_names is provided and its value is one of the following: `y`, `yes`, `true`, `t`, `on`, `1`, or empty, then the key will instead be the actual name of the field. This field accepts an `array` containing objects with the name of the file. The response contains an `array` of more detailed objects related to the files.
- `field_16`: *integer* — Accepts one of the following option ids as integer value This field accepts an `integer` representing the chosen select option id related to the field. Available ids can be found when getting or listing the field. The response represents chosen field, but also the value and color is exposed..
- `field_17`: *array* — This field represents the `multiple_select` field. The number in field_17 is in a normal request or response the id of the field. If the GET parameter user_field_names is provided and its value is one of the following: `y`, `yes`, `true`, `t`, `on`, `1`, or empty, then the key will instead be the actual name of the field. This field accepts a list of `integer` each of which representing the chosen select option id related to the field. Available ids can be foundwhen getting or listing the field. You can also send a list of option names in which case the option are searched by name. The first one that matches is used. This field also accepts a string with names separated by a comma or an array of file names. The response represents chosen field, but also the value and color is exposed.
- `field_18`: *string* — This field represents the `phone_number` field. The number in field_18 is in a normal request or response the id of the field. If the GET parameter user_field_names is provided and its value is one of the following: `y`, `yes`, `true`, `t`, `on`, `1`, or empty, then the key will instead be the actual name of the field. 
- `field_23`: *array* — This field represents the `multiple_collaborators` field. The number in field_23 is in a normal request or response the id of the field. If the GET parameter user_field_names is provided and its value is one of the following: `y`, `yes`, `true`, `t`, `on`, `1`, or empty, then the key will instead be the actual name of the field. This field accepts a list of objects representing the chosen collaborators through the object's `id` property. The id is Baserow user id. The response objects also contains the collaborator name directly along with its id.
- `field_26`: *string* — This field represents the `password` field. The number in field_26 is in a normal request or response the id of the field. If the GET parameter user_field_names is provided and its value is one of the following: `y`, `yes`, `true`, `t`, `on`, `1`, or empty, then the key will instead be the actual name of the field. Allows setting a write only password value. Providing a string will set the password, `null` will unset it, `true` will be ignored. The response will respond with `true` is a password is set, but will never expose the password itself.
- `field_28`: *string* — This field represents the `ai` field. The number in field_28 is in a normal request or response the id of the field. If the GET parameter user_field_names is provided and its value is one of the following: `y`, `yes`, `true`, `t`, `on`, `1`, or empty, then the key will instead be the actual name of the field. Holds a value that is generated by a generative AI model using a dynamic prompt.

---

## DELETE /api/database/rows/table/{table_id}/{row_id}/

****  
*operationId: `delete_database_table_row`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `ClientUndoRedoActionGroupId` (header) — An optional header that marks the action performed by this request as having occurred in a particular action group.Then calling the undo/redo endpoint with the same ClientSessionId header, all the actions belonging to the same action group can be undone/redone together in a single API call.
- `row_id` (path) — Deletes the row related to the value.
- `send_webhook_events` (query) — A flag query parameter that triggers webhooks after the operation, if set to `y`, `yes`, `true`, `t`, `on`, `1`, or left empty. Defaults to `true`
- `table_id` (path) — Deletes the row in the table related to the value.
- `view` (query) — Provide if the row is deleted in a view. This can result in different permission checking and default values.

---

## GET /api/database/rows/table/{table_id}/{row_id}/adjacent/

****  
*operationId: `get_adjacent_database_table_row`*

**Параметры:**

- `previous` (query) — A flag query parameter which if provided returns theprevious row to the specified row_id. If it's not setit will return the next row.
- `row_id` (path) — Returns the row adjacent the provided value.
- `search` (query) — If provided, the adjacent row will be one that matchesthe search query.
- `search_mode` (query) — If provided, allows API consumers to determine what kind of search experience they wish to have. If the default `SearchMode.FT_WITH_COUNT` is used, then Postgres full-text search is used. If `SearchMode.COMPAT` is provided then the search term will be exactly searched for including whitespace on each cell. This is the Baserow legacy search behaviour.
- `table_id` (path) — Returns the row of the table related to the provided value.
- `user_field_names` (query) — A flag query parameter that, if provided with one of the following values: `y`, `yes`, `true`, `t`, `on`, `1`, or an empty value, will cause the returned JSON to use the user-specified field names instead of the internal Baserow field names (e.g., field_123).
- `view_id` (query) — Applies the filters and sorts of the provided view.

---

## GET /api/database/rows/table/{table_id}/{row_id}/history/

****  
*operationId: `get_database_table_row_history`*

**Параметры:**

- `limit` (query) — The maximum number of row change history entries to return.
- `offset` (query) — The offset of the row change history entries to return.
- `row_id` (path) — The id of the row to fetch the change history from.
- `table_id` (path) — The id of the table to fetch the row change history from.

---

## PATCH /api/database/rows/table/{table_id}/{row_id}/move/

****  
*operationId: `move_database_table_row`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `ClientUndoRedoActionGroupId` (header) — An optional header that marks the action performed by this request as having occurred in a particular action group.Then calling the undo/redo endpoint with the same ClientSessionId header, all the actions belonging to the same action group can be undone/redone together in a single API call.
- `before_id` (query) — Moves the row related to the given `row_id` before the row related to the provided value. If not provided, then the row will be moved to the end.
- `row_id` (path) — Moves the row related to the value.
- `send_webhook_events` (query) — A flag query parameter that triggers webhooks after the operation, if set to `y`, `yes`, `true`, `t`, `on`, `1`, or left empty. Defaults to `true`
- `table_id` (path) — Moves the row in the table related to the value.
- `user_field_names` (query) — A flag query parameter that, if provided with one of the following values: `y`, `yes`, `true`, `t`, `on`, `1`, or an empty value, will cause the returned JSON to use the user-specified field names instead of the internal Baserow field names (e.g., field_123).

---

## PATCH /api/row_comments/{table_id}/comment/{comment_id}/

****  
*operationId: `update_row_comment`*

**Параметры:**

- `comment_id` (path) — The row comment to update.
- `table_id` (path) — The table the row is in.
- `view` (query) — Optionally provide a view id. If the user doesn't have table-level permissions, the system will check if the user has view-level permissions as a fallback.

---

## DELETE /api/row_comments/{table_id}/comment/{comment_id}/

****  
*operationId: `delete_row_comment`*

**Параметры:**

- `comment_id` (path) — The row comment to delete.
- `table_id` (path) — The table the row is in.
- `view` (query) — Optionally provide a view id. If the user doesn't have table-level permissions, the system will check if the user has view-level permissions as a fallback.

---

## GET /api/row_comments/{table_id}/{row_id}/

****  
*operationId: `get_row_comments`*

**Параметры:**

- `limit` (query) — Defines how many rows should be returned.
- `offset` (query) — Can only be used in combination with the `limit` parameter and defines from which offset the rows should be returned.
- `page` (query) — Defines which page of rows should be returned. Either the `page` or `limit` can be provided, not both.
- `row_id` (path) — The row to get row comments for.
- `size` (query) — Can only be used in combination with the `page` parameter and defines how many rows should be returned.
- `table_id` (path) — The table the row is in.
- `view` (query) — Optionally provide a view id. If the user doesn't have table-level permissions, the system will check if the user has view-level permissions as a fallback.

---

## POST /api/row_comments/{table_id}/{row_id}/

****  
*operationId: `create_row_comment`*

**Параметры:**

- `row_id` (path) — The row to create a comment for.
- `table_id` (path) — The table to find the row to comment on in.
- `view` (query) — Optionally provide a view id. If the user doesn't have table-level permissions, the system will check if the user has view-level permissions as a fallback.

**Тело запроса:**

- `message`: ** (обязательно) — The rich text comment content.

---

## PUT /api/row_comments/{table_id}/{row_id}/notification-mode/

****  
*operationId: `update_row_comment_notification_mode`*

**Параметры:**

- `row_id` (path) — The row on which to manage the comment subscription.
- `table_id` (path) — The table id where the row is in.
- `view` (query) — Optionally provide a view id. If the user doesn't have table-level permissions, the system will check if the user has view-level permissions as a fallback.

**Тело запроса:**

- `mode`: ** (обязательно) — The mode to use to receive notifications for new comments on a table row.

* `all` - all
* `mentions` - mentions

---
