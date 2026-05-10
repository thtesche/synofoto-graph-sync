"""
FILE: scripts/hello_world_check.py
DESCRIPTION: Connection test for PostgreSQL (Synology) and Neo4j (Docker).
"""

import psycopg2
from py2neo import Graph
import sys

# --- CONFIGURATION ---
PG_CONFIG = {
    "database": "synofoto",
    "user": "postgres",
    "host": "/run/postgresql/", # Unix socket path
    "port": "5432"
}

NEO4J_CONFIG = {
    "uri": "bolt://localhost:7687", # NAS IP if running elsewhere
    "user": "neo4j",
    "password": "your_password"
}

def test_connections():
    print("--- Starting connection test ---")

    # 1. Test PostgreSQL (Synology Photos)
    try:
        pg_conn = psycopg2.connect(**PG_CONFIG)
        cursor = pg_conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM unit;")
        count = cursor.fetchone()[0]
        print(f"[OK] PostgreSQL: Connection successful. Images in DB: {count}")
        cursor.close()
        pg_conn.close()
    except Exception as e:
        print(f"[ERROR] PostgreSQL: {e}")

    # 2. Test Neo4j (Docker)
    try:
        graph = Graph(NEO4J_CONFIG["uri"], auth=(NEO4J_CONFIG["user"], NEO4J_CONFIG["password"]))
        # Small test query
        result = graph.run("RETURN 'Connection established!' AS message").evaluate()
        print(f"[OK] Neo4j: {result}")
    except Exception as e:
        print(f"[ERROR] Neo4j: {e}")

if __name__ == "__main__":
    test_connections()
