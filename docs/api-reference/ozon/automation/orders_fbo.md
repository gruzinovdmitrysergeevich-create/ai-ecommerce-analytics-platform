# Заказы и поставки FBO

## Управление поставками

### `POST /v1/supply-order/status/counter`

Количество заявок по статусам.

### `POST /v3/supply-order/list`

Список заявок на поставку.

### `POST /v3/supply-order/get`

Информация о заявке.

### `POST /v1/supply-order/bundle`

Состав поставки.

### `POST /v1/supply-order/timeslot/get`

Доступные интервалы поставки.

### `POST /v1/supply-order/timeslot/update`

Изменение интервала.

### `POST /v1/supply-order/pass/create`

Добавление данных водителя и автомобиля для пропуска.

### `POST /v1/supply-order/pass/status`

Статус ввода данных пропуска.

## Создание заявки через черновик

### `POST /v1/draft/crossdock/create`

Черновик кросс-докинга.

### `POST /v1/draft/direct/create`

Черновик прямой поставки.

### `POST /v1/draft/multi-cluster/create`

Черновик для нескольких кластеров.

### `POST /v2/draft/create/info`

Информация о черновике.

### `POST /v2/draft/timeslot/info`

Доступные таймслоты.

### `POST /v2/draft/supply/create`

Создание заявки из черновика.

### `POST /v2/draft/supply/create/status`

Статус создания заявки.

## Грузоместа

### `POST /v1/cargoes/create`

Установка грузомест.

### `POST /v2/cargoes/create/info`

Информация об установке.

### `POST /v1/cargoes-label/create`

Генерация этикеток для грузомест.

### `POST /v1/cargoes-label/get`

Получение этикеток.

[Документация](https://docs.ozon.ru/api/seller/)
