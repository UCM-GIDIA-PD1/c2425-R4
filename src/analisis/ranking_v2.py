import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Cargar datos
data = pd.read_csv("df_limpio-4.csv")  
df = pd.DataFrame(data)

# Convertir la columna DATE a formato datetime y ordenar de más antigua a más reciente
df["DATE"] = pd.to_datetime(df["DATE"], errors='coerce')  
df = df.sort_values(by="DATE", ascending=True)

LAMBDA = 0.2  # Penalización más leve para peleas antiguas

# Función para calcular la importancia del tiempo con caída gradual
def calcular_factor_tiempo(fecha_pelea):
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

# Diccionario para rastrear la información de cada peleador
peleadores_historial = {}

# DataFrame para almacenar la información histórica de cada pelea
df_historico = []

# Proceso de cálculo de puntos y almacenamiento de información histórica
for i, pelea in df.iterrows():
    ganador = pelea["WINNER"]
    peleador_a = pelea["Peleador_A"]
    peleador_b = pelea["Peleador_B"]
    fecha_pelea = pelea["DATE"]
    
    # Inicializar peleadores si no existen
    for peleador in [peleador_a, peleador_b]:
        if peleador not in peleadores_historial:
            peleadores_historial[peleador] = {"Puntos": 0, "Peleas": 0, "Racha": 0, "Ultima_Pelea": None}

    # Extraer valores actuales antes de la pelea
    puntos_a = peleadores_historial[peleador_a]["Puntos"]
    puntos_b = peleadores_historial[peleador_b]["Puntos"]
    racha_a = peleadores_historial[peleador_a]["Racha"]
    racha_b = peleadores_historial[peleador_b]["Racha"]

    # Guardar información previa en el histórico
    df_historico.append([
        fecha_pelea, peleador_a, puntos_a, racha_a, peleadores_historial[peleador_a]["Peleas"], pelea["CATEGORY"], peleador_b, "Ganó" if ganador == 0 else "Perdió"
    ])
    df_historico.append([
        fecha_pelea, peleador_b, puntos_b, racha_b, peleadores_historial[peleador_b]["Peleas"], pelea["CATEGORY"], peleador_a, "Ganó" if ganador == 1 else "Perdió"
    ])

    # Calcular modificadores
    factorTiempo = calcular_factor_tiempo(fecha_pelea)
    factorM = obtener_factor_metodo(pelea["METHOD"])
    factor_oAW = calcular_factor_oponente(puntos_a, puntos_b, ganador=True)
    factor_oAL = calcular_factor_oponente(puntos_a, puntos_b, ganador=False)
    factor_oBW = calcular_factor_oponente(puntos_b, puntos_a, ganador=True)
    factor_oBL = calcular_factor_oponente(puntos_b, puntos_a, ganador=False)

    factorTitleWin = 3 if pelea["TITLE_FIGHT"] else 1
    factorTitleLoss = 0.3 if pelea["TITLE_FIGHT"] else 1

    # Modificación por racha
    racha_A = 1 + 0.15 * peleadores_historial[peleador_a]["Racha"]
    racha_B = 1 + 0.15 * peleadores_historial[peleador_b]["Racha"]

    tiempo_total = calcular_tiempo(pelea)
    t_pelea = 1500 if pelea["TITLE_FIGHT"] else 900

    factorTime = max(1, min(2, 2 - 0.5 * (tiempo_total / t_pelea)))
    penalizacionA = (10 * factorTitleLoss * factorTime * factorM * factor_oAL * 3 / max(1, racha_B))
    penalizacionB = (10 * factorTitleLoss * factorTime * factorM * factor_oBL * 3 / max(1, racha_A))

    # Aplicar cambios en puntos
    if ganador == 0:  # Gana A
        peleadores_historial[peleador_a]["Racha"] += 1
        peleadores_historial[peleador_b]["Racha"] = 0
        peleadores_historial[peleador_a]["Puntos"] += (10 * factorTitleWin * factorTime * factorM * factor_oAW * factorTiempo * racha_A)
        peleadores_historial[peleador_b]["Puntos"] -= penalizacionB * factorTiempo
    elif ganador == 1:  # Gana B
        peleadores_historial[peleador_b]["Racha"] += 1
        peleadores_historial[peleador_a]["Racha"] = 0
        peleadores_historial[peleador_a]["Puntos"] -= penalizacionA * factorTiempo
        peleadores_historial[peleador_b]["Puntos"] += (10 * factorTitleWin * factorTime * factorM * factor_oBW  * factorTiempo * racha_B)

    peleadores_historial[peleador_a]["Puntos"] = max(0, peleadores_historial[peleador_a]["Puntos"])
    peleadores_historial[peleador_b]["Puntos"] = max(0, peleadores_historial[peleador_b]["Puntos"])

    # Actualizar número de peleas
    peleadores_historial[peleador_a]["Peleas"] += 1
    peleadores_historial[peleador_b]["Peleas"] += 1
    peleadores_historial[peleador_a]["Ultima_Pelea"] = fecha_pelea
    peleadores_historial[peleador_b]["Ultima_Pelea"] = fecha_pelea

# Convertir el historial a DataFrame
df_historico = pd.DataFrame(df_historico, columns=["Fecha", "Peleador", "Puntos", "Racha", "Peleas", "Categoria", "Oponente", "Resultado"])

# Filtrar peleadores inactivos
#df_historico["Fecha"] = pd.to_datetime(df_historico["Fecha"])
#fecha_limite = datetime.today() - timedelta(days=3*365)
#df_historico = df_historico[df_historico["Fecha"] >= fecha_limite]
# Convertir el diccionario a un DataFrame


df_peleadores = pd.DataFrame.from_dict(peleadores_historial, orient="index")

# Agregar la columna de nombres de peleadores
df_peleadores["Peleador"] = df_peleadores.index

# Ordenar por puntos y mostrar los 15 mejores
df_top15 = df_peleadores.sort_values(by="Puntos", ascending=False).head(15)

print(df_top15)
# Mostrar el resultado

print(df_historico[df_historico["Peleador"]=="Ilia Topuria"])
print(peleadores_historial["Ilia Topuria"])
