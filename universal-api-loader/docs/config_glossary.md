# 📘 Глоссарий JSON-конфигураций universal-api-loader

В этом документе подробно описаны все ключи, используемые в JSON-файлах конфигураций отчётов. Конфиги находятся в папках `configs/wildberries/` и `configs/ozon/`.

## Обязательные поля (присутствуют в каждом конфиге)

| Ключ | Тип | Описание |
|------|-----|----------|
| `api_base_url` | string | Базовый URL API без завершающего слеша. |
| `api_key_env` | string | Имя переменной окружения в `.env` с токеном/ключом. |
| `report_name` | string | Уникальное имя отчёта. |
| `api_endpoint` | string | Путь к ресурсу API. |
| `method` | string | HTTP метод: `GET` или `POST`. |
| `field_mapping` | object | Словарь: путь к полю в ответе API → тип данных Baserow (`text`, `integer`, `number`, `date`, `boolean`, `long_text`). |
| `max_depth_days` | integer | Глубина загрузки при первом запуске. |
| `batch_size` | integer | Размер страницы при пагинации. |
| `is_async` | boolean | Является ли отчёт асинхронным. |
| `rate_limit_per_sec` | number | Максимальное число запросов в секунду. |
| `response_data_path` | string | Путь к массиву данных в ответе (например, `"result.rows"`). |
| `pagination_config` | object | Параметры пагинации. |
| `request_body_template` | string | Шаблон тела для POST-запросов с плейсхолдерами `{from_date}`, `{to_date}` и др. |

## Управление пагинацией

| Ключ | Тип | Описание |
|------|-----|----------|
| `pagination_type` | string | `none`, `page_number`, `offset`, `rrdid`, `last_id` |
| `pagination_config` | object | Содержит параметры: `rrdid_param`, `limit_param`, `offset_param`, `page_param`, `page_size_param`, `last_id_param` |

## Управление датами

| Ключ | Тип | Описание |
|------|-----|----------|
| `date_from_param` | string | Имя параметра начала периода для GET. |
| `date_to_param` | string | Имя параметра конца периода для GET. |
| `split_by_month` | boolean | Разбивать длинный период по месяцам. |
| `template_vars` | object | Подстановка переменных в шаблон: `from_month`, `from_year`, `to_month`, `to_year`, `prev_month`, `prev_year` |

## Уникальность записей (дедупликация)

| Ключ | Тип | Описание |
|------|-----|----------|
| `unique_key` | string | Одиночное поле – уникальный идентификатор. |
| `unique_key_fields` | array | Список полей для составного ключа. |

## Асинхронные отчёты

Для отчётов, где API сначала создаёт задачу, а потом отдаёт результат, используется `is_async: true` и секция `async_config`.

**Поля `async_config`:**

| Ключ | Тип | Описание |
|------|-----|----------|
| `api_base_url` | string | Базовый URL для асинхронных операций (если отличается). |
| `create_endpoint` | string | Эндпоинт создания задачи. |
| `poll_endpoint` | string | Эндпоинт опроса статуса с `{uuid}`. |
| `uuid_path` | string | Путь к UUID в ответе создания задачи. |
| `status_path` | string | Путь к полю статуса в ответе опроса. |
| `status_ready` | string | Значения статуса готовности (через запятую). |
| `status_error` | string | Значения статуса ошибки. |
| `poll_interval_sec` | integer | Интервал опроса в секундах. |
| `poll_max_attempts` | integer | Максимальное число попыток. |
| `result_type` | string | `url` (ссылка на файл) или `inline` (данные в ответе). |
| `result_url_path` | string | Путь к URL для скачивания (если `result_type: url`). |
| `auth_type` | string | `default`, `bearer`, `oauth_client_credentials`. |
| `oauth_token_url` | string | URL получения OAuth-токена. |
| `oauth_client_id_env` | string | Переменная с Client ID. |
| `oauth_client_secret_env` | string | Переменная с Client Secret. |
| `prefill_list_key` | string | Ключ в теле, куда вставить список ID. |
| `prefill_list_endpoint` | string | Эндпоинт для получения списка ID. |
| `prefill_id_path` | string | Путь к ID внутри элемента списка. |
| `prefill_filter` | object | Фильтр (`field`, `values`, `exclude_values`). |

## Дополнительные параметры

| Ключ | Тип | Описание |
|------|-----|----------|
| `extra_params` | object | Дополнительные параметры строки запроса для GET. |
| `empty_response_code` | integer | HTTP-код, означающий отсутствие данных (например, `204`). |

## Пример синхронного GET-конфига

```json
{
  "api_base_url": "https://statistics-api.wildberries.ru",
  "api_key_env": "WB_TOKEN",
  "report_name": "sales",
  "api_endpoint": "/api/v1/supplier/sales",
  "method": "GET",
  "pagination_type": "none",
  "field_mapping": {
    "date": "text",
    "nmId": "integer",
    "forPay": "number"
  },
  "unique_key": "srid",
  "max_depth_days": 90,
  "batch_size": 80000,
  "is_async": false,
  "rate_limit_per_sec": 5,
  "response_data_path": "",
  "date_from_param": "dateFrom",
  "date_to_param": "dateTo",
  "pagination_config": {},
  "request_body_template": ""
}
Пример асинхронного конфига (Ozon)
json
{
  "api_base_url": "https://api-seller.ozon.ru",
  "api_key_env": "OZON_CREDS",
  "report_name": "stock_on_warehouses",
  "api_endpoint": "/v1/report/stock/create",
  "method": "POST",
  "is_async": true,
  "async_config": {
    "create_endpoint": "/v1/report/stock/create",
    "poll_endpoint": "/v1/report/info/{uuid}",
    "uuid_path": "result.task_id",
    "status_path": "result.status",
    "status_ready": "success",
    "poll_interval_sec": 5,
    "poll_max_attempts": 60,
    "result_type": "url",
    "result_url_path": "result.file"
  },
  ...
}
