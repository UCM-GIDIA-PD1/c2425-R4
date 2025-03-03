import pandas as pd

# Supongamos que tienes dos DataFrames:
# df_enfrentamientos: Contiene las peleas entre dos peleadores
# df_info_peleadores: Contiene la información de cada peleador (Height, Reach, Leg Reach)

# Ejemplo de DataFrames

def nuevas_col(df_pelea,df_peleadores):
    df_peleas = df_pelea

    df_info_peleadores = df_peleadores

    # Crear columnas vacías para la información de cada peleador
    for col in ['height', 'reach', 'leg_reach']:
        df_peleas[f'Peleador_A_{col}'] = None
        df_peleas[f'Peleador_B_{col}'] = None

    # Recorrer cada fila del DataFrame de peleas
    for index, row in df_peleas.iterrows():
        peleador_a = row['Peleador_A']
        peleador_b = row['Peleador_B']
        
        # Buscar la información del Peleador_A en df_info_peleadores
        info_peleador_a = df_info_peleadores[df_info_peleadores['name'] == peleador_a.upper()]
        if not info_peleador_a.empty:
            df_peleas.at[index, 'Peleador_A_height'] = info_peleador_a['height'].values[0]
            df_peleas.at[index, 'Peleador_A_reach'] = info_peleador_a['reach'].values[0]
            df_peleas.at[index, 'Peleador_A_leg_reach'] = info_peleador_a['leg_reach'].values[0]
        
        # Buscar la información del Peleador_B en df_info_peleadores
        info_peleador_b = df_info_peleadores[df_info_peleadores['name'] == peleador_b.upper()]
        if not info_peleador_b.empty:
            df_peleas.at[index, 'Peleador_B_height'] = info_peleador_b['height'].values[0]
            df_peleas.at[index, 'Peleador_B_reach'] = info_peleador_b['reach'].values[0]
            df_peleas.at[index, 'Peleador_B_leg_reach'] = info_peleador_b['leg_reach'].values[0]

     
    return df_peleas
