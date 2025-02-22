import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Cargar datos
df_peleas = pd.read_csv("df_peleas.csv")
df_peleas["DATE"] = pd.to_datetime(df_peleas["DATE"], errors='coerce')

df_peleas = df_peleas.sort_values(by=["DATE"])

# Función para calcular la importancia del tiempo con caída gradual
def calcular_factor_tiempo(fecha_pelea):
    LAMBDA = 0.2  # Penalización más leve para peleas antiguas
    años_transcurridos = (datetime.today() - fecha_pelea).days / 365
    return np.exp(-LAMBDA * (años_transcurridos ** 1.1))

# Función para calcular el tiempo de pelea
def calcular_tiempo(pelea):
    tiempo = pelea["TIME"]
    round_p = (pelea["ROUND"] - 1) * 5 * 60
    return round_p + tiempo

# Función para obtener factor de método
def obtener_factor_metodo(metodo):
    factores = {
        'KO/TKO': 2.5,
        'Submission': 2.4,
        'Decision - Unanimous': 1.5,
        'Decision - Majority': 1,
        'Decision - Split': 0.85,
        "TKO - Doctor's Stoppage": 1.0
    }
    return factores.get(metodo, 1)

# Función para calcular el factor de oponente en un rango de 1 a 5
def calcular_factor_oponente(puntos_ganador, puntos_perdedor, ganador=True):
    if puntos_ganador == 0:
        return 1  # Evita división por cero
    
    ratio = (puntos_perdedor + 100) / (puntos_ganador + 100)
    ratio = max(0.5, min(ratio, 2.0))

    min_ratio = 0.5
    max_ratio = 2.0

    factor_oponente = 1 + 9 * ((np.sqrt(ratio) - np.sqrt(min_ratio)) / (np.sqrt(max_ratio) - np.sqrt(min_ratio)))

    return max(1, min(5, factor_oponente))

# Diccionario de historial
peleadores_historial = {}
historial_datos = []
df_historico_peleas = []

# Columnas a procesar
stats_columns = ["KD", "SIG_STR", "TD_PORC", "SUB_ATT", "REV", "CTRL"]
stats_columns_2= ["TD_T", "TD_M",
"TOTAL_STR_T", "TOTAL_STR_M",
"STR_HEAD_T", "STR_HEAD_M",
"STR_BODY_T", "STR_BODY_M",
"STR_LEG_T", "STR_LEG_M",
"STR_DISTANCE_T", "STR_DISTANCE_M",
"STR_CLINCH_T", "STR_CLINCH_M",
"STR_GROUND_T", "STR_GROUND_M"]


def obtener_historial(peleador, fecha):
    """
    Devuelve el historial del peleador antes de la pelea.
    Si el peleador no tiene historial, devuelve valores iniciales en 0.
    """
    if peleador in peleadores_historial:
        return {"Peleador": peleador, "Fecha": fecha, **peleadores_historial[peleador].copy()}
    else:
        return {
            "Peleador": peleador,
            "Fecha": fecha,
            **{stat+"_A": 0 for stat in stats_columns},
            **{stat+"_R": 0 for stat in stats_columns},
            **{stat+"_A": 0 for stat in stats_columns_2},
            **{stat+"_R": 0 for stat in stats_columns_2},
            "Peleas": 0,
            "Puntos": 0,
            "Racha": 0
        }

def actualizar_estadisticas(peleador, stats_nuevas):
    """
    Actualiza las estadísticas de un peleador manteniendo la media acumulativa.
    """
    if peleador not in peleadores_historial:
        peleadores_historial[peleador] = stats_nuevas.copy()
        peleadores_historial[peleador]["Peleas"] = 1
        peleadores_historial[peleador]["Puntos"] = 0
        peleadores_historial[peleador]["Racha"] = 0
    else:
        peleas_previas = peleadores_historial[peleador]["Peleas"]
        for stat in stats_nuevas:
            peleadores_historial[peleador][stat] = (
                (peleadores_historial[peleador][stat] * peleas_previas) + stats_nuevas[stat]
            ) / (peleas_previas + 1)
        peleadores_historial[peleador]["Peleas"] += 1

