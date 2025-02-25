import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


def lectura(archivo):
    df = pd.read_csv(archivo)

    df["DATE"] = pd.to_datetime(df["DATE"], format="%B %d, %Y")

    # Ordenar el DataFrame por la columna de fechas
    df = df.sort_values(by="DATE")
    df = df.reset_index()
    df.head()

    return df

def limpieza_na(df):
    """Función para limpiar los NAs, tras estudiar el dataframe vemos que los NAs están representados con ---
    por lo tanto primero sustituyo los --- por NAs e imputo los NAs calculando los valores manualmente,
    ya que las columnas con NAs eran porcentajes los cuales se podían hallar"""
    columnas_con_na = []

    for columnas in df.columns:
        if (df[columnas] == "---").any():
            columnas_con_na.append(columnas)


    indices_con_na_sig_str_a = df.index[df['SIG_STR_A'] == '---'].tolist()

    print(indices_con_na_sig_str_a)

    for columna in columnas_con_na:
        df[columna] = df[columna].replace('---', np.nan)
        
    df['SIG_STR_A'] = df['SIG_STR_A'].fillna(df.apply(lambda row: (row['TOTAL_STR_A_x'] / row['TOTAL_STR_A_y'])*100 if row['TOTAL_STR_A_y'] != 0 else 0, axis=1))

    df['SIG_STR_B'] = df['SIG_STR_B'].fillna(df.apply(lambda row: (row['TOTAL_STR_B_x'] / row['TOTAL_STR_B_y'])*100 if row['TOTAL_STR_B_y'] != 0 else 0, axis=1))

    df['TD_PORC_A'] = df['TD_PORC_A'].fillna(df.apply(lambda row: (row['TD_A_x'] / row['TD_A_y'])*100 if row['TD_A_y'] != 0 else 0, axis=1))

    df['TD_PORC_B'] = df['TD_PORC_B'].fillna(df.apply(lambda row: (row['TD_B_x'] / row['TD_B_y'])*100 if row['TD_B_y'] != 0 else 0, axis=1))

    print(df.loc[indices_con_na_sig_str_a, ['SIG_STR_A','TOTAL_STR_A_x', 'TOTAL_STR_A_y']])
    return df

def limpieza_of(df):
    """Elimino las columnas que tenían el tipo x of y, creando dos columnas la columna x y la columna y separando los valores 
    y estableciendo estas columnas como numéricas"""
    columnas_con_of = ['TOTAL_STR_A', 'TOTAL_STR_B', 
                     'TD_A', 'TD_B', 'STR_HEAD_A', 'STR_HEAD_B', 'STR_BODY_A', 'STR_BODY_B', 
                     'STR_LEG_A', 'STR_LEG_B', 'STR_DISTANCE_A', 'STR_DISTANCE_B',	'STR_CLINCH_A',	'STR_CLINCH_B',	'STR_GROUND_A'	,'STR_GROUND_B']


    for col in columnas_con_of:
        df[col] = df[col].astype(str)
        df[[f'{col}_x', f'{col}_y']] = df[col].str.extract(r'(\d+)\s*of\s*(\d+)', expand=True)
        df[[f'{col}_x', f'{col}_y']] = df[[f'{col}_x', f'{col}_y']].apply(pd.to_numeric, errors='coerce')


    df = df.drop(columns=columnas_con_of, errors="ignore") 

    df.head()
    return df

def convertir_porcentaje(valor):
    """"Convierto el valor con porcentajes a tipo float eliminando también el símbolo(%)"""
    if isinstance(valor, str) and "%" in valor:
        return float(valor.strip("%")) / 100
    
    return valor/100

def limpieza_porcentajes(df):
    """Aplico convertir_porcentaje a las columnas con porcentajes"""
    # Columnas que contienen porcentajes
    columnas_porcentaje = ["SIG_STR_A", "SIG_STR_B", "TD_PORC_A", "TD_PORC_B"]

    # Aplicar la conversión
    for col in columnas_porcentaje:
        df[col] = df[col].apply(convertir_porcentaje)

    # Verificar los cambios
    print(df[columnas_porcentaje].head())
    return df

