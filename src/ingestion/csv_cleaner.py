import pandas as pd
import json
import os
import ast

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
    df=df.head(10000)  # Limitar a las primeras 10000 filas

    df["job_skills"] = df["job_skills"].apply(parse_skills)
    df["job_type_skills"] = df["job_type_skills"].apply(parse_skills)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"CSV limpio guardado en {output_path}")