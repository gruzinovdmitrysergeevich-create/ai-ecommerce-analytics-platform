Как использовать песочницу и аналитические библиотеки

bash
tee ~/.roo/rules/06-analytics.md << 'EOF'
# Аналитика и песочница

## Песочница для выполнения кода
- **Скрипт**: `~/my-ai-stack/analytics/runner.py`
- **Интерпретатор**: виртуальное окружение `~/my-ai-stack/analytics/venv/bin/python`
- **Команда запуска**: 
  ```bash
  cd ~/my-ai-stack/analytics && ./runner.py <file.py>
Что делает: перехватывает stdout/stderr, возвращает код возврата. Подходит для выполнения любого Python-кода в изолированной среде.

Доступные библиотеки (из pip list в venv)
pandas, numpy, scipy

lifetimes, uncertainties, numpy_financial

requests, python-dotenv

openpyxl, matplotlib, seaborn

и другие стандартные для анализа данных.

Рекомендации
Всегда тестируй сгенерированный код в песочнице перед вставкой в n8n или в боевые скрипты.

При добавлении новых библиотек активируй venv и устанавливай через pip:

bash
source ~/my-ai-stack/analytics/venv/bin/activate
pip install <package>
Не забывай про .env в ~/my-ai-stack/analytics/ для хранения токенов API.
EOF
