#!/usr/bin/env python3
"""
sandbox.py — умная песочница для исполнения кода модели.

Особенности:
  - Анализ ошибки: понимает ЧТО упало (KeyError, TypeError, etc.)
  - Умный retry: подсказывает модели, что исправить
  - Таймаут: защита от бесконечных циклов
  - Graceful degradation: если код не работает → отдаёт сырые данные

Использование:
    from src.sandbox import Sandbox
    sb = Sandbox(dataframes)
    ok, output, error_hint = sb.execute(code)
"""

import sys, io, re, traceback, signal
from pathlib import Path
from contextlib import contextmanager

import pandas as pd
import numpy as np


class TimeoutError(Exception):
    pass


@contextmanager
def timeout(seconds: int):
    """Контекстный менеджер для таймаута."""
    def handler(signum, frame):
        raise TimeoutError(f"Код выполнялся > {seconds} сек")
    old = signal.signal(signal.SIGALRM, handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old)


class Sandbox:
    def __init__(self, dataframes: dict):
        """
        dataframes: {"df_имя": pd.DataFrame, ...}
        """
        self.dfs = dataframes
        self.max_retries = 3
        self.timeout_sec = 30
        self.history = []  # история попыток

    def execute(self, code: str, attempt: int = 1) -> tuple[bool, str, str | None]:
        """
        Исполняет код в песочнице.
        Возвращает: (ok, output, error_hint)
          - ok: True если код выполнился без ошибок
          - output: stdout код
          - error_hint: подсказка модели что исправить (None если ok)
        """
        # Чистим код
        code = self._clean_code(code)
        if not code:
            return False, "", "Модель не сгенерировала код"

        # Строим окружение
        env = {
            "pd": pd,
            "np": np,
            "print": print,
            "__builtins__": __builtins__,
            "json": __import__("json"),
            "datetime": __import__("datetime"),
        }
        env.update(self.dfs)

        # Перехватываем stdout
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()

        try:
            with timeout(self.timeout_sec):
                exec(code, env)
            output = sys.stdout.getvalue()
            self.history.append({"attempt": attempt, "ok": True, "code": code[:200]})
            return True, output, None

        except TimeoutError:
            hint = f"Код работал > {self.timeout_sec} сек. Упрости: меньше данных (df.head()), меньше циклов."
            self.history.append({"attempt": attempt, "ok": False, "error": "timeout"})
            return False, "", hint

        except Exception as e:
            error_type = type(e).__name__
            error_msg = str(e)
            output = sys.stdout.getvalue()

            # Анализируем ошибку и генерируем подсказку
            hint = self._analyze_error(error_type, error_msg, code)

            self.history.append({
                "attempt": attempt,
                "ok": False,
                "error": f"{error_type}: {error_msg}",
                "hint": hint,
                "partial_output": output[:200],
            })

            return False, output, hint

        finally:
            sys.stdout = old_stdout

    def execute_with_retry(self, generate_fn, question: str, schemas_info: str) -> tuple[bool, str, list]:
        """
        Полный цикл: генерация кода → песочница → retry до 3 раз.
        generate_fn(prompt) → str (код)

        Возвращает: (ok, final_output, history)
        """
        code = None
        error_hint = None

        for attempt in range(1, self.max_retries + 1):
            # Строим промпт
            if attempt == 1:
                prompt = self._build_code_prompt(question, schemas_info)
            else:
                prompt = self._build_retry_prompt(question, schemas_info, code, error_hint)

            # Генерируем код
            code = generate_fn(prompt)
            if not code:
                self.history.append({"attempt": attempt, "ok": False, "error": "Модель не ответила"})
                continue

            # Исполняем
            ok, output, error_hint = self.execute(code, attempt)
            if ok:
                return True, output, self.history

        # Все попытки исчерпаны → отдаём что есть
        return False, self._fallback_output(), self.history

    # ════ Анализ ошибок ════

    def _analyze_error(self, error_type: str, error_msg: str, code: str) -> str:
        """Анализирует ошибку и даёт модели конкретную подсказку."""

        if error_type == "KeyError":
            # Какая колонка не найдена?
            m = re.search(r"'([^']+)'", error_msg)
            if m:
                missing = m.group(1)
                available = self._list_all_columns()
                return (
                    f"ОШИБКА: Колонка '{missing}' не найдена.\n"
                    f"Доступные колонки в DataFrame'ах:\n{available}\n"
                    f"Используй ТОЛЬКО эти названия. Проверь регистр."
                )

        elif error_type == "TypeError":
            return (
                f"ОШИБКА ТИПА: {error_msg[:100]}\n"
                f"Проверь типы данных. Возможно, нужно pd.to_numeric() или astype()."
            )

        elif error_type == "NameError":
            m = re.search(r"name '(\w+)' is not defined", error_msg)
            if m:
                missing = m.group(1)
                available_dfs = list(self.dfs.keys())
                return (
                    f"ОШИБКА: Переменная '{missing}' не определена.\n"
                    f"Доступные DataFrame'ы: {', '.join(available_dfs)}\n"
                    f"Используй ТОЛЬКО эти имена."
                )

        elif error_type == "ValueError":
            return (
                f"ОШИБКА ЗНАЧЕНИЯ: {error_msg[:150]}\n"
                f"Возможно, несовместимые типы при merge/join. Проверь ключи."
            )

        elif error_type == "AttributeError":
            return (
                f"ОШИБКА АТРИБУТА: {error_msg[:150]}\n"
                f"Проверь, что объект имеет нужный метод. Для DataFrame используй .columns (не .keys())."
            )

        elif error_type == "SyntaxError":
            return (
                f"СИНТАКСИЧЕСКАЯ ОШИБКА: {error_msg[:150]}\n"
                f"Проверь скобки, кавычки, двоеточия."
            )

        return f"ОШИБКА: {error_msg[:200]}"

    def _list_all_columns(self) -> str:
        """Список всех колонок всех DataFrame."""
        lines = []
        for name, df in self.dfs.items():
            cols = ", ".join(df.columns[:15])
            lines.append(f"  {name}: [{cols}]")
        return "\n".join(lines)

    # ════ Сборка промптов ════

    def _build_code_prompt(self, question: str, schemas_info: str) -> str:
        """Промпт для генерации кода (первая попытка)."""
        return f"""Напиши Python-код для ответа на вопрос. ТОЛЬКО КОД, без markdown, без <think>.

Вопрос: {question}

ДАННЫЕ (уже загружены в DataFrame'ы):
{schemas_info}

ТРЕБОВАНИЯ:
1. Используй ТОЛЬКО переменные df_*. НЕ используй read_csv/read_excel.
2. Для дат: pd.to_datetime(errors='coerce'), фильтруй .dt.year / .dt.month.
3. Проверяй существование колонок ПЕРЕД использованием.
4. Все суммы агрегируй через .sum() или .groupby().sum().
5. Выводи результат через print().
6. Если связываешь таблицы — используй merge() по датам.
7. НЕ используй f-строки с русским текстом внутри print() — только переменные.
8. ВАЖНО: если колонка не найдена, выведи print('COLUMN_NOT_FOUND: имя_колонки')

Выведи ТОЛЬКО Python-код."""

    def _build_retry_prompt(self, question: str, schemas_info: str,
                            previous_code: str, error_hint: str) -> str:
        """Промпт для повторной попытки с контекстом ошибки."""
        return f"""Предыдущий код упал с ошибкой. Исправь.

Вопрос: {question}

ПРЕДЫДУЩИЙ КОД:
```python
{previous_code[:1500]}
```

{error_hint}

Данные те же:
{schemas_info}

Напиши ИСПРАВЛЕННЫЙ код. ТОЛЬКО КОД, без пояснений. Без <think>."""

    def _fallback_output(self) -> str:
        """Если все попытки провалились — отдаём сырые данные."""
        lines = ["⚠️ Модель не смогла сгенерировать рабочий код. Вот сырые данные:\n"]
        for name, df in list(self.dfs.items())[:5]:
            lines.append(f"\n=== {name} ===")
            lines.append(f"Строк: {len(df)}, Колонок: {len(df.columns)}")
            lines.append(f"Колонки: {', '.join(df.columns[:10])}")
            lines.append(df.head(3).to_string())
        return "\n".join(lines)

    # ════ Очистка кода ════

    @staticmethod
    def _clean_code(code: str) -> str:
        """Очищает код от <think> и markdown."""
        code = re.sub(r'<think>.*?</think>', '', code, flags=re.DOTALL)

        # Извлекаем из ```python ... ```
        m = re.search(r'```(?:python|py)?\s*\n(.*?)```', code, re.DOTALL)
        if m:
            return m.group(1).strip()

        # Ищем первую строку кода
        lines = code.split('\n')
        start = 0
        for i, line in enumerate(lines):
            if re.match(r'^\s*(import|from|def|class|print|df\d*|pd\.|np\.|if|for|while|try)', line.strip()):
                start = i
                break
        return '\n'.join(lines[start:]).strip()
