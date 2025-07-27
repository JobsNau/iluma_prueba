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

    def guardar_datos(self, df, chunk_size=1000):
        if not self._engine:
            print("No hay conexión activa.")
            return
        
        # Verifica que la tabla y los schema existan
        try:
            # Usa begin() para que se haga commit automático
            with self._engine.begin() as conn:
                conn.execute(text("CREATE SCHEMA IF NOT EXISTS carga"))
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS carga.data_jobs (
                        id SERIAL PRIMARY KEY,
                        job_title_short TEXT,
                        job_title TEXT,
                        job_location TEXT,
                        job_via TEXT,
                        job_schedule_type TEXT,
                        job_work_from_home BOOLEAN,
                        search_location TEXT,
                        job_posted_date TEXT,
                        job_no_degree_mention BOOLEAN,
                        job_health_insurance BOOLEAN,
                        job_country TEXT,
                        salary_rate TEXT,
                        salary_year_avg DOUBLE PRECISION,
                        salary_hour_avg DOUBLE PRECISION,
                        company_name TEXT,
                        job_skills TEXT,
                        job_type_skills TEXT
                    )
                """))
                print("Esquema y tabla verificados o creados correctamente.")
        except SQLAlchemyError as e:
            print("Error al crear esquema o tabla:", e)
            raise

        try:
            conn = self._engine.raw_connection()
            cursor = conn.cursor()
            columns = list(df.columns)
            col_names = ', '.join(columns)
            placeholders = ', '.join(['%s'] * len(columns))
            query = f'INSERT INTO carga.data_jobs ({col_names}) VALUES ({placeholders})'

            total = len(df)
            for chunk in range(0, total, chunk_size):
                end = min(chunk + chunk_size, total)
                df_chunk = df.iloc[chunk:end]
                if not df_chunk.empty:
                    print(f"Insertando registros {chunk + 1} a {min(chunk + chunk_size, total)} de {total}...")
                data = [tuple(row) for row in df_chunk.itertuples(index=False)]
                cursor.executemany(query, data)
                conn.commit()
                print(f"Insertadas filas {chunk + 1} a {min(chunk + chunk_size, total)} de {total}")
            print("Datos cargados exitosamente en 'carga.data_jobs'")
        except Exception as e:
            conn.rollback()
            print("Error insertando datos:", e)
            raise
        finally:
            cursor.close()
            conn.close()

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


    def cargar_csv_directo(self, csv_path, schema="carga", table="data_jobs"):
        if not self._engine:
            print("No hay conexión activa.")
            return

        # Crear esquema y tabla si no existen
        try:
            with self._engine.begin() as conn:
                conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema}"))
                conn.execute(text(f"""
                    CREATE TABLE IF NOT EXISTS {schema}.{table} (
                        id SERIAL PRIMARY KEY,
                        job_title_short TEXT,
                        job_title TEXT,
                        job_location TEXT,
                        job_via TEXT,
                        job_schedule_type TEXT,
                        job_work_from_home BOOLEAN,
                        search_location TEXT,
                        job_posted_date TEXT,
                        job_no_degree_mention BOOLEAN,
                        job_health_insurance BOOLEAN,
                        job_country TEXT,
                        salary_rate TEXT,
                        salary_year_avg DOUBLE PRECISION,
                        salary_hour_avg DOUBLE PRECISION,
                        company_name TEXT,
                        job_skills TEXT,
                        job_type_skills TEXT
                    )
                """))
                print(f"Esquema y tabla {schema}.{table} creados/verificados.")
        except SQLAlchemyError as e:
            print("Error creando tabla:", e)
            raise

        # Insertar datos usando COPY
        try:
            conn = self._engine.raw_connection()
            cursor = conn.cursor()
            with open(csv_path, 'r', encoding='utf-8') as f:
                columns = (
                            "job_title_short, job_title, job_location, job_via, job_schedule_type, "
                            "job_work_from_home, search_location, job_posted_date, job_no_degree_mention, "
                            "job_health_insurance, job_country, salary_rate, salary_year_avg, "
                            "salary_hour_avg, company_name, job_skills, job_type_skills"
                        )
                sql = f"""
                    COPY {schema}.{table} ({columns}) FROM STDIN WITH (
                        FORMAT csv,
                        HEADER true,
                        DELIMITER ',',
                        NULL '',
                        ENCODING 'UTF8'
                    )
                """
                cursor.copy_expert(sql, f)

            conn.commit()
            print(f"Archivo {csv_path} cargado exitosamente en {schema}.{table} con COPY.")
        except Exception as e:
            conn.rollback()
            print("Error al insertar CSV con COPY:", e)
            raise
        finally:
            cursor.close()
            conn.close()

