# Структура директорий

## Основные пути
- **Домашняя папка**: `/home/werna81`
- **Глобальные правила Roo**: `~/.roo/rules/`
- **Основной стек (Docker, скрипты)**: `~/my-ai-stack/`
  - `docker-compose.yml`
  - `analytics/` – песочница (`runner.py`, venv)
  - `ai-цеха.sh`, `ai-робот.sh`, `ai-статус.sh`
  - `voice/` – Whisper
  - `archive/` – старые парсеры
  - `projects/` – симлинк на общий диск

## Глобальные правила Roo Code (`~/.roo/rules/`)
| Файл | Назначение |
|------|------------|
| *(все файлы в этой папке используются также Kilo Code (через симлинк) и любым терминальным агентом)* | |
| `00-infrastructure.md` | IP, Docker, порты, пути, песочница |
| `01-communication-style.md` | Стиль общения: коротко, детский язык, поэтапно |
| `02-mcp-usage.md` | MCP‑серверы, когда их включать |
| `03-directory-structure.md` | Структура папок (этот файл) |
| `04-workflow.md` | Гибридный vs автономный сценарии, режимы Architect/Code |
| `05-baserow-reference.md` | Мета‑таблицы Baserow (workspace 143) |
| `06-analytics.md` | Использование песочницы `runner.py`, библиотеки |
| `90-secrets.md` | Секреты, API‑ключи, пароли (явные значения) |
| `99-reminders.md` | Напоминания: скрытые папки, модели на стационаре, доступ и др. |

## Общий диск (Windows‑раздел)
- **Точка монтирования**: `/mnt/3E7ADD3C7ADCF19F`
- **Папка проектов**: `/mnt/3E7ADD3C7ADCF19F/ai-projects`
- **Симлинк**: `~/my-ai-stack/projects` → `/mnt/3E7ADD3C7ADCF19F/ai-projects`

## Проект на общем диске (структура)
Каждый проект имеет корень в `/mnt/3E7ADD3C7ADCF19F/ai-projects/<project>/`:
- `.roo/rules/` – локальные правила проекта
- `memory-bank/` – контекстные файлы:
  - `activeContext.md` – текущая активность
  - `productContext.md` – зачем проект
  - `progress.md` – что сделано
  - `systemPatterns.md` – архитектурные решения
  - `techContext.md` – технологии, версии
  - `projectbrief.md` – цели и задачи
- `src/` – исходный код
- `docs/` – документация
- `.env` – переменные окружения (не коммитить)

## Docker‑контейнеры (данные)
- `~/my-ai-stack/baserow_data/`
- `~/my-ai-stack/qdrant_data/`
- `~/my-ai-stack/n8n_data/`
- `~/my-ai-stack/flowise_data/`
- `~/my-ai-stack/n8n-postgres_data/`
