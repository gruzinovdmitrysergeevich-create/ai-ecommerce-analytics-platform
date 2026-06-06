# Database table view filters

## GET /api/database/views/filter-group/{view_filter_group_id}/

****  
*operationId: `get_database_table_view_filter_group`*

**Параметры:**

- `view_filter_group_id` (path) — The ID of the view filter group to return.

---

## PATCH /api/database/views/filter-group/{view_filter_group_id}/

****  
*operationId: `update_database_table_view_filter_group`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `ClientUndoRedoActionGroupId` (header) — An optional header that marks the action performed by this request as having occurred in a particular action group.Then calling the undo/redo endpoint with the same ClientSessionId header, all the actions belonging to the same action group can be undone/redone together in a single API call.
- `view_filter_group_id` (path) — The ID of the view filter group to update.

**Тело запроса:**

- `filter_type`: ** — Indicates whether all the rows should apply to all filters (AND) or to any filter (OR) in the group to be shown.

* `AND` - And
* `OR` - Or

---

## DELETE /api/database/views/filter-group/{view_filter_group_id}/

****  
*operationId: `delete_database_table_view_filter_group`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `ClientUndoRedoActionGroupId` (header) — An optional header that marks the action performed by this request as having occurred in a particular action group.Then calling the undo/redo endpoint with the same ClientSessionId header, all the actions belonging to the same action group can be undone/redone together in a single API call.
- `view_filter_group_id` (path) — The ID of the view filter group to delete.

---

## GET /api/database/views/filter/{view_filter_id}/

****  
*operationId: `get_database_table_view_filter`*

**Параметры:**

- `view_filter_id` (path) — The ID of the view filter to return.

---

## PATCH /api/database/views/filter/{view_filter_id}/

****  
*operationId: `update_database_table_view_filter`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `ClientUndoRedoActionGroupId` (header) — An optional header that marks the action performed by this request as having occurred in a particular action group.Then calling the undo/redo endpoint with the same ClientSessionId header, all the actions belonging to the same action group can be undone/redone together in a single API call.
- `view_filter_id` (path) — The ID of the view filter to update.

**Тело запроса:**

- `field`: *integer* — The field of which the value must be compared to the filter value.
- `type`: ** — Indicates how the field's value must be compared to the filter's value. The filter is always in this order `field` `type` `value` (example: `field_1` `contains` `Test`).