def convertir_a_segundos(tiempo):
    """Función que pasa de escala segundos:minutos a solo segundos"""
    if isinstance(tiempo, str) and ":" in tiempo:
        minutos, segundos = map(int, tiempo.split(":"))
        return minutos * 60 + segundos
    return 0  # Si el valor no es un string con formato válido, poner 0

def nuevas_columnas(df):
    """"Creo nuevas columnas que podrán ser útiles en el futuro
    como diferencias entre los peleadores durante el combate o el tipo de 
    estilo de cada luchador"""
    df['KD_DIFF'] = df['KD_A'] - df['KD_B'] #Creo columna de diferencia de knockdowns

    df['SIG_STR_DIFF'] = df['SIG_STR_A'] - df['SIG_STR_B'] #Diferencia de golpes significativos


    df['TD_DIFF'] = (df['TD_A_x']/(df['TD_A_y']+1)) - (df['TD_B_x']/(df['TD_B_y']+1)) #Diferencia de efectividad en derribos


    df['SUB_ATT_DIFF'] = df['SUB_ATT_A'] - df['SUB_ATT_B'] #Diferencia intentos de submisión

    df['REV_DIFF'] = df['REV_A'] - df['REV_B'] #Diferencia en reversals

    df['CTRL_DIFF'] = df['CTRL_A'] - df['CTRL_B'] #Diferencia de tiempo controlado
    
    ##Varibales para saber el estilo de peleador
    df['STRIKER_A'] = df['TOTAL_STR_A_y']/(df['TD_A_y'] + 1) #Estudio si lanza muchos golpes y intenta pocos derribos

    df['STRIKER_B'] = df['TOTAL_STR_B_y']/(df['TD_B_y'] + 1)

    df['GRAPPLER_A'] = df['TD_A_y']/(df['TOTAL_STR_A_y'] + 1) #Hago lo contrario 

    df['GRAPPLER_B'] = df['TD_B_y']/(df['TOTAL_STR_B_y'] + 1)
    return df

def obtener_peleas_por_titulo(df):
    """Obtengo si la pelea es por un titulo o no creando una nueva columna"""
    #Filtrar peleas por titulo 
    df["TITLE_FIGHT"] =  df["CATEGORY"].str.contains("TITLE", case=False, na=False)

    print(df[["TITLE_FIGHT","CATEGORY"]])

    return df

def obtener_peleas_mujeres(df):
    """Creo una nueva columna sobre el género del comabate(Masculino o Femenino)"""
    df["WOMEN"] = df["CATEGORY"].str.contains("WOMEN",case=False,na=False)

    return df

def filtrar_por_categorias(df):
    """Creo una nueva columna la cual guarda el peso del combate(Peso Pluma, Peso Pesado...)"""
    df["CATEGORY"] = df["CATEGORY"].str.replace(
    r"\bLIGHT HEAVYWEIGHT\b", "LIGHTHEAVYWEIGHT", regex=True
    )

    df["CATEGORY"] = df["CATEGORY"].str.extract(r"(\b\w+WEIGHT\b)", expand=False)

    print(df["CATEGORY"].value_counts())

    return df

def limpiar_round(df):
        """Limpio la columna Round"""
        df["ROUND"] = df["ROUND"].str.replace('ROUND: ','',regex=False)

        df["ROUND"]

def pasar_a_dummies(df,col):
    """"Paso a columnas dummies ciertas columnas"""
    df = pd.get_dummies(df, columns=[col], drop_first=True)

    return df



df = lectura("C:/Users/mattu/OneDrive/Documentos/GitHub/c2425-R4/src/transformacion/csv_peleas.csv")
print(df.head())

