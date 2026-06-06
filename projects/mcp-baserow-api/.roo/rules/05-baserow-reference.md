# Baserow: мета-таблицы (workspace 143)

## Таблица services (ID 893)
| Поле          | Field ID | Тип      | Пример                |
|---------------|----------|----------|-----------------------|
| Name          | 9111     | text     | wildberries           |
| api_base_url  | 9115     | text     | https://statistics-api.wildberries.ru |
| auth_type     | 9116     | text     | header                |

## Таблица service_reports (ID 894)
| Поле          | Field ID | Тип       | Пример (sales)        |
|---------------|----------|-----------|-----------------------|
| service_id    | 9120     | link_row  | [1] (wildberries)     |
| report_name   | 9122     | text      | sales                 |
| api_endpoint  | 9123     | text      | /api/v1/supplier/sales|
| method        | 9124     | text      | GET                   |
| field_mapping | 9125     | long_text | {"date":"date",...}   |
| unique_key    | 9126     | text      | srid                  |

## Таблица clients (ID 895)
| Поле          | Field ID | Тип    | Пример                |
|---------------|----------|--------|-----------------------|
| Name          | 9127     | text   | dmitry_gruzinov       |
| workspace_id  | 9132     | number | NULL (создаётся авто) |

## Таблица client_services (ID 896)
| Поле            | Field ID | Тип      | Пример               |
|-----------------|----------|----------|----------------------|
| client_id       | 9136     | link_row | [1] (dmitry)         |
| service_id      | 9138     | link_row | [1] (wildberries)    |
| api_key         | 9140     | text     | REAL_WB_TOKEN        |
| target_table_id | 9141     | number   | NULL (будет создан)  |
| last_run        | 9142     | date     | NULL                 |

## Использование
- Для создания таблиц для клиента требуется JWT (логин/пароль администратора Baserow).
- Database token `S79owXt1Q4XlvhGW8q825aOntwVI0wiE` позволяет читать/писать, но не создавать таблицы.
