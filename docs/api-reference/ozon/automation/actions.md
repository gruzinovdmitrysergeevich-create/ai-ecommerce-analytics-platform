# Акции и стратегии ценообразования

## Акции Ozon

### `GET /v1/actions`

Список доступных акций.

### `POST /v1/actions/candidates`

Товары, доступные для акции.

### `POST /v1/actions/products`

Товары, участвующие в акции.

### `POST /v1/actions/products/activate`

Добавить товары в акцию.

### `POST /v1/actions/products/deactivate`

Удалить товары из акции.

### `POST /v1/actions/discounts-task/list`

Заявки на скидку от покупателей.

### `POST /v1/actions/discounts-task/approve`

Согласовать заявку.

### `POST /v1/actions/discounts-task/decline`

Отклонить заявку.

## Акции продавца (Seller Actions)

### `POST /v1/seller-actions/create/discount`

Создать акцию «Скидка».

### `POST /v1/seller-actions/create/voucher`

Создать акцию «Скидка по промокоду».

### `POST /v1/seller-actions/list`

Список акций продавца.

### `POST /v1/seller-actions/products/add`

Добавить товары в акцию.

### `POST /v1/seller-actions/change-activity`

Включить/выключить акцию.

## Стратегии ценообразования

### `POST /v1/pricing-strategy/competitors/list`

Список конкурентов.

### `POST /v1/pricing-strategy/list`

Список стратегий.

### `POST /v1/pricing-strategy/create`

Создать стратегию.

### `POST /v1/pricing-strategy/products/add`

Добавить товары в стратегию.

### `POST /v1/pricing-strategy/status`

Изменить статус стратегии.

[Документация](https://docs.ozon.ru/api/seller/)