* `equal` - equal
* `not_equal` - not_equal
* `filename_contains` - filename_contains
* `files_lower_than` - files_lower_than
* `has_file_type` - has_file_type
* `contains` - contains
* `contains_not` - contains_not
* `contains_word` - contains_word
* `doesnt_contain_word` - doesnt_contain_word
* `length_is_lower_than` - length_is_lower_than
* `higher_than` - higher_than
* `higher_than_or_equal` - higher_than_or_equal
* `lower_than` - lower_than
* `lower_than_or_equal` - lower_than_or_equal
* `is_even_and_whole` - is_even_and_whole
* `date_equal` - date_equal
* `date_before` - date_before
* `date_before_or_equal` - date_before_or_equal
* `date_after_days_ago` - date_after_days_ago
* `date_after` - date_after
* `date_after_or_equal` - date_after_or_equal
* `date_not_equal` - date_not_equal
* `date_equals_today` - date_equals_today
* `date_before_today` - date_before_today
* `date_after_today` - date_after_today
* `date_within_days` - date_within_days
* `date_within_weeks` - date_within_weeks
* `date_within_months` - date_within_months
* `date_equals_days_ago` - date_equals_days_ago
* `date_equals_months_ago` - date_equals_months_ago
* `date_equals_years_ago` - date_equals_years_ago
* `date_equals_week` - date_equals_week
* `date_equals_month` - date_equals_month
* `date_equals_day_of_month` - date_equals_day_of_month
* `date_equals_year` - date_equals_year
* `date_is` - date_is
* `date_is_not` - date_is_not
* `date_is_before` - date_is_before
* `date_is_on_or_before` - date_is_on_or_before
* `date_is_after` - date_is_after
* `date_is_on_or_after` - date_is_on_or_after
* `date_is_within` - date_is_within
* `single_select_equal` - single_select_equal
* `single_select_not_equal` - single_select_not_equal
* `single_select_is_any_of` - single_select_is_any_of
* `single_select_is_none_of` - single_select_is_none_of
* `link_row_has` - link_row_has
* `link_row_has_not` - link_row_has_not
* `link_row_contains` - link_row_contains
* `link_row_not_contains` - link_row_not_contains
* `boolean` - boolean
* `empty` - empty
* `not_empty` - not_empty
* `multiple_select_has` - multiple_select_has
* `multiple_select_has_not` - multiple_select_has_not
* `multiple_collaborators_has` - multiple_collaborators_has
* `multiple_collaborators_has_not` - multiple_collaborators_has_not
* `user_is` - user_is
* `user_is_not` - user_is_not
* `has_value_equal` - has_value_equal
* `has_not_value_equal` - has_not_value_equal
* `has_value_contains` - has_value_contains
* `has_not_value_contains` - has_not_value_contains
* `has_value_contains_word` - has_value_contains_word
* `has_not_value_contains_word` - has_not_value_contains_word
* `has_value_length_is_lower_than` - has_value_length_is_lower_than
* `has_all_values_equal` - has_all_values_equal
* `has_empty_value` - has_empty_value
* `has_not_empty_value` - has_not_empty_value
* `has_any_select_option_equal` - has_any_select_option_equal
* `has_none_select_option_equal` - has_none_select_option_equal
* `has_value_lower` - has_value_lower
* `has_value_lower_or_equal` - has_value_lower_or_equal
* `has_value_higher` - has_value_higher
* `has_value_higher_or_equal` - has_value_higher_or_equal
* `has_not_value_higher_or_equal` - has_not_value_higher_or_equal
* `has_not_value_higher` - has_not_value_higher
* `has_not_value_lower_or_equal` - has_not_value_lower_or_equal
* `has_not_value_lower` - has_not_value_lower
* `has_date_equal` - has_date_equal
* `has_not_date_equal` - has_not_date_equal
* `has_date_before` - has_date_before
* `has_not_date_before` - has_not_date_before
* `has_date_on_or_before` - has_date_on_or_before
* `has_not_date_on_or_before` - has_not_date_on_or_before
* `has_date_on_or_after` - has_date_on_or_after
* `has_not_date_on_or_after` - has_not_date_on_or_after
* `has_date_after` - has_date_after
* `has_not_date_after` - has_not_date_after
* `has_date_within` - has_date_within
* `has_not_date_within` - has_not_date_within
- `value`: *string* — The filter value that must be compared to the field's value.

---

## DELETE /api/database/views/filter/{view_filter_id}/

****  
*operationId: `delete_database_table_view_filter`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `ClientUndoRedoActionGroupId` (header) — An optional header that marks the action performed by this request as having occurred in a particular action group.Then calling the undo/redo endpoint with the same ClientSessionId header, all the actions belonging to the same action group can be undone/redone together in a single API call.
- `view_filter_id` (path) — The ID of the view filter to delete.

---

## POST /api/database/views/{view_id}/filter-groups/

****  
*operationId: `create_database_table_view_filter_group`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `ClientUndoRedoActionGroupId` (header) — An optional header that marks the action performed by this request as having occurred in a particular action group.Then calling the undo/redo endpoint with the same ClientSessionId header, all the actions belonging to the same action group can be undone/redone together in a single API call.
- `view_id` (path) — The ID of the view where create the new filter group.

**Тело запроса:**

- `filter_type`: ** — Indicates whether all the rows should apply to all filters (AND) or to any filter (OR) in the group to be shown.

* `AND` - And
* `OR` - Or
- `parent_group`: *integer* — 

---

## GET /api/database/views/{view_id}/filters/

****  
*operationId: `list_database_table_view_filters`*

**Параметры:**

- `view_id` (path) — Returns only filters of the view related to the provided value.

---

## POST /api/database/views/{view_id}/filters/

****  
*operationId: `create_database_table_view_filter`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `ClientUndoRedoActionGroupId` (header) — An optional header that marks the action performed by this request as having occurred in a particular action group.Then calling the undo/redo endpoint with the same ClientSessionId header, all the actions belonging to the same action group can be undone/redone together in a single API call.
- `view_id` (path) — Creates a filter for the view related to the provided value.

**Тело запроса:**

- `field`: *integer* (обязательно) — The field of which the value must be compared to the filter value.
- `type`: ** (обязательно) — Indicates how the field's value must be compared to the filter's value. The filter is always in this order `field` `type` `value` (example: `field_1` `contains` `Test`).

