import pytest

@pytest.mark.parametrize("fk_table, fk_column", [
    ("companies", "company_id"),
    ("locations", "location_id"),
    ("schedules", "schedule_id"),
    ("sources", "source_id"),
    ("countries", "country_id"),
    ("salary_rates", "salary_rate_id")
])
def test_foreign_keys_integrity(conn, fk_table, fk_column):
    cur = conn.cursor()
    cur.execute(f"""
        SELECT COUNT(*)
        FROM report.jobs j
        LEFT JOIN report.{fk_table} f ON j.{fk_column} = f.id
        WHERE j.{fk_column} IS NOT NULL AND f.id IS NULL;
    """)
    missing = cur.fetchone()[0]
    assert missing == 0, f"Existen {missing} {fk_column} inválidos en report.jobs"
