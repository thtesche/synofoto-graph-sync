from py2neo import Graph, Node, Relationship
import logging

logger = logging.getLogger(__name__)

class GraphImporter:
    def __init__(self, uri, user, password):
        try:
            self.graph = Graph(uri, auth=(user, password))
            logger.info("Connected to Neo4j")
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j: {e}")
            raise

    def import_media_data(self, media_item):
        """
         media_item = {
            'unit_id': 123,
            'filename': 'img.jpg',
            'folder_path': '/photo/vacation',
            'people': ['Alice', 'Bob'],
            'tags': ['Summer', 'Beach']
        }
        """
        # Create or update Image node
        tx = self.graph.begin()
        
        # Cypher for Image
        image_query = """
        MERGE (i:Image {unit_id: $unit_id})
        SET i.filename = $filename,
            i.path = $path
        RETURN i
        """
        tx.run(image_query, 
               unit_id=media_item['unit_id'], 
               filename=media_item['filename'], 
               path=f"{media_item['folder_path']}/{media_item['filename']}")

        # People
        for person_name in media_item.get('people', []):
            person_query = """
            MATCH (i:Image {unit_id: $unit_id})
            MERGE (p:Person {name: $person_name})
            MERGE (i)-[:HAS_PERSON]->(p)
            """
            tx.run(person_query, unit_id=media_item['unit_id'], person_name=person_name)

        # Tags
        for tag_name in media_item.get('tags', []):
            tag_query = """
            MATCH (i:Image {unit_id: $unit_id})
            MERGE (t:Tag {name: $tag_name})
            MERGE (i)-[:HAS_TAG]->(t)
            """
            tx.run(tag_query, unit_id=media_item['unit_id'], tag_name=tag_name)

        self.graph.commit(tx)

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
