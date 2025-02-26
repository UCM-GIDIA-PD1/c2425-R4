import argparse
from WebScrapCombates import extraer_peleas
from scraper_peleadores import extraer_peleadores
from scraper_fecha_nacimiento import extrar_fechas_nacimiento

def main():
    parser = argparse.ArgumentParser(description="Extracción de datos de combates")
    parser.add_argument("--pagina_inicio", default=1, help="Página por la que se inica la extracción de los combates")
    parser.add_argument("--pagina_final", default= 29, help="Página hasta la que se extraen los combates")
    args = parser.parse_args()

    extraer_peleas(args.pagina_inicio, args.pagina_final)
    
    parser2 = argparse.ArgumentParser(description="Extracción de datos de peleadores")
    parser2.add_argument("--pagina_inicio", default=1, help="Página por la que se inica la extracción de los peleadores")
    parser2.add_argument("--pagina_final", default=None, help="Página hasta la que se extraen los peleadores, no poner nada para llegar al final")
    args2 = parser2.parse_args()
    
    extraer_peleadores(args2.pagina_inicio, args2.pagina_final)
    
    parser3 = argparse.ArgumentParser(description="Extracción de la fecha de nacimiento de los peleadores. Rango 0 - N (N = nº filas peleadores.csv). Solo se pueden hacer seguidas 100 filas. Y aproximadamente 500 filas por día")
    parser3.add_argument("--fila_inicio", default=0, help="Fila desde la que se extrae la fecha de nacimiento")
    parser3.add_argument("--fila_final", default=200 , help="Fila desde la que se extrae la fecha de nacimiento")
    args3 = parser3.parse_args()

    extrar_fechas_nacimiento(args3.fila_inicio, args3.fila_final)

if __name__ == "__main__":
    main()
