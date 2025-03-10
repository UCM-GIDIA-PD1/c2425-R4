import os
from obtener_info_peleadores import obtener_info_peleadores
from sklearn.model_selection import train_test_split
import pandas as pd

def constructor_train_test(test_size):
    """
    Esta función se encarga de cargar los datos de peleas, dividirlos en entrenamiento y prueba y obtener 
    el conjunto de test tanto para los modelos de predicción usando datos de peleas como los modelos que usan 
    datos de los peleadores.
    """
    ruta = os.path.join(os.getcwd(), "..", "..", "data", "processed", "peleas.parquet")
    df = pd.read_parquet(ruta)
    df = df.drop(columns=["DATE","CATEGORY","METHOD","ROUND","TIME","Record_A","Record_B","STRIKER_A","STRIKER_B","GRAPPLER_A","GRAPPLER_B","TITLE_FIGHT","WOMEN"])
    X = df.drop(columns=["WINNER","Peleador_A", "Peleador_B"])
    y = df[["WINNER", "Peleador_A", "Peleador_B"]]
    X_train,X_test_peleas,y_train,y_test = train_test_split(X,y,test_size=test_size,random_state=42)
    X_test = obtener_info_peleadores(y_test["Peleador_A"].values,y_test["Peleador_B"].values)
    """
    Escribo asserts para evitar que los datos queden desplazados por errores de falta de peleadores, 
    es decir si al obtener_info_peleadores no se encuentra información de un peleador, el conjunto de test
    quedaría invalidado por lo tanto obtendríamos unos resultados del modelo erróneos.
    """
    assert len(X_test) == len(y_test), "El tamaño de X_test y y_test no coincide"
    assert (X_test["Peleador_A"].values == y_test["Peleador_A"].values).all(), "Los Peleador_A no coinciden entre X_test y y_test"
    assert (X_test["Peleador_B"].values == y_test["Peleador_B"].values).all(), "Los Peleador_B no coinciden entre X_test y y_test"
    y_train = y_train.drop(columns=["Peleador_A","Peleador_B"])
    y_test = y_test.drop(columns=["Peleador_A","Peleador_B"])
    X_test = X_test.drop(columns=["Peleador_A","Peleador_B"])
    return X_train, X_test, X_test_peleas, y_train, y_test

#X_train, X_test, X_test_peleas, y_train, y_test = constructor_train_test(0.2)
#print(X_test)
#print(X_test_peleas)