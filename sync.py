import os
import logging
from src.synofoto_graph_sync.extractor import MetadataExtractor
from src.synofoto_graph_sync.parser import XMPParser
from src.synofoto_graph_sync.importer import GraphImporter

# --- CONFIGURATION ---
PG_CONFIG = {
    "database": "synofoto",
    "user": "postgres",
    "host": "/run/postgresql/",
    "port": "5432"
}

NEO4J_CONFIG = {
    "uri": "bolt://localhost:7687",
    "user": "neo4j",
    "password": "your_password"
}

# Mapping Synology photo path to local filesystem path
# Often Synology DB stores paths relative to /volume1/photo
PHOTO_ROOT = "/volume1/photo"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    logger.info("Starting Sync Process")
    
    extractor = MetadataExtractor(PG_CONFIG)
    importer = GraphImporter(NEO4J_CONFIG["uri"], NEO4J_CONFIG["user"], NEO4J_CONFIG["password"])
    
    try:
        extractor.connect()
        media_items = extractor.fetch_media_with_people()
        logger.info(f"Found {len(media_items)} items in PostgreSQL")
        
        for item in media_items:
            # Construct full path for XMP parsing
            # Folder path in DB is usually the directory name
            file_path = os.path.join(PHOTO_ROOT, item['folder_path'] or '', item['filename'])
            
            logger.info(f"Processing: {file_path}")
            
            # Milestone 2: Parse Tags
            tags = XMPParser.extract_tags(file_path)
            item['tags'] = tags
            
            # Milestone 3: Import to Neo4j
            importer.import_media_data(item)
            
        logger.info("Sync completed successfully")
        
    except Exception as e:
        logger.error(f"Sync failed: {e}")
    finally:
        extractor.close()

if __name__ == "__main__":
    main()
