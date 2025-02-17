import requests
from bs4 import BeautifulSoup
import re

def get_birthdate(url):
    headers = {'User-Agent': 'Mozilla/5.0'}  # Evitar bloqueo por parte del sitio
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        return f"Error: No se pudo acceder a la página (Código {response.status_code})"
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Buscar fecha de nacimiento en la página
    text = soup.get_text()
    date_pattern = re.compile(r'\b(\d{4}-\d{2}-\d{2})\b')
    match = date_pattern.search(text)
    
    return match.group(0) if match else "Fecha de nacimiento no encontrada"

url = "https://www.tapology.com/fightcenter/fighters/129278-ilia-topuria"
birthdate = get_birthdate(url)
print("Fecha de nacimiento:", birthdate)