import os
import re
import time
import pandas as pd
import requests # Solicitudes HTTP
from bs4 import BeautifulSoup #Librería para parsear HTML
from selenium import webdriver #Automatización de navegadores
from selenium.webdriver.common.by import By # Localizar elementos HTML
from selenium.webdriver.common.keys import Keys # Simular pulsación de teclas

def get_birthdate(url):
    """Función que extrae fecha de nacimiento desde una URL usando requests y BeautifulSoup"""
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers) #Solicitud HTTP
    
    if response.status_code != 200: #Verifica si la solicitud tuvo éxito
        return f"Error: No se pudo acceder a la página (Código {response.status_code})" 
    
    soup = BeautifulSoup(response.text, 'html.parser') #Parsear HTML
    text = soup.get_text()
    date_pattern = re.compile(r'\b(\d{4}-\d{2}-\d{2})\b')
    match = date_pattern.search(text) #Buscar la fecha en el texto
    
    return match.group(0) if match else "Fecha de nacimiento no encontrada"


def extraer_fecha_nacimiento(fila_inicial, fila_final):
    """Función que extrae la fecha de nacimiento de un conjunto de peleadores"""
    archivo_general = r"../data/raw/peleadores.csv" #Ruta del archivo con los nombres de los peleadores
    
    if not os.path.exists(archivo_general): #Verifica que existe el archivo
        print(f"El archivo {archivo_general} no existe.")
        return
    
    df_general = pd.read_csv(archivo_general)
    df_rango = df_general.iloc[fila_inicial:fila_final] #Selecciona las filas según el rango indicado

    peleadores = df_rango["Nombre"].tolist()
    
    options = webdriver.ChromeOptions()
    #options.add_argument('--headless')
    options.add_argument("--no-sandbox") #Evita errores en entornos restringidos
    options.add_argument("--disable-gpu") #Desacctiva la GPU para evitar incompatibilidades 
    options.add_argument("--disable-web-security") #Desabilita resctricciones de seguridad
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36") #Simula usuario real
    
    driver = webdriver.Chrome(options=options) #Inicia navegador
    fechas = []
    url_busqueda = 'https://www.tapology.com/search' #URL base
    
    try:
        for peleador in peleadores: #Itera sobre cada peleador
            try:
                driver.get(url_busqueda)
                time.sleep(1)
                
                search_box = driver.find_element(By.NAME, "term") #Busca barra de búsqueda
                search_box.clear()
                search_box.send_keys(peleador) #Escribe el nombre del peleador
                search_box.send_keys(Keys.RETURN)
                time.sleep(1)
                
                fighter_link = driver.find_element(By.CSS_SELECTOR, "a[href*='/fighters/']") #Selecciona el primer peleador que aparece
                fighter_url = fighter_link.get_attribute("href")
                driver.get(fighter_url) #Abre la página del peleador 
                time.sleep(1)
                
                birthdate = get_birthdate(fighter_url) #Extrae la fecha de nacimiento con la función anterior 
                print(f"Peleador: {peleador} | Fecha de nacimiento: {birthdate}")
                fechas.append(birthdate) #Guarda la fecha
                
            except Exception as e:
                print(f"Error con {peleador}: {e}")
                fechas.append("No encontrado")
            
            time.sleep(1)
            
    except Exception as e:
        print("Error durante el scraping:", e)
    finally:
        driver.quit()
    
    df_rango["Nacimiento"] = fechas

    # Crear la carpeta si no existe
    carpeta_destino = "../data/raw/nacimiento_peleadores"
    os.makedirs(carpeta_destino, exist_ok=True)

    # Definir el nombre del archivo con el rango de filas
    nombre_archivo = f"peleadores_{fila_inicial}_{fila_final}_fecha_nacimiento.csv"
    ruta_archivo = os.path.join(carpeta_destino, nombre_archivo)

    # Guardar el archivo
    df_rango.to_csv(ruta_archivo, index=False, encoding="utf-8")
    print(f"Archivo guardado en {ruta_archivo}")
