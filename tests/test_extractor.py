import pytest
from unittest.mock import MagicMock, patch
from synofoto_graph_sync.extractor import MetadataExtractor

@pytest.fixture
def mock_config():
    return {
        "database": "testdb",
        "user": "user",
        "password": "password",
        "host": "localhost"
    }

def test_extractor_initialization(mock_config):
    extractor = MetadataExtractor(mock_config)
    assert extractor.config == mock_config
    assert extractor.conn is None

@patch("psycopg2.connect")
def test_extractor_connection(mock_connect, mock_config):
    mock_conn = MagicMock()
    mock_connect.return_value = mock_conn
    
    extractor = MetadataExtractor(mock_config)
    extractor.connect()
    
    mock_connect.assert_called_once_with(**mock_config)
    assert extractor.conn == mock_conn

@patch("psycopg2.connect")
def test_fetch_media_with_people_empty(mock_connect, mock_config):
    # Setup mocks
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    
    # Mock empty database result
    mock_cursor.fetchall.return_value = []
    
    extractor = MetadataExtractor(mock_config)
    extractor.connect()
    results = extractor.fetch_media_with_people()
    
    assert results == []
    assert mock_cursor.execute.called

@patch("psycopg2.connect")
def test_fetch_media_with_people_grouping(mock_connect, mock_config):
    # Setup mocks
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    
    # Mock rows with same unit_id but different people
    mock_cursor.fetchall.return_value = [
        {'unit_id': 1, 'filename': 'pic1.jpg', 'folder_path': '/photo', 'person_name': 'Alice'},
        {'unit_id': 1, 'filename': 'pic1.jpg', 'folder_path': '/photo', 'person_name': 'Bob'},
        {'unit_id': 2, 'filename': 'pic2.jpg', 'folder_path': '/photo', 'person_name': 'Charlie'}
    ]
    
    extractor = MetadataExtractor(mock_config)
    extractor.connect()
    results = extractor.fetch_media_with_people()
    
    assert len(results) == 2
    
    # Check Alice and Bob are grouped for unit 1
    unit1 = next(r for r in results if r['unit_id'] == 1)
    assert set(unit1['people']) == {'Alice', 'Bob'}
    
    # Check unit 2
    unit2 = next(r for r in results if r['unit_id'] == 2)
    assert unit2['people'] == ['Charlie']
