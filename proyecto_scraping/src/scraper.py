from bs4 import BeautifulSoup
import requests
from database import insertar_cita
import logging

def scrapeo_citas():
    URL = 'https://quotes.toscrape.com/'
    respuestas_url = requests.get(URL)
    soup = BeautifulSoup(respuestas_url.text, "html.parser")

    for cita in soup.find_all('div', class_='quote'):
        texto = cita.find('span', class_='text').get_text(strip=True)
        autor = cita.find('small', class_='author').get_text(strip=True)
        etiquetas = [tag.get_text(strip=True) for tag in cita.find_all('a', class_='tag')]
        if cita not in insertar_cita:
            insertar_cita.append(texto, autor, etiquetas)
    
    print("Citas guardadas en la base de datos")
    logging.info("")