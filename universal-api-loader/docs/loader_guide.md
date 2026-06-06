
🚀 Руководство по эксплуатации universal-api-loader
Первый запуск
bash
cd /mnt/3E7ADD3C7ADCF19F/ai-projects/universal-api-loader
python3 src/universal_loader.py
Загрузчик создаст workspace «Дмитрий Грузинов» и базы wildberries / ozon.

Для каждого отчёта выполнится полная загрузка на глубину max_depth_days.

Состояние сохранится в state/last_run.json.

Ежедневный инкрементальный запуск
При повторных запусках загружаются только новые данные (с даты последней успешной загрузки до текущей).
Если за период данных нет, дата в last_run.json не обновляется.

Полная перезагрузка истории
bash
rm -f state/last_run.json
python3 src/universal_loader.py
Будут заново загружены все данные за max_depth_days для каждого отчёта.

Добавление нового отчёта
Создать JSON-конфиг в configs/wildberries/ или configs/ozon/ (или в новой папке, например, configs/vk/).

Проверить конфиг валидатором:

bash
python3 src/validate_config.py --diagnose --config configs/.../новый_отчёт.json
Запустить загрузчик. Новый отчёт получит полную историю за max_depth_days.

Типовые ошибки
HTTP 429 (WB) – превышен лимит запросов. Уменьшите rate_limit_per_sec или запустите позже.

HTTP 400 / 404 – проверьте endpoint и параметры через валидатор.

Нет данных – возможно, за период действительно нет операций.

Мониторинг
logs/loader.log – технический журнал.

logs/status.md – человеко-читаемый отчёт последнего запуска.
