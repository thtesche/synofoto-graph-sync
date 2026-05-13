import psycopg2
from psycopg2.extras import RealDictCursor
import logging

logger = logging.getLogger(__name__)

class MetadataExtractor:
    def __init__(self, config):
        self.config = config
        self.conn = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(**self.config)
            logger.info("Connected to PostgreSQL")
        except Exception as e:
            logger.error(f"Failed to connect to PostgreSQL: {e}")
            raise

    def check_connection(self):
        """Simple check to see if database is reachable."""
        try:
            if not self.conn:
                self.connect()
            with self.conn.cursor() as cursor:
                cursor.execute("SELECT 1")
            return True
        except Exception as e:
            logger.error(f"PostgreSQL connection check failed: {e}")
            return False

    def close(self):
        if self.conn:
            self.conn.close()

    def fetch_media_with_people(self, owner=None):
        """
        Fetches media units and their associated recognized people.
        Note: The schema might vary slightly depending on the Synology Photos version.
        This query joins unit, person via the relationship table.
        """
        query = """
        SELECT 
            u.id AS unit_id,
            u.filename,
            f.name AS folder_path,
            p.name AS person_name,
            ui.name AS owner_name
        FROM unit u
        LEFT JOIN folder f ON u.id_folder = f.id
        LEFT JOIN many_unit_has_many_person mup ON u.id = mup.unit_id
        LEFT JOIN person p ON mup.person_id = p.id
        JOIN user_info ui ON u.id_user = ui.id
        """
        params = []
            
        query += " WHERE u.type = 0" # Assuming 0 is image
        
        if owner:
            query += " AND ui.name = %s"
            params.append(owner)
            
        query += " ORDER BY u.id;"
        
        results = []
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
                if params:
                    cursor.execute(query, tuple(params))
                else:
                    cursor.execute(query)
                rows = cursor.fetchall()
                
                # Group by unit_id since one media can have multiple people
                media_map = {}
                for row in rows:
                    uid = row['unit_id']
                    if uid not in media_map:
                        media_map[uid] = {
                            'unit_id': uid,
                            'filename': row['filename'],
                            'folder_path': row['folder_path'],
                            'owner_name': row['owner_name'],
                            'people': []
                        }
                    if row['person_name']:
                        media_map[uid]['people'].append(row['person_name'])
                
                results = list(media_map.values())
        except Exception as e:
            logger.error(f"Error fetching metadata: {e}")
            
        return results

    def fetch_media_by_path(self, path_substring, owner=None):
        """
        Fetches media units matching a specific folder path.
        """
        query = """
        SELECT 
            u.id AS id,
            u.filename AS filename,
            f.name AS folder,
            ui.name AS owner_name
        FROM unit u
        JOIN folder f ON u.id_folder = f.id
        JOIN user_info ui ON u.id_user = ui.id
        """
        params = [f"%{path_substring}%"]
            
        query += " WHERE f.name LIKE %s AND u.type = 0"
        
        if owner:
            query += " AND ui.name = %s"
            params.append(owner)
            
        query += " ORDER BY u.id;"
        
        results = []
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, tuple(params))
                rows = cursor.fetchall()
                results = [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error fetching metadata by path: {e}")
            try:
                self.conn.rollback()
                query_fallback = query.replace("id_folder", "folder_id")
                with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute(query_fallback, tuple(params))
                    rows = cursor.fetchall()
                    results = [dict(row) for row in rows]
            except Exception as fallback_e:
                logger.error(f"Fallback error fetching metadata: {fallback_e}")
            
        return results

if __name__ == "__main__":
    # Test block
    logging.basicConfig(level=logging.INFO)
    PG_CONFIG = {
        "database": "synofoto",
        "user": "postgres",
        "host": "/run/postgresql/",
        "port": "5432"
    }
    extractor = MetadataExtractor(PG_CONFIG)
    try:
        extractor.connect()
        data = extractor.fetch_media_with_people()
        print(f"Fetched {len(data)} media items.")
        if data:
            print(f"Sample item: {data[0]}")
    except Exception:
        pass
    finally:
        extractor.close()
