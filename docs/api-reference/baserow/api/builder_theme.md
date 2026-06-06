# Builder theme

## PATCH /api/builder/{builder_id}/theme/

****  
*operationId: `update_builder_theme`*

**Параметры:**

- `ClientSessionId` (header) — An optional header that marks the action performed by this request as having occurred in a particular client session. Then using the undo/redo endpoints with the same ClientSessionId header this action can be undone/redone.
- `builder_id` (path) — Updates the theme for the application builder related to the provided value.

**Тело запроса:**

- `primary_color`: *string* — 
- `secondary_color`: *string* — 
- `border_color`: *string* — 
- `main_success_color`: *string* — 
- `main_warning_color`: *string* — 
- `main_error_color`: *string* — 
- `custom_colors`: ** — 
- `heading_1_text_decoration`: *array* — Text decoration: [underline, stroke, uppercase, italic]
- `heading_2_text_decoration`: *array* — Text decoration: [underline, stroke, uppercase, italic]
- `heading_3_text_decoration`: *array* — Text decoration: [underline, stroke, uppercase, italic]
- `heading_4_text_decoration`: *array* — Text decoration: [underline, stroke, uppercase, italic]
- `heading_5_text_decoration`: *array* — Text decoration: [underline, stroke, uppercase, italic]
- `heading_6_text_decoration`: *array* — Text decoration: [underline, stroke, uppercase, italic]
- `body_font_family`: *string* — 
- `body_font_size`: *integer* — 
- `body_font_weight`: ** — 
- `body_text_color`: *string* — 
- `body_text_alignment`: ** — 
- `heading_1_font_family`: *string* — 
- `heading_1_font_size`: *integer* — 
- `heading_1_font_weight`: ** — 
- `heading_1_text_color`: *string* — 
- `heading_1_text_alignment`: ** — 
- `heading_2_font_family`: *string* — 
- `heading_2_font_size`: *integer* — 
- `heading_2_font_weight`: ** — 
- `heading_2_text_color`: *string* — 
- `heading_2_text_alignment`: ** — 
- `heading_3_font_family`: *string* — 
- `heading_3_font_size`: *integer* — 
- `heading_3_font_weight`: ** — 
- `heading_3_text_color`: *string* — 
- `heading_3_text_alignment`: ** — 
- `heading_4_font_family`: *string* — 
- `heading_4_font_size`: *integer* — 
- `heading_4_font_weight`: ** — 
- `heading_4_text_color`: *string* — 
- `heading_4_text_alignment`: ** — 
- `heading_5_font_family`: *string* — 
- `heading_5_font_size`: *integer* — 
- `heading_5_font_weight`: ** — 
- `heading_5_text_color`: *string* — 
- `heading_5_text_alignment`: ** — 
- `heading_6_font_family`: *string* — 
- `heading_6_font_size`: *integer* — 
- `heading_6_font_weight`: ** — 
- `heading_6_text_color`: *string* — 
- `heading_6_text_alignment`: ** — 
- `button_font_family`: *string* — 
- `button_font_size`: *integer* — 
- `button_font_weight`: ** — 
- `button_alignment`: ** — 
- `button_text_alignment`: ** — 
- `button_width`: ** — 
- `button_background_color`: *string* — The background color of buttons
- `button_text_color`: *string* — The text color of buttons
- `button_border_color`: *string* — The border color of buttons
- `button_border_size`: *integer* — Button border size
- `button_border_radius`: *integer* — Button border radius
- `button_vertical_padding`: *integer* — Button vertical padding
- `button_horizontal_padding`: *integer* — Button horizontal padding
- `button_hover_background_color`: *string* — The background color of buttons when hovered
- `button_hover_text_color`: *string* — The text color of buttons when hovered
- `button_hover_border_color`: *string* — The border color of buttons when hovered
- `button_active_background_color`: *string* — The background color of buttons when active
- `button_active_text_color`: *string* — The text color of buttons when active
- `button_active_border_color`: *string* — The border color of buttons when active
- `image_max_height`: *integer* — The image max height
- `image_alignment`: ** — 
- `image_max_width`: *integer* — The max-width for this image element.
- `image_border_radius`: *integer* — The border radius for this image element.
- `image_constraint`: ** — The image constraint to apply to this image

* `cover` - Cover
* `contain` - Contain
* `full-width` - Full Width
- `page_background_file`: ** — The image file
- `page_background_color`: *string* — The background color of the page
- `page_background_mode`: ** — The mode of the background image

* `tile` - Tile
* `fill` - Fill
* `fit` - Fit
- `label_font_family`: *string* — The font family of the label
- `label_text_color`: *string* — The text color of the label
- `label_font_size`: *integer* — The font size of the label
- `label_font_weight`: ** — 
- `input_font_family`: *string* — The font family of the input
- `input_font_size`: *integer* — 
- `input_font_weight`: ** — 
- `input_text_color`: *string* — The text color of the input
- `input_background_color`: *string* — The background color of the input
- `input_border_color`: *string* — The color of the input border
- `input_border_size`: *integer* — Input border size
- `input_border_radius`: *integer* — Input border radius
- `input_vertical_padding`: *integer* — Input vertical padding
- `input_horizontal_padding`: *integer* — Input horizontal padding
- `table_border_color`: *string* — The color of the table border
- `table_border_size`: *integer* — Table border size
- `table_border_radius`: *integer* — Table border radius
- `table_header_background_color`: *string* — The background color of the table header cells
- `table_header_text_color`: *string* — The text color of the table header cells
- `table_header_font_size`: *integer* — The font size of the header cells
- `table_header_font_weight`: ** — 
- `table_header_font_family`: *string* — The font family of the table header cells
- `table_header_text_alignment`: ** — 
- `table_cell_background_color`: *string* — The background color of the table cells
- `table_cell_alternate_background_color`: *string* — The alternate background color of the table cells
- `table_cell_alignment`: ** — 
- `table_cell_vertical_padding`: *integer* — Table cell vertical padding
- `table_cell_horizontal_padding`: *integer* — Table cell horizontal padding
- `table_vertical_separator_color`: *string* — The color of the table vertical separator
- `table_vertical_separator_size`: *integer* — Table vertical separator size
- `table_horizontal_separator_color`: *string* — The color of the table horizontal separator
- `table_horizontal_separator_size`: *integer* — Table horizontal separator size
- `link_default_text_decoration`: *array* — Default text decoration: [underline, stroke, uppercase, italic]
- `link_hover_text_decoration`: *array* — Hover text decoration: [underline, stroke, uppercase, italic]
- `link_active_text_decoration`: *array* — Active text decoration: [underline, stroke, uppercase, italic]
- `link_font_family`: *string* — 
- `link_font_size`: *integer* — 
- `link_font_weight`: ** — 
- `link_text_alignment`: ** — 
- `link_text_color`: *string* — The text color of links
- `link_hover_text_color`: *string* — The hover color of links when hovered
- `link_active_text_color`: *string* — The hover color of links when active

---
