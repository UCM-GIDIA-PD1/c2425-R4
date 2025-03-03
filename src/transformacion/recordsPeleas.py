import pandas as pd


def recordPeleas(peleadores,peleas):
    peleadores['name'] = peleadores['name'].str.title()
    peleas = peleas.iloc[:,2:]
    peleas = peleas.sort_values(by='DATE', ascending = False)
    peleadores['Record'] = peleadores['Record'].apply(lambda x: list(map(int, x.split(" ")[0].split("-"))))

    r = dict(zip(peleadores['name'].str.title(), peleadores['Record'].apply(lambda x: x.copy())))

    #Hay 31 peleadores que tienen mal puesto el record en la página de donde lo hemos sacado, por lo que hemos sacado a mano sus records
    #ya que era la única opción para tenerlos
    r['Tito Ortiz'] = [21, 12, 1]
    r['Rodrigo Ruas'] = [4, 5, 1]
    r['Eddie Mendez'] = [8, 3, 1]
    r['Amaury Bitetti'] = [5, 2, 0]
    r['Joey Gilbert'] = [2, 3, 1]
    r['Nate Loughran'] = [11, 2, 0]
    r['Maurice Smith'] = [14, 17, 0]
    r['Curtis Stout'] = [11, 12, 1]
    r['Yuki Kondo'] = [65, 40, 9]
    r['Daiju Takase'] = [12, 15, 2]
    r['Luiz Cane'] = [17, 7, 0]
    r['Ron Faircloth'] = [33, 20, 0]
    r['Bas Rutten'] = [28, 4, 1]
    r['Mark Hughes'] = [6, 2, 0]
    r['Phil Johns'] = [30, 14, 1]
    r['John Lewis'] = [3, 4, 3]
    r['Kenichi Yamamoto'] = [5, 17, 2]
    r['Joao Pierini'] = [4, 1, 0]
    r['Paul Rodriguez'] = [10, 9, 2]
    r['Frank Shamrock'] = [23, 10, 2]
    r['Ben Earwood'] = [13, 3, 0]
    r['Benji Radach'] = [16, 7, 0]
    r['Scott Smith'] = [18, 11, 0]
    r['Nick Serra'] = [7, 3, 0]
    r['Kit Cope'] = [6, 7, 0]
    r['Chris Sanford'] = [5, 1, 0]
    r['Lodune Sincaid'] = [15, 9, 0]
    r['Bobby Southworth'] = [10, 6, 0]
    r['Jason Thacker'] = [0, 1, 0]
    r['Yoji Anjo'] = [0, 5, 1]
    r['Danillo Villefort'] = [15, 6, 0]



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


    peleas = peleas.sort_values(by='DATE', ascending = True)
    return peleas