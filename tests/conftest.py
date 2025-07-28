import pytest
import psycopg2
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path="docker/.env")
from src.utils.logger import get_logger
logger = get_logger(__name__)


@pytest.fixture(scope="module")
def conn():
    try:
        logger.info("Estableciendo conexión a la base de datos para pruebas.")
        connection = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST"),
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            port=os.getenv("POSTGRES_PORT")
        )
        logger.info("Conexión establecida exitosamente.")

        yield connection
        connection.close()
        logger.info("Conexión cerrada exitosamente.")
    except Exception as e:
        logger.error(f"Error al establecer la conexión a la base de datos: {e}")
        raise e
