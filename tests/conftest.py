import pytest
from testcontainers.postgres import PostgresContainer
import psycopg2
import os

@pytest.fixture(scope="session")
def postgres_container():
    # Start Postgres 15 container (matching Synology Postgres version roughly)
    with PostgresContainer("postgres:15-alpine") as postgres:
        # Get connection details
        config = {
            "host": postgres.get_container_host_ip(),
            "port": postgres.get_exposed_port(5432),
            "user": postgres.username,
            "password": postgres.password,
            "database": postgres.dbname
        }
        
        # Init schema and dummy data
        init_sql_path = os.path.join(os.path.dirname(__file__), 'init.sql')
        with open(init_sql_path, 'r') as f:
            sql_script = f.read()
            
        conn = psycopg2.connect(**config)
        conn.autocommit = True
        with conn.cursor() as cursor:
            cursor.execute(sql_script)
        conn.close()
        
        yield config
