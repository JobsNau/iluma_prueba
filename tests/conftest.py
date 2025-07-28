import pytest
import psycopg2
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path="docker/.env")


@pytest.fixture(scope="module")
def conn():
    connection = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        port=os.getenv("POSTGRES_PORT")
    )
    yield connection
    connection.close()
