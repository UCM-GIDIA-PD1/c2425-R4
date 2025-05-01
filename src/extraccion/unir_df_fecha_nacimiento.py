import os
import pandas as pd

def unir():
    """Función que une los distintos .csv generados"""
    # Ruta de la carpeta con los archivos CSV
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    carpeta = os.path.join(base_dir, "data", "raw", "nacimiento_peleadores")

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
