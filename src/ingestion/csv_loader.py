from sqlalchemy import text
from src.utils.logger import get_logger
logger = get_logger(__name__)

def cargar_csv_directo(engine, csv_path, schema="carga", table="data_jobs"):
    # Crear tabla si no existe
    with engine.begin() as conn:
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
                        job_skills JSONB,
                        job_type_skills JSONB
                    )
                """))

    # Insertar datos
    conn = engine.raw_connection()
    cursor = conn.cursor()
    try:
        # hacer un truncate si la tabla ya tiene datos
        cursor.execute(f"TRUNCATE TABLE {schema}.{table}")
        
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
        with open(csv_path, 'r', encoding='utf-8') as f:
            cursor.copy_expert(sql, f)
        conn.commit()
        logger.info("Carga completada desde %s a %s.%s", csv_path, schema, table)
    except Exception as e:
        conn.rollback()
        logger.error("Error al insertar: %s", e)
        raise
    finally:
        cursor.close()
        conn.close()
