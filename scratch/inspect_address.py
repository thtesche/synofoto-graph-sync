import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

load_dotenv()

def inspect_address_data(unit_id):
    conn = psycopg2.connect(
        dbname=os.getenv("PG_DB", "synofoto"),
        user=os.getenv("PG_USER", "postgres"),
        password=os.getenv("PG_PASSWORD"),
        host=os.getenv("PG_HOST", "/run/postgresql/"),
        port=os.getenv("PG_PORT", 5432)
    )
    
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            print(f"\n--- Full Inspection for Unit ID: {unit_id} ---")
            cur.execute("SELECT * FROM address WHERE id_unit = %s ORDER BY level", (unit_id,))
            rows = cur.fetchall()
            for row in rows:
                print(row)
    finally:
        conn.close()

if __name__ == "__main__":
    inspect_address_data(54133)
