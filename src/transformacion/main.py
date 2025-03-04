import argparse
from tratamiento_peleadores import transformacion_peleadores
from tratamiento_peleas import transformacion_peleas
from nuevas_variables import nuevas_col
from recordsPeleas import recordPeleas
from nuevas_columnas_peleas_peleadores import transformacion
import os

def main():
    # Rutas relativas desde la carpeta transformacion/
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    ruta_peleas = os.path.join(base_dir, "data", "raw", "peleas.csv")
    ruta_peleadores = os.path.join(base_dir, "data", "raw", "peleadores.csv")
    ruta_processed = os.path.join(base_dir, "data", "processed")

    # Crear carpeta 'processed' si no existe
    os.makedirs(ruta_processed, exist_ok=True)

    # Configurar argparse
    parser = argparse.ArgumentParser(description="Transformaciones de los dataframes")
    parser.add_argument("--dir_peleas", default=ruta_peleas, help="Introduce la dirección del dataframe de peleas")
    parser.add_argument("--dir_peleadores", default=ruta_peleadores, help="Introduce la dirección del dataframe de peleadores")
    args = parser.parse_args()

    # Transformaciones
    df_peleas = transformacion_peleas(args.dir_peleas)
    df_peleadores = transformacion_peleadores(args.dir_peleadores)
    df_peleas = recordPeleas(df_peleadores,df_peleas)
    df_peleas,df_peleadores = transformacion(df_peleas,df_peleadores)
    # Guardar los DataFrames transformados en 'data/processed'
    df_peleas.to_parquet(os.path.join(ruta_processed, "peleas.parquet"), index=False)
    df_peleadores.to_parquet(os.path.join(ruta_processed, "peleadores.parquet"), index=False)


if __name__ == "__main__":
    main()
