from bs4 import BeautifulSoup
import requests

URL = 'https://quotes.toscrape.com/'
respuestas_url = requests.get(URL)

soup = BeautifulSoup(respuestas_url.text, "html.parser")
citas = []

for cita in soup.find_all('div', class_='quote'):
    texto = cita.find('span', class_='text').get_text(strip=True)
    autor = cita.find('small', class_='author').get_text(strip=True)
    etiquetas = [tag.get_text(strip=True) for tag in cita.find_all('a', class_='tag')]
    if cita not in citas:
        citas.append({
            'text': texto,
            'author': autor,
            'tags': etiquetas
        })
for cita in citas:
    print(cita)