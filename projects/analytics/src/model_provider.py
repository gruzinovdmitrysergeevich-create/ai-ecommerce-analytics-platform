#!/usr/bin/env python3
"""
model_provider.py — абстракция AI-моделей: код (облако) + интерпретация (локально).

Архитектура:
  - code_model: DeepSeek API (генерит Python-код)
  - interpret_model: deepseek-fin локально (интерпретирует результаты)
  - fallback: если локальная не ответила → облако

Использование:
    from model_provider import ModelProvider
    p = ModelProvider()
    code = p.code("напиши код для анализа")
    result = p.interpret("вот цифры, объясни")
"""

import re
import requests
import yaml
from pathlib import Path

CONFIG_PATH = Path(__file__).parent.parent / "config.yaml"


class ModelProvider:
    def __init__(self, config_path=None):
        cfg_path = config_path or CONFIG_PATH
        with open(cfg_path) as f:
            self.config = yaml.safe_load(f)
        self._code_cfg = self.config["models"]["code"]
        self._interp_cfg = self.config["models"]["interpret"]
        self._fallback_cfg = self.config["models"].get("fallback", self._code_cfg)

    # ════ Генерация кода (облако DeepSeek) ════

    def code(self, prompt: str, temperature: float = None, max_tokens: int = None) -> str | None:
        """Генерирует Python-код через облако."""
        temp = temperature if temperature is not None else self._code_cfg.get("temperature", 0.1)
        mt = max_tokens if max_tokens is not None else self._code_cfg.get("max_tokens", 3000)

        return self._call_api(
            url=f"{self._code_cfg['api_base']}/chat/completions",
            api_key=self._code_cfg["api_key"],
            model=self._code_cfg["model"],
            system="Ты программист. Отвечай ТОЛЬКО Python-кодом. Без markdown. Без <think>. Без комментариев на русском. Код должен сразу исполняться.",
            prompt=prompt,
            temperature=temp,
            max_tokens=mt,
            timeout=120,
        )

    # ════ Интерпретация (локально deepseek-fin) ════

    def interpret(self, prompt: str, temperature: float = None, max_tokens: int = None) -> str | None:
        """Интерпретирует результаты через локальную модель."""
        temp = temperature if temperature is not None else self._interp_cfg.get("temperature", 0.3)
        mt = max_tokens if max_tokens is not None else self._interp_cfg.get("max_tokens", 2000)

        result = self._call_ollama(
            url=self._interp_cfg["url"],
            model=self._interp_cfg["model"],
            prompt=prompt,
            temperature=temp,
            max_tokens=mt,
            keep_alive=self._interp_cfg.get("keep_alive", 3600),
            timeout=180,
        )

        if result is None:
            print("  ⚠️ Локальная модель не ответила — переключаюсь на облако")
            result = self._call_api(
                url=f"{self._fallback_cfg['api_base']}/chat/completions",
                api_key=self._fallback_cfg["api_key"],
                model=self._fallback_cfg["model"],
                system="Ты финансовый аналитик. Отвечай на русском, без <think>, по существу.",
                prompt=prompt,
                temperature=temp,
                max_tokens=mt,
                timeout=120,
            )

        return result

    # ════ Универсальный метод (сам выбирает модель) ════

    def classify(self, prompt: str) -> str | None:
        """Классификация/категоризация — локальная модель."""
        return self.interpret(prompt, temperature=0.0, max_tokens=1000)

    # ════ Внутренние методы ════

    def _call_ollama(self, url: str, model: str, prompt: str,
                     temperature: float, max_tokens: int,
                     keep_alive: int, timeout: int) -> str | None:
        """Вызов Ollama chat API."""
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
            "options": {"temperature": temperature, "num_predict": max_tokens},
            "keep_alive": keep_alive,
        }
        try:
            r = requests.post(f"{url}/api/chat", json=payload, timeout=timeout)
            if r.status_code == 200:
                content = r.json().get("message", {}).get("content", "")
                if content.strip():
                    return self._strip_think(content.strip())
            # Fallback: generate API
            r = requests.post(f"{url}/api/generate",
                json={"model": model, "prompt": prompt, "stream": False,
                      "options": {"temperature": temperature, "num_predict": max_tokens},
                      "keep_alive": keep_alive, "raw": True},
                timeout=timeout)
            r.raise_for_status()
            resp = r.json().get("response", "").strip()
            return self._strip_think(resp) if resp else None
        except Exception as e:
            print(f"  Ollama error: {e}")
            return None

    def _call_api(self, url: str, api_key: str, model: str,
                  system: str, prompt: str, temperature: float,
                  max_tokens: int, timeout: int) -> str | None:
        """Вызов OpenAI-совместимого API."""
        if not api_key:
            print("  ❌ Нет API-ключа")
            return None
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        try:
            r = requests.post(url, json=payload, headers=headers, timeout=timeout)
            r.raise_for_status()
            text = r.json()["choices"][0]["message"]["content"].strip()
            return self._strip_think(text)
        except Exception as e:
            print(f"  API error: {e}")
            return None

    @staticmethod
    def _strip_think(text: str) -> str:
        """Удаляет <think>...</think> блоки."""
        return re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL).strip()

    @staticmethod
    def extract_code(text: str) -> str:
        """Извлекает Python-код из ответа модели."""
        # Убираем <think>
        text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
        # Ищем ```python ... ```
        m = re.search(r'```(?:python|py)?\s*\n(.*?)```', text, re.DOTALL)
        if m:
            return m.group(1).strip()
        # Ищем import/def/print
        lines = text.split('\n')
        code_start = 0
        for i, line in enumerate(lines):
            if re.match(r'^\s*(import|from|def|class|print|if|for|while|try|df\d*|pd\.|np\.)', line.strip()):
                code_start = i
                break
        code = '\n'.join(lines[code_start:]).strip()
        return code
