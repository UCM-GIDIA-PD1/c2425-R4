import pandas as pd

peleas = pd.read_csv("C:\\Users\\Equipo\\Documents\\UCM\\PD1\\limpieza\\limpieza1\\peleasCompleto.csv")
peleadores = pd.read_csv("C:\\Users\\Equipo\\Documents\\UCM\\PD1\\limpieza\\limpieza1\\completo.csv")

peleadores['Nombre'] = peleadores['Nombre'].str.title()
peleas = peleas.iloc[:,2:]
peleas = peleas.sort_values(by='DATE', ascending = False)
peleadores['Record'] = peleadores['Record'].apply(lambda x: list(map(int, x.split(" ")[0].split("-"))))

r = dict(zip(peleadores['Nombre'].str.title(), peleadores['Record'].apply(lambda x: x.copy())))

for idx, row in peleas.iterrows():
    peleador1, peleador2 = row['Peleador_A'], row['Peleador_B']

    # Obtiene los récords o asigna valores por defecto si no se encuentra el peleador
    rec1 = r[peleador1] if peleador1 in r else [-1000, -1000, -1000]
    rec2 = r[peleador2] if peleador2 in r else [-1000, -1000, -1000]

    ganador = row['WINNER']

    # Actualiza los récords según el ganador
    if ganador == 0:
        rec1[0] -= 1
        rec2[1] -= 1
    elif ganador == 1:
        rec2[0] -= 1
        rec1[1] -= 1
    else:
        rec1[2] -= 1
        rec2[2] -= 1


    # Función para formatear el récord o devolver vacío si todos son < 0
    def formatear_record(rec):
        return "" if all(x < 0 for x in rec) else f"{rec[0]}-{rec[1]}-{rec[2]}"


    # Asigna los valores formateados a las columnas correspondientes
    peleas.loc[idx, 'Record_A'] = formatear_record(rec1)
    peleas.loc[idx, 'Record_B'] = formatear_record(rec2)

r = dict(zip(peleadores['Nombre'].str.title(), peleadores['Record'].apply(lambda x: x.copy())))

peleas.to_csv('peleasConElRecord.csv', index=False)

##########EJEMPLO##########
filtro = (peleas['Peleador_A'] == 'Israel Adesanya') | (peleas['Peleador_B'] == 'Israel Adesanya')
print(r['Israel Adesanya'])
print(peleas[filtro])
