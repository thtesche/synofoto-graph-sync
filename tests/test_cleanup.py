import unittest
from unittest.mock import MagicMock, patch
from src.synofoto_graph_sync.cleanup import GraphCleanup

class TestGraphCleanup(unittest.TestCase):
    def setUp(self):
        self.pg_config = {"database": "test", "user": "u", "host": "h", "port": "p"}
        self.cleanup = GraphCleanup(pg_config=self.pg_config, graph_uri="bolt://test", graph_user="u", graph_password="p")

    @patch('psycopg2.connect')
    @patch('neo4j.GraphDatabase.driver')
    def test_cleanup_orphaned_photos(self, mock_driver, mock_pg):
        # Mock PG connection and cursor
        mock_pg_conn = MagicMock()
        mock_pg.return_value = mock_pg_conn
        mock_cursor = mock_pg_conn.cursor.return_value.__enter__.return_value
        # Postgres returns only ID 1 as existing
        mock_cursor.fetchall.return_value = [(1,)]

        # Mock Graph driver and session
        mock_drv_inst = MagicMock()
        mock_driver.return_value = mock_drv_inst
        mock_session = MagicMock()
        mock_drv_inst.session.return_value.__enter__.return_value = mock_session
        
        # Graph DB has IDs 1 and 2
        mock_session.run.side_effect = [
            [{"id": 1}, {"id": 2}], # First call: get all IDs
            None                    # Second call: delete orphaned
        ]

        self.cleanup.connect()
        self.cleanup.cleanup_orphaned_photos()

        # Verify that only ID 2 was deleted
        delete_call = mock_session.run.call_args_list[-1]
        self.assertIn("DETACH DELETE p", delete_call[0][0])
        self.assertEqual(delete_call[1]['ids'], [2])

if __name__ == "__main__":
    unittest.main()
