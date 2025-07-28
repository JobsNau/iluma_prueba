def test_skills_are_unique(conn):
    cur = conn.cursor()
    cur.execute("""
        SELECT name, COUNT(*) FROM report.skills GROUP BY name HAVING COUNT(*) > 1;
    """)
    duplicates = cur.fetchall()
    assert len(duplicates) == 0, f"Skills duplicadas: {duplicates}"
