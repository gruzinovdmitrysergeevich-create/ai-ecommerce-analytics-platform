#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Управление Ollama (локально и на стационаре) + vLLM.
"""

import subprocess
import os
import signal

STATION_IP = "100.64.243.115"
STATION_USER = "werna"
STATION_PASS = "1981vbars"
LOCAL_MODELS_PATH = "/home/werna81/Ollama_System/models"
VLLM_DIR = os.path.expanduser("~/my-ai-stack")
VLLM_PID_FILE = os.path.join(VLLM_DIR, "vllm_reranker.pid")
VLLM_LOG = os.path.join(VLLM_DIR, "vllm_reranker.log")
VLLM_PORT = 8001
VLLM_MODEL = os.path.join(VLLM_DIR, "vllm_models/Qwen3-Reranker-4B")
VLLM_VENV = os.path.join(VLLM_DIR, "venv_vllm")

def _run(cmd: str, timeout=15) -> str:
    try:
        p = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return p.stdout if p.returncode == 0 else f"ERR: {p.stderr}"
    except Exception as e:
        return f"Exception: {e}"

def ollama_action(location: str, action: str) -> str:
    """
    location: 'local' | 'station'
    action: 'start' | 'stop' | 'status'
    """
    if location == "local":
        if action == "start":
            rc, _, _ = subprocess.run("ss -tln | grep -q :11434", shell=True, capture_output=True).returncode, "", ""
            if rc == 0:
                return "Уже запущена"
            env = f"OLLAMA_MODELS={LOCAL_MODELS_PATH} OLLAMA_HOST=0.0.0.0"
            cmd = f"{env} nohup ollama serve > /dev/null 2>&1 &"
            subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return "Запускается..."
        elif action == "stop":
            subprocess.run("pkill -f 'ollama serve'", shell=True)
            return "Остановлена"

    elif location == "station":
        ssh_opts = "-o ConnectTimeout=5 -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"
        if action == "start":
            cmd = (
                f"sshpass -p '{STATION_PASS}' ssh {ssh_opts} {STATION_USER}@{STATION_IP} "
                f"\"powershell Start-ScheduledTask -TaskName 'OllamaServer'\""
            )
            _run(cmd, timeout=10)
            return "Задача планировщика запущена"
        elif action == "stop":
            cmd1 = (
                f"sshpass -p '{STATION_PASS}' ssh {ssh_opts} {STATION_USER}@{STATION_IP} "
                f"\"powershell Stop-ScheduledTask -TaskName 'OllamaServer'\""
            )
            cmd2 = (
                f"sshpass -p '{STATION_PASS}' ssh {ssh_opts} {STATION_USER}@{STATION_IP} "
                f"\"taskkill /F /IM ollama.exe\""
            )
            _run(cmd1, timeout=10)
            _run(cmd2, timeout=10)
            return "Остановлена"

    return "Unknown"

def vllm_action(action: str) -> str:
    if action == "start":
        if os.path.exists(VLLM_PID_FILE):
            try:
                with open(VLLM_PID_FILE, "r") as f:
                    pid = int(f.read().strip())
                if os.path.exists(f"/proc/{pid}"):
                    return "Уже запущен"
            except Exception:
                pass

        if not os.path.isdir(VLLM_VENV):
            return f"Виртуальное окружение не найдено: {VLLM_VENV}"

        activate = os.path.join(VLLM_VENV, "bin", "activate")
        cmd = (
            f"cd {VLLM_DIR} && source {activate} && "
            f"nohup python -m vllm.entrypoints.openai.api_server "
            f"--model {VLLM_MODEL} --port {VLLM_PORT} "
            f"--api-key ragflow-reranker-key --max-model-len 8192 "
            f"--gpu-memory-utilization 0.9 > {VLLM_LOG} 2>&1 & "
            f"echo $! > {VLLM_PID_FILE}"
        )
        subprocess.Popen(cmd, shell=True, executable="/bin/bash", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return "Запускается (фон)..."

    elif action == "stop":
        if os.path.exists(VLLM_PID_FILE):
            try:
                with open(VLLM_PID_FILE, "r") as f:
                    pid = int(f.read().strip())
                os.kill(pid, signal.SIGTERM)
            except Exception:
                pass
            os.remove(VLLM_PID_FILE)
        subprocess.run("pkill -f 'vllm.*Qwen3-Reranker-4B'", shell=True)
        return "Остановлен"

    return "Unknown"
