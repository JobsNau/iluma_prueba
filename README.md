# Proyecto de Ingeniería de Datos - iluma_prueba

Este proyecto implementa un pipeline completo de ingeniería de datos que procesa una gran cantidad de ofertas laborales, valida su calidad, y las transforma en un modelo relacional normalizado en tercera forma normal (3FN), utilizando Python, PostgreSQL y Docker.

---

## 1. Decisiones de Diseño

### 🔹 Arquitectura Modular

El código está estructurado en módulos especializados, lo que facilita el mantenimiento, la escalabilidad y la colaboración entre desarrolladores. Cada módulo cumple una función específica dentro del pipeline:

- `ingestion/`: limpieza, transformación inicial y carga de los datos crudos.
- `db/`: conexión a la base de datos, definición y migración del esquema relacional.
- `schemas/`: validación de datos utilizando Pandera para asegurar la calidad antes de la carga.
- `tests/`: pruebas automatizadas (con Pytest) para verificar la integridad y consistencia de los datos.
- `utils/`: utilidades y funciones de soporte, como el manejo centralizado de logs y configuración.

Esta estructura modular sigue principios de buenas prácticas como la separación de responsabilidades, facilitando la extensión y el testeo del pipeline.

### 🔹 Modelo Relacional en 3FN

El modelo de datos fue diseñado bajo los principios de la **Tercera Forma Normal (3FN)** con el objetivo de eliminar la redundancia, garantizar la integridad referencial y facilitar el análisis. A continuación, se describen los componentes principales del modelo:

#### Tabla de Hechos: `report.jobs`

La tabla principal `report.jobs` representa cada **oferta de trabajo individual** y contiene atributos propios del hecho:

- `title_short`, `title_raw`, `posted_date`, `salary_year_avg`, `salary_hour_avg`, `work_from_home`, `no_degree_mention`, `health_insurance`
- Llaves foráneas a dimensiones: `company_id`, `location_id`, `schedule_id`, `source_id`, `country_id`, `salary_rate_id`
- `job_row_id`: campo auxiliar único para trazabilidad contra el archivo original

Esta tabla constituye el **centro del modelo relacional**.

#### Tablas Dimensionales

Para reducir redundancia y permitir una mejor estructura analítica, se separaron los siguientes atributos en **tablas dimensionales**:

| Tabla                | Descripción                                                  |
|----------------------|--------------------------------------------------------------|
| `report.companies`   | Empresa que publica la oferta                                |
| `report.locations`   | Ciudad o región específica de la vacante                     |
| `report.schedules`   | Tipo de jornada laboral (tiempo completo, parcial, etc.)     |
| `report.sources`     | Fuente de publicación (Indeed, LinkedIn, etc.)               |
| `report.countries`   | País donde se localiza la oferta                             |
| `report.salary_rates`| Periodicidad del salario (anual o por hora)                  |
| `report.skills`      | Habilidades mencionadas en cada vacante                      |

#### Relación muchos-a-muchos: `report.job_skills`

La relación entre `jobs` y `skills` es de tipo **muchos a muchos**. Para modelarla correctamente se creó la tabla intermedia:

```sql
CREATE TABLE report.job_skills (
    job_id INT REFERENCES report.jobs(id),
    skill_id INT REFERENCES report.skills(id),
    PRIMARY KEY (job_id, skill_id)
);
```
---


### 🔹 Herramientas Utilizadas

| Herramienta           | Justificación                                                                 |
|------------------------|------------------------------------------------------------------------------|
| **PostgreSQL + Docker**| Base de datos relacional confiable y contenedorizada fácilmente con Docker. |
| **Python (pandas)**    | Transformación eficiente de grandes volúmenes de datos tabulares.            |
| **Pandera**            | Validación robusta del `DataFrame` antes de la carga en la base de datos.    |
| **Pytest**             | Automatización de pruebas de calidad de datos.                               |
| **Logging**            | Registro profesional de errores, ejecuciones y trazabilidad del pipeline.    |

