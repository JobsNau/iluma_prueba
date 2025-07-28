import pandas as pd
import json
import os
import ast
from src.utils.logger import get_logger
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
    df=df.head(100000)

    df["job_skills"] = df["job_skills"].apply(parse_skills)
    df["job_type_skills"] = df["job_type_skills"].apply(parse_skills)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    logger.info("CSV limpio guardado en %s", output_path)