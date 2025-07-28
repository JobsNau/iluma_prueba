import pandas as pd
import json
import os
import ast
import pandera
from src.utils.logger import get_logger
from src.schemas.job_schema import job_schema
logger = get_logger(__name__)

def parse_skills(val):
    if pd.isna(val):
        return None
    if isinstance(val, str):
        try:
            val = ast.literal_eval(val)
        except (ValueError, SyntaxError):
            return None
    return json.dumps(val)

def clean_csv(input_path: str, output_path: str):
    df = pd.read_csv(input_path)
    
    try:
        validated_df = job_schema.validate(df, lazy=True)
        logger.info("CSV validado correctamente.")
    except pandera.errors.SchemaErrors as err:
        logger.error("Errores encontrados en validación:")
        logger.error(err.failure_cases)
        raise
    validated_df = validated_df.head(100000)

    validated_df["job_skills"] = validated_df["job_skills"].apply(parse_skills)
    validated_df["job_type_skills"] = validated_df["job_type_skills"].apply(parse_skills)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    validated_df.to_csv(output_path, index=False)
    logger.info("CSV limpio guardado en %s", output_path)