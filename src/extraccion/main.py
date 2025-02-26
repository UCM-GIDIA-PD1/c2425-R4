import argparse
from extraccion.WebScrapCombates import extraer_peleas

def main():
    parser = argparse.ArgumentParser(description="Extracción de datos desde la web")
    parser.add_argument("--pagina_inicio", help="Página por la que se inica la extracción de los combates")
    parser.add_argument("--pagina_final", help="Página hasta la que se extraen los combates")
    args = parser.parse_args()

    extraer_peleas(args.pagina_inicio, args.pagina_final)

if __name__ == "__main__":
    main()
