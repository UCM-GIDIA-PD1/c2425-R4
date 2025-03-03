import os
import pandas as pd

def unir():
    # Ruta de la carpeta con los archivos CSV
    carpeta = r"C:\Users\andre\OneDrive - Universidad Complutense de Madrid (UCM)\Escritorio\UNIVERSIDAD\2º\2º Cuatrimestre\PD1\c2425-R4\src\data\raw\nacimiento_peleadores"

    # Ruta de salida para el archivo combinado
    ruta_salida = r"C:\Users\andre\OneDrive - Universidad Complutense de Madrid (UCM)\Escritorio\UNIVERSIDAD\2º\2º Cuatrimestre\PD1\c2425-R4\src\data\raw\peleadores.csv"

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
        
    
    return df_final
