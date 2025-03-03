from extraccion.WebScrapCombates import extraer_peleas
from extraccion.scraper_peleadores import extraer_peleadores
from extraccion.scraper_fecha_nacimiento import extraer_fecha_nacimiento

def main():
    print("Iniciando extracción de peleas")
    extraer_peleas(1, 29)  

    print("Iniciando extracción de peleadores")
    extraer_peleadores(1, None)  

    print("Iniciando extracción de fechas de nacimiento")
    extraer_fecha_nacimiento(0, 200)  

    print("Extracción completa")

if __name__ == "__main__":
    main()
