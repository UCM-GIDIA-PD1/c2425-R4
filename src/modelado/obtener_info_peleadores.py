import os
import pandas as pd

def obtener_info_peleadores(lista_peleadores_A, lista_peleadores_B):
    """
    Dadas dos listas de nombres de peleadores, devuelve la información en formato de pelea.
    """
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    ruta_processed = os.path.join(base_dir, "data", "processed")
    df = pd.read_parquet(os.path.join(ruta_processed, "peleadores.parquet"))
    if len(lista_peleadores_A) != len(lista_peleadores_B):
        print("Las listas de peleadores A y B deben tener la misma longitud.")
        return pd.DataFrame()

    data_peleas = []
    for Peleador_A, Peleador_B in zip(lista_peleadores_A, lista_peleadores_B):
        peleador_A = df[df["Peleador"] == Peleador_A]
        peleador_B = df[df["Peleador"] == Peleador_B]

        if peleador_A.empty or peleador_B.empty:
            print(f"No se encontró información de {Peleador_A} o {Peleador_B}")
            continue

        data_pelea = {
        "Peleador_A": Peleador_A,
        "Peleador_B": Peleador_B,
        "KD_A": peleador_A["KD_A"].values[0],
        "KD_B": peleador_B["KD_A"].values[0],
        "SIG_STR_A": peleador_A["SIG_STR_A"].values[0],
        "SIG_STR_B": peleador_B["SIG_STR_A"].values[0], 
        "TD_PORC_A": peleador_A["TD_PORC_A"].values[0], 
        "TD_PORC_B": peleador_B["TD_PORC_A"].values[0],
        "SUB_ATT_A": peleador_A["SUB_ATT_A"].values[0],
        "SUB_ATT_B": peleador_B["SUB_ATT_A"].values[0],
        "REV_A": peleador_A["REV_A"].values[0],
        "REV_B": peleador_B["REV_A"].values[0],
        "CTRL_A": peleador_A["CTRL_A"].values[0],
        "CTRL_B": peleador_B["CTRL_A"].values[0],
        "TOTAL_STR_A_x": peleador_A["TOTAL_STR_x_A"].values[0],
        "TOTAL_STR_A_y": peleador_A["TOTAL_STR_y_A"].values[0],
        "TOTAL_STR_B_x": peleador_B["TOTAL_STR_x_A"].values[0],
        "TOTAL_STR_B_y": peleador_B["TOTAL_STR_y_A"].values[0],
        "TD_A_x": peleador_A["TD_x_A"].values[0],
        "TD_A_y": peleador_A["TD_y_A"].values[0],
        "TD_B_x": peleador_B["TD_x_A"].values[0],
        "TD_B_y": peleador_B["TD_y_A"].values[0],
        "STR_HEAD_A_x": peleador_A["STR_HEAD_x_A"].values[0],
        "STR_HEAD_A_y": peleador_A["STR_HEAD_y_A"].values[0],
        "STR_HEAD_B_x": peleador_B["STR_HEAD_x_A"].values[0],
        "STR_HEAD_B_y": peleador_B["STR_HEAD_y_A"].values[0],
        "STR_BODY_A_x": peleador_A["STR_BODY_x_A"].values[0],
        "STR_BODY_A_y": peleador_A["STR_BODY_y_A"].values[0],
        "STR_BODY_B_x": peleador_B["STR_BODY_x_A"].values[0],
        "STR_BODY_B_y": peleador_B["STR_BODY_y_A"].values[0],
        "STR_LEG_A_x": peleador_A["STR_LEG_x_A"].values[0],
        "STR_LEG_A_y": peleador_A["STR_LEG_y_A"].values[0],
        "STR_LEG_B_x": peleador_B["STR_LEG_x_A"].values[0],
        "STR_LEG_B_y": peleador_B["STR_LEG_y_A"].values[0],
        "STR_DISTANCE_A_x": peleador_A["STR_DISTANCE_x_A"].values[0],
        "STR_DISTANCE_A_y": peleador_A["STR_DISTANCE_y_A"].values[0],
        "STR_DISTANCE_B_x": peleador_B["STR_DISTANCE_x_A"].values[0],
        "STR_DISTANCE_B_y": peleador_B["STR_DISTANCE_y_A"].values[0],
        "STR_CLINCH_A_x": peleador_A["STR_CLINCH_x_A"].values[0],
        "STR_CLINCH_A_y": peleador_A["STR_CLINCH_y_A"].values[0],
        "STR_CLINCH_B_x": peleador_B["STR_CLINCH_x_A"].values[0],
        "STR_CLINCH_B_y": peleador_B["STR_CLINCH_y_A"].values[0],
        "STR_GROUND_A_x": peleador_A["STR_GROUND_x_A"].values[0],
        "STR_GROUND_A_y": peleador_A["STR_GROUND_y_A"].values[0],
        "STR_GROUND_B_x": peleador_B["STR_GROUND_x_A"].values[0],
        "STR_GROUND_B_y": peleador_B["STR_GROUND_y_A"].values[0],
        "KD_DIFF":  peleador_A["KD_A"].values[0] - peleador_B["KD_A"].values[0],
        "SIG_STR_DIFF": peleador_A["SIG_STR_A"].values[0] - peleador_B["SIG_STR_A"].values[0],
        "TD_DIFF": peleador_A["TD_x_A"].values[0]/(peleador_A["TD_y_A"].values[0]+1) - peleador_B["TD_x_A"].values[0]/(peleador_B["TD_y_A"].values[0]+1),
        "SUB_ATT_DIFF": peleador_A["SUB_ATT_A"].values[0] - peleador_B["SUB_ATT_A"].values[0],
        "REV_DIFF": peleador_A["REV_A"].values[0] - peleador_B["REV_A"].values[0],
        "CTRL_DIFF": peleador_A["CTRL_A"].values[0] - peleador_B["CTRL_A"].values[0],
        "Peleas_A": peleador_A["Peleas"].values[0],
        "Peleas_B": peleador_B["Peleas"].values[0],
        "Puntos_A": peleador_A["Puntos"].values[0],
        "Puntos_B": peleador_B["Puntos"].values[0],
        "Racha_A": peleador_A["Racha"].values[0],
        "Racha_B": peleador_B["Racha"].values[0],
        "Victorias_KO_A": peleador_A["Victorias_KO"].values[0],
        "Victorias_KO_B": peleador_B["Victorias_KO"].values[0],
        "Victorias_Sub_A": peleador_A["Victorias_Sub"].values[0],
        "Victorias_Sub_B": peleador_B["Victorias_Sub"].values[0],
        "Victorias_Decision_A": peleador_A["Victorias_Decision"].values[0],
        "Victorias_Decision_B": peleador_B["Victorias_Decision"].values[0],
        "Derrotas_KO_A": peleador_A["Derrotas_KO"].values[0],
        "Derrotas_KO_B": peleador_B["Derrotas_KO"].values[0],
        "Derrotas_Sub_A": peleador_A["Derrotas_Sub"].values[0],
        "Derrotas_Sub_B": peleador_B["Derrotas_Sub"].values[0],
        "Derrotas_Decision_A": peleador_A["Derrotas_Decision"].values[0],
        "Derrotas_Decision_B": peleador_B["Derrotas_Decision"].values[0],
    }
        data_peleas.append(data_pelea)

    df_peleas = pd.DataFrame(data_peleas)
    return df_peleas
