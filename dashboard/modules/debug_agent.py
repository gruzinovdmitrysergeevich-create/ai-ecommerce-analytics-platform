#!/usr/bin/env python3
"""
Дебаг-агент: находит и ИСПРАВЛЯЕТ баги в проекте через Hermes (DeepSeek API).
Сканирует файлы, анализирует, применяет исправления, отчитывается.
"""
import os, re, requests
from typing import Dict, Any

DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"
PROJECT_ROOT = os.path.expanduser("~/my-ai-stack")

def _load_api_key():
    key = os.environ.get("DEEPSEEK_API_KEY")
    if key: return key
    env_file = os.path.expanduser("~/.hermes/.env")
    if os.path.exists(env_file):
        with open(env_file) as f:
            for line in f:
                if line.startswith("DEEPSEEK_API_KEY="):
                    return line.strip().split("=",1)[1].strip().strip('"').strip("'")
    return None

def _scan_project() -> str:
    """Сканирует ВЕСЬ проект, исключая venv/node_modules/__pycache__."""
    files = []
    exclude_dirs = {'venv','node_modules','__pycache__','.git','n8n_data','baserow_data',
                    'baserow_postgres_data','n8n_postgres_data','vllm_models','site-packages',
                    'speech-venv','venv_vllm','archive','templates'}
    text_exts = {'.py','.yaml','.yml','.json','.md','.txt','.cfg','.toml'}
    
    for root, dirs, filenames in os.walk(PROJECT_ROOT):
        dirs[:] = [d for d in dirs if d not in exclude_dirs and not d.startswith('.')]
        for fn in filenames:
            ext = os.path.splitext(fn)[1].lower()
            if ext not in text_exts: continue
            fpath = os.path.join(root, fn)
            try:
                fsize = os.path.getsize(fpath)
                if fsize > 100000: continue
                with open(fpath) as f:
                    content = f.read()
                preview = content if fsize <= 5000 else content[:5000] + f"\n... (всего {fsize}B, {content.count(chr(10))} строк)"
                files.append(f"=== {fpath} ({fsize}B) ===\n{preview}")
            except: pass
    
    priority = ['loader','runner','orchestrat','baserow','config','status','docker']
    files.sort(key=lambda item: (
        0 if any(p in item.lower() for p in priority) else 1,
        item
    ))
    return "\n\n".join(files[:25])

def _apply_fixes(code_block: str) -> list:
    """Парсит # file: path и записывает исправленный код. Возвращает список изменённых файлов."""
    changed = []
    # Паттерн: # file: путь/к/файлу
    pattern = re.compile(r'#\s*file\s*:\s*(.+?)\s*\n')
    parts = pattern.split(code_block)
    
    if len(parts) < 3:
        return changed
    
    # parts[0] — текст до первого # file: (игнорируем)
    for i in range(1, len(parts), 2):
        filepath = parts[i].strip()
        code = parts[i+1].strip() if i+1 < len(parts) else ""
        if not code: continue
        
        # Определяем полный путь
        if not filepath.startswith('/'):
            # Пробуем найти относительно PROJECT_ROOT
            candidate = os.path.join(PROJECT_ROOT, filepath)
            if not os.path.exists(os.path.dirname(candidate)):
                # Ищем файл по имени
                for root, dirs, files in os.walk(PROJECT_ROOT):
                    if os.path.basename(filepath) in files:
                        candidate = os.path.join(root, os.path.basename(filepath))
                        break
            
            if not os.path.exists(os.path.dirname(candidate)):
                continue
            filepath = candidate
        
        try:
            # Бэкап
            backup = filepath + ".debug_backup"
            if not os.path.exists(backup):
                with open(filepath) as f:
                    original = f.read()
                with open(backup, 'w') as f:
                    f.write(original)
            
            # Записываем исправленный код
            with open(filepath, 'w') as f:
                f.write(code)
            
            changed.append({
                "file": filepath,
                "backup": backup,
                "size": len(code)
            })
        except Exception as e:
            changed.append({
                "file": filepath,
                "error": str(e)
            })
    
    return changed

def debug_script_with_model(code: str = "", problem: str = "", model: str = "Hermes", apply_fixes: bool = False) -> Dict[str, Any]:
    """Анализирует проект, находит баги. Если apply_fixes=True — применяет исправления.
       По умолчанию ТОЛЬКО анализ (безопасный режим для демо)."""
    result = {
        "analysis": None, "fixed_code": None, "changes": [],
        "error": None, "status": "unknown"
    }
    
    api_key = _load_api_key()
    if not api_key:
        result["error"] = "DEEPSEEK_API_KEY не найден"
        result["status"] = "error"
        return result
    
    project_context = _scan_project()
    problem_text = problem or "Найди и исправь все баги, устаревшие endpoints, дубликаты."
    
    prompt = (
        "Ты — Senior Python-разработчик. НАЙДИ И ИСПРАВЬ проблемы в проекте.\n\n"
        f"ЗАПРОС: {problem_text}\n\n"
        f"ФАЙЛЫ:\n{project_context[:25000]}\n\n"
        "ИНСТРУКЦИЯ:\n"
        "1. Найди ВСЕ баги: импорты, устаревшие API, дубликаты, невалидные конфиги.\n"
        "2. Для каждого — seriousness (critical/warning/info).\n"
        "3. В секции CODE дай ПОЛНЫЙ исправленный код каждого файла.\n"
        "4. Каждый файл предваряй строкой: # file: ПОЛНЫЙ_ПУТЬ_К_ФАЙЛУ\n\n"
        "ФОРМАТ:\n"
        "---ANALYSIS---\n"
        "(анализ: что сломано, как исправлено)\n"
        "---CODE---\n"
        "# file: /home/werna81/my-ai-stack/path/to/file.py\n"
        "(полный исправленный код файла)\n"
        "# file: /home/werna81/my-ai-stack/path/to/another.py\n"
        "(полный исправленный код другого файла)\n"
    )
    
    try:
        resp = requests.post(DEEPSEEK_URL,
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={"model": "deepseek-chat", "messages": [{"role":"user","content":prompt}],
                  "temperature": 0.2, "max_tokens": 4000},
            timeout=180)
        resp.raise_for_status()
        answer = resp.json()["choices"][0]["message"]["content"].strip()
        
        # Парсим
        if "---CODE---" in answer:
            parts = answer.split("---CODE---", 1)
            result["analysis"] = parts[0].replace("---ANALYSIS---", "").strip()
            code_block = parts[1].strip()
            result["fixed_code"] = code_block
            
            # Применяем исправления ТОЛЬКО если явно запрошено
            if apply_fixes:
                changes = _apply_fixes(code_block)
                result["changes"] = changes
            else:
                result["changes"] = [{"info": "Режим анализа. Файлы НЕ изменены. Для применения добавь apply_fixes=True."}]
        else:
            result["analysis"] = answer
        
        result["status"] = "ok"
        result["usage"] = resp.json().get("usage", {})
        
    except requests.exceptions.Timeout:
        result["error"] = "Таймаут DeepSeek API (>180с)"
        result["status"] = "error"
    except Exception as e:
        result["error"] = str(e)
        result["status"] = "error"
    
    return result
