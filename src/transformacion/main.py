import argparse
from tratamiento_peleadores import transformacion_peleadores
from tratamiento_peleas import transformacion_peleas
from nuevas_variables import nuevas_col
import os

def main():

    # Ruta relativa desde transformacion/
    ruta_peleas = os.path.join("..", "data","raw", "peleas.csv")
    ruta_peleadores = os.path.join("..", "data","raw", "peleadores.csv")



    parser = argparse.ArgumentParser(description="Transformaciones de los dataframes")
    parser.add_argument("--dir_peleas",
                        default= ruta_peleas,
                        help="Introduce la dirección del dataframe de peleas")
    parser.add_argument("--dir_peleadores",default = ruta_peleadores, help="Introduce la dirección del dataframe de peleadores")
    args = parser.parse_args()

    df_peleas = transformacion_peleas(args.dir_peleas)
    df_peleadores = transformacion_peleadores(args.dir_peleadores)
    df_peleas = nuevas_col(df_peleas,df_peleadores)
    print(df_peleas.head())

if __name__ == "__main__":
    main()

