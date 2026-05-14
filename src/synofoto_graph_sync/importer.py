from neo4j import GraphDatabase
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class GraphImporter:
    def __init__(self, uri, user=None, password=None):
        try:
            # Handle optional authentication (Memgraph often has none by default)
            driver_kwargs = {
                "uri": uri,
                "connection_timeout": 120.0,
                "max_connection_lifetime": 600.0
            }
            
            if user:
                # Use provided user, even if password is empty
                driver_kwargs["auth"] = (user, password or "")
                logger.info(f"Connecting to Graph DB with user: {user}")
            else:
                # Try explicit empty auth which some Memgraph versions prefer
                driver_kwargs["auth"] = ("", "") 
                logger.info("Connecting to Graph DB with empty credentials")
            
            self.driver = GraphDatabase.driver(**driver_kwargs)
            
            # Verify connectivity immediately
            self.driver.verify_connectivity()
            logger.info("Connected to Graph Database (Memgraph/Bolt)")
        except Exception as e:
            logger.error(f"Failed to connect to Graph Database: {e}")
            raise

    def close(self):
        if hasattr(self, 'driver'):
            self.driver.close()

    def check_connection(self):
        """Simple check to see if Neo4j is reachable."""
        try:
            self.driver.verify_connectivity()
            return True
        except Exception as e:
            logger.error(f"Neo4j connection check failed: {e}")
            return False

    def import_media_data(self, media_item):
        """
        Imports or updates media metadata and its relationships in the graph.
        """
        with self.driver.session() as session:
            session.execute_write(self._import_transaction, media_item)

    @staticmethod
    def _import_transaction(tx, media_item):
        unit_id = media_item.get('id', media_item.get('unit_id'))
        filename = media_item.get('filename')
        folder_path = media_item.get('folder', media_item.get('folder_path'))
        owner = media_item.get('owner')

        # 1. Photo Node
        takentime_raw = media_item.get('takentime')
        takentime_iso = None
        if takentime_raw:
            try:
                # Synology takentime is typically a Unix timestamp in seconds
                takentime_iso = datetime.fromtimestamp(takentime_raw).isoformat()
            except Exception:
                pass

        photo_query = """
        MERGE (p:Photo {id: $unit_id})
        SET p.filename = $filename,
            p.folder = $folder_path,
            p.latitude = $latitude,
            p.longitude = $longitude,
            p.takentime = $takentime_raw,
            p.takentime_iso = $takentime_iso,
            p.cache_key = $cache_key
        """
        tx.run(photo_query, 
               unit_id=unit_id, 
               filename=filename, 
               folder_path=folder_path,
               latitude=media_item.get('latitude'),
               longitude=media_item.get('longitude'),
               takentime_raw=takentime_raw,
               takentime_iso=takentime_iso,
               cache_key=media_item.get('cache_key'))

        # 2. Owner Node
        if owner:
            owner_query = """
            MATCH (p:Photo {id: $unit_id})
            MERGE (o:Owner {name: $owner})
            MERGE (p)-[:OWNED_BY]->(o)
            """
            tx.run(owner_query, unit_id=unit_id, owner=owner)

        # 3. Person & Family Relationships
        for person_name in media_item.get('people') or []:
            person_query = """
            MATCH (p:Photo {id: $unit_id})
            MERGE (per:Person {name: $person_name})
            MERGE (p)-[:HAS_PERSON]->(per)
            """
            tx.run(person_query, unit_id=unit_id, person_name=person_name)
            
            # Extract Family from Person (e.g. "John Doe" -> "Doe")
            parts = person_name.strip().split()
            if len(parts) > 1:
                family_name = parts[-1]
                family_query = """
                MATCH (per:Person {name: $person_name})
                MERGE (f:Family {name: $family_name})
                MERGE (per)-[:BELONGS_TO_FAMILY]->(f)
                """
                tx.run(family_query, person_name=person_name, family_name=family_name)

        # 4. Object (Tags) Relationships
        for tag_name in media_item.get('tags') or []:
            tag_query = """
            MATCH (p:Photo {id: $unit_id})
            MERGE (o:Object {name: $tag_name})
            MERGE (p)-[:HAS_OBJECT]->(o)
            """
            tx.run(tag_query, unit_id=unit_id, tag_name=tag_name)

        # 5. Location Hierarchy
        address_parts = media_item.get('address_parts') or []
        if address_parts:
            count = len(address_parts)
            prev_name = None
            
            for i, part in enumerate(address_parts):
                part_name = part.get('value')
                level_id = part.get('level')
                if not part_name:
                    continue
                
                # Determine labels and guessed type
                labels = ["Location"]
                guessed_type = "District"
                
                if i == 0:
                    labels.append("Country")
                    guessed_type = "Country"
                elif i == count - 1 and count > 1:
                    labels.append("Street")
                    guessed_type = "Street"
                elif i == count - 2 and count > 2:
                    guessed_type = "City"
                elif i == 1:
                    guessed_type = "State"
                elif i == 2:
                    guessed_type = "County"

                # MERGE node as :Location first to ensure uniqueness, then SET labels/props
                label_str = ":" + ":".join(labels)
                loc_merge = f"MERGE (l:Location {{name: $part_name}}) SET l{label_str}, l.type = $type, l.level = $level, l.index = $index"
                tx.run(loc_merge, part_name=part_name, type=guessed_type, level=level_id, index=i)
                
                # Link to parent (e.g., Street -> City -> County -> State -> Country)
                if prev_name and prev_name != part_name:
                    link_query = """
                    MATCH (child:Location {name: $part_name})
                    MATCH (parent:Location {name: $prev_name})
                    MERGE (child)-[:PART_OF]->(parent)
                    """
                    tx.run(link_query, part_name=part_name, prev_name=prev_name)
                
                prev_name = part_name

            # Link Photo to the most specific location found
            if prev_name:
                photo_loc_query = """
                MATCH (p:Photo {id: $unit_id})
                MATCH (l:Location {name: $prev_name})
                MERGE (p)-[:LOCATED_AT]->(l)
                """
                tx.run(photo_loc_query, unit_id=unit_id, prev_name=prev_name)

if __name__ == "__main__":
    # Test block
    importer = GraphImporter("bolt://localhost:7687", "neo4j", "your_password")
    sample = {
        'unit_id': 1,
        'filename': 'test.jpg',
        'folder_path': '/volume1/photo',
        'people': ['Test Person'],
        'tags': ['Test Tag']
    }
    # importer.import_media_data(sample)
    importer.close()