---

### 🔹 Consideraciones Generales
* Antes de ejecutar `main.py`, verifica que el archivo `data_jobs.csv` se encuentre en la ruta `./data/data_jobs.csv` (relativa al root del proyecto) y que esté en formato CSV estándar (delimitado por comas, codificación UTF-8).
* La forma de cargar la información proveniente de `data_jobs.csv` se hace por medio de `copyexport` a la base de datos, esto se realiza por rapidez.
* Antes de subir la información a la base de datos, se realiza una validación con Pandera para garantizar la integridad de los datos y evitar cargar datos sucios.
* Además, se configuran las columnas `job_skills` garantizando que sean de tipo `list` y `job_type_skills` garantizando que sean de tipo `dict`.


##  2. Instrucciones de Ejecución

### 🔸 Requisitos Previos

- Python 3.10+
- Docker y Docker Compose
- Instalar librerias de python. `pip install -r requirements.txt`

### 🔸 Configuración Inicial

1. Clonar el repositorio:

```bash
git clone https://github.com/JobsNau/iluma_prueba.git
cd iluma_prueba
```

2. Crear un archivo `.env` en la ruta `./docker/.env` con el siguiente contenido:

```env
POSTGRES_USER=postgres_user
POSTGRES_PASSWORD=postgres_password
POSTGRES_DB=iluma_db
POSTGRES_PORT=5433
POSTGRES_HOST=localhost
```

3. Levantar el entorno de base de datos:

```bash
docker-compose up -d
```

4. Crear tablas para el modelo relacional

Las definiciones SQL de todas las tablas del modelo relacional (incluyendo `report.jobs`, dimensiones y relaciones) se encuentran en el archivo [`/src/db/schema_report.sql`](./src/db/schema_report.sql).  

Asegúrate de que la base de datos esté corriendo y que las variables de entorno coincidan con tu configuración.

5. Ejecutar el pipeline completo:

```bash
python main.py
```

Esto realiza:

- Limpieza y validación del archivo `data_jobs.csv`
- Validación con Pandera
- Carga en tabla de staging `carga.data_jobs`
- Transformación y normalización a 3FN en `report.*`

---

## 3. Guía de Testing

### 🔸 Objetivo de las Pruebas

Las pruebas verifican:

- Integridad referencial entre tablas
- Que no existan datos nulos donde no deben
- Que las dimensiones estén correctamente pobladas
- Calidad general del proceso de normalización

### 🔸 Ejecución Manual de Pruebas

```bash
pytest -v tests/  
```

### 🔸 Estructura de Pruebas

| Archivo                        | Propósito                                              |
|-------------------------------|--------------------------------------------------------|
| `test_jobs_table.py`          | Verifica integridad de la tabla principal `report.jobs` |
| `test_foreign_keys.py`        | Comprueba claves foráneas hacia dimensiones            |
| `test_skills.py`              | Valida relación muchos-a-muchos de habilidades         |

---

## 4. DAG de Airflow

A continuación se muestra un ejemplo sencillo de un DAG de Apache Airflow para orquestar el pipeline de ingeniería de datos. Este DAG está etiquetado como `desarrollo`, se ejecuta todos los días a las 5:00 AM y realiza tareas básicas de ejemplo.

```python
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='iluma_pipeline_dag',
    default_args=default_args,
    description='DAG de desarrollo para pipeline de ingeniería de datos',
    schedule_interval='0 5 * * *',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['desarrollo'],
    ) as dag:


    ejecutar_pipeline = BashOperator(
        task_id='ejecutar_pipeline',
        bash_command='python /usr/local/airflow/dags/main.py'
    )
```
---


## Autor

**Jobany Nausa Cáceres**  
Ingeniero de Datos | Python | PostgreSQL | Docker | ETL