df = limpieza_of(df)
df = limpieza_na(df)
df = limpieza_porcentajes(df)
df['WINNER'] = df['WINNER'].astype(bool)
df["CTRL_A"] = df["CTRL_A"].apply(convertir_a_segundos)
df["CTRL_B"] = df["CTRL_B"].apply(convertir_a_segundos)
df = nuevas_columnas(df)
df["TIME"] = df["TIME"].str.replace('TIME: ', '',regex=False)
df["TIME"] = df["TIME"].apply(convertir_a_segundos)
df = obtener_peleas_por_titulo(df)
df = obtener_peleas_mujeres(df)
df = filtrar_por_categorias(df)
df = pasar_a_dummies(df,'METHOD')
df["ROUND"] = df["ROUND"].str.replace('ROUND: ','',regex=False)

#Crear dataframe invirtiendo los datos de los peleadores 
df_invertido=df.rename(columns={
    'Peleador_A':'Peleador_B',
    'Peleador_B':'Peleador_A',
    'KD_A':'KD_B',
    'KD_B':'KD_A',
    'SIG_STR_A':'SIG_STR_B',
    'SIG_STR_B':'SIG_STR_A',
    'TD_PORC_A':'TD_PORC_B',
    'TD_PORC_B':'TD_PORC_A',
    'SUB_ATT_A':'SUB_ATT_B',
    'SUB_ATT_B':'SUB_ATT_A',
    'REV_A':'REV_B',
    'REV_B':'REV_A',
    'CTRL_A':'CTRL_B',
    'CTRL_B':'CTRL_A',
    'TOTAL_STR_A_x':'TOTAL_STR_B_x',
    'TOTAL_STR_B_x':'TOTAL_STR_A_x',
    'TOTAL_STR_A_y':'TOTAL_STR_B_y',
    'TOTAL_STR_B_y':'TOTAL_STR_A_y',
    'TD_A_x':'TD_B_x',
    'TD_B_x':'TD_A_x',
    'TD_A_y':'TD_B_y',
    'TD_B_y':'TD_A_y',
    'STR_HEAD_A_x':'STR_HEAD_B_x',
    'STR_HEAD_B_x':'STR_HEAD_A_x',
    'STR_HEAD_A_y':'STR_HEAD_B_y',
    'STR_HEAD_B_y':'STR_HEAD_A_y',
    'STR_BODY_A_x':'STR_BODY_B_x',
    'STR_BODY_B_x':'STR_BODY_A_x',
    'STR_BODY_A_y':'STR_BODY_B_y',
    'STR_BODY_B_y':'STR_BODY_A_y',
    'STR_LEG_A_x':'STR_LEG_B_x',
    'STR_LEG_B_x':'STR_LEG_A_x',
    'STR_LEG_A_y':'STR_LEG_B_y',
    'STR_LEG_B_y':'STR_LEG_A_y',
    'STR_DISTANCE_A_x':'STR_DISTANCE_B_x',
    'STR_DISTANCE_B_x':'STR_DISTANCE_A_x',
    'STR_DISTANCE_A_y':'STR_DISTANCE_B_y',
    'STR_DISTANCE_B_y':'STR_DISTANCE_A_y',
    'STR_CLINCH_A_x':'STR_CLINCH_B_x',
    'STR_CLINCH_B_x':'STR_CLINCH_A_x',
    'STR_CLINCH_A_y':'STR_CLINCH_B_y',
    'STR_CLINCH_B_y':'STR_CLINCH_A_y',
    'STR_GROUND_A_x':'STR_GROUND_B_x',
    'STR_GROUND_B_x':'STR_GROUND_A_x',
    'STR_GROUND_A_y':'STR_GROUND_B_y',
    'STR_GROUND_B_y':'STR_GROUND_A_y',

})[df.columns]

#Unir ambos dataframe
df=pd.concat([df,df_invertido],ignore_index=True)

df.to_csv("df_peleas_limpio.csv")



