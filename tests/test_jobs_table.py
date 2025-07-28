from datetime import datetime

def test_jobs_not_empty(conn):
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM report.jobs;")
    count = cur.fetchone()[0]
    assert count > 0, "La tabla report.jobs está vacía"

def test_job_row_id_unique(conn):
    cur = conn.cursor()
    cur.execute("""
        SELECT COUNT(*) - COUNT(DISTINCT job_row_id)
        FROM report.jobs;
    """)
    duplicates = cur.fetchone()[0]
    assert duplicates == 0, "Existen job_row_id duplicados"

def test_required_fields_not_null(conn):
    cur = conn.cursor()
    cur.execute("""
        SELECT COUNT(*)
        FROM report.jobs
        WHERE title_short IS NULL OR posted_date IS NULL;
    """)
    count = cur.fetchone()[0]
    assert count == 0, "Hay trabajos con campos críticos nulos"


def test_posted_date_not_in_future(conn):
    cur = conn.cursor()
    cur.execute("""
        SELECT COUNT(*)
        FROM report.jobs
        WHERE posted_date > NOW();
    """)
    count = cur.fetchone()[0]
    assert count == 0, f"{count} trabajos tienen fecha de publicación en el futuro"

