import os
#!/usr/bin/env python3
"""
ETL Bridge: Baserow API → PostgreSQL flat tables → Metabase visualization.
Reads all Baserow tables via REST API and writes them as flat PostgreSQL tables
that Metabase can query directly.

Usage: python3 export_baserow_to_postgres.py [--database DATABASE_ID]
"""
import requests
import psycopg2
import json
import sys
import os
from datetime import datetime

# ── Config ──
BASEROW_URL = "http://localhost:8000"
JWT_EMAIL = os.getenv("BASEROW_EMAIL", "")
JWT_PASS = os.getenv("BASEROW_PASSWORD", "")

PG_HOST = "localhost"
PG_PORT = 5432
PG_DB = "baserow"
PG_USER = "baserow"
PG_PASS = "StrongPassword123"
PG_SCHEMA = "flat"  # separate schema for flat tables

# Databases to export (None = all)
TARGET_DBS = None  # or [362, 363, 394, 395]


def get_jwt():
    resp = requests.post(f"{BASEROW_URL}/api/user/token-auth/",
        json={"email": JWT_EMAIL, "password": JWT_PASS}, timeout=10)
    resp.raise_for_status()
    return resp.json()["access_token"]


def get_databases(jwt):
    headers = {"Authorization": f"JWT {jwt}"}
    resp = requests.get(f"{BASEROW_URL}/api/applications/", headers=headers, timeout=10)
    resp.raise_for_status()
    return resp.json()


def get_tables(jwt, db_id):
    headers = {"Authorization": f"JWT {jwt}"}
    resp = requests.get(f"{BASEROW_URL}/api/database/tables/database/{db_id}/",
        headers=headers, timeout=10)
    resp.raise_for_status()
    return resp.json()


def get_rows(jwt, table_id):
    """Fetch ALL rows from a Baserow table."""
    headers = {"Authorization": f"JWT {jwt}"}
    rows = []
    page = 1
    while True:
        resp = requests.get(
            f"{BASEROW_URL}/api/database/rows/table/{table_id}/",
            headers=headers,
            params={"page": page, "size": 200, "user_field_names": "true"},
            timeout=30)
        resp.raise_for_status()
        data = resp.json()
        rows.extend(data["results"])
        if not data.get("next"):
            break
        page += 1
    return rows


def infer_pg_type(value):
    """Infer PostgreSQL type from Python value."""
    if value is None:
        return "TEXT"
    if isinstance(value, bool):
        return "BOOLEAN"
    if isinstance(value, int):
        return "NUMERIC"
    if isinstance(value, float):
        return "NUMERIC"
    s = str(value)
    # Check if it's a date
    for fmt in ["%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%SZ",
                "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%S%z"]:
        try:
            datetime.strptime(s[:26] if len(s) > 26 else s, fmt)
            return "TIMESTAMP"
        except:
            continue
    try:
        float(s.replace(",", ".").replace(" ", ""))
        return "NUMERIC"
    except:
        pass
    return "TEXT"


def safe_table_name(name):
    """Convert Baserow table name to safe PostgreSQL identifier."""
    import re
    name = name.lower().strip()
    name = re.sub(r'[^a-z0-9_]', '_', name)
    name = re.sub(r'_+', '_', name)
    return f"br_{name}"[:63]


def create_flat_table(cursor, schema, table_name, columns, sample_values):
    """Create a flat PostgreSQL table based on inferred schema."""
    cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {schema}")
    
    # Build column definitions
    col_defs = ['id SERIAL PRIMARY KEY']
    for col in columns:
        safe_col = f'"{col}"'  # quote column names
        pg_type = infer_pg_type(sample_values.get(col))
        col_defs.append(f"{safe_col} {pg_type}")
    
    # Drop and recreate
    cursor.execute(f"DROP TABLE IF EXISTS {schema}.{table_name} CASCADE")
    create_sql = f"CREATE TABLE {schema}.{table_name} ({', '.join(col_defs)})"
    cursor.execute(create_sql)
    return True


def insert_rows(cursor, schema, table_name, columns, rows):
    """Insert data into flat table."""
    if not rows:
        return 0
    
    safe_cols = [f'"{c}"' for c in columns]
    placeholders = ', '.join(['%s'] * len(columns))
    insert_sql = f"INSERT INTO {schema}.{table_name} ({', '.join(safe_cols)}) VALUES ({placeholders})"
    
    count = 0
    for row in rows:
        values = []
        for col in columns:
            val = row.get(col)
            if val is None:
                values.append(None)
            elif isinstance(val, (int, float, bool)):
                values.append(val)
            else:
                # Try numeric
                try:
                    values.append(float(str(val).replace(",", ".").replace(" ", "")))
                except:
                    values.append(str(val)[:10000])  # truncate long text
        try:
            cursor.execute(insert_sql, values)
            count += 1
        except Exception as e:
            print(f"  WARN: row insert failed: {e}")
    
    return count


def main():
    print("=" * 60)
    print("Baserow → PostgreSQL ETL Bridge")
    print("=" * 60)
    
    # Connect to PostgreSQL
    print("\nConnecting to PostgreSQL...")
    conn = psycopg2.connect(
        host=PG_HOST, port=PG_PORT, dbname=PG_DB,
        user=PG_USER, password=PG_PASS
    )
    cursor = conn.cursor()
    print("Connected.")
    
    # Get JWT
    print("\nAuthenticating with Baserow...")
    jwt = get_jwt()
    print("Authenticated.")
    
    # Get databases
    databases = get_databases(jwt)
    if TARGET_DBS:
        databases = [d for d in databases if d['id'] in TARGET_DBS]
    
    total_tables = 0
    total_rows = 0
    
    for db in databases:
        db_id = db['id']
        db_name = db['name']
        print(f"\n{'─'*40}")
        print(f"Database: {db_name} (ID: {db_id})")
        
        tables = get_tables(jwt, db_id)
        for table in tables:
            table_id = table['id']
            table_name = table['name']
            print(f"  Table: {table_name} (ID: {table_id})", end=" ")
            
            # Fetch rows
            try:
                rows = get_rows(jwt, table_id)
            except Exception as e:
                print(f"→ SKIP (fetch error: {e})")
                continue
            
            if not rows:
                print(f"→ SKIP (empty)")
                continue
            
            # Get columns (from first row)
            columns = [k for k in rows[0].keys() 
                      if k not in ('id', 'order', '')]
            
            # Get sample values for type inference
            sample_values = {}
            for col in columns:
                for row in rows:
                    if row.get(col) is not None:
                        sample_values[col] = row[col]
                        break
            
            # Create flat table
            pg_table = safe_table_name(table_name)
            try:
                create_flat_table(cursor, PG_SCHEMA, pg_table, columns, sample_values)
                count = insert_rows(cursor, PG_SCHEMA, pg_table, columns, rows)
                conn.commit()
                print(f"→ {pg_table}: {count} rows")
                total_tables += 1
                total_rows += count
            except Exception as e:
                print(f"→ FAIL: {e}")
                conn.rollback()
    
    cursor.close()
    conn.close()
    
    print(f"\n{'='*60}")
    print(f"DONE: {total_tables} tables, {total_rows} rows exported to schema '{PG_SCHEMA}'")
    print(f"Metabase can now query these tables at: {PG_SCHEMA}.<table_name>")
    print(f"Run 'Sync schema' in Metabase admin to load them.")


if __name__ == "__main__":
    main()
