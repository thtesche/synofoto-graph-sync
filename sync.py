import os
import sys

# Erlaubt das direkte Ausführen ohne PYTHONPATH=src
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

import logging
import argparse
from dotenv import load_dotenv
from synofoto_graph_sync.extractor import MetadataExtractor
from synofoto_graph_sync.parser import XMPParser
from synofoto_graph_sync.importer import GraphImporter

# Load environment variables from .env file
load_dotenv()

# --- CONFIGURATION ---
PG_CONFIG = {
    "database": os.getenv("PG_DB", "synofoto"),
    "user": os.getenv("PG_USER", "postgres"),
    "host": os.getenv("PG_HOST", "/run/postgresql/"),
    "port": os.getenv("PG_PORT", "5432")
}

GRAPHDB_CONFIG = {
    "uri": os.getenv("GRAPHDB_URI", "bolt://localhost:7687"),
    "user": os.getenv("GRAPHDB_USER", ""),      # Optional for Memgraph
    "password": os.getenv("GRAPHDB_PASSWORD", "") # Optional for Memgraph
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
    extractor.close()
    
    # 2. Check Graph Database (Memgraph)
    logger.info(f"Checking Graph DB at {GRAPHDB_CONFIG['uri']}...")
    importer = None
    try:
        importer = GraphImporter(GRAPHDB_CONFIG["uri"], GRAPHDB_CONFIG["user"], GRAPHDB_CONFIG["password"])
        graph_ok = importer.check_connection()
        if graph_ok:
            logger.info("✅ Graph DB: OK")
        else:
            logger.error("❌ Graph DB: FAILED")
    except Exception as e:
        logger.error(f"❌ Graph DB: FAILED ({e})")
        graph_ok = False
    finally:
        if importer:
            importer.close()
        
    if pg_ok and graph_ok:
        logger.info("--- Everything looks good! 🚀 ---")
        return True
    else:
        logger.error("--- ⚠️  Some checks failed. Please check your .env and NAS settings. ---")
        return False

def main():
    parser = argparse.ArgumentParser(description="Synofoto to Neo4j Sync Tool")
    parser.add_argument("--doctor", action="store_true", help="Run diagnostic connection checks")
    parser.add_argument("--path-filter", type=str, help="Filter images by folder path substring")
    parser.add_argument("--owner", type=str, help="Set the owner for the images")
    parser.add_argument("--dry-run", action="store_true", help="Print data to console instead of writing to DB")
    args = parser.parse_args()

    if args.doctor:
        success = run_doctor()
        sys.exit(0 if success else 1)

    logger.info("Starting Sync Process")
    
    extractor = MetadataExtractor(PG_CONFIG)
    importer = None
    
    try:
        extractor.connect()
        
        if args.path_filter:
            media_items = extractor.fetch_media_by_path(args.path_filter, owner=args.owner)
        else:
            media_items = extractor.fetch_media_with_people(owner=args.owner)
            
        logger.info(f"Found {len(media_items)} items in PostgreSQL")
        
        if not args.dry_run:
            importer = GraphImporter(GRAPHDB_CONFIG["uri"], GRAPHDB_CONFIG["user"], GRAPHDB_CONFIG["password"])
        
        for item in media_items:
            item['owner'] = args.owner if args.owner else item.get('owner_name')
            _id = item.get('unit_id')
            _folder = item.get('folder_path', '')
            _people = ", ".join(item.get('people') or [])
            _tags = ", ".join(item.get('tags') or [])
            _loc = ", ".join(item.get('address_parts') or [])

            if args.dry_run:
                msg = f"DRY RUN - ID: {_id}, Filename: {item['filename']}, Folder: {_folder}, Owner: {item.get('owner')}"
                if _people: msg += f", People: [{_people}]"
                if _tags: msg += f", DB-Tags: [{_tags}]"
                if _loc: msg += f", Location: ({_loc})"
                print(msg)
                continue

            # Construct full path for XMP parsing
            file_path = os.path.join(PHOTO_ROOT, _folder.lstrip('/'), item['filename'])
            
            logger.info(f"Processing: {file_path}")
            
            # Milestone 2: Parse Tags from XMP (local file)
            xmp_tags = XMPParser.extract_tags(file_path)
            # Merge with Synology DB tags (general_tag)
            db_tags = item.get('tags', [])
            item['tags'] = list(set(xmp_tags + db_tags))
            
            # Milestone 3: Import to Neo4j
            importer.import_media_data(item)
            
        if args.dry_run:
            logger.info("Dry run completed")
        else:
            logger.info("Sync completed successfully")
        
    except Exception as e:
        logger.error(f"Sync failed: {e}")
    finally:
        extractor.close()
        if importer:
            importer.close()

if __name__ == "__main__":
    main()
