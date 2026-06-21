import logging
import os
from dotenv import load_dotenv
import psycopg2
from neo4j import GraphDatabase

# Load environment variables from .env file
load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class GraphCleanup:
    def __init__(self, pg_config=None, graph_uri=None, graph_user=None, graph_password=None):
        # Use provided config or fallback to environment variables
        self.pg_config = pg_config or {
            "database": os.getenv("PG_DB"),
            "user": os.getenv("PG_USER"),
            "host": os.getenv("PG_HOST"),
            "port": os.getenv("PG_PORT")
        }
        self.graph_uri = graph_uri or os.getenv("GRAPHDB_URI")
        self.graph_user = graph_user or os.getenv("GRAPHDB_USER")
        self.graph_password = graph_password or os.getenv("GRAPHDB_PASSWORD")
        
        self.pg_conn = None
        self.graph_driver = None

    def connect(self):
        # Connect to PostgreSQL
        try:
            self.pg_conn = psycopg2.connect(**self.pg_config)
            logger.info("Connected to PostgreSQL")
        except Exception as e:
            logger.error(f"Failed to connect to PostgreSQL: {e}")
            raise

        # Connect to Graph DB
        try:
            driver_kwargs = {
                "uri": self.graph_uri,
                "connection_timeout": 120.0,
                "max_connection_lifetime": 600.0
            }
            if self.graph_user:
                driver_kwargs["auth"] = (self.graph_user, self.graph_password or "")
            else:
                driver_kwargs["auth"] = ("", "")
            self.graph_driver = GraphDatabase.driver(**driver_kwargs)
            self.graph_driver.verify_connectivity()
            logger.info("Connected to Graph Database")
        except Exception as e:
            logger.error(f"Failed to connect to Graph Database: {e}")
            raise

    def close(self):
        if self.pg_conn:
            self.pg_conn.close()
        if self.graph_driver:
            self.graph_driver.close()

    def cleanup_orphaned_photos(self):
        """
        Iterates over all Photo nodes in the Graph DB and deletes them if they 
        no longer exist in the PostgreSQL 'unit' table.
        """
        with self.graph_driver.session() as session:
            # 1. Get all Photo IDs from Graph DB
            result = session.run("MATCH (p:Photo) RETURN p.id AS id")
            graph_ids = [record["id"] for record in result]
            
        if not graph_ids:
            logger.info("No Photo nodes found in Graph DB.")
            return

        logger.info(f"Checking {len(graph_ids)} Photo nodes against PostgreSQL...")

        # 2. Check which IDs still exist in Postgres
        existing_ids = set()
        try:
            with self.pg_conn.cursor() as cursor:
                # Using a tuple for the IN clause
                cursor.execute("SELECT id FROM unit WHERE id = ANY(%s)", (graph_ids,))
                existing_ids = {row[0] for row in cursor.fetchall()}
        except Exception as e:
            logger.error(f"Error querying PostgreSQL: {e}")
            return

        # 3. Identify IDs to delete (in Graph but not in Postgres)
        ids_to_delete = [pid for pid in graph_ids if pid not in existing_ids]
        
        if not ids_to_delete:
            logger.info("No orphaned Photo nodes found.")
            return

        logger.info(f"Found {len(ids_to_delete)} orphaned Photo nodes to delete.")

        # 4. Delete from Graph DB (including relationships)
        with self.graph_driver.session() as session:
            # DETACH DELETE removes the node and all its relationships
            delete_query = "MATCH (p:Photo) WHERE p.id IN $ids DETACH DELETE p"
            session.run(delete_query, ids=ids_to_delete)
        
        logger.info(f"Successfully deleted {len(ids_to_delete)} orphaned Photo nodes.")

if __name__ == "__main__":
    cleanup = GraphCleanup()
    try:
        cleanup.connect()
        cleanup.cleanup_orphaned_photos()
    except Exception as e:
        logger.error(f"Cleanup failed: {e}")
    finally:
        cleanup.close()
