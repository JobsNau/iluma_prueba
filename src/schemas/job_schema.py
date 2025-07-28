import pandera as pa
from pandera import Column, DataFrameSchema, Check

job_schema = DataFrameSchema({
    "job_title_short": Column(pa.String, nullable=True),    
    "job_title": Column(pa.String, nullable=True),    
    "job_location": Column(pa.String, nullable=True),    
    "job_via": Column(pa.String, nullable=True),    
    "job_schedule_type": Column(pa.String, nullable=True),    
    "job_work_from_home": Column(pa.Bool, nullable=False),    
    "search_location": Column(pa.String, nullable=False),    
    "job_posted_date": Column(pa.String, nullable=False, checks=Check.str_matches(r"\d{4}-\d{2}-\d{2}")),    
    "job_no_degree_mention": Column(pa.Bool, nullable=False),    
    "job_health_insurance": Column(pa.Bool, nullable=False),    
    "job_country": Column(pa.String, nullable=True),    
    "salary_rate": Column(pa.String, nullable=True),    
    "salary_year_avg": Column(pa.Float, nullable=True, checks=Check.ge(0)),    
    "salary_hour_avg": Column(pa.Float, nullable=True, checks=Check.ge(0)),    
    "company_name": Column(pa.String, nullable=True),    
    "job_skills": Column(pa.String, nullable=True),    
    "job_type_skills": Column(pa.String, nullable=True)
})
