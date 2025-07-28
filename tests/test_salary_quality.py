def test_salaries_are_positive(conn):
    cur = conn.cursor()
    cur.execute("""
        SELECT COUNT(*)
        FROM report.jobs
        WHERE (salary_year_avg < 0 OR salary_hour_avg < 0);
    """)
    count = cur.fetchone()[0]
    assert count == 0, "Hay salarios negativos"

def test_salary_matches_rate(conn):
    cur = conn.cursor()
    cur.execute("""
        SELECT r.rate, COUNT(*)
        FROM report.jobs j
        JOIN report.salary_rates r ON j.salary_rate_id = r.id
        GROUP BY r.rate;
    """)
    results = cur.fetchall()
    for rate, count in results:
        assert count > 0, f"No hay trabajos con rate '{rate}'"
