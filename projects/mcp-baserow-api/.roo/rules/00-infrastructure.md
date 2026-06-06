# Инфраструктура (кратко)

## Устройства и сеть
- Ноутбук (Ubuntu) — Tailscale IP: 100.83.96.84
- Стационар (Windows) — Tailscale IP: 100.64.243.115
- VPS (Webdock, Дания): 92.113.151.208, Ubuntu 24.04
  - Панель 3X-UI: порт 2053, путь `/8TmMPGk6uGvjWxI/`
  - Логин/пароль панели: dmitry / 1959
  - Inbound Reality: порт 443, VLESS+gRPC, sni wikipedia.org
  - Доступ через Termius: port forwarding localhost:2053 → 127.0.0.1:2053

## Docker-контейнеры (все на ноутбуке)
- n8n:5678, flowise:3000, baserow:8000, qdrant:6333-6334
- n8n-runner:5680 (образ my-ai-stack-n8n-runner)
- Вспомогательные: baserow-postgres, baserow-redis, n8n-postgres

## Пути
- Общий диск (проекты): `/mnt/3E7ADD3C7ADCF19F/ai-projects`
- Симлинк: `~/my-ai-stack/projects` → `/mnt/3E7ADD3C7ADCF19F/ai-projects`
- Песочница для кода: `~/my-ai-stack/analytics/runner.py` (venv)
- Команда запуска: `cd ~/my-ai-stack/analytics && ./runner.py <file.py>`

## Важно
- При создании проектов в VS Code открывать реальный путь `/mnt/3E7ADD3C7ADCF19F/ai-projects`, а не симлинк.
- Секреты хранить в переменных окружения или `.env` (не в коде).

## Глобальные правила для всех агентов

- **Roo Code** читает `~/.roo/rules/`
- **Kilo Code** читает `~/.kilocode/rules/` (симлинк → `~/.roo/rules/`)
- **OpenCode** (CLI) должен читать `~/.roo/rules/` – настраивается через `~/.config/opencode/opencode.json` (секция `instructions`)

Все агенты используют единую базу глобальных правил.  
Если в ходе работы меняется системная архитектура, агент **обязан** предложить обновить соответствующие файлы в `~/.roo/rules/` (см. `04-workflow.md`).
