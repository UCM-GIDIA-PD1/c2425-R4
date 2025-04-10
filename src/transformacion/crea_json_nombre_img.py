import pandas as pd
import json
import os

# Definir rutas
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
ruta_peleadores = os.path.join(base_dir, "data", "raw", "peleadores.csv")
ruta_processed = os.path.join(base_dir, "data", "processed")
ruta_json = os.path.join(ruta_processed, "imagenes.json")

# Leer el archivo CSV
df = pd.read_csv(ruta_peleadores)

# Asegurarse de que las columnas correctas están presentes
if 'Nombre' in df.columns and 'Imagen' in df.columns:
    # Crear lista de diccionarios con nombre e imagen
    peleadores_json = df[['Nombre', 'Imagen']].to_dict(orient='records')

    # Guardar como JSON en archivo
    with open(ruta_json, 'w', encoding='utf-8') as f:
        json.dump(peleadores_json, f, indent=4, ensure_ascii=False)

    print(f"JSON guardado correctamente en: {ruta_json}")
else:
    print("Las columnas 'Nombre' e 'Imagen' no están presentes en el DataFrame.")
