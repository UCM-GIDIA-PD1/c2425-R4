import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score,log_loss, make_scorer, f1_score, roc_auc_score, precision_score, recall_score

def calcular_ultimas_tres(df):
    """
    Realizado por Mateo Turati.
    Dado un dataframe con las columnas Peleador_A, Peleador_B y DATE consulta si existen 
    tres peleas anteriores para cada peleador. En caso de que existan se crea un nuevo dataframe
    con las medias ponderadas de cada atributo del dataframe de peleas respecto a sus tres últimas 
    peleas. 
    El principal objetivo este nuevo dataframe será que sea usado para realizar un modelo para 
    predecir peleas futuras basándose en las medias ponderadas de sus últimas peleas.
    Item Backlog: Script para obtener dataframe de peleas con medias ponderadas
    """
    # Asegurarse de que DATE esté como datetime
    df['DATE'] = pd.to_datetime(df['DATE'])
    df = df[df["DATE"] >= "2010-01-01"].reset_index(drop=True)
    
    # Crear listas para almacenar los resultados
    peleas_ajustadas = []
    
    for _, pelea in df.iterrows():
        fecha = pelea['DATE']
        peleador_a = pelea['Peleador_A']
        peleador_b = pelea['Peleador_B']
        
        # Obtener las últimas tres peleas de cada peleador antes de la pelea actual
        peleas_a = df[(df['DATE'] < fecha) & 
                    ((df['Peleador_A'] == peleador_a) | (df['Peleador_B'] == peleador_a))].tail(3)
        
        peleas_b = df[(df['DATE'] < fecha) & 
                    ((df['Peleador_A'] == peleador_b) | (df['Peleador_B'] == peleador_b))].tail(3)
        
        if len(peleas_a) < 3 or len(peleas_b) < 3: #Si no tienen tres peleas anteriores no se procesa ese combate
            continue

        # Calcular la media ponderada para cada atributo
        def media_ponderada(peleas,peleador,columnas_a,columnas_b,columnas_gen):
            assert not peleas.empty, "Pelea vacio"
            dic = {}
            peleas = peleas.sort_values(by='DATE',ascending=False)
            # Tomar los valores como matriz y ajustar los pesos según el número de peleas
            for col_a, col_b, col_gen in zip(columnas_a, columnas_b, columnas_gen):
                values = []
                for _, pelea in peleas.iterrows():
                    values.append(pelea[col_a] if peleador == pelea['Peleador_A'] else pelea[col_b])
                values_series = pd.Series(values)
                ewm_mean = values_series.ewm(span=4, adjust=False).mean().iloc[-1]
                dic[col_gen] = ewm_mean
                    
            return dic
        
        columnas_a = [
            'KD_A', 'SIG_STR_A', 'TD_PORC_A', 'SUB_ATT_A', 'REV_A', 'CTRL_A',
            'TOTAL_STR_A_x', 'TOTAL_STR_A_y', 'TD_A_x', 'TD_A_y', 'STR_HEAD_A_x',
            'STR_HEAD_A_y', 'STR_BODY_A_x', 'STR_BODY_A_y', 'STR_LEG_A_x',
            'STR_LEG_A_y', 'STR_DISTANCE_A_x', 'STR_DISTANCE_A_y',
            'STR_CLINCH_A_x', 'STR_CLINCH_A_y', 'STR_GROUND_A_x', 'STR_GROUND_A_y',
            'STRIKER_A', 'GRAPPLER_A','Victorias_KO_A', 'Victorias_Sub_A', 'Victorias_Decision_A',
                                       'Derrotas_KO_A', 'Derrotas_Sub_A', 'Derrotas_Decision_A'
        ]
        
        columnas_b = [
            'KD_B', 'SIG_STR_B', 'TD_PORC_B', 'SUB_ATT_B', 'REV_B', 'CTRL_B',
            'TOTAL_STR_B_x', 'TOTAL_STR_B_y', 'TD_B_x', 'TD_B_y', 'STR_HEAD_B_x',
            'STR_HEAD_B_y', 'STR_BODY_B_x', 'STR_BODY_B_y', 'STR_LEG_B_x',
            'STR_LEG_B_y', 'STR_DISTANCE_B_x', 'STR_DISTANCE_B_y',
            'STR_CLINCH_B_x', 'STR_CLINCH_B_y', 'STR_GROUND_B_x', 'STR_GROUND_B_y',
            'STRIKER_B', 'GRAPPLER_B','Victorias_KO_B', 'Victorias_Sub_B', 'Victorias_Decision_B',
                                       'Derrotas_KO_B', 'Derrotas_Sub_B', 'Derrotas_Decision_B'
        ]
        
        atributos_generales = [
            'KD', 'SIG_STR', 'TD_PORC', 'SUB_ATT', 'REV', 'CTRL',
            'TOTAL_STR_x', 'TOTAL_STR_y', 'TD_x', 'TD_y', 'STR_HEAD_x',
            'STR_HEAD_y', 'STR_BODY_x', 'STR_BODY_y', 'STR_LEG_x',
            'STR_LEG_y', 'STR_DISTANCE_x', 'STR_DISTANCE_y',
            'STR_CLINCH_x', 'STR_CLINCH_y', 'STR_GROUND_x', 'STR_GROUND_y',
            'STRIKER', 'GRAPPLER','Victorias_KO', 'Victorias_Sub', 'Victorias_Decision',
                                       'Derrotas_KO', 'Derrotas_Sub', 'Derrotas_Decision'
        ]


        media_a = media_ponderada(peleas_a, peleador_a, columnas_a,columnas_b,atributos_generales)
        media_b = media_ponderada(peleas_b, peleador_b, columnas_a,columnas_b,atributos_generales)

        
        pelea_ajustada = {
            'DATE': fecha,
            'Peleador_A': peleador_a,
            'Peleador_B': peleador_b,
            'WINNER': pelea['WINNER']
        }
        
        for cont in range(len(columnas_a)):
            pelea_ajustada[columnas_a[cont]] = media_a[atributos_generales[cont]]
            pelea_ajustada[columnas_b[cont]] = media_b[atributos_generales[cont]]


        def actualizar_record(peleador,ult_pelea):
            """"Actualiza el record teniendo en cuenta el resultado de su última pelea"""

            if peleador == ult_pelea["Peleador_A"] and ult_pelea["WINNER"] == 0:
                return ult_pelea["Record_A"] +1
            elif peleador == ult_pelea["Peleador_B"] and ult_pelea["WINNER"] == 1:
                return ult_pelea["Record_B"] +1
            elif peleador == ult_pelea["Peleador_B"]:
                return ult_pelea["Record_B"] - 1
            else:
                return ult_pelea["Record_A"] - 1

        pelea_ajustada['Record_A'] = actualizar_record(peleador_a,peleas_a.iloc[-1])
        pelea_ajustada['Record_B'] = actualizar_record(peleador_b,peleas_b.iloc[-1])
        

        def actualizar_racha(peleador,ult_pelea):
            """"Actualiza la racha teniendo en cuenta el resultado de su última pelea"""

            if peleador == ult_pelea["Peleador_A"] and ult_pelea["WINNER"] == 0:
                return ult_pelea["Racha_A"] +1
            elif peleador == ult_pelea["Peleador_B"] and ult_pelea["WINNER"] == 1:
                return ult_pelea["Racha_B"] +1
            elif peleador == ult_pelea["Peleador_B"]:
                return 0
            else:
                return 0

        pelea_ajustada['Racha_A'] = actualizar_racha(peleador_a,peleas_a.iloc[-1])
        pelea_ajustada['Racha_B'] = actualizar_racha(peleador_b,peleas_b.iloc[-1])

        def actualizar_puntos(peleador,ult_pelea):
            """Función que establece los puntos de su futura pelea teniendo en cuenta lo 
            que paso en la última"""
            pelea = ult_pelea
            if peleador == pelea["Peleador_A"]:
                if pelea["WINNER"] == 0:
                    nuevos_puntos = max(pelea["Puntos_A"],pelea["Puntos_B"])
                else:
                    nuevos_puntos = pelea["Puntos_A"] - pelea["Puntos_A"]* 0.1
            else:
                if pelea["WINNER"] == 1:
                    nuevos_puntos = max(pelea["Puntos_A"],pelea["Puntos_B"])
                else:
                    nuevos_puntos = pelea["Puntos_B"] - pelea["Puntos_B"]* 0.1
            return nuevos_puntos

        pelea_ajustada["Puntos_A"] = actualizar_puntos(peleador_a,peleas_a.iloc[-1])
        pelea_ajustada["Puntos_B"] = actualizar_puntos(peleador_b,peleas_b.iloc[-1])


        
        peleas_ajustadas.append(pelea_ajustada)

    # Convertir resultados a un DataFrame
    df_ajustado = pd.DataFrame(peleas_ajustadas)

    df_ajustado['KD_DIFF'] = df_ajustado['KD_A'] - df_ajustado['KD_B'] #Creo columna de diferencia de knockdowns

    df_ajustado['SIG_STR_DIFF'] = df_ajustado['SIG_STR_A'] - df_ajustado['SIG_STR_B'] #Diferencia de golpes significativos


    df_ajustado['TD_DIFF'] = (df_ajustado['TD_A_x']/(df_ajustado['TD_A_y']+1)) - (df_ajustado['TD_B_x']/(df_ajustado['TD_B_y']+1)) #Diferencia de efectividad en derribos


    df_ajustado['SUB_ATT_DIFF'] = df_ajustado['SUB_ATT_A'] - df_ajustado['SUB_ATT_B'] #Diferencia intentos de submisión

    df_ajustado['REV_DIFF'] = df_ajustado['REV_A'] - df_ajustado['REV_B'] #Diferencia en reversals

    df_ajustado['CTRL_DIFF'] = df_ajustado['CTRL_A'] - df_ajustado['CTRL_B'] #Diferencia de tiempo controlado
    print(df_ajustado)
    return df_ajustado


ruta = os.path.join(os.getcwd(), "..", "..", "data", "processed", "peleas.parquet")
df = pd.read_parquet(ruta)
df_pond= calcular_ultimas_tres(df)
print("Ponderadas")
print(df_pond[(df_pond["Peleador_A"] == "Ilia Topuria") | (df_pond["Peleador_B"] == "Ilia Topuria")][["Peleador_A","Peleador_B","Puntos_A","Puntos_B","Record_A","Record_B","Racha_A","Racha_B","DATE"]])
print("Original")
print(df[(df["Peleador_A"] == "Ilia Topuria") | (df["Peleador_B"] == "Ilia Topuria")][["Peleador_A","Peleador_B","Puntos_A","Puntos_B","Record_A","Record_B","Racha_A","Racha_B","DATE"]])