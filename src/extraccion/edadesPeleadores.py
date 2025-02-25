import pandas as pd

peleadores = pd.read_csv("C:\\Users\\Equipo\\Documents\\UCM\\PD1\\limpieza\\limpieza1\\completo.csv")
peleas = pd.read_csv("C:\\Users\\Equipo\\Documents\\UCM\\PD1\\limpieza\\limpieza1\\peleasCompleto.csv")

dic = dict(zip(peleadores['Nombre'].str.title(), peleadores['Nacimiento']))
fechas1 = []
fechas2 = []
incorrectos = [] #hay peleadores cuya fecha de nacimiento es 2025
for i, row in peleas.iterrows():
    peleador1, peleador2, fechaPelea = row['Peleador_A'], row['Peleador_B'], row['DATE']
    # print(peleador1,peleador2)
    fechaPelea = pd.to_datetime(fechaPelea)
    # print(fecha)
    f1 = dic.get(peleador1.title())
    f2 = dic.get(peleador2.title())
    # print(f1,f2)
    if f1 and f1 != 'No encontrado':
        f1 = pd.to_datetime(f1)
        edad1 = (fechaPelea - f1).days / 365.25
        #if ((edad1 <= 0) & (peleador1.title() not in incorrectos)):
            #print("No se ha extraido bien la fecha de", peleador1.title(), edad1)
            #incorrectos.append(peleador1.title())
        fechas1.append(int(edad1))
        # print(peleador1, f1, fechaPelea, edad1)
    else:
        fechas1.append('')
    if f2 and f2 not in ['No encontrado', 'Fecha de nacimiento no encontrada',
                         'Error: No se pudo acceder a la página (Código 503)']:
        f2 = pd.to_datetime(f2)
        edad2 = (fechaPelea - f2).days / 365.25
        #if ((edad2 < 0) & (peleador2.title() not in incorrectos)):
            #print("No se ha extraido bien la fecha de", peleador2.title(), edad2)
            #incorrectos.append(peleador2.title())
        fechas2.append(int(edad2))
        # print(peleador2, f2, fechaPelea, edad2)
    else:
        fechas2.append('')

peleas['Edad_A'] = fechas1
peleas['Edad_B'] = fechas2

peleas.to_csv('peleasConLaEdad.csv', index=False)

print(peleas)