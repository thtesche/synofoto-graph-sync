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
    assert len(results) == 4
    
    # pic1.jpg (id 100) has 2 people, tag, and 3 address parts
    unit100 = next(r for r in results if r['unit_id'] == 100)
    assert set(unit100['people']) == {'Alice', 'Bob'}
    assert unit100['tags'] == ['Landscape']
    assert unit100['address_parts'] == [
        {'level': 1, 'value': 'Germany'},
        {'level': 2, 'value': 'Berlin'},
        {'level': 3, 'value': 'Mitte'}
    ]
    assert unit100['latitude'] == 52.52
    assert unit100['takentime'] == 1715684400
    assert unit100['cache_key'] == 'key100'
    
    # pic2.jpg (id 101) has Charlie, 2 tags, and 2 address parts
    unit101 = next(r for r in results if r['unit_id'] == 101)
    assert unit101['people'] == ['Charlie']
    assert set(unit101['tags']) == {'Landscape', 'Architecture'}
    assert unit101['address_parts'] == [
        {'level': 1, 'value': 'Germany'},
        {'level': 2, 'value': 'Hamburg'}
    ]
    
    extractor.close()

def test_fetch_media_with_people_owner_filter(postgres_container):
    extractor = MetadataExtractor(postgres_container)
    extractor.connect()
    results = extractor.fetch_media_with_people(owner="thtesche")
    
    assert len(results) == 3
    for r in results:
        assert r['owner_name'] == 'thtesche'
    extractor.close()

def test_fetch_media_by_path(postgres_container):
    extractor = MetadataExtractor(postgres_container)
    extractor.connect()
    
    results = extractor.fetch_media_by_path("/2026/02")
    assert len(results) == 3
    
    results_owner = extractor.fetch_media_by_path("/2026/02", owner="thtesche")
    assert len(results_owner) == 2
    assert results_owner[0]['unit_id'] == 100
    assert results_owner[1]['unit_id'] == 101
    
    extractor.close()
