import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

load_dotenv()

def debug_address(unit_ids):
    conn = psycopg2.connect(
        dbname=os.getenv("PG_DB"),
        user=os.getenv("PG_USER"),
        password=os.getenv("PG_PASSWORD"),
        host=os.getenv("PG_HOST"),
        port=os.getenv("PG_PORT", 5432)
    )
    
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            for uid in unit_ids:
                print(f"\n--- Debugging Unit ID: {uid} ---")
                cur.execute("""
                    SELECT level, value, lang 
                    FROM address 
                    WHERE id_unit = %s 
                    ORDER BY level, lang
                """, (uid,))
                rows = cur.fetchall()
                for row in rows:
                    print(f"Level: {row['level']} | Lang: {row['lang']} | Value: {row['value']}")
    finally:
        conn.close()

if __name__ == "__main__":
    # Wir nehmen mal ein paar IDs aus deinen Beispielen, falls du sie parat hast.
    # Da ich die IDs nicht kenne, suche ich mal nach 'Deutschland' und 'France' Einheiten.
    conn = psycopg2.connect(
        dbname=os.getenv("PG_DB"),
        user=os.getenv("PG_USER"),
        password=os.getenv("PG_PASSWORD"),
        host=os.getenv("PG_HOST")
    )
    with conn.cursor() as cur:
        cur.execute("SELECT id_unit FROM address WHERE value = 'Deutschland' LIMIT 2")
        de_ids = [r[0] for r in cur.fetchall()]
        cur.execute("SELECT id_unit FROM address WHERE value = 'France' LIMIT 2")
        fr_ids = [r[0] for r in cur.fetchall()]
        
    debug_address(de_ids + fr_ids)
