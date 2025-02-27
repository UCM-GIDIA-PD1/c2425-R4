import os
import re
import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def get_birthdate(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        return f"Error: No se pudo acceder a la página (Código {response.status_code})"
    
    soup = BeautifulSoup(response.text, 'html.parser')
    text = soup.get_text()
    date_pattern = re.compile(r'\b(\d{4}-\d{2}-\d{2})\b')
    match = date_pattern.search(text)
    
    return match.group(0) if match else "Fecha de nacimiento no encontrada"

def extraer_fecha_nacimiento(fila_inicial, fila_final):
    archivo_general = r"../data/raw/peleadores.csv"
    
    if not os.path.exists(archivo_general):
        print(f"El archivo {archivo_general} no existe.")
        return
    
    df_general = pd.read_csv(archivo_general)
    df_rango = df_general.iloc[fila_inicial:fila_final]
    
    peleadores = df_rango["Nombre"].tolist()
    
    options = webdriver.ChromeOptions()
    #options.add_argument('--headless')
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
                
                search_box = driver.find_element(By.NAME, "term")
                search_box.clear()
                search_box.send_keys(peleador)
                search_box.send_keys(Keys.RETURN)
                time.sleep(1)
                
                fighter_link = driver.find_element(By.CSS_SELECTOR, "a[href*='/fighters/']")
                fighter_url = fighter_link.get_attribute("href")
                driver.get(fighter_url)
                time.sleep(1)
                
                birthdate = get_birthdate(fighter_url)
                print(f"Peleador: {peleador} | Fecha de nacimiento: {birthdate}")
                fechas.append(birthdate)
                
            except Exception as e:
                print(f"Error con {peleador}: {e}")
                fechas.append("No encontrado")
            
            time.sleep(1)
            
    except Exception as e:
        print("Error durante el scraping:", e)
    finally:
        driver.quit()
    
    df_rango["Nacimiento"] = fechas
    
    carpeta_destino = "fecha"
    os.makedirs(carpeta_destino, exist_ok=True)

    df_rango.to_csv(r"../data/raw/peleadores_fechas_nacimiento.csv", index=False, encoding="utf-8")
    print(f"Archivo guardado en peleadores_fecha_nacimiento")
