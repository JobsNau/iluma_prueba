def test_skills_are_unique(conn):
    cur = conn.cursor()
    cur.execute("""
        SELECT name, COUNT(*) FROM report.skills GROUP BY name HAVING COUNT(*) > 1;
    """)
    duplicates = cur.fetchall()
    assert len(duplicates) == 0, f"Skills duplicadas: {duplicates}"

def test_jobs_have_skills(conn):
    cur = conn.cursor()
    cur.execute("""
        SELECT COUNT(*)
        FROM report.jobs j
        LEFT JOIN report.job_skills js ON j.id = js.job_id
        WHERE js.job_id IS NULL;
    """)
    count = cur.fetchone()[0]
    assert count == 0, f"{count} trabajos sin skills asignados"
