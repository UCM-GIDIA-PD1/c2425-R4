import os
import pandas as pd
import numpy as np

def calcular_ultimas_tres(df):
    # Asegurarse de que DATE esté como datetime
    df['DATE'] = pd.to_datetime(df['DATE'])
    
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
        
        if len(peleas_a) < 3 or len(peleas_b) < 3:
            continue

        # Calcular la media ponderada para cada atributo
        def media_ponderada(peleas,peleador,columnas_a,columnas_b,columnas_gen):
            assert not peleas.empty, "Pelea vacio"
            dic = {}
            peleas = peleas.sort_values(by='DATE',ascending=False)
            # Tomar los valores como matriz y ajustar los pesos según el número de peleas
            n = len(peleas)
            pesos = np.array([0.5, 0.3, 0.2])
            pesos_recortados = pesos[:n]
            for cont in range(len(columnas_gen)):
                values = []
                for _, pelea in peleas.iterrows():             
                    if peleador == pelea["Peleador_A"]:
                        values.append(pelea[columnas_a[cont]])
                    else:
                        values.append(pelea[columnas_b[cont]])
                dic[columnas_gen[cont]] = np.average(values, weights=pesos_recortados)                 
            return dic
        
        columnas_a = [
            'KD_A', 'SIG_STR_A', 'TD_PORC_A', 'SUB_ATT_A', 'REV_A', 'CTRL_A',
            'TOTAL_STR_A_x', 'TOTAL_STR_A_y', 'TD_A_x', 'TD_A_y', 'STR_HEAD_A_x',
            'STR_HEAD_A_y', 'STR_BODY_A_x', 'STR_BODY_A_y', 'STR_LEG_A_x',
            'STR_LEG_A_y', 'STR_DISTANCE_A_x', 'STR_DISTANCE_A_y',
            'STR_CLINCH_A_x', 'STR_CLINCH_A_y', 'STR_GROUND_A_x', 'STR_GROUND_A_y',
            'STRIKER_A', 'GRAPPLER_A', 'Record_A', 'Peleas_A', 'Puntos_A', 'Racha_A',
            'Victorias_KO_A', 'Victorias_Sub_A', 'Victorias_Decision_A',
            'Derrotas_KO_A', 'Derrotas_Sub_A', 'Derrotas_Decision_A'
        ]

        
        columnas_b = [  
            'KD_B', 'SIG_STR_B', 'TD_PORC_B', 'SUB_ATT_B', 'REV_B', 'CTRL_B',  
            'TOTAL_STR_B_x', 'TOTAL_STR_B_y', 'TD_B_x', 'TD_B_y', 'STR_HEAD_B_x',  
            'STR_HEAD_B_y', 'STR_BODY_B_x', 'STR_BODY_B_y', 'STR_LEG_B_x',  
            'STR_LEG_B_y', 'STR_DISTANCE_B_x', 'STR_DISTANCE_B_y',  
            'STR_CLINCH_B_x', 'STR_CLINCH_B_y', 'STR_GROUND_B_x', 'STR_GROUND_B_y',  
            'STRIKER_B', 'GRAPPLER_B', 'Record_B', 'Peleas_B', 'Puntos_B', 'Racha_B',  
            'Victorias_KO_B', 'Victorias_Sub_B', 'Victorias_Decision_B',  
            'Derrotas_KO_B', 'Derrotas_Sub_B', 'Derrotas_Decision_B'  
        ]

        atributos_generales = [  
            'KD', 'SIG_STR', 'TD_PORC', 'SUB_ATT', 'REV', 'CTRL',  
            'TOTAL_STR_x', 'TOTAL_STR_y', 'TD_x', 'TD_y', 'STR_HEAD_x',  
            'STR_HEAD_y', 'STR_BODY_x', 'STR_BODY_y', 'STR_LEG_x',  
            'STR_LEG_y', 'STR_DISTANCE_x', 'STR_DISTANCE_y',  
            'STR_CLINCH_x', 'STR_CLINCH_y', 'STR_GROUND_x', 'STR_GROUND_y',  
            'STRIKER', 'GRAPPLER', 'Record', 'Peleas', 'Puntos', 'Racha',  
            'Victorias_KO', 'Victorias_Sub', 'Victorias_Decision',  
            'Derrotas_KO', 'Derrotas_Sub', 'Derrotas_Decision'  
        ]


        media_a = media_ponderada(peleas_a, peleador_a, columnas_a,columnas_b,atributos_generales)
        media_b = media_ponderada(peleas_b, peleador_b, columnas_a,columnas_b,atributos_generales)
        
        # Añadir las medias ponderadas a las columnas del nuevo DataFrame
        pelea_ajustada = {
            'DATE': fecha,
            'Peleador_A': peleador_a,
            'Peleador_B': peleador_b,
            'WINNER': pelea['WINNER']
        }
        
        for cont in range(len(columnas_a)):
            pelea_ajustada[columnas_a[cont]] = media_a[atributos_generales[cont]]
            pelea_ajustada[columnas_b[cont]] = media_b[atributos_generales[cont]]
        
        peleas_ajustadas.append(pelea_ajustada)

    # Convertir resultados a un DataFrame
    df_ajustado = pd.DataFrame(peleas_ajustadas)

    df_ajustado['KD_DIFF'] = df_ajustado['KD_A'] - df_ajustado['KD_B'] #Creo columna de diferencia de knockdowns

    df_ajustado['SIG_STR_DIFF'] = df_ajustado['SIG_STR_A'] - df_ajustado['SIG_STR_B'] #Diferencia de golpes significativos


    df_ajustado['TD_DIFF'] = (df_ajustado['TD_A_x']/(df_ajustado['TD_A_y']+1)) - (df_ajustado['TD_B_x']/(df_ajustado['TD_B_y']+1)) #Diferencia de efectividad en derribos


    df_ajustado['SUB_ATT_DIFF'] = df_ajustado['SUB_ATT_A'] - df['SUB_ATT_B'] #Diferencia intentos de submisión

    df_ajustado['REV_DIFF'] = df_ajustado['REV_A'] - df_ajustado['REV_B'] #Diferencia en reversals

    df_ajustado['CTRL_DIFF'] = df_ajustado['CTRL_A'] - df_ajustado['CTRL_B'] #Diferencia de tiempo controlado
    print(df_ajustado)
    return df_ajustado



