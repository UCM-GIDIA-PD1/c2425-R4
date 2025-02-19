import pandas as pd

#Leo datos

df=pd.read_csv('C:\\Users\\Mario\\Documents\\pd1\\fighters_inicial.csv')

#CAMBIO NOMBRES

df.columns = df.columns.str.lower().str.replace(r'\s+', '_', regex=True)
df.columns = df.columns.str.rstrip("._")

df.rename(columns={"nombre": "name"}, inplace=True)
df.rename(columns={"striking_accuracy_(%)": "striking_accuracy(%)"}, inplace=True)
df.rename(columns={"golpes_significativos_conectados": "sig_str_landed"}, inplace=True)
df.rename(columns={"golpes_significativos_intentados": "sig_str_attempted"}, inplace=True)
df.rename(columns={"golpes_significativos_conectados_por_minuto": "sig_str_landed_per_min"}, inplace=True)
df.rename(columns={"golpes_significativos_recibidos_por_minuto": "sig_str_absorbed_per_min"}, inplace=True)
df.rename(columns={"promedio_de_knockdown_por_15m": "knockdown_per_15min(avg)"}, inplace=True)
df.rename(columns={"promedio_de_sumisiÃ³n_por_15m": "submission_per_15min(avg)"}, inplace=True)
df.rename(columns={"defensa_de_golpes_sig": "sig_str_defense(%)"}, inplace=True)
df.rename(columns={"defensa_de_derribo": "takedown_defense(%)"}, inplace=True)
df.rename(columns={"promedio_de_tiempo_de_pelea": "time_fight(avg)"}, inplace=True)
df.rename(columns={"golpes_de_pie": "sig_str_standing"}, inplace=True)
df.rename(columns={"porcentaje_de_pie": "sig_str_standing(%)"}, inplace=True)
df.rename(columns={"golpes_clinch": "sig_str_clinch"}, inplace=True)
df.rename(columns={"porcentaje_clinch": "sig_str_clinch(%)"}, inplace=True)
df.rename(columns={"golpes_suelo": "sig_str_ground"}, inplace=True)
df.rename(columns={"porcentajes_suelo": "sig_str_ground(%)"}, inplace=True)
df.rename(columns={"golpes_cabeza": "sig_str_to_head"}, inplace=True)
df.rename(columns={"porcentaje_cabeza": "sig_str_to_head(%)"}, inplace=True)
df.rename(columns={"golpes_cuerpo": "sig_str_to_body"}, inplace=True)
df.rename(columns={"porcentaje_cuerpo": "sig_str_to_body(%)"}, inplace=True)
df.rename(columns={"golpes_pierna": "sig_str_to_legs"}, inplace=True)
df.rename(columns={"porcentaje_pierna": "sig_str_to_legs(%)"}, inplace=True)
df.rename(columns={"ko/tko": "wins_by_ko/tko"}, inplace=True)
df.rename(columns={"porcentaje_ko/tko": "wins_by_ko/tko(%)"}, inplace=True)
df.rename(columns={"dec": "wins_by_decision"}, inplace=True)
df.rename(columns={"porcentaje_dec": "wins_by_decision(%)"}, inplace=True)
df.rename(columns={"sub": "wins_by_submission"}, inplace=True)
df.rename(columns={"porcentaje_sub": "wins_by_submission(%)"}, inplace=True)
df.rename(columns={"efectividad_de_derribo": "takedown_accuracy(%)"}, inplace=True)
df.rename(columns={"derribos_conseguidos": "takedowns_landed"}, inplace=True)
df.rename(columns={"derribos_intentados": "takedowns_attempted"}, inplace=True)

#ELIMINO '%'

columnas=[]
for col in df.columns:
    if '%' in col:
        columnas.append(col)
for col in columnas:
    df[col]=df[col].str.replace('%','').astype(float)/100

#PASO MINUTOS A SEGUNDOS

def convertir_a_segundos(tiempo):
    if isinstance(tiempo, str) and ":" in tiempo:
        minutos, segundos = map(int, tiempo.split(":"))
        return minutos * 60 + segundos
    else :
        return tiempo

df['time_fight(avg)']=df['time_fight(avg)'].apply(convertir_a_segundos)

#Tratamiento nan

filas_vacias=df[df.drop(columns='name').isna().all(axis=1)].index
df=df.drop(index=filas_vacias)
df['takedowns_landed']=df['takedowns_landed'].fillna(df['takedowns_attempted']*df['efectividad_de_derribo_(%)'])

#Guardo df
df.to_csv("C:\\Users\\Mario\\Documents\\pd1\\fighters_final.csv", index=False)