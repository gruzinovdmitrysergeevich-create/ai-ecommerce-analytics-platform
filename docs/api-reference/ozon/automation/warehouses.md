# Склады и кластеры

## `POST /v1/warehouse/fbo/list`

Точки отгрузки для кросс-докинга и прямых поставок.

### Параметры
| Параметр | Тип | Описание |
|----------|-----|----------|
| `filter_by_supply_type` | array | `CREATE_TYPE_CROSSDOCK`, `CREATE_TYPE_DIRECT` |
| `search` | string | Поиск по названию |

---

## `POST /v1/cluster/list`

Информация о кластерах и их складах.

### Параметры
| Параметр | Тип | Описание |
|----------|-----|----------|
| `cluster_type` | string | `CLUSTER_TYPE_OZON`, `CLUSTER_TYPE_CIS` |

---

## `POST /v1/warehouse/ozon/list`

Список складов Ozon (FBO, возвратные и др.).

### Параметры
| Параметр | Тип | Описание |
|----------|-----|----------|
| `warehouse_types` | array | `FULL_FILLMENT`, `FULL_FILLMENT_RETURNS`, `EXPRESS_DARK_STORE`, `CROSS_DOCK` и др. |

---

## `POST /v2/warehouse/list`

Список складов FBS и rFBS.

[Документация](https://docs.ozon.ru/api/seller/)
