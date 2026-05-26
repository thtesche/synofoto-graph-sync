import os
import sys
# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))

from synofoto_graph_sync.importer import GraphImporter
from neo4j import GraphDatabase

uri = "bolt://192.168.0.105:7687"
user = "admin"
password = "EeGFS2z1Nh1"

print("--- Running Importer Integration Test ---")

# 1. Clean up any existing test nodes
driver = GraphDatabase.driver(uri, auth=(user, password))
try:
    with driver.session() as session:
        print("Cleaning up existing test nodes...")
        session.run("MATCH (l:Location) WHERE l.id STARTS WITH 'TestCountry' DETACH DELETE l")
        session.run("MATCH (p:Photo {id: 99999}) DETACH DELETE p")
finally:
    driver.close()

# 2. Import using GraphImporter
importer = GraphImporter(uri, user, password)
try:
    mock_media = {
        'unit_id': 99999,
        'filename': 'test_photo.jpg',
        'address_parts': [
            {'level': 1, 'value': 'TestCountry'},
            {'level': 2, 'value': 'TestState'},
            {'level': 3, 'value': 'TestCity'},
            {'level': 4, 'value': 'TestStreet'}
        ]
    }
    print("Importing mock media item...")
    importer.import_media_data(mock_media)
finally:
    importer.close()

# 3. Verify in database
driver = GraphDatabase.driver(uri, auth=(user, password))
try:
    with driver.session() as session:
        print("\nVerifying nodes created:")
        result = session.run("MATCH (l:Location) WHERE l.id STARTS WITH 'TestCountry' RETURN l.id AS id, l.name AS name, l.type AS type, labels(l) AS labels, l.level AS level, l.index AS index ORDER BY l.index")
        nodes = []
        for r in result:
            print(f"ID: {r['id']}, Name: {r['name']}, Type: {r['type']}, Labels: {r['labels']}, Level: {r['level']}, Index: {r['index']}")
            nodes.append(r)
            
        assert len(nodes) == 4
        assert nodes[0]['id'] == 'TestCountry'
        assert 'Country' in nodes[0]['labels']
        assert nodes[0]['type'] == 'Country'
        
        assert nodes[1]['id'] == 'TestCountry|TestState'
        assert nodes[1]['type'] == 'State'
        
        assert nodes[2]['id'] == 'TestCountry|TestState|TestCity'
        assert nodes[2]['type'] == 'City'
        
        assert nodes[3]['id'] == 'TestCountry|TestState|TestCity|TestStreet'
        assert 'Street' in nodes[3]['labels']
        assert nodes[3]['type'] == 'Street'
        
        print("\nVerifying relationships created:")
        rel_result = session.run("MATCH (child:Location)-[r:PART_OF]->(parent:Location) WHERE child.id STARTS WITH 'TestCountry' RETURN child.id AS child_id, parent.id AS parent_id")
        rels = []
        for r in rel_result:
            print(f"({r['child_id']}) -[:PART_OF]-> ({r['parent_id']})")
            rels.append((r['child_id'], r['parent_id']))
            
        assert ('TestCountry|TestState|TestCity|TestStreet', 'TestCountry|TestState|TestCity') in rels
        assert ('TestCountry|TestState|TestCity', 'TestCountry|TestState') in rels
        assert ('TestCountry|TestState', 'TestCountry') in rels
        
        print("\nVerifying photo-to-location relationship:")
        photo_result = session.run("MATCH (p:Photo {id: 99999})-[r:LOCATED_AT]->(l:Location) RETURN p.filename AS filename, l.id AS loc_id")
        photo_rel = photo_result.single()
        assert photo_rel is not None
        print(f"({photo_rel['filename']}) -[:LOCATED_AT]-> ({photo_rel['loc_id']})")
        assert photo_rel['loc_id'] == 'TestCountry|TestState|TestCity|TestStreet'
        
        # 4. Clean up after success
        print("\nTest passed! Cleaning up test nodes...")
        session.run("MATCH (l:Location) WHERE l.id STARTS WITH 'TestCountry' DETACH DELETE l")
        session.run("MATCH (p:Photo {id: 99999}) DETACH DELETE p")
        print("Cleanup complete.")
finally:
    driver.close()
