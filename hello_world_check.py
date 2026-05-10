"""
FILE: hello_world_check.py
DESCRIPTION: Testet die Verbindung zu PostgreSQL (Synology) und Neo4j (Docker).
"""

import psycopg2
from py2neo import Graph
import sys

# --- KONFIGURATION ---
PG_CONFIG = {
    "database": "synofoto",
    "user": "postgres",
    "host": "/run/postgresql/", # Unix-Socket Pfad
    "port": "5432"
}

NEO4J_CONFIG = {
    "uri": "bolt://localhost:7687", # Falls Skript auf NAS läuft, sonst NAS-IP
    "user": "neo4j",
    "password": "dein_passwort"
}

def test_connections():
    print("--- Verbindungstest startet ---")

    # 1. Test PostgreSQL (Synology Photos)
    try:
        pg_conn = psycopg2.connect(**PG_CONFIG)
        cursor = pg_conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM unit;")
        count = cursor.fetchone()[0]
        print(f"[OK] PostgreSQL: Verbindung erfolgreich. Bilder in DB: {count}")
        cursor.close()
        pg_conn.close()
    except Exception as e:
        print(f"[FEHLER] PostgreSQL: {e}")

    # 2. Test Neo4j (Docker)
    try:
        graph = Graph(NEO4J_CONFIG["uri"], auth=(NEO4J_CONFIG["user"], NEO4J_CONFIG["password"]))
        # Kleiner Test-Query
        result = graph.run("RETURN 'Verbindung steht!' AS message").evaluate()
        print(f"[OK] Neo4j: {result}")
    except Exception as e:
        print(f"[FEHLER] Neo4j: {e}")

if __name__ == "__main__":
    test_connections()
