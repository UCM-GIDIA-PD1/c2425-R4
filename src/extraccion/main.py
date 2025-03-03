import argparse
from scraper_peleas import extraer_peleas
from scraper_peleadores import extraer_peleadores
from scraper_fecha_nacimiento import extraer_fecha_nacimiento  # Corregido
from unir_df_fecha_nacimiento import unir
import os

def main():

    # Obtener la ruta del script actual
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Definir la ruta correcta dentro del proyecto
    ruta = os.path.join(base_dir, "..", "data", "raw", "nacimiento_peleadores")

    # Crear las carpetas si no existen
    os.makedirs(ruta, exist_ok=True)
    
    parser = argparse.ArgumentParser(description="Extracción de datos de combates y peleadores")
    subparsers = parser.add_subparsers(dest="comando", required=True)

    # Subcomando para extraer peleas
    parser_peleas = subparsers.add_parser("peleas", help="Extraer datos de combates")
    parser_peleas.add_argument("--pagina_inicio", type=int, default=1, help="Página de inicio")
    parser_peleas.add_argument("--pagina_final", type=int, default=29, help="Página final")

    # Subcomando para extraer peleadores
    parser_peleadores = subparsers.add_parser("peleadores", help="Extraer datos de peleadores")
    parser_peleadores.add_argument("--pagina_inicio", type=int, default=1, help="Página de inicio")
    parser_peleadores.add_argument("--pagina_final", type=int, default=None, help="Página final (None para llegar al final)")

    # Subcomando para extraer fechas de nacimiento
    parser_fechas = subparsers.add_parser("fechas", help="Extraer fechas de nacimiento de peleadores")
    parser_fechas.add_argument("--fila_inicio", type=int, default=0, help="Fila de inicio")
    parser_fechas.add_argument("--fila_final", type=int, default=200, help="Fila final")

    args = parser.parse_args()

    # Ejecutar la función correspondiente según el subcomando elegido
    if args.comando == "peleas":
        extraer_peleas(args.pagina_inicio, args.pagina_final)
    elif args.comando == "peleadores":
        extraer_peleadores(args.pagina_inicio, args.pagina_final)
    elif args.comando == "fechas":
        extraer_fecha_nacimiento(args.fila_inicio, args.fila_final)
        unir()

if __name__ == "__main__":
    main()
