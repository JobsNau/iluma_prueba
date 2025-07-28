import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="./docker/.env")

class Settings:
    DB_USER = os.getenv("POSTGRES_USER")
    DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    DB_HOST = "localhost"
    DB_PORT = os.getenv("POSTGRES_PORT", 5433)
    DB_NAME = os.getenv("POSTGRES_DB")

    @classmethod
    def db_uri(cls) -> str:
        return f"postgresql+psycopg2://{cls.DB_USER}:{cls.DB_PASSWORD}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}"
