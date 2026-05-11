import os
import psycopg2
from py2neo import Graph
from dotenv import load_dotenv
import sys

# Load environment variables from .env file
load_dotenv()

# --- CONFIGURATION ---
PG_CONFIG = {
    "database": os.getenv("PG_DB", "synofoto"),
    "user": os.getenv("PG_USER", "postgres"),
    "host": os.getenv("PG_HOST", "/run/postgresql/"),
    "port": os.getenv("PG_PORT", "5432")
}

NEO4J_CONFIG = {
    "uri": os.getenv("NEO4J_URI", "bolt://localhost:7687"),
    "user": os.getenv("NEO4J_USER", "neo4j"),
    "password": os.getenv("NEO4J_PASSWORD", "your_password")
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
