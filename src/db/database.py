from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
from src.config import Settings

class Database:
    def __init__(self):
        self._engine: Engine | None = None

    def connect(self) -> Engine:
        try:
            self._engine = create_engine(Settings.db_uri())
            with self._engine.connect() as conn:
                # consulta la version
                conn.execute(text("SELECT version()"))
            print("Conexión a la base de datos establecida.")
            return self._engine
        except SQLAlchemyError as e:
            print("Error al conectar con la base de datos:", e)
            raise

    def disconnect(self):
        if self._engine:
            self._engine.dispose()
            print("Conexión cerrada correctamente.")
        else:
            print("No hay conexión activa para cerrar.")

    def obtener_datos(self):
        if not self._engine:
            print("No hay conexión activa.")
            return None

        try:
            with self._engine.connect() as conn:
                result = conn.execute(text("SELECT * FROM carga.data_jobs"))
                return result.fetchall()
        except SQLAlchemyError as e:
            print("Error al obtener datos:", e)
            raise
