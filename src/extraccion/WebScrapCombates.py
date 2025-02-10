from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

# Configuración del navegador
options = webdriver.ChromeOptions()
#options.add_argument('--headless') 
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Inicializar el navegador
driver = webdriver.Chrome(options=options)

# URL base de la lista de eventos
url_base = "http://ufcstats.com/statistics/events/completed?page="

data = []
cont = 0
try:
    # Recorrer las páginas de eventos
    for num in range(1, 29):
        url = f"{url_base}{num}"
        driver.get(url)
        time.sleep(1)  # Espera a que cargue la página
        
        # Extraer todas las URLs de los eventos en la página actual
        eventos_elements = driver.find_elements(By.CSS_SELECTOR, "tr.b-statistics__table-row a.b-link.b-link_style_black")
        event_urls = [evento.get_attribute("href") for evento in eventos_elements]
        
        # Recorrer cada evento en la lista
        for event_url in event_urls:
            try:
                driver.get(event_url)  # Navegar al evento
                time.sleep(1)
                
                # Extraer todas las URLs de las peleas del evento.
                # Asegúrate de que el selector corresponda con la estructura real del HTML.
                pelea_elements = driver.find_elements(By.CSS_SELECTOR, "tbody tr")
                pelea_urls = []
                for pelea in pelea_elements:
                    try:
                        link = pelea.find_element(By.CSS_SELECTOR, "a")
                        pelea_urls.append(link.get_attribute("href"))
                    except Exception as inner_e:
                        print(f"No se pudo extraer el link de la pelea: {inner_e}")
                
                # Recorrer cada pelea en el evento
                for pelea_url in pelea_urls:
                    driver.get(pelea_url)
                    time.sleep(1)
                    
                    WINNER = 1
                    first_person_status = driver.find_element(By.CSS_SELECTOR, ".b-fight-details__person-status")
                    if "b-fight-details__person-status_style_green" in first_person_status.get_attribute("class"):
                        WINNER = 0
                        print("Ha ganado")
                    else:
                        print("Ha perdido")
                    
                    tabla = driver.find_elements(By.CSS_SELECTOR, "tr.b-fight-details__table-row td")
                    # Verifica que se hayan encontrado todos los elementos necesarios
                    if len(tabla) < 18:
                        print("No se encontraron todas las columnas esperadas en la tabla de la pelea.")
                        continue
                    
                    tabla_filtrada = [elem for elem in tabla if elem.text.strip() != ""]
                    nombres = tabla_filtrada[0].text.split("\n")
                    peleadorA = nombres[0]
                    peleadorB = nombres[1]

                    KD = tabla_filtrada[1].text.split("\n")
                    KD_A = KD[0]
                    KD_B = KD[1]
                    SIG_STR = tabla_filtrada[3].text.split("\n")
                    SIG_STR_A = SIG_STR[0]
                    SIG_STR_B = SIG_STR[1]

                    TOTALSTR = tabla_filtrada[4].text.split("\n")
                    TOTAL_STR_A = TOTALSTR[0]
                    TOTAL_STR_B = TOTALSTR[1]

                    TD = tabla_filtrada[5].text.split("\n")
                    TD_A = TD[0]
                    TD_B = TD[1]

                    TD_PORC = tabla_filtrada[6].text.split("\n")
                    TD_PORC_A = TD_PORC[0]
                    TD_PORC_B = TD_PORC[1]

                    SUB_ATT = tabla_filtrada[7].text.split("\n")
                    SUB_ATT_A = SUB_ATT[0]
                    SUB_ATT_B = SUB_ATT[1]

                    REV = tabla_filtrada[8].text.split("\n")
                    REV_A = REV[0]
                    REV_B = REV[1]

                    CTRL = tabla_filtrada[9].text.split("\n")
                    CTRL_A = CTRL[0]
                    CTRL_B = CTRL[1]
                    
                    STR_HEAD = tabla_filtrada[13].text.split("\n")
                    STR_HEAD_A = STR_HEAD[0]
                    STR_HEAD_B = STR_HEAD[1]
                    STR_BODY = tabla_filtrada[14].text.split("\n")
                    STR_BODY_A = STR_BODY[0]
                    STR_BODY_B = STR_BODY[1]
                    STR_LEG = tabla_filtrada[15].text.split("\n")
                    STR_LEG_A = STR_LEG[0]
                    STR_LEG_B = STR_LEG[1]
                    STR_DISTANCE = tabla_filtrada[16].text.split("\n")
                    STR_DISTANCE_A = STR_DISTANCE[0]
                    STR_DISTANCE_B = STR_DISTANCE[1]
                    STR_CLINCH = tabla_filtrada[17].text.split("\n")
                    STR_CLINCH_A = STR_CLINCH[0]
                    STR_CLINCH_B = STR_CLINCH[1]
                    STR_GROUND = tabla_filtrada[18].text.split("\n")
                    
                    STR_GROUND_A = STR_GROUND[0]
                    STR_GROUND_B = STR_GROUND[1]
                    datos = {
                        "Peleador_A": peleadorA,
                        "Peleador_B": peleadorB,
                        "WINNER": WINNER,
                        "KD_A": KD_A, "KD_B": KD_B,
                        "SIG_STR_A": SIG_STR_A, "SIG_STR_B": SIG_STR_B,
                        "TOTAL_STR_A": TOTAL_STR_A, "TOTAL_STR_B": TOTAL_STR_B,
                        "TD_A": TD_A, "TD_B": TD_B,
                        "TD_PORC_A": TD_PORC_A, "TD_PORC_B": TD_PORC_B,
                        "SUB_ATT_A": SUB_ATT_A, "SUB_ATT_B": SUB_ATT_B,
                        "REV_A": REV_A, "REV_B": REV_B,
                        "CTRL_A": CTRL_A, "CTRL_B": CTRL_B,
                        "STR_HEAD_A": STR_HEAD_A, "STR_HEAD_B": STR_HEAD_B,
                        "STR_BODY_A": STR_BODY_A, "STR_BODY_B": STR_BODY_B,
                        "STR_LEG_A": STR_LEG_A, "STR_LEG_B": STR_LEG_B,
                        "STR_DISTANCE_A": STR_DISTANCE_A, "STR_DISTANCE_B": STR_DISTANCE_B,
                        "STR_CLINCH_A": STR_CLINCH_A, "STR_CLINCH_B": STR_CLINCH_B,
                        "STR_GROUND_A": STR_GROUND_A, "STR_GROUND_B": STR_GROUND_B
                    }
                    data.append(datos)
                    

            except Exception as e:
                print(f"Error extrayendo datos del evento {event_url}: {e}")
        
       
finally:
    # Guardar los datos en un CSV
    df = pd.DataFrame(data)
    df.to_csv("primeras_peleas_ufc.csv", index=False, encoding="utf-8")
    print("Datos guardados en primeras_peleas_ufc.csv")

    # Cerrar el navegador
    driver.quit()
