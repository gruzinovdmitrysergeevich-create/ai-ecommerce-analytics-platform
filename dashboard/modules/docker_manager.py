#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Управление Docker-контейнерами через docker-compose.
"""

import subprocess
import os

COMPOSE_DIR = os.path.expanduser("~/my-ai-stack")

def docker_action(action: str, target: str = "", tail: int = 50) -> str:
    """
    action: up, down, start, stop, restart, logs
    target: имя контейнера (для start/stop/logs) или пусто
    """
    env = os.environ.copy()
    env["COMPOSE_PROJECT_NAME"] = "ai-stack"

    if action == "up":
        cmd = f"cd {COMPOSE_DIR} && docker-compose up -d"
    elif action == "down":
        cmd = f"cd {COMPOSE_DIR} && docker-compose down"
    elif action == "start":
        cmd = f"docker start {target}"
    elif action == "stop":
        cmd = f"docker stop {target}"
    elif action == "restart":
        cmd = f"cd {COMPOSE_DIR} && docker-compose restart"
    elif action == "logs":
        if target:
            cmd = f"docker logs --tail {tail} {target}"
        else:
            cmd = f"cd {COMPOSE_DIR} && docker-compose logs --tail {tail}"
    else:
        return f"Unknown action: {action}"

    try:
        p = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
        return p.stdout if p.returncode == 0 else f"ERR: {p.stderr}"
    except subprocess.TimeoutExpired:
        return "Timeout (60s)"
    except Exception as e:
        return f"Exception: {e}"
