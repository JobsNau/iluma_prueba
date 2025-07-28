from src.db.database import Database
from src.ingestion.csv_cleaner import clean_csv
from src.ingestion.csv_loader import cargar_csv_directo
from src.ingestion.transformacion_dimensiones import transform_and_load_companies
from src.ingestion.transformacion_dimensiones import transform_and_load_locations
from src.ingestion.transformacion_dimensiones import transform_and_load_schedules
from src.ingestion.transformacion_dimensiones import transform_and_load_sources
from src.ingestion.transformacion_dimensiones import transform_and_load_countries
from src.ingestion.transformacion_dimensiones import transform_and_load_salary_rates
from src.ingestion.transformacion_dimensiones import transform_and_load_skills
from src.ingestion.transformacion_dimensiones import transform_and_load_jobs
from src.ingestion.transformacion_dimensiones import transform_and_load_job_skills


def main():
    
    try:
        raw_csv = "data/data_jobs.csv"
        clean_csv_path = "data/data_jobs_clean.csv"
        clean_csv(raw_csv, clean_csv_path)

        db = Database()
        engine = db.connect()
        cargar_csv_directo(engine, clean_csv_path)

        # Transformar y cargar dimensiones
        transform_and_load_companies(engine)
        transform_and_load_locations(engine)
        transform_and_load_schedules(engine)
        transform_and_load_sources(engine)
        transform_and_load_countries(engine)
        transform_and_load_salary_rates(engine)
        transform_and_load_skills(engine)
        transform_and_load_jobs(engine)
        transform_and_load_job_skills(engine)

    finally:
        db.disconnect()

if __name__ == "__main__":
    main()
