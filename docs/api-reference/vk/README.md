# VK Ads API – документация для интеграции

Полное описание ресурсов API VK Рекламы. Используется для получения статистики и управления рекламным кабинетом (создание кампаний, настройка аудиторий, ОРД и др.).

## ⚠️ Перед началом работы
**Обязательно прочитайте [`general.md`](general.md)** – базовый URL, авторизация, форматы, лимиты, ошибки.

## Структура
- **[`general.md`](general.md)** – общие принципы API.
- **[`api/`](api/)** – методы, сгруппированные по темам:
  - [`auth.md`](api/auth.md) – получение и обновление токенов.
  - [`ad_plans.md`](api/ad_plans.md) – рекламные кампании.
  - [`ad_groups.md`](api/ad_groups.md) – группы объявлений и таргетинги.
  - [`banners.md`](api/banners.md) – объявления (креативы).
  - [`statistics.md`](api/statistics.md) – статистика.
  - [`audience.md`](api/audience.md) – сегменты, списки пользователей, счётчики.
  - [`packages.md`](api/packages.md) – пакеты (форматы), площадки.
  - [`mobile_apps.md`](api/mobile_apps.md) – мобильные приложения, трекеры, SkAdNetwork.
  - [`lead_forms.md`](api/lead_forms.md) – лид-формы и опросы.
  - [`billing.md`](api/billing.md) – финансы и транзакции.
  - [`ord.md`](api/ord.md) – отчётность в ОРД.
  - [`agency.md`](api/agency.md) – управление клиентами агентства.
  - [`dictionaries.md`](api/dictionaries.md) – справочники (регионы, ОС, интересы).
  - [`subscriptions.md`](api/subscriptions.md) – вебхуки на изменения.

## Официальные источники
- https://ads.vk.com/doc/api/
- https://target.vk.ru/partners/help/management_api
