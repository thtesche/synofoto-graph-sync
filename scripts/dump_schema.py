import psycopg2
import sys
import os

PG_CONFIG = {
    "database": os.getenv("PG_DB", "synofoto"),
    "user": os.getenv("PG_USER", "postgres"),
    "host": os.getenv("PG_HOST", "/run/postgresql/"),
    "port": os.getenv("PG_PORT", "5432")
}

def dump_schema():
    try:
        conn = psycopg2.connect(**PG_CONFIG)
        cursor = conn.cursor()

        # Alle Tabellen im public Schema abrufen
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()
        
        print("# Synofoto Database Schema\n")
        
        for (table_name,) in tables:
            print(f"## Table: `{table_name}`\n")
            cursor.execute("""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns
                WHERE table_name = %s AND table_schema = 'public'
                ORDER BY ordinal_position;
            """, (table_name,))
            columns = cursor.fetchall()
            
            print("| Column Name | Data Type | Nullable | Default |")
            print("|-------------|-----------|----------|---------|")
            for col_name, data_type, is_nullable, col_default in columns:
                default_val = col_default if col_default else ""
                # Markdown-Escape für eventuelle Pipes in Defaults
                default_val = str(default_val).replace("|", "\\|")
                print(f"| {col_name} | {data_type} | {is_nullable} | {default_val} |")
            print("\n")
            
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error connecting to database or fetching schema: {e}")

if __name__ == "__main__":
    dump_schema()
