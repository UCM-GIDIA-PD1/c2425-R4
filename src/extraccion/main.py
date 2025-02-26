import argparse
from extraccion.WebScrapCombates import extraer_peleas

def main():
    parser = argparse.ArgumentParser(description="Extracción de datos de combates")
    parser.add_argument("--pagina_inicio", help="Página por la que se inica la extracción de los combates")
    parser.add_argument("--pagina_final", help="Página hasta la que se extraen los combates")
    args = parser.parse_args()

    extraer_peleas(args.pagina_inicio, args.pagina_final)
    
    parser2 = argparse.ArgumentParser(description="Extracción de datos de peleadores")
    parser2.add_argument("--pagina_inicio", help="Página por la que se inica la extracción de los peleadores")
    parser2.add_argument("--pagina_final", help="Página hasta la que se extraen los peleadores")
    args2 = parser2.parse_args()
    
    

if __name__ == "__main__":
    main()
