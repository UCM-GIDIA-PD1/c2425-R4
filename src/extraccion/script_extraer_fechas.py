import os
import re
import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Función para obtener la fecha de nacimiento usando requests y BeautifulSoup
def get_birthdate(url):
    headers = {'User-Agent': 'Mozilla/5.0'}  # Evitar bloqueo por parte del sitio
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        return f"Error: No se pudo acceder a la página (Código {response.status_code})"
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Buscar fecha de nacimiento en el texto de la página
    text = soup.get_text()
    date_pattern = re.compile(r'\b(\d{4}-\d{2}-\d{2})\b')
    match = date_pattern.search(text)
    
    return match.group(0) if match else "Fecha de nacimiento no encontrada"

def procesar_grupo(grupo_num):
    # Rutas de origen y destino
    carpeta_origen = 'dataframes_divididos'
    archivo_origen = os.path.join(carpeta_origen, f'grupo_{grupo_num}.csv')
    
    if not os.path.exists(archivo_origen):
        print(f"El archivo {archivo_origen} no existe.")
        return
    
    # Cargar el dataframe del grupo
    df = pd.read_csv(archivo_origen)
    
    # Extraer la lista de peleadores (ajusta el nombre de la columna si es necesario)
    peleadores = df["Nombre"].tolist()
    
    # Configurar Selenium en modo headless
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--allow-running-insecure-content")
    options.add_argument("--disable-web-security")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(options=options)
    
    fechas = []
    url_busqueda = 'https://www.tapology.com/search'
    
    try:
        for peleador in peleadores:
            try:
                driver.get(url_busqueda)
                time.sleep(1)
                
                # Buscar caja de búsqueda y enviar el nombre del peleador
                search_box = driver.find_element(By.NAME, "term")
                search_box.clear()
                search_box.send_keys(peleador)
                search_box.send_keys(Keys.RETURN)
                time.sleep(1)
                
                # Seleccionar el primer enlace que contenga '/fighters/'
                fighter_link = driver.find_element(By.CSS_SELECTOR, "a[href*='/fighters/']")
                fighter_url = fighter_link.get_attribute("href")
                driver.get(fighter_url)
                time.sleep(1)
                
                # Obtener fecha de nacimiento
                birthdate = get_birthdate(fighter_url)
                print(f"Peleador: {peleador} | Fecha de nacimiento: {birthdate}")
                fechas.append(birthdate)
                
            except Exception as e:
                print(f"Error con {peleador}: {e}")
                fechas.append("No encontrado")
            
            # Espera para evitar bloqueos (ajusta el tiempo según necesites)
            time.sleep(1)
            
    except Exception as e:
        print("Error durante el scraping:", e)
    finally:
        driver.quit()
    
    # Añadir la columna "Nacimiento" al DataFrame original
    df["Nacimiento"] = fechas
    
    # La carpeta de destino es "fecha"
    carpeta_destino = "fecha"
    os.makedirs(carpeta_destino, exist_ok=True)
    
    # Guardar el DataFrame actualizado
    archivo_destino = os.path.join(carpeta_destino, f'grupo_{grupo_num}_procesado.csv')
    df.to_csv(archivo_destino, index=False)
    print(f"Archivo guardado en: {archivo_destino}")

# Define aquí el número de grupo que deseas procesar
grupo = 11  # Cambia este valor al grupo deseado

# Ejecutar la función con el grupo definido
procesar_grupo(grupo)
