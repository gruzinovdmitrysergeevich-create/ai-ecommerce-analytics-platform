# Admin data scanner

## GET /api/admin/data-scanner/results/

****  
*operationId: `admin_data_scanner_list_results`*

**Параметры:**

- `ids` (query) — A comma-separated list of data scan results IDs to filter by. When provided, only data scan results with those IDs are returned.
- `page` (query) — Defines which page should be returned.
- `search` (query) — If provided only data scan results with matched_value that match the query will be returned.
- `size` (query) — Defines how many data scan results should be returned per page.
- `sorts` (query) — A comma separated string of attributes to sort by, each attribute must be prefixed with `+` for a descending sort or a `-` for an ascending sort. The accepted attribute names are: `first_identified_on, last_identified_on`. For example `sorts=-first_identified_on,-last_identified_on` will sort the data scan results first by descending first_identified_on and then ascending last_identified_on. A sortparameter with multiple instances of the same sort attribute will respond with the ERROR_INVALID_SORT_ATTRIBUTE error.

---

## POST /api/admin/data-scanner/results/export/

****  
*operationId: `admin_data_scanner_export_results`*


**Тело запроса:**

- `url`: *string* (обязательно) — 
- `export_charset`: ** — The character set to use when creating the export file.

* `utf-8` - utf-8
* `iso-8859-6` - iso-8859-6
* `windows-1256` - windows-1256
* `iso-8859-4` - iso-8859-4
* `windows-1257` - windows-1257
* `iso-8859-14` - iso-8859-14
* `iso-8859-2` - iso-8859-2
* `windows-1250` - windows-1250
* `gbk` - gbk
* `gb18030` - gb18030
* `big5` - big5
* `koi8-r` - koi8-r
* `koi8-u` - koi8-u
* `iso-8859-5` - iso-8859-5
* `windows-1251` - windows-1251
* `x-mac-cyrillic` - mac-cyrillic
* `iso-8859-7` - iso-8859-7
* `windows-1253` - windows-1253
* `iso-8859-8` - iso-8859-8
* `windows-1255` - windows-1255
* `euc-jp` - euc-jp
* `iso-2022-jp` - iso-2022-jp
* `shift-jis` - shift-jis
* `euc-kr` - euc-kr
* `macintosh` - macintosh
* `iso-8859-10` - iso-8859-10
* `iso-8859-16` - iso-8859-16
* `windows-874` - cp874
* `windows-1254` - windows-1254
* `windows-1258` - windows-1258
* `iso-8859-1` - iso-8859-1
* `windows-1252` - windows-1252
* `iso-8859-3` - iso-8859-3
- `csv_column_separator`: ** — The value used to separate columns in the resulting csv file.

* `,` - ,
* `;` - ;
* `|` - |
* `tab` - 	
* `record_separator` - 
* `unit_separator` - 
- `csv_first_row_header`: *boolean* — Whether or not to generate a header row at the top of the csv file.
- `filter_scan_id`: *integer* — Optional: Filter results by scan ID.

---

## DELETE /api/admin/data-scanner/results/{result_id}/

****  
*operationId: `admin_data_scanner_delete_result`*

**Параметры:**

- `result_id` (path) — 

---

## GET /api/admin/data-scanner/scans/

****  
*operationId: `admin_data_scanner_list_scans`*

**Параметры:**

- `ids` (query) — A comma-separated list of data scans IDs to filter by. When provided, only data scans with those IDs are returned.
- `page` (query) — Defines which page should be returned.
- `search` (query) — If provided only data scans with name that match the query will be returned.
- `size` (query) — Defines how many data scans should be returned per page.
- `sorts` (query) — A comma separated string of attributes to sort by, each attribute must be prefixed with `+` for a descending sort or a `-` for an ascending sort. The accepted attribute names are: `name, scan_type, frequency, created_on`. For example `sorts=-name,-scan_type` will sort the data scans first by descending name and then ascending scan_type. A sortparameter with multiple instances of the same sort attribute will respond with the ERROR_INVALID_SORT_ATTRIBUTE error.

---

## POST /api/admin/data-scanner/scans/

****  
*operationId: `admin_data_scanner_create_scan`*


**Тело запроса:**

- `name`: *string* (обязательно) — 
- `scan_type`: ** (обязательно) — 
- `pattern`: *string* — 
- `frequency`: ** — 
- `scan_all_workspaces`: *boolean* — 
- `workspace_ids`: *array* — 
- `list_items`: *array* — 
- `source_table_id`: *integer* — 
- `source_field_id`: *integer* — 
- `whole_words`: *boolean* — 

---

## GET /api/admin/data-scanner/scans/{scan_id}/

****  
*operationId: `admin_data_scanner_get_scan`*

**Параметры:**

- `scan_id` (path) — 

---

## PATCH /api/admin/data-scanner/scans/{scan_id}/

****  
*operationId: `admin_data_scanner_update_scan`*

**Параметры:**

- `scan_id` (path) — 

**Тело запроса:**

- `name`: *string* — 
- `scan_type`: ** — 
- `pattern`: *string* — 
- `frequency`: ** — 
- `scan_all_workspaces`: *boolean* — 
- `workspace_ids`: *array* — 
- `list_items`: *array* — 
- `source_table_id`: *integer* — 
- `source_field_id`: *integer* — 
- `whole_words`: *boolean* — 

---

## DELETE /api/admin/data-scanner/scans/{scan_id}/

****  
*operationId: `admin_data_scanner_delete_scan`*

**Параметры:**

- `scan_id` (path) — 

---

## POST /api/admin/data-scanner/scans/{scan_id}/trigger/

****  
*operationId: `admin_data_scanner_trigger_scan`*

**Параметры:**

- `scan_id` (path) — 

---

## GET /api/admin/data-scanner/workspace-structure/{workspace_id}/

****  
*operationId: `admin_data_scanner_workspace_structure`*

**Параметры:**

- `workspace_id` (path) — 

---
