import os
from extraccion.scraper_peleas import extraer_peleas
from extraccion.scraper_peleadores import extraer_peleadores
from extraccion.scraper_fecha_nacimiento import extraer_fecha_nacimiento
from extraccion.unir_df_fecha_nacimiento import unir
from transformacion.tratamiento_peleadores import transformacion_peleadores
from transformacion.tratamiento_peleas import transformacion_peleas
from transformacion.nuevas_variables import nuevas_col
from transformacion.recordsPeleas import recordPeleas
import pandas as pd

def main():
    # Definir rutas
    base_dir = os.path.dirname(os.path.abspath(__file__))
    raw_data_dir = os.path.join(base_dir, "..","data", "raw")
    processed_data_dir = os.path.join(base_dir, "..", "data", "processed")

    os.makedirs(raw_data_dir, exist_ok=True)
    os.makedirs(processed_data_dir, exist_ok=True)

    #Extracción de datos
    
    print("Extrayendo datos de peleas...")
    df_peleas = extraer_peleas(1, 1)

    df_peleas.to_csv(r"c2425-R4/data/raw/peleas.csv", index=False, encoding="utf-8")

    print("Extrayendo datos de peleadores...")
    df_peleadores = extraer_peleadores(1, 1)

    df_peleadores.to_csv(r"c2425-R4/data/raw/peleadores.csv", index=False, encoding="utf-8")

    print("Extrayendo fechas de nacimiento...")
    extraer_fecha_nacimiento(0, 4)
    df_fechas = unir()
    
    df_fechas.to_csv(r"c2425-R4/data/raw/peleadores_fechas.csv", index=False, encoding="utf-8")
    
    # Transformaciones
    ruta_peleas = os.path.join(raw_data_dir, "peleas.csv")
    ruta_peleadores = os.path.join(raw_data_dir, "peleadores.csv")
    
    print("Transformando datos de peleadores...")
    df_peleadores = transformacion_peleadores(ruta_peleadores)
    
    print("Transformando datos de peleas...")
    df_peleas = transformacion_peleas(ruta_peleas)
    df_peleas = nuevas_col(df_peleas, df_peleadores)
    df_peleas = recordPeleas(df_peleadores, df_peleas)
    
    # Guardar archivos
    df_peleas.to_parquet(os.path.join(processed_data_dir, "peleas.parquet"), index=False)
    df_peleadores.to_parquet(os.path.join(processed_data_dir, "peleadores.parquet"), index=False)
    
    print("Proceso completado. Archivos guardados en 'data/processed'.")

if __name__ == "__main__":
    main()
