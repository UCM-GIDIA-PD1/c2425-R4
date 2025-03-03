import os
import pandas as pd

# Ruta de la carpeta con los archivos CSV
carpeta = r"C:\Users\andre\OneDrive - Universidad Complutense de Madrid (UCM)\Escritorio\UNIVERSIDAD\2º\2º Cuatrimestre\PD1\c2425-R4\src\data\raw\nacimiento_peleadores"

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
    
    # Guardar el archivo final
    salida = os.path.join(carpeta, "peleadores.csv")
    df_final.to_csv(salida, index=False)
    print(f"Archivo combinado guardado en: {salida}")
else:
    print("No se encontraron archivos CSV en la carpeta especificada.")