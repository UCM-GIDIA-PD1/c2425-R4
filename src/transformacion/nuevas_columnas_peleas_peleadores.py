import pandas as pd
from datetime import datetime
import numpy as np
import unicodedata

def transformacion(df_peleas_or,df_peleadores_2):

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
            "TKO - Doctor's Stoppage": 1.8
        }
        return factores.get(metodo, 1)

    # Función para calcular el factor de oponente en un rango de 1 a 5
    def calcular_factor_oponente(puntos_ganador, puntos_perdedor, ganador=True):
        try:
            if puntos_ganador <= -100:
                return 1  # Previene división por cero o negativos extremos

            ratio = (puntos_perdedor + 100) / (puntos_ganador + 100)
            if ratio < 0:
                ratio = 0.5  # Clamping extra por seguridad

            ratio = max(0.5, min(ratio, 2.0))
            factor_oponente = 1 + 9 * ((np.sqrt(ratio) - np.sqrt(0.5)) / (np.sqrt(2.0) - np.sqrt(0.5)))

            return max(1, min(5, factor_oponente))
        except Exception as e:
            print(f"Error en calcular_factor_oponente: {e}, con puntos_ganador={puntos_ganador}, puntos_perdedor={puntos_perdedor}")
            return 1

    # Cargar los datos
    df_peleas = df_peleas_or
    df_peleas["DATE"] = pd.to_datetime(df_peleas["DATE"], errors='coerce')


    df_info_peleadores = df_peleadores_2

    for col in ["Peleas", "Puntos", "Racha", "Victorias_KO", "Victorias_Sub", 
                "Victorias_Decision", "Derrotas_KO", "Derrotas_Sub", "Derrotas_Decision"]: #"height", "reach", "leg_reach" eliminadas
        df_peleas[f"{col}_A"] = None
        df_peleas[f"{col}_B"] = None
    # Crear columnas vacías para la información de cada peleador
    
    # Recorrer cada fila del DataFrame de peleas
    for index, row in df_peleas.iterrows():
        peleador_a = row['Peleador_A']
        peleador_b = row['Peleador_B']
        """
        # Buscar la información del Peleador_A en df_info_peleadores
        info_peleador_a = df_info_peleadores[df_info_peleadores['name'] == peleador_a.upper()]
        if not info_peleador_a.empty:
            df_peleas.at[index, 'height_A'] = info_peleador_a['height'].values[0]
            df_peleas.at[index, 'reach_A'] = info_peleador_a['reach'].values[0]
            df_peleas.at[index, 'leg_reach_A'] = info_peleador_a['leg_reach'].values[0]
        
        # Buscar la información del Peleador_B en 
        info_peleador_b = df_info_peleadores[df_info_peleadores['name'] == peleador_b.upper()]
        if not info_peleador_b.empty:
            df_peleas.at[index, 'height_B'] = info_peleador_b['height'].values[0]
            df_peleas.at[index, 'reach_B'] = info_peleador_b['reach'].values[0]
            df_peleas.at[index, 'leg_reach_B'] = info_peleador_b['leg_reach'].values[0]
            """

    
    df_peleas = df_peleas.sort_values(by=["DATE"])

    # Diccionario de historial
    peleadores_historial = {}
    historial_datos = []
    df_historico_peleas = []

    # Columnas a procesar
    stats_columns = ["KD", "SIG_STR", "TD_PORC", "SUB_ATT", "REV", "CTRL"]
    stats_columns_2= ["TD_x", "TD_y",
    "TOTAL_STR_x", "TOTAL_STR_y",
    "STR_HEAD_x", "STR_HEAD_y",
    "STR_BODY_x", "STR_BODY_y",
    "STR_LEG_x", "STR_LEG_y",
    "STR_DISTANCE_x", "STR_DISTANCE_y",
    "STR_CLINCH_x", "STR_CLINCH_y",
    "STR_GROUND_x", "STR_GROUND_y"]

    def actualizar_victorias_derrotas(historial_a, historial_b, ganador, metodo):
        """
        Actualiza las estadísticas de victorias y derrotas según el método de finalización de la pelea.

        :param historial_a: Diccionario con el historial del peleador A
        :param historial_b: Diccionario con el historial del peleador B
        :param ganador: 0 si gana peleador A, 1 si gana peleador B
        :param metodo: String con el método de finalización de la pelea
        """
        if ganador == 0:  # Gana Peleador A
            if "KO" in metodo or "TKO" in metodo:
                historial_a["Victorias_KO"] += 1
                historial_b["Derrotas_KO"] += 1
            elif "Submission" in metodo:
                historial_a["Victorias_Sub"] += 1
                historial_b["Derrotas_Sub"] += 1
            elif "Decision" in metodo:
                historial_a["Victorias_Decision"] += 1
                historial_b["Derrotas_Decision"] += 1
        elif ganador == 1:  # Gana Peleador B
            if "KO" in metodo or "TKO" in metodo:
                historial_b["Victorias_KO"] += 1
                historial_a["Derrotas_KO"] += 1
            elif "Submission" in metodo:
                historial_b["Victorias_Sub"] += 1
                historial_a["Derrotas_Sub"] += 1
            elif "Decision" in metodo:
                historial_b["Victorias_Decision"] += 1
                historial_a["Derrotas_Decision"] += 1
        
    def obtener_historial(peleador, fecha):
        """
        Devuelve el historial del peleador antes de la pelea.
        Si el peleador no tiene historial, devuelve valores iniciales en 0.
        """
        if peleador in peleadores_historial:
            return peleadores_historial[peleador]
        else:
            peleadores_historial[peleador]={
                "Peleador": peleador,
                "Fecha": fecha,
                **{stat+"_A": 0 for stat in stats_columns},
                **{stat+"_R": 0 for stat in stats_columns},
                **{stat+"_A": 0 for stat in stats_columns_2},
                **{stat+"_R": 0 for stat in stats_columns_2},
                "Peleas": 0,
                "Puntos": 0,
                "Racha": 0,
                "Victorias_KO": 0,
                "Victorias_Sub": 0,
                "Victorias_Decision": 0,
                "Derrotas_KO": 0,
                "Derrotas_Sub": 0,
                "Derrotas_Decision": 0
            }
            return peleadores_historial[peleador]

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
        historial_a["Fecha"] = fecha_pelea
        historial_b["Fecha"] = fecha_pelea
        actualizar_victorias_derrotas(historial_a, historial_b, ganador, row["METHOD"])

        historial_datos.append(historial_a.copy())
        historial_datos.append(historial_b.copy())

        for col in ["Peleas", "Puntos", "Racha", "Victorias_KO", "Victorias_Sub", 
                    "Victorias_Decision", "Derrotas_KO", "Derrotas_Sub", "Derrotas_Decision"]:
            
            df_peleas.loc[index, f"{col}_A"] = peleadores_historial[peleador_a][col]
            df_peleas.loc[index, f"{col}_B"] = peleadores_historial[peleador_b][col]
        
    

        pelea_data = {"Fecha": fecha_pelea, "Peleador_A": peleador_a, "Peleador_B": peleador_b}
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
            # Peleador A obtiene sus valores de las columnas A_x y A_y
            stats_a[stat+"_A"] = row.get(stat.replace("_x", "_A_x").replace("_y", "_A_y"), 0)
            stats_a[stat+"_R"] = row.get(stat.replace("_x", "_B_x").replace("_y", "_B_y"), 0)

            # Peleador B obtiene sus valores de las columnas B_x y B_y
            stats_b[stat+"_A"] = row.get(stat.replace("_x", "_B_x").replace("_y", "_B_y"), 0)
            stats_b[stat+"_R"] = row.get(stat.replace("_x", "_A_x").replace("_y", "_A_y"), 0)
                
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

    # Crear DataFrame con el historial completo de peleadores en cada pelea
    df_historial = pd.DataFrame(historial_datos)

    # Crear copia de df_peleas para no modificar el original
    df_peleas_actualizado = df_peleas.copy()

    # Columnas de estadísticas que queremos agregar
    estadisticas = ["Peleas", "Puntos", "Racha", "Victorias_KO", "Victorias_Sub", 
                    "Victorias_Decision", "Derrotas_KO", "Derrotas_Sub", "Derrotas_Decision"]

    # Iterar sobre cada pelea para obtener los valores correctos en el tiempo
    for index, row in df_peleas_actualizado.iterrows():
        peleador_a = row["Peleador_A"]
        peleador_b = row["Peleador_B"]
        fecha_pelea = row["DATE"]

        # Obtener el historial más reciente **antes** de la pelea
        historial_a = df_historial[
            (df_historial["Peleador"] == peleador_a) & (df_historial["Fecha"] == fecha_pelea)
        ].sort_values(by="Fecha", ascending=True)

        historial_b = df_historial[
            (df_historial["Peleador"] == peleador_b) & (df_historial["Fecha"] == fecha_pelea)
        ].sort_values(by="Fecha", ascending=True)

        # Si hay historial previo, tomar la última fila antes de la pelea
        if not historial_a.empty:
            ultimo_a = historial_a.iloc[-1]  # Último estado antes de la pelea
            for stat in estadisticas:
                df_peleas_actualizado.at[index, f"{stat}_A"] = ultimo_a[stat]

        if not historial_b.empty:
            ultimo_b = historial_b.iloc[-1]  # Último estado antes de la pelea
            for stat in estadisticas:
                df_peleas_actualizado.at[index, f"{stat}_B"] = ultimo_b[stat]

    # Guardar el DataFrame actualizado
    #df_peleas_actualizado.to_csv("df_peleas_actualizado.csv", index=False)

    # Filtrar y mostrar historial de Ilia Topuria antes de cada pelea
    df_topuria_peleas = df_peleas_actualizado[
        (df_peleas_actualizado["Peleador_A"] == "Ilia Topuria") | 
        (df_peleas_actualizado["Peleador_B"] == "Ilia Topuria")
    ]

    # Mostrar los puntos de Ilia Topuria antes de cada pelea
    #print(df_topuria_peleas[["DATE", "Peleador_A", "Peleador_B", "Puntos_A", "Puntos_B"]])


    df_peleadores = pd.DataFrame.from_dict(peleadores_historial, orient="index")

    # Ordenar por puntos y mostrar los 15 mejores
    df_top15 = df_peleadores.sort_values(by="Puntos", ascending=False).head(15)

    #print(df_top15)

    # Función para normalizar nombres eliminando acentos y caracteres especiales
    def normalizar_nombre(nombre):
        if pd.isna(nombre):
            return ""
        nombre = unicodedata.normalize("NFKD", nombre).encode("ascii", "ignore").decode("utf-8")
        return nombre.upper().strip()

    # Cargar el DataFrame de peleadores con estadísticas
    df_stats = df_peleadores
    df_stats.index = df_stats.index.map(normalizar_nombre)  # Normalizar nombres en el índice

    # Cargar el DataFrame con la información física de los peleadores
    df_info_peleadores = df_peleadores_2

    # Normalizar nombres en df_info_peleadores
    df_info_peleadores['name'] = df_info_peleadores['name'].apply(normalizar_nombre)

    # Asegurar que no haya nombres duplicados en df_info_peleadores
    df_info_peleadores = df_info_peleadores.groupby("name").agg({
        "height": "mean",  # Tomar promedio si hay valores repetidos
        "reach": "mean",
        "leg_reach": "mean"
    }).reset_index()

    # Crear diccionario para acceso rápido a los datos físicos
    peleadores_info = df_info_peleadores.set_index('name')[['height', 'reach', 'leg_reach']].to_dict(orient='index')

    # Agregar height, reach y leg_reach al DataFrame de estadísticas
    df_stats["height"] = df_stats.index.map(lambda x: peleadores_info.get(x, {}).get("height", np.nan))
    df_stats["reach"] = df_stats.index.map(lambda x: peleadores_info.get(x, {}).get("reach", np.nan))
    df_stats["leg_reach"] = df_stats.index.map(lambda x: peleadores_info.get(x, {}).get("leg_reach", np.nan))

    df_stats = df_stats.drop(columns=[col for col in df_stats.columns if col.endswith('_R')])

    # Guardar el DataFrame actualizado
    #df_stats.to_csv("peleadores_stats_actualizado.csv")

    #print(df_stats.loc["CHARLES OLIVEIRA"])

    df_stats = df_stats.drop(columns=["height","reach","leg_reach"])
    return df_peleas_actualizado,df_stats