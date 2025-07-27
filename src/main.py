from src.db.database import Database
import pandas as pd
import os

def main():
    
    try:
        db = Database()
        db.connect()
        
        df = pd.read_csv("data/data_jobs.csv")
        csv_path = os.path.join("data", "data_jobs.csv")

        # db.guardar_datos(df, chunk_size=5000)
        db.cargar_csv_directo(csv_path)
        # datos = db.obtener_datos()
        
        # print("Datos obtenidos:")
        # for fila in datos:
        #     print(fila)
    finally:
        db.disconnect()

if __name__ == "__main__":
    main()
