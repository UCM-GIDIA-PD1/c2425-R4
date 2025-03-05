import os
import pandas as pd

def unir():
    # Ruta de la carpeta con los archivos CSV
    carpeta = r"../../data/raw/nacimiento_peleadores"

    # Ruta de salida para el archivo combinado
    ruta_salida = r"../../data/raw/peleadores_fechas.csv"

    # Lista para almacenar los DataFrames
    dataframes = []

    # Iterar sobre los archivos en la carpeta
    for archivo in os.listdir(carpeta):
        if archivo.endswith(".csv"):  # Filtrar solo los archivos CSV
            ruta_completa = os.path.join(carpeta, archivo)
            df = pd.read_csv(ruta_completa)  # Leer el archivo CSV
            dataframes.append(df)

    # Unir todos los DataFrames en uno solo
    if dataframes:
        df_final = pd.concat(dataframes, ignore_index=True)
        
        # Guardar el archivo final en la ruta de salida
        return df_final
    else:
        print("No se encontraron archivos CSV en la carpeta especificada.")
        return pd.DataFrame()
