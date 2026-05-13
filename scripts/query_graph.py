import os
import sys
from neo4j import GraphDatabase
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

URI = os.getenv("GRAPHDB_URI", "bolt://localhost:7687")
USER = os.getenv("GRAPHDB_USER", "neo4j")
PASSWORD = os.getenv("GRAPHDB_PASSWORD", "password")

def run_query(query):
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    try:
        with driver.session() as session:
            result = session.run(query)
            records = list(result)
            
            if not records:
                print("No results found.")
                return

            # Get keys (column names)
            keys = result.keys()
            
            # Calculate column widths
            widths = {key: len(key) for key in keys}
            data_rows = []
            
            for record in records:
                row = []
                for key in keys:
                    val = str(record[key])
                    widths[key] = max(widths[key], len(val))
                    row.append(val)
                data_rows.append(row)
            
            # Print Header
            header = " | ".join(key.ljust(widths[key]) for key in keys)
            print("-" * len(header))
            print(header)
            print("-" * len(header))
            
            # Print Rows
            for row in data_rows:
                print(" | ".join(val.ljust(widths[key]) for val, key in zip(row, keys)))
            print("-" * len(header))
            print(f"Total: {len(records)} records")

    except Exception as e:
        print(f"Error executing query: {e}")
    finally:
        driver.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python query_graph.py \"MATCH (n) RETURN n LIMIT 5\"")
        sys.exit(1)
    
    query = " ".join(sys.argv[1:])
    run_query(query)
