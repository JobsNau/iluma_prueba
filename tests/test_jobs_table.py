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
