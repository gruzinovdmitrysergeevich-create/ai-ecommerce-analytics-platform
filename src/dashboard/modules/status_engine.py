import os
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Движок проверки статусов всех компонентов AI-стека.
Использует subprocess, curl, pgrep для получения реального состояния.
"""

import subprocess
import os
import json
import requests
from typing import Dict, List, Any

BASEROW_TOKEN = os.getenv("BASEROW_TOKEN", "")
STATION_IP = "100.64.243.115"
VLLM_PORT = 8001

def _run(cmd: str, timeout=5) -> tuple:
    try:
        p = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return p.returncode, p.stdout, p.stderr
    except Exception as e:
        return -1, "", str(e)

def _curl_code(url: str, timeout=3) -> int:
    try:
        r = requests.head(url, timeout=timeout, allow_redirects=True)
        return r.status_code
    except Exception:
        return 0

def get_overview_status() -> Dict[str, Any]:
    """Сводный статус всего стека."""
    status = {}

    # Docker
    rc, _, _ = _run("systemctl is-active docker")
    status["docker_running"] = (rc == 0)

    # Ollama local
    rc, _, _ = _run("ss -tln | grep -q :11434")
    status["ollama_local"] = (rc == 0)
    if status["ollama_local"]:
        try:
            r = requests.get("http://localhost:11434/api/tags", timeout=3)
            if r.status_code == 200:
                status["local_models"] = r.json().get("models", [])
            else:
                status["local_models"] = []
        except Exception:
            status["local_models"] = []
    else:
        status["local_models"] = []

    # vLLM
    status["vllm_running"] = (_curl_code(f"http://127.0.0.1:{VLLM_PORT}/v1/models") == 200)
    status["vllm_port"] = VLLM_PORT

    # Tailscale — проверяем доступность стационара
    rc, _, _ = _run(f"ping -c 1 -W 1 {STATION_IP} > /dev/null 2>&1")
    status["tailscale_ok"] = (rc == 0)
    status["tailscale_ip"] = STATION_IP if status["tailscale_ok"] else "N/A"

    # Baserow
    status["baserow_ready"] = (_curl_code("http://localhost:8000") == 200)

    # Qdrant
    status["qdrant_ready"] = (_curl_code("http://localhost:6333/dashboard") == 200)

    # Metabase
    status["metabase_ready"] = (_curl_code("http://localhost:3001") == 200)

    # Контейнеры
    rc, out, _ = _run("docker ps -q | wc -l")
    try:
        status["containers_running"] = int(out.strip()) if rc == 0 else 0
    except ValueError:
        status["containers_running"] = 0

    # БД готовность
    status["db_ready"] = status.get("baserow_ready", False)

    # Стационар
    status["ollama_station"] = get_ollama_station_status()

    # Загрузчики
    loaders_dir = os.path.expanduser("~/my-ai-stack/analytics/loaders")
    status["loader_count"] = len([f for f in os.listdir(loaders_dir) if f.endswith(".py")]) if os.path.exists(loaders_dir) else 0

    return status

def get_docker_status() -> List[Dict[str, Any]]:
    """Статус Docker-контейнеров из docker-compose."""
    compose_dir = os.path.expanduser("~/my-ai-stack")
    containers = []
    # Список ожидаемых контейнеров с портами
    expected = [
        {"name": "baserow", "port": 8000},
        {"name": "baserow-postgres", "port": 5432},
        {"name": "baserow-redis", "port": None},
        {"name": "qdrant", "port": 6333},
        {"name": "metabase", "port": 3001},
        {"name": "n8n", "port": 5678},
        {"name": "flowise", "port": 3000},
        {"name": "n8n-postgres", "port": None},
    ]

    rc, out, _ = _run("docker ps --format '{{.Names}}|{{.Status}}|{{.Ports}}'", timeout=5)
    running_names = set()
    status_map = {}
    if rc == 0:
        for line in out.strip().split("\n"):
            if "|" in line:
                parts = line.split("|")
                name = parts[0]
                status_text = parts[1] if len(parts) > 1 else "unknown"
                ports = parts[2] if len(parts) > 2 else ""
                running_names.add(name)
                status_map[name] = {"status": status_text, "ports": ports}

    for exp in expected:
        name = exp["name"]
        is_running = name in running_names
        containers.append({
            "name": name,
            "running": is_running,
            "port": exp["port"],
            "status": status_map.get(name, {}).get("status", "stopped"),
        })
    return containers

def get_ollama_local_status() -> Dict[str, Any]:
    rc, _, _ = _run("ss -tln | grep -q :11434")
    running = (rc == 0)
    models = []
    if running:
        try:
            r = requests.get("http://localhost:11434/api/tags", timeout=3)
            if r.status_code == 200:
                data = r.json()
                for m in data.get("models", []):
                    models.append({"name": m.get("name", "?"), "size": m.get("size", "N/A")})
        except Exception:
            pass
    return {"running": running, "models": models}

def get_ollama_station_status() -> Dict[str, Any]:
    result = {"running": False, "ip": STATION_IP, "models": [], "gpu": None}
    rc, _, _ = _run(f"ping -c 1 -W 1 {STATION_IP} > /dev/null 2>&1")
    if rc != 0:
        return result
    try:
        r = requests.get(f"http://{STATION_IP}:11434/api/tags", timeout=5)
        if r.status_code == 200:
            result["running"] = True
            data = r.json()
            for m in data.get("models", []):
                result["models"].append(m.get("name", "?"))
    except Exception:
        pass
    # GPU через SSH (опционально, если ключи настроены)
    rc, out, _ = _run(
        f"ssh -o ConnectTimeout=3 -o BatchMode=yes werna@{STATION_IP} "
        f"\"powershell -Command & 'C:\\\\Program Files\\\\NVIDIA Corporation\\\\NVSMI\\\\nvidia-smi.exe' --query-gpu=utilization.gpu,memory.used,memory.total --format=csv,noheader\" 2>/dev/null",
        timeout=8,
    )
    if rc == 0 and out.strip():
        parts = out.strip().split(",")
        if len(parts) >= 3:
            result["gpu"] = {
                "util": parts[0].strip().replace(" %", ""),
                "mem_used": parts[1].strip().replace(" MiB", ""),
                "mem_total": parts[2].strip().replace(" MiB", ""),
            }
    return result

def get_vllm_status() -> Dict[str, Any]:
    running = (_curl_code(f"http://127.0.0.1:{VLLM_PORT}/v1/models") == 200)
    pid = None
    log_tail = ""
    vllm_dir = os.path.expanduser("~/my-ai-stack")
    log_file = os.path.join(vllm_dir, "vllm_reranker.log")
    if os.path.exists(log_file):
        try:
            with open(log_file, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
                log_tail = "".join(lines[-30:])
        except Exception:
            pass
    pid_file = os.path.join(vllm_dir, "vllm_reranker.pid")
    if os.path.exists(pid_file):
        try:
            with open(pid_file, "r") as f:
                pid = f.read().strip()
        except Exception:
            pass
    return {"running": running, "port": VLLM_PORT, "pid": pid, "log_tail": log_tail}

def get_tailscale_status() -> Dict[str, Any]:
    rc, out, _ = _run("tailscale ip -4 2>/dev/null | head -1")
    ok = (rc == 0 and out.strip() != "")
    return {"ok": ok, "ip": out.strip() if ok else "N/A"}

def get_metabase_status() -> bool:
    return _curl_code("http://localhost:3001") == 200

def get_baserow_status() -> bool:
    return _curl_code("http://localhost:8000") == 200

def get_qdrant_status() -> bool:
    return _curl_code("http://localhost:6333/dashboard") == 200
