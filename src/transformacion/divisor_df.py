import os
import pandas as pd

# Cargar el dataframe original
# Supongamos que el dataframe se encuentra en un archivo CSV llamado 'data.csv'
df = pd.read_csv('fighters_completo.csv')

# Número de observaciones por grupo
n = 100

# Crear carpeta de destino si no existe
output_folder = 'dataframes_divididos'
os.makedirs(output_folder, exist_ok=True)

# Dividir el dataframe y guardarlo en archivos separados
for i in range(0, len(df), n):
    # Seleccionar un grupo de n observaciones
    df_group = df.iloc[i:i+n]
    # Generar nombre de archivo, p. ej. 'grupo_1.csv', 'grupo_2.csv', etc.
    group_number = i // n + 1
    output_path = os.path.join(output_folder, f'grupo_{group_number}.csv')
    # Guardar el dataframe en un archivo CSV
    df_group.to_csv(output_path, index=False)
    print(f'Guardado {output_path}')
