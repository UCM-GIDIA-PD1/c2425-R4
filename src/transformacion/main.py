import argparse
from tratamiento_peleadores import transformacion_peleadores
from tratamiento_peleas import transformacion_peleas
from recordsPeleas import recordPeleas
from nuevas_columnas_peleas_peleadores import transformacion
from peleasMediasPond import calcular_ultimas_tres
from dfDif import crearDfDif
import os
import pandas as pd 

def main():
    # Rutas relativas desde la carpeta transformacion/
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    ruta_nuevas_peleas = os.path.join(base_dir, "data", "raw", "nuevas_peleas.csv")
    ruta_peleas = os.path.join(base_dir, "data", "raw", "peleas.csv")
    ruta_peleadores = os.path.join(base_dir, "data", "raw", "peleadores.csv")
    ruta_processed = os.path.join(base_dir, "data", "processed")

    # Cargar los CSVs
    df_nuevas = pd.read_csv(ruta_nuevas_peleas)
    df_peleas = pd.read_csv(ruta_peleas)

    # Concatenar y eliminar duplicados si es necesario
    df_combinado = pd.concat([df_peleas, df_nuevas], ignore_index=True)

    # (Opcional) Eliminar duplicados
    df_combinado.drop_duplicates(inplace=True)

    # Guardar en el mismo archivo original (sobrescribe)
    df_combinado.to_csv(ruta_peleas, index=False)

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
    df_peleadores["Puntos"] = df_peleadores["Puntos"].apply(lambda x: x.real if isinstance(x, complex) else x)
    df_peleas.to_parquet(os.path.join(ruta_processed, "peleas.parquet"), index=False)
    df_peleadores.to_parquet(os.path.join(ruta_processed, "peleadores.parquet"), index=False)
    print("Peleas y peleadores guardados")
    print("Procesando peleas con ponderaciones")
    df_peleas_pond = calcular_ultimas_tres(df_peleas)
    # Guardar los DataFrames transformados en 'data/processed'
    df_peleas_pond.to_parquet(os.path.join(ruta_processed,"peleas_ponderadas.parquet")) 
    df_dif = crearDfDif(df_peleas_pond)
    df_dif.to_parquet(os.path.join(ruta_processed,"df_dif.parquet"))


if __name__ == "__main__":
    main()
