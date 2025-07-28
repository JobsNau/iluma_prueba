
CREATE SCHEMA IF NOT EXISTS report;

-- Tablas dimensionales
CREATE TABLE report.companies (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE report.locations (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE
);

CREATE TABLE report.schedules (
    id SERIAL PRIMARY KEY,
    type TEXT UNIQUE
);

CREATE TABLE report.sources (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE
);

CREATE TABLE report.countries (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE
);

CREATE TABLE report.salary_rates (
    id SERIAL PRIMARY KEY,
    rate TEXT CHECK (rate IN ('hourly', 'yearly'))
);

CREATE TABLE report.skills (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE
);

-- Tabla principal
CREATE TABLE report.jobs (
    id SERIAL PRIMARY KEY,
    title_short TEXT,
    title_raw TEXT,
    posted_date TIMESTAMP,
    salary_year_avg NUMERIC,
    salary_hour_avg NUMERIC,
    work_from_home BOOLEAN,
    no_degree_mention BOOLEAN,
    health_insurance BOOLEAN,
    company_id INT REFERENCES report.companies(id),
    location_id INT REFERENCES report.locations(id),
    schedule_id INT REFERENCES report.schedules(id),
    source_id INT REFERENCES report.sources(id),
    country_id INT REFERENCES report.countries(id),
    salary_rate_id INT REFERENCES report.salary_rates(id)
    job_row_id INT UNIQUE
);
-- ALTER TABLE report.jobs ADD COLUMN job_row_id INT UNIQUE;

-- Relación muchos a muchos: jobs - skills
CREATE TABLE report.job_skills (
    job_id INT REFERENCES report.jobs(id),
    skill_id INT REFERENCES report.skills(id),
    PRIMARY KEY (job_id, skill_id)
);
