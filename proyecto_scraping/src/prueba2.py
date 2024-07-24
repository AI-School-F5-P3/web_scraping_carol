from bs4 import BeautifulSoup
import requests

BASE_URL = 'https://quotes.toscrape.com'
page_website = f'{BASE_URL}/page/{{}}/'

citas = []
autores = {}

def obtener_info_autor(url):
    respuesta = requests.get(url)
    soup = BeautifulSoup(respuesta.text, "html.parser")
    
    nombre = soup.find('h3', class_='author-title').get_text(strip=True)
    nacimiento = soup.find('span', class_='author-born-date').get_text(strip=True)
    lugar = soup.find('span', class_='author-born-location').get_text(strip=True)
    descripcion = soup.find('div', class_='author-description').get_text(strip=True)
      
    return {
        'nombre': nombre,
        'nacimiento': nacimiento,
        'lugar': lugar,
        'descripcion': descripcion
    }

for page_number in range(1, 11):
    URL = page_website.format(page_number)
    print(f'Scrapeando la página: {URL}')
    
    respuestas_url = requests.get(URL)
    soup = BeautifulSoup(respuestas_url.text, "html.parser")

    for cita in soup.find_all('div', class_='quote'):
        texto = cita.find('span', class_='text').get_text(strip=True)
        autor = cita.find('small', class_='author').get_text(strip=True)
        etiquetas = [tag.get_text(strip=True) for tag in cita.find_all('a', class_='tag')]
        
        nueva_cita = {
            'text': texto,
            'author': autor,
            'tags': etiquetas
        }
        
        if nueva_cita not in citas:
            citas.append(nueva_cita)
        
        # Obtener información del autor si aún no la tenemos
        if autor not in autores:
            about_link = cita.find('a', href=True)['href']
            autor_url = BASE_URL + about_link
            autores[autor] = obtener_info_autor(autor_url)

    # Si no hay más citas en la página, salimos del bucle
    if not soup.find_all('div', class_='quote'):
        break

print(f"Total de citas recopiladas: {len(citas)}")
print(f"Total de autores recopilados: {len(autores)}")

# Imprimir citas y autores
for cita in citas:
    print(f"Cita: {cita['text']}")
    print(f"Autor: {cita['author']}")
    print(f"Tags: {', '.join(cita['tags'])}")
    autor_info = autores[cita['author']]
    print(f"Información del autor:")
    print(f"  Nombre: {autor_info['nombre']}")
    print(f"  Nacimiento: {autor_info['nacimiento']}")
    print(f"  Lugar: {autor_info['lugar']}")
    print(f"  Descripción: {autor_info['descripcion']}")
    print("\n")