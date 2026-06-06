# Baserow: технические детали локальной установки

## Подключение к PostgreSQL напрямую
Host: `baserow-postgres`, Port: `5432`, DB: `baserow`, User: `baserow`, Password: `StrongPassword123!`

## Команды управления (Django)
docker exec -it baserow_backend_1 python manage.py ...

text

## Важные переменные окружения
- `DATABASE_HOST`, `DATABASE_USER`, `DATABASE_PASSWORD`
- `REDIS_HOST`, `REDIS_PORT`

## Логи и отладка
- `docker logs baserow_backend_1`
- `python manage.py shell_plus`
