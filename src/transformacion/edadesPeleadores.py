import pandas as pd


def edadesPeleadores(peleadores,peleas):

    #estos peleadores los he sacado a mano ya que había un problema y el web scraping no los extraía correctamente
    peleadores.loc[peleadores['Nombre'] == 'Stephan Bonnar', 'Nacimiento'] = '1977-04-04'
    peleadores.loc[peleadores['Nombre'] == 'Felipe Colares', 'Nacimiento'] = '1994-03-31'
    peleadores.loc[peleadores['Nombre'] == 'Rodrigo De Lima', 'Nacimiento'] = '1994-05-21'
    peleadores.loc[peleadores['Nombre'] == 'Shane Del Rosario', 'Nacimiento'] = '1983-09-23'
    peleadores.loc[peleadores['Nombre'] == 'Abdul-Kerim Edilov', 'Nacimiento'] = '1992-11-25'
    peleadores.loc[peleadores['Nombre'] == 'Justin Eilers', 'Nacimiento'] = '1978-06-28'
    peleadores.loc[peleadores['Nombre'] == 'Sean Gannon', 'Nacimiento'] = '1971-12-23'
    peleadores.loc[peleadores['Nombre'] == 'Brian Gassaway', 'Nacimiento'] = '1972-08-07'
    peleadores.loc[peleadores['Nombre'] == 'Tim Hague', 'Nacimiento'] = '1983-05-09'
    peleadores.loc[peleadores['Nombre'] == 'Geane Herrera', 'Nacimiento'] = '1990-04-27'
    peleadores.loc[peleadores['Nombre'] == 'Corey Hill', 'Nacimiento'] = '1978-10-03'
    peleadores.loc[peleadores['Nombre'] == 'Art Jimmerson', 'Nacimiento'] = '1963-08-04'
    peleadores.loc[peleadores['Nombre'] == 'Ryan Jimmo', 'Nacimiento'] = '1981-11-27'
    peleadores.loc[peleadores['Nombre'] == 'Anthony Johnson', 'Nacimiento'] = '1984-03-06'
    peleadores.loc[peleadores['Nombre'] == 'David Lee', 'Nacimiento'] = '1979-08-04'
    peleadores.loc[peleadores['Nombre'] == 'John Lewis', 'Nacimiento'] = '1969-03-08'
    peleadores.loc[peleadores['Nombre'] == 'Benji Radach', 'Nacimiento'] = '1979-04-05'
    peleadores.loc[peleadores['Nombre'] == 'Kevin Randleman', 'Nacimiento'] = '1971-08-10'
    peleadores.loc[peleadores['Nombre'] == 'Josh Samman', 'Nacimiento'] = '1988-03-14'
    peleadores.loc[peleadores['Nombre'] == 'Kimbo Slice', 'Nacimiento'] = '1974-02-08'
    peleadores.loc[peleadores['Nombre'] == 'Evan Tanner', 'Nacimiento'] = '1971-02-11'
    peleadores.loc[peleadores['Nombre'] == 'Elias Theodorou', 'Nacimiento'] = '1988-05-31'
    peleadores.loc[peleadores['Nombre'] == 'Teila Tuli', 'Nacimiento'] = '1969-06-14'
    peleadores.loc[peleadores['Nombre'] == 'Guilherme Vasconcelos', 'Nacimiento'] = '1986-03-23'
    peleadores.loc[peleadores['Nombre'] == 'Curt Warburton', 'Nacimiento'] = '1981-06-03'
    peleadores.loc[peleadores['Nombre'] == 'Jorge Gonzalez', 'Nacimiento'] = '1984-2-29'

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

    return peleas