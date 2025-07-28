import json
import ast
import pandas as pd

def transform_and_load_companies(engine):
    query_select = """
        SELECT DISTINCT company_name
        FROM carga.data_jobs
        WHERE company_name IS NOT NULL
    """

    insert_query = """
        INSERT INTO report.companies (name)
        VALUES (%s)
        ON CONFLICT (name) DO NOTHING
    """

    conn = engine.raw_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query_select)
        companies = cursor.fetchall()
        print(f"Se encontraron {len(companies)} compañías únicas.")

        values_to_insert = [(company[0],) for company in companies if company[0] is not None]
        if values_to_insert:
            cursor.executemany(insert_query, values_to_insert)

        conn.commit()
        print("Carga a report.companies completada.")
    except Exception as e:
        conn.rollback()
        print(f"Error al cargar compañías: {e}")
    finally:
        cursor.close()
        conn.close()


def transform_and_load_locations(engine):
    query_select = """
        SELECT DISTINCT job_location
        FROM carga.data_jobs
        WHERE job_location IS NOT NULL
    """

    insert_query = """
        INSERT INTO report.locations (name)
        VALUES (%s)
        ON CONFLICT (name) DO NOTHING
    """

    conn = engine.raw_connection()
    cur = conn.cursor()
    try:
        cur.execute(query_select)
        locations = cur.fetchall()
        print(f"Se encontraron {len(locations)} ubicaciones únicas.")

        values_to_insert = [(location[0],) for location in locations if location[0] is not None]
        if values_to_insert:
            cur.executemany(insert_query, values_to_insert)

        conn.commit()
        print("Carga a report.locations completada.")
    except Exception as e:
        conn.rollback()
        print(f"Error al cargar ubicaciones: {e}")
    finally:
        cur.close()
        conn.close()


def transform_and_load_schedules(engine):
    query_select = """
        SELECT DISTINCT job_schedule_type
        FROM carga.data_jobs
        WHERE job_schedule_type IS NOT NULL
    """

    insert_query = """
        INSERT INTO report.schedules (type)
        VALUES (%s)
        ON CONFLICT (type) DO NOTHING
    """

    conn = engine.raw_connection()
    cur = conn.cursor()
    try:
        cur.execute(query_select)
        schedules = cur.fetchall()
        print(f"Se encontraron {len(schedules)} tipos de jornada únicos.")

        values_to_insert = [(schedule[0],) for schedule in schedules if schedule[0] is not None]
        if values_to_insert:
            cur.executemany(insert_query, values_to_insert)

        conn.commit()
        print("Carga a report.schedules completada.")
    except Exception as e:
        conn.rollback()
        print(f"Error al cargar tipos de jornada: {e}")
    finally:
        cur.close()
        conn.close()


def transform_and_load_sources(engine):
    query_select = """
        SELECT DISTINCT job_via
        FROM carga.data_jobs
        WHERE job_via IS NOT NULL
    """

    insert_query = """
        INSERT INTO report.sources (name)
        VALUES (%s)
        ON CONFLICT (name) DO NOTHING
    """

    conn = engine.raw_connection()
    cur = conn.cursor()
    try:
        cur.execute(query_select)
        sources = cur.fetchall()
        print(f"Se encontraron {len(sources)} fuentes únicas.")

        values_to_insert = [(source[0],) for source in sources if source[0] is not None]
        if values_to_insert:
            cur.executemany(insert_query, values_to_insert)

        conn.commit()
        print("Carga a report.sources completada.")
    except Exception as e:
        conn.rollback()
        print(f"Error al cargar fuentes: {e}")
    finally:
        cur.close()
        conn.close()


def transform_and_load_countries(engine):
    query_select = """
        SELECT DISTINCT job_country
        FROM carga.data_jobs
        WHERE job_country IS NOT NULL
    """

    insert_query = """
        INSERT INTO report.countries (name)
        VALUES (%s)
        ON CONFLICT (name) DO NOTHING
    """

    conn = engine.raw_connection()
    cur = conn.cursor()
    try:
        cur.execute(query_select)
        countries = cur.fetchall()
        print(f"Se encontraron {len(countries)} países únicos.")

        values_to_insert = [(country[0],) for country in countries if country[0] is not None]
        if values_to_insert:
            cur.executemany(insert_query, values_to_insert)

        conn.commit()
        print("Carga a report.countries completada.")
    except Exception as e:
        conn.rollback()
        print(f"Error al cargar países: {e}")
    finally:
        cur.close()
        conn.close()


def transform_and_load_salary_rates(engine):
    query_select = """
        SELECT DISTINCT salary_rate
        FROM carga.data_jobs
        WHERE salary_rate IS NOT NULL
    """

    insert_query = """
        INSERT INTO report.salary_rates (rate)
        VALUES (%s)
        ON CONFLICT (rate) DO NOTHING
    """

    conn = engine.raw_connection()
    cur = conn.cursor()
    try:
        cur.execute(query_select)
        rates = cur.fetchall()
        print(f"Se encontraron {len(rates)} tipos de salario únicos.")

        values_to_insert = [(rate[0],) for rate in rates if rate[0] is not None]
        if values_to_insert:
            cur.executemany(insert_query, values_to_insert)

        conn.commit()
        print("Carga a report.salary_rates completada.")
    except Exception as e:
        conn.rollback()
        print(f"Error al cargar tipos de salario: {e}")
    finally:
        cur.close()
        conn.close()


