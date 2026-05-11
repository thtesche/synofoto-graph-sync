import os
import logging
import argparse
import sys
from dotenv import load_dotenv
from src.synofoto_graph_sync.extractor import MetadataExtractor
from src.synofoto_graph_sync.parser import XMPParser
from src.synofoto_graph_sync.importer import GraphImporter

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

# Mapping Synology photo path to local filesystem path
PHOTO_ROOT = os.getenv("PHOTO_ROOT", "/volume1/photo")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_doctor():
    """Diagnostic tool to check connections."""
    logger.info("--- 🩺 Running Connection Doctor ---")
    
    # 1. Check PostgreSQL
    logger.info(f"Checking PostgreSQL at {PG_CONFIG['host']}:{PG_CONFIG['port']}...")
    extractor = MetadataExtractor(PG_CONFIG)
    pg_ok = extractor.check_connection()
    if pg_ok:
        logger.info("✅ PostgreSQL: OK")
    else:
        logger.error("❌ PostgreSQL: FAILED")
    
    # 2. Check Neo4j
    logger.info(f"Checking Neo4j at {NEO4J_CONFIG['uri']}...")
    try:
        importer = GraphImporter(NEO4J_CONFIG["uri"], NEO4J_CONFIG["user"], NEO4J_CONFIG["password"])
        neo_ok = importer.check_connection()
        if neo_ok:
            logger.info("✅ Neo4j: OK")
        else:
            logger.error("❌ Neo4j: FAILED")
    except Exception as e:
        logger.error(f"❌ Neo4j: FAILED ({e})")
        neo_ok = False
        
    if pg_ok and neo_ok:
        logger.info("--- Everything looks good! 🚀 ---")
        return True
    else:
        logger.error("--- ⚠️  Some checks failed. Please check your .env and NAS settings. ---")
        return False

def main():
    parser = argparse.ArgumentParser(description="Synofoto to Neo4j Sync Tool")
    parser.add_argument("--doctor", action="store_true", help="Run diagnostic connection checks")
    args = parser.parse_args()

    if args.doctor:
        success = run_doctor()
        sys.exit(0 if success else 1)

    logger.info("Starting Sync Process")
    
    extractor = MetadataExtractor(PG_CONFIG)
    importer = GraphImporter(NEO4J_CONFIG["uri"], NEO4J_CONFIG["user"], NEO4J_CONFIG["password"])
    
    try:
        extractor.connect()
        media_items = extractor.fetch_media_with_people()
        logger.info(f"Found {len(media_items)} items in PostgreSQL")
        
        for item in media_items:
            # Construct full path for XMP parsing
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
