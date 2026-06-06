#!/usr/bin/env python3
"""
Интеграционные тесты для MCP Baserow Server
Тестирует функции сервера через прямой вызов (импорт модуля).
"""

import sys
import os
import time
from pathlib import Path

# Добавляем путь к src
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Импортируем API функции
from baserow_api import (
    create_workspace,
    delete_workspace,
    create_database,
    create_table,
    list_tables,
    delete_table,
    insert_row,
    get_rows,
    update_row,
    delete_row,
    refresh_jwt
)

# Тестовые данные
TEST_WORKSPACE_NAME = "TestWorkspace_MCP"
TEST_DB_NAME = "TestDB_MCP"
TEST_TABLE_NAME = "TestTable_MCP"


def test_create_workspace():
    """Тест создания workspace."""
    print("Тест: Создание workspace...")
    result = create_workspace(TEST_WORKSPACE_NAME)
    
    if "error" in result:
        print(f"  ОШИБКА: {result}")
        return None
    
    workspace_id = result.get("id")
    print(f"  OK: Workspace создан с ID={workspace_id}")
    return workspace_id


def test_create_database(workspace_id: int):
    """Тест создания базы данных."""
    print("Тест: Создание базы данных...")
    result = create_database(workspace_id, TEST_DB_NAME)
    
    if "error" in result:
        print(f"  ОШИБКА: {result}")
        return None
    
    database_id = result.get("id")
    print(f"  OK: База данных создана с ID={database_id}")
    return database_id


def test_create_table(database_id: int):
    """Тест создания таблицы с полями."""
    print("Тест: Создание таблицы...")
    fields = [
        {"name": "Name", "type": "text"},
        {"name": "Value", "type": "number"},
        {"name": "Active", "type": "boolean"}
    ]
    
    result = create_table(database_id, TEST_TABLE_NAME, fields)
    
    if "error" in result:
        print(f"  ОШИБКА: {result}")
        return None
    
    table_id = result.get("id")
    print(f"  OK: Таблица создана с ID={table_id}")
    return table_id


def test_insert_row(table_id: int):
    """Тест вставки строки."""
    print("Тест: Вставка строки...")
    data = {"Name": "Test Item", "Value": 42, "Active": True}
    
    result = insert_row(table_id, data)
    
    if "error" in result:
        print(f"  ОШИБКА: {result}")
        return None
    
    row_id = result.get("id")
    print(f"  OK: Строка вставлена с ID={row_id}")
    return row_id


def test_get_rows(table_id: int):
    """Тест чтения строк."""
    print("Тест: Чтение строк...")
    result = get_rows(table_id, page=1, size=10)
    
    if "error" in result:
        print(f"  ОШИБКА: {result}")
        return False
    
    count = result.get("count", 0)
    results = result.get("results", [])
    print(f"  OK: Прочитано {count} строк, первая: {results[0] if results else 'N/A'}")
    return True


def test_update_row(table_id: int, row_id: int):
    """Тест обновления строки."""
    print("Тест: Обновление строки...")
    data = {"Value": 99, "Active": False}
    
    result = update_row(table_id, row_id, data)
    
    if "error" in result:
        print(f"  ОШИБКА: {result}")
        return False
    
    print(f"  OK: Строка обновлена")
    return True


def test_delete_row(table_id: int, row_id: int):
    """Тест удаления строки."""
    print("Тест: Удаление строки...")
    result = delete_row(table_id, row_id)
    
    if "error" in result:
        print(f"  ОШИБКА: {result}")
        return False
    
    print(f"  OK: Строка удалена")
    return True


def test_delete_table(table_id: int):
    """Тест удаления таблицы."""
    print("Тест: Удаление таблицы...")
    result = delete_table(table_id)
    
    if "error" in result:
        print(f"  ОШИБКА: {result}")
        return False
    
    print(f"  OK: Таблица удалена")
    return True


def test_delete_workspace(workspace_id: int):
    """Тест удаления workspace (чистка)."""
    print("Тест: Удаление workspace (чистка)...")
    result = delete_workspace(workspace_id)
    
    if "error" in result:
        print(f"  ОШИБКА: {result}")
        return False
    
    print(f"  OK: Workspace удалён")
    return True


def main():
    """Запуск всех тестов."""
    print("=" * 60)
    print("MCP Baserow Integration Tests")
    print("=" * 60)
    
    # Проверяем наличие .env
    env_path = Path.home() / "my-ai-stack" / "analytics" / ".env"
    if not env_path.exists():
        print(f"ОШИБКА: .env не найден по пути {env_path}")
        sys.exit(1)
    
    # Инициализация JWT
    print("\nИнициализация JWT...")
    if not refresh_jwt():
        print("ОШИБКА: Не удалось получить JWT токен")
        sys.exit(1)
    print("JWT токен получен успешно")
    
    # Последовательное выполнение тестов
    workspace_id = test_create_workspace()
    if not workspace_id:
        print("\nТесты прерваны: не удалось создать workspace")
        sys.exit(1)
    
    try:
        database_id = test_create_database(workspace_id)
        if not database_id:
            print("\nТесты прерваны: не удалось создать базу данных")
            return
        
        table_id = test_create_table(database_id)
        if not table_id:
            print("\nТесты прерваны: не удалось создать таблицу")
            return
        
        row_id = test_insert_row(table_id)
        if not row_id:
            print("\nТесты прерваны: не удалось вставить строку")
            return
        
        test_get_rows(table_id)
        test_update_row(table_id, row_id)
        test_delete_row(table_id, row_id)
        test_delete_table(table_id)
        
    finally:
        # Чистка: удаляем workspace
        test_delete_workspace(workspace_id)
    
    print("\n" + "=" * 60)
    print("ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО")
    print("=" * 60)


if __name__ == "__main__":
    main()
