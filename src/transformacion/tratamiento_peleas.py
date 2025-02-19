import pandas as pd 
import numpy as np

df = pd.read_csv("df_peleas_inicial.csv")


columnas_con_na = []

for columnas in df.columns:
    if (df[columnas] == "---").any():
        columnas_con_na.append(columnas)


indices_con_na_sig_str_a = df.index[df['SIG_STR_A'] == '---'].tolist()

#print(indices_con_na_sig_str_a)

for columna in columnas_con_na:
    df[columna] = df[columna].replace('---', np.nan)
    
#print(columnas_con_na)

#Quito el of de las columnas x of y, me quedo solo con x.
columnas_con_of = ['TOTAL_STR_A', 'TOTAL_STR_B', 
                     'TD_A', 'TD_B', 'STR_HEAD_A', 'STR_HEAD_B', 'STR_BODY_A', 'STR_BODY_B', 
                     'STR_LEG_A', 'STR_LEG_B', 'STR_DISTANCE_A', 'STR_DISTANCE_B',	'STR_CLINCH_A',	'STR_CLINCH_B',	'STR_GROUND_A'	,'STR_GROUND_B']


for col in columnas_con_of:
    df[col] = df[col].astype(str)
    df[[f'{col}_x', f'{col}_y']] = df[col].str.extract(r'(\d+)\s*of\s*(\d+)', expand=True)
    df[[f'{col}_x', f'{col}_y']] = df[[f'{col}_x', f'{col}_y']].apply(pd.to_numeric, errors='coerce')


df = df.drop(columns=columnas_con_of, errors="ignore") 


df['SIG_STR_A'] = df['SIG_STR_A'].fillna(df.apply(lambda row: (row['TOTAL_STR_A_x'] / row['TOTAL_STR_A_y'])*100 if row['TOTAL_STR_A_y'] != 0 else 0, axis=1))

df['SIG_STR_B'] = df['SIG_STR_B'].fillna(df.apply(lambda row: (row['TOTAL_STR_B_x'] / row['TOTAL_STR_B_y'])*100 if row['TOTAL_STR_B_y'] != 0 else 0, axis=1))

df['TD_PORC_A'] = df['TD_PORC_A'].fillna(df.apply(lambda row: (row['TD_A_x'] / row['TD_A_y'])*100 if row['TD_A_y'] != 0 else 0, axis=1))

df['TD_PORC_B'] = df['TD_PORC_B'].fillna(df.apply(lambda row: (row['TD_B_x'] / row['TD_B_y'])*100 if row['TD_B_y'] != 0 else 0, axis=1))

#print(df.loc[indices_con_na_sig_str_a, ['SIG_STR_A','TOTAL_STR_A_x', 'TOTAL_STR_A_y']])

def convertir_porcentaje(valor):
    if isinstance(valor, str) and "%" in valor:
        return float(valor.strip("%")) / 100
    return valor

# Columnas que contienen porcentajes
columnas_porcentaje = ["SIG_STR_A", "SIG_STR_B", "TD_PORC_A", "TD_PORC_B"]

# Aplicar la conversión
for col in columnas_porcentaje:
    df[col] = df[col].apply(convertir_porcentaje)

# Verificar los cambios
#print(df[columnas_porcentaje].head())

# Convertir las columnas de tiempo (CTRL_A, CTRL_B) en segundos
def convertir_a_segundos(tiempo):
    if isinstance(tiempo, str) and ":" in tiempo:
        minutos, segundos = map(int, tiempo.split(":"))
        return minutos * 60 + segundos
    return 0  # Si el valor no es un string con formato válido, poner 0

df["CTRL_A"] = df["CTRL_A"].apply(convertir_a_segundos)
df["CTRL_B"] = df["CTRL_B"].apply(convertir_a_segundos)

#Limpieza columna TIME y paso a segundos los minutos

df["TIME"] = df["TIME"].str.replace('TIME: ', '',regex=False)

df["TIME"] = df["TIME"].apply(convertir_a_segundos)
#df["TIME"]

df["ROUND"] = df["ROUND"].str.replace('ROUND: ','',regex=False)

#df["ROUND"]

#df["METHOD"].unique()

df = pd.get_dummies(df, columns=['METHOD'], drop_first=True)

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

df = df.drop(columns=['Peleador_A', 'Peleador_B', 'DATE','KD_A','KD_B'])


# 1. Definir la variable objetivo y las predictoras
X = df.drop('WINNER', axis=1)  # Variables predictoras
y = df['WINNER']               # Variable objetivo

# 2. Dividir en conjunto de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Crear el modelo de clasificación (Random Forest en este caso)
modelo = RandomForestClassifier(random_state=42)

# 4. Entrenar el modelo
modelo.fit(X_train, y_train)

# 5. Hacer predicciones
y_pred = modelo.predict(X_test)

# 6. Evaluar el rendimiento (Accuracy)
accuracy = accuracy_score(y_test, y_pred)
#print(f'Accuracy del modelo: {accuracy:.4f}')

importancias = modelo.feature_importances_

importancia_df = pd.DataFrame({
    'Característica': X.columns,
    'Importancia': importancias
})

# Ordenar de mayor a menor importancia
importancia_df = importancia_df.sort_values(by='Importancia', ascending=False)

#print(importancia_df)

#guardo cambios
df.to_csv("df_peleas_limpio.csv")