def transform_and_load_skills(engine):
    query_select = """
        SELECT job_skills
        FROM carga.data_jobs
        WHERE job_skills IS NOT NULL
    """

    insert_query = """
        INSERT INTO report.skills (name)
        VALUES (%s)
        ON CONFLICT (name) DO NOTHING
    """

    conn = engine.raw_connection()
    cur = conn.cursor()
    try:
        cur.execute(query_select)
        rows = cur.fetchall()

        unique_skills = set()
        for (skills_json,) in rows:
            try:
                if isinstance(skills_json, list):
                    unique_skills.update([s.strip() for s in skills_json if s.strip()])
            except Exception as e:
                print(f"Error al parsear skills: {e}")

        print(f"Se encontraron {len(unique_skills)} habilidades únicas.")

        values_to_insert = [(skill,) for skill in unique_skills if skill]
        if values_to_insert:
            cur.executemany(insert_query, values_to_insert)

        conn.commit()
        print("Carga a report.skills completada.")
    except Exception as e:
        conn.rollback()
        print(f"Error al cargar habilidades: {e}")
    finally:
        cur.close()
        conn.close()



def transform_and_load_job_skills(engine):
    conn = engine.raw_connection()
    cur = conn.cursor()
    try:
        # Obtener mapeo de skill name → skill_id
        cur.execute("SELECT id, name FROM report.skills")
        skill_map = {name.lower(): id for id, name in cur.fetchall()}

        # Obtener los trabajos con skills y su job_id
        cur.execute("""
            SELECT 
                job_skills
                , jobs.id AS job_id
            FROM carga.data_jobs AS data_jobs
            LEFT JOIN report.jobs AS jobs ON data_jobs.id = jobs.job_row_id
            WHERE data_jobs.job_skills IS NOT NULL
        """)
        
        insert_query = """
            INSERT INTO report.job_skills (job_id, skill_id)
            VALUES (%s, %s)
            ON CONFLICT DO NOTHING
        """
        rows = cur.fetchall()
        print(f"Procesando {len(rows)} trabajos con habilidades...")
        df_rws = pd.DataFrame(rows, columns=["job_skills", "job_id"])
        df_rws["job_skills"] = df_rws["job_skills"].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
        df_rws = df_rws.explode("job_skills").dropna(subset=["job_skills"])
        df_rws["skill_id"] = df_rws["job_skills"].str.lower().map(skill_map)

        data_to_save = df_rws[["job_id", "skill_id"]].dropna().values.tolist()

        if data_to_save:
            cur.executemany(insert_query, data_to_save)

        conn.commit()
        print("Carga a report.job_skills completada.")
    except Exception as e:
        conn.rollback()
        print(f"Error al cargar job_skills: {e}")
    finally:
        cur.close()
        conn.close()



def transform_and_load_jobs(engine):
    conn = engine.raw_connection()
    cur = conn.cursor()
    try:
        # Cargar diccionarios para buscar ids de entidades relacionadas
        def load_map(table, key_col="name"):
            cur.execute(f"SELECT id, {key_col} FROM report.{table};")
            return {row[1]: row[0] for row in cur.fetchall()}

        company_map = load_map("companies")
        location_map = load_map("locations")
        schedule_map = load_map("schedules", "type")
        source_map = load_map("sources")
        country_map = load_map("countries")
        rate_map = load_map("salary_rates", "rate")

        # Leer datos desde tabla de carga
        cur.execute("""
            SELECT id, job_title_short, job_title, job_posted_date,
                   salary_year_avg, salary_hour_avg,
                   job_work_from_home, job_no_degree_mention, job_health_insurance,
                   company_name, job_location, job_schedule_type, job_via,
                   job_country, salary_rate
            FROM carga.data_jobs;
        """)
        rows = cur.fetchall()

        insert_query = """
            INSERT INTO report.jobs (
                title_short, title_raw, posted_date,
                salary_year_avg, salary_hour_avg,
                work_from_home, no_degree_mention, health_insurance,
                company_id, location_id, schedule_id, source_id, country_id, salary_rate_id,
                job_row_id
            ) VALUES (
                %s, %s, %s,
                %s, %s,
                %s, %s, %s,
                %s, %s, %s, %s, %s, %s,
                %s
            ) ON CONFLICT (job_row_id) DO NOTHING;
        """

        data_to_insert = []

        for row in rows:
            (
                carga_id,
                title_short, title_raw, posted_date,
                salary_year_avg, salary_hour_avg,
                work_from_home, no_degree_mention, health_insurance,
                company_name, location, schedule_type, source,
                country, rate
            ) = row

            company_id = company_map.get(company_name)
            location_id = location_map.get(location)
            schedule_id = schedule_map.get(schedule_type)
            source_id = source_map.get(source)
            country_id = country_map.get(country)
            rate_id = rate_map.get(rate)

            data_to_insert.append((
                title_short, title_raw, posted_date,
                salary_year_avg, salary_hour_avg,
                work_from_home, no_degree_mention, health_insurance,
                company_id, location_id, schedule_id, source_id, country_id, rate_id,
                carga_id
            ))
        
        if data_to_insert:
            cur.executemany(insert_query, data_to_insert)

        conn.commit()
        print("Carga a report.jobs completada.")
    except Exception as e:
        conn.rollback()
        print(f"Error al cargar jobs: {e}")
    finally:
        cur.close()
        conn.close()