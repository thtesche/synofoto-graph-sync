import pytest
from synofoto_graph_sync.extractor import MetadataExtractor

def test_extractor_initialization(postgres_container):
    extractor = MetadataExtractor(postgres_container)
    assert extractor.config == postgres_container
    assert extractor.conn is None

def test_extractor_connection(postgres_container):
    extractor = MetadataExtractor(postgres_container)
    extractor.connect()
    assert extractor.conn is not None
    assert not extractor.conn.closed
    extractor.close()
    assert extractor.conn.closed

def test_fetch_media_with_people(postgres_container):
    extractor = MetadataExtractor(postgres_container)
    extractor.connect()
    results = extractor.fetch_media_with_people()
    
    # We expect 4 items with type=0
    # id 100 -> Alice, Bob (owner: thtesche)
    # id 101 -> Charlie (owner: thtesche)
    # id 102 -> [] (owner: thtesche)
    # id 104 -> [] (owner: otheruser)
    assert len(results) == 4
    
    unit100 = next(r for r in results if r['unit_id'] == 100)
    assert set(unit100['people']) == {'Alice', 'Bob'}
    assert unit100['owner_name'] == 'thtesche'
    assert unit100['filename'] == 'pic1.jpg'
    
    unit102 = next(r for r in results if r['unit_id'] == 102)
    assert unit102['people'] == []

def test_fetch_media_with_people_owner_filter(postgres_container):
    extractor = MetadataExtractor(postgres_container)
    extractor.connect()
    results = extractor.fetch_media_with_people(owner="thtesche")
    
    # Should only return units 100, 101, 102 (from user thtesche)
    assert len(results) == 3
    for r in results:
        assert r['owner_name'] == 'thtesche'

def test_fetch_media_by_path(postgres_container):
    extractor = MetadataExtractor(postgres_container)
    extractor.connect()
    
    # Path '/2026/02' -> folders 1 and 3 -> units 100, 101, 104 (type 0)
    # unit 103 is type 1 and should be ignored
    results = extractor.fetch_media_by_path("/2026/02")
    assert len(results) == 3
    
    # Check that owner_name is fetched properly
    unit104 = next(r for r in results if r['id'] == 104)
    assert unit104['owner_name'] == 'otheruser'
    
    # With owner filter
    results = extractor.fetch_media_by_path("/2026/02", owner="thtesche")
    assert len(results) == 2
    assert results[0]['id'] == 100
    assert results[1]['id'] == 101
    
    extractor.close()