# Iterar sobre cada pelea
for _, row in df_peleas.iterrows():
    peleador_a, peleador_b = row["Peleador_A"], row["Peleador_B"]
    fecha_pelea = row["DATE"]
    ganador = row["WINNER"]

    historial_a = obtener_historial(peleador_a, fecha_pelea)
    historial_b = obtener_historial(peleador_b, fecha_pelea)
    historial_datos.append(historial_a)
    historial_datos.append(historial_b)

    pelea_data = {"Fecha": fecha_pelea, "Peleador_A": peleador_a, "Peleador_B": peleador_b, "WINNER": ganador}
    for stat in stats_columns + stats_columns_2:
        pelea_data[stat+"_A"] = historial_a.get(stat+"_A", 0)
        pelea_data[stat+"_R_A"] = historial_a.get(stat+"_R", 0)
        pelea_data[stat+"_B"] = historial_b.get(stat+"_A", 0)
        pelea_data[stat+"_R_B"] = historial_b.get(stat+"_R", 0)
    pelea_data["Puntos_A"] = historial_a["Puntos"]
    pelea_data["Puntos_B"] = historial_b["Puntos"]
    pelea_data["Racha_A"] = historial_a["Racha"]
    pelea_data["Racha_B"] = historial_b["Racha"]
    df_historico_peleas.append(pelea_data)
    
    stats_a = {stat+"_A": row[stat+"_A"] for stat in stats_columns}
    stats_a.update({stat+"_R": row[stat+"_B"] for stat in stats_columns})
    
    stats_b = {stat+"_A": row[stat+"_B"] for stat in stats_columns}
    stats_b.update({stat+"_R": row[stat+"_A"] for stat in stats_columns})

    for stat in stats_columns_2:
        base_stat = stat[:-2]  # Elimina _T o _M
        stats_a[stat+"_A"] = row.get(base_stat+"_A_x", 0)
        stats_a[stat+"_R"] = row.get(base_stat+"_B_x", 0)
        stats_b[stat+"_A"] = row.get(base_stat+"_B_x", 0)
        stats_b[stat+"_R"] = row.get(base_stat+"_A_x", 0)
        
        stats_a[stat+"_A"] = row.get(base_stat+"_A_x", 0) / max(row.get(base_stat+"_A_y", 1), 1)
        stats_a[stat+"_R"] = row.get(base_stat+"_B_x", 0) / max(row.get(base_stat+"_B_y", 1), 1)
        stats_b[stat+"_A"] = row.get(base_stat+"_B_x", 0) / max(row.get(base_stat+"_B_y", 1), 1)
        stats_b[stat+"_R"] = row.get(base_stat+"_A_x", 0) / max(row.get(base_stat+"_A_y", 1), 1)
            
    actualizar_estadisticas(peleador_a, stats_a)
    actualizar_estadisticas(peleador_b, stats_b)
    
    factorTiempo = calcular_factor_tiempo(fecha_pelea)
    factorM = obtener_factor_metodo(row["METHOD"])
    factor_oAW = calcular_factor_oponente(peleadores_historial[peleador_a]["Puntos"], peleadores_historial[peleador_b]["Puntos"], ganador=True)
    factor_oAL = calcular_factor_oponente(peleadores_historial[peleador_a]["Puntos"], peleadores_historial[peleador_b]["Puntos"], ganador=False)
    factor_oBW = calcular_factor_oponente(peleadores_historial[peleador_b]["Puntos"], peleadores_historial[peleador_a]["Puntos"], ganador=True)
    factor_oBL = calcular_factor_oponente(peleadores_historial[peleador_b]["Puntos"], peleadores_historial[peleador_a]["Puntos"], ganador=False)
    
    factorTitleWin = 3 if row["TITLE_FIGHT"] else 1
    factorTitleLoss = 0.3 if row["TITLE_FIGHT"] else 1
    
    racha_A = 1 + 0.15 * peleadores_historial[peleador_a]["Racha"]
    racha_B = 1 + 0.15 * peleadores_historial[peleador_b]["Racha"]

    
    if ganador == 0:
        peleadores_historial[peleador_a]["Racha"] += 1
        peleadores_historial[peleador_b]["Racha"] = 0
        peleadores_historial[peleador_a]["Puntos"] += (10 * factorTitleWin * factorM * factor_oAW * factorTiempo * racha_A)
        peleadores_historial[peleador_b]["Puntos"] -= (10 * factorTitleLoss * factorM * factor_oBL * factorTiempo)
    elif ganador == 1:
        peleadores_historial[peleador_b]["Racha"] += 1
        peleadores_historial[peleador_a]["Racha"] = 0
        peleadores_historial[peleador_b]["Puntos"] += (10 * factorTitleWin * factorM * factor_oBW * factorTiempo * racha_B)
        peleadores_historial[peleador_a]["Puntos"] -= (10 * factorTitleLoss * factorM * factor_oAL * factorTiempo)
    
    peleadores_historial[peleador_a]["Puntos"] = max(0, peleadores_historial[peleador_a]["Puntos"])
    peleadores_historial[peleador_b]["Puntos"] = max(0, peleadores_historial[peleador_b]["Puntos"])
   
# Convertir el diccionario a un DataFrame

df_historico_peleas = pd.DataFrame(df_historico_peleas)
df_historico_peleas.to_csv("historial_peleas.csv", index=False)
df_historico = pd.DataFrame(historial_datos)
print(df_historico[df_historico["Peleador"]=="Ilia Topuria"])