* `equal` - equal
* `not_equal` - not_equal
* `filename_contains` - filename_contains
* `files_lower_than` - files_lower_than
* `has_file_type` - has_file_type
* `contains` - contains
* `contains_not` - contains_not
* `contains_word` - contains_word
* `doesnt_contain_word` - doesnt_contain_word
* `length_is_lower_than` - length_is_lower_than
* `higher_than` - higher_than
* `higher_than_or_equal` - higher_than_or_equal
* `lower_than` - lower_than
* `lower_than_or_equal` - lower_than_or_equal
* `is_even_and_whole` - is_even_and_whole
* `date_equal` - date_equal
* `date_before` - date_before
* `date_before_or_equal` - date_before_or_equal
* `date_after_days_ago` - date_after_days_ago
* `date_after` - date_after
* `date_after_or_equal` - date_after_or_equal
* `date_not_equal` - date_not_equal
* `date_equals_today` - date_equals_today
* `date_before_today` - date_before_today
* `date_after_today` - date_after_today
* `date_within_days` - date_within_days
* `date_within_weeks` - date_within_weeks
* `date_within_months` - date_within_months
* `date_equals_days_ago` - date_equals_days_ago
* `date_equals_months_ago` - date_equals_months_ago
* `date_equals_years_ago` - date_equals_years_ago
* `date_equals_week` - date_equals_week
* `date_equals_month` - date_equals_month
* `date_equals_day_of_month` - date_equals_day_of_month
* `date_equals_year` - date_equals_year
* `date_is` - date_is
* `date_is_not` - date_is_not
* `date_is_before` - date_is_before
* `date_is_on_or_before` - date_is_on_or_before
* `date_is_after` - date_is_after
* `date_is_on_or_after` - date_is_on_or_after
* `date_is_within` - date_is_within
* `single_select_equal` - single_select_equal
* `single_select_not_equal` - single_select_not_equal
* `single_select_is_any_of` - single_select_is_any_of
* `single_select_is_none_of` - single_select_is_none_of
* `link_row_has` - link_row_has
* `link_row_has_not` - link_row_has_not
* `link_row_contains` - link_row_contains
* `link_row_not_contains` - link_row_not_contains
* `boolean` - boolean
* `empty` - empty
* `not_empty` - not_empty
* `multiple_select_has` - multiple_select_has
* `multiple_select_has_not` - multiple_select_has_not
* `multiple_collaborators_has` - multiple_collaborators_has
* `multiple_collaborators_has_not` - multiple_collaborators_has_not
* `user_is` - user_is
* `user_is_not` - user_is_not
* `has_value_equal` - has_value_equal
* `has_not_value_equal` - has_not_value_equal
* `has_value_contains` - has_value_contains
* `has_not_value_contains` - has_not_value_contains
* `has_value_contains_word` - has_value_contains_word
* `has_not_value_contains_word` - has_not_value_contains_word
* `has_value_length_is_lower_than` - has_value_length_is_lower_than
* `has_all_values_equal` - has_all_values_equal
* `has_empty_value` - has_empty_value
* `has_not_empty_value` - has_not_empty_value
* `has_any_select_option_equal` - has_any_select_option_equal
* `has_none_select_option_equal` - has_none_select_option_equal
* `has_value_lower` - has_value_lower
* `has_value_lower_or_equal` - has_value_lower_or_equal
* `has_value_higher` - has_value_higher
* `has_value_higher_or_equal` - has_value_higher_or_equal
* `has_not_value_higher_or_equal` - has_not_value_higher_or_equal
* `has_not_value_higher` - has_not_value_higher
* `has_not_value_lower_or_equal` - has_not_value_lower_or_equal
* `has_not_value_lower` - has_not_value_lower
* `has_date_equal` - has_date_equal
* `has_not_date_equal` - has_not_date_equal
* `has_date_before` - has_date_before
* `has_not_date_before` - has_not_date_before
* `has_date_on_or_before` - has_date_on_or_before
* `has_not_date_on_or_before` - has_not_date_on_or_before
* `has_date_on_or_after` - has_date_on_or_after
* `has_not_date_on_or_after` - has_not_date_on_or_after
* `has_date_after` - has_date_after
* `has_not_date_after` - has_not_date_after
* `has_date_within` - has_date_within
* `has_not_date_within` - has_not_date_within
- `value`: *string* — The filter value that must be compared to the field's value.
- `group`: *integer* — The id of the filter group the new filter will belong to. If this is null, the filter will not be part of a filter group, but directly part of the view.

---
