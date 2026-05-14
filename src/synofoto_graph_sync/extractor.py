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

    def _get_base_query(self):
        return """
        SELECT 
            u.id AS unit_id,
            u.filename,
            u.takentime,
            u.cache_key,
            f.name AS folder_path,
            ui.name AS owner_name,
            m.latitude, 
            m.longitude,
            (SELECT array_agg(DISTINCT p.name) 
             FROM face fc 
             JOIN person p ON fc.id_person = p.id 
             WHERE fc.id_unit = u.id) AS people,
            (SELECT array_agg(DISTINCT gt.name) 
             FROM many_unit_has_many_general_tag muht 
             JOIN general_tag gt ON muht.id_general_tag = gt.id 
             WHERE muht.id_unit = u.id) AS tags,
            (SELECT jsonb_agg(jsonb_build_object('level', ad.level, 'value', ad.value) ORDER BY ad.level) 
             FROM address ad 
             WHERE ad.id_unit = u.id AND ad.lang = 0) AS address_parts
        FROM unit u
        LEFT JOIN folder f ON u.id_folder = f.id
        JOIN user_info ui ON u.id_user = ui.id
        LEFT JOIN metadata m ON u.id = m.id_unit
        WHERE u.type = 0
        """

    def fetch_media_with_people(self, owner=None):
        """
        Fetches media units and their associated metadata using correlated subqueries.
        """
        query = self._get_base_query()
        params = []
        
        if owner:
            query += " AND ui.name = %s"
            params.append(owner)
            
        query += " ORDER BY u.id"
        
        results = []
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, tuple(params))
                results = [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Error fetching metadata: {e}")
            if self.conn:
                self.conn.rollback()
        return results

    def fetch_media_by_path(self, path_substring, owner=None):
        """
        Fetches media units matching a specific folder path with full metadata.
        """
        query = self._get_base_query()
        params = [f"%{path_substring}%"]
        query += " AND f.name LIKE %s"
        
        if owner:
            query += " AND ui.name = %s"
            params.append(owner)
            
        query += " ORDER BY u.id"
        
        results = []
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, tuple(params))
                results = [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Error fetching metadata by path: {e}")
            if self.conn:
                self.conn.rollback()
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
