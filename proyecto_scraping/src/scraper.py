from bs4 import BeautifulSoup
import requests
from logger import Logger
from database import insertar_cita, engine #Session, Cita
from sqlalchemy import inspect

logger = Logger("ScrapeQuotes")

#para la primera variable se crea para recorrer la primera página, la segunda se crea para iterar sobre cada una de las otras páginas. 
BASE_URL = 'https://quotes.toscrape.com'
page_website = 'https://quotes.toscrape.com/page/{}/'

#en estas variables se recogerá la información que se vaya extrayendo de las páginas.
citas = []
autores = {}

def verificar_tabla():
    inspector = inspect(engine)
    if 'citas' not in inspector.get_table_names():
        Base.metadata.create_all(engine)
        logger.info("Tabla 'citas' creada.")
    else:
        columns = [c['name'] for c in inspector.get_columns('citas')]
        expected_columns = ['id', 'texto', 'autor', 'etiquetas']
        logger.info(f"Columnas existentes: {columns}")
        logger.info(f"Columnas esperadas: {expected_columns}")
        if not all(col in columns for col in expected_columns):
            logger.error("La estructura de la tabla 'citas' no es correcta.")
            return False
    return True

# Llama a esta función antes de comenzar el scraping
if not verificar_tabla():
    logger.error("No se puede continuar debido a problemas con la estructura de la base de datos.")
    exit(1)
#función que recoge la información del autor y la limpia
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
#iteración por las páginas
for page_number in range(1, 11):
    URL = page_website.format(page_number)
    print(f'Scrapeando la página: {URL}')
    logger.info(f"Página {URL} escrapeada correctamente")
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
            logger.info("Nueva cita incluida correctamente")

            try:
                insertar_cita(texto, autor, etiquetas)
                logger.info(f"Cita de {autor} insertada correctamente")
            except Exception as e:
                logger.error(f"Error al insertar cita en la base de datos: {e}")
        # Obtener información del autor si aún no la tenemos
        if autor not in autores:
            about_link = cita.find('a', href=True)['href']
            autor_url = BASE_URL + about_link
            autores[autor] = obtener_info_autor(autor_url)

    # Si no hay más citas en la página, salimos del bucle
    if not soup.find_all('div', class_='quote'):
        logger.info("No se encontraron más citas. Finalizando el scraping")
        break

logger.info(f"Total de citas recopiladas: {len(citas)}")
logger.info(f"Total de autores recopilados: {len(autores)}")

# Imprimir citas y autores
for cita in citas:
    logger.debug(f"Cita: {cita['text']}")
    logger.debug(f"Autor: {cita['author']}")
    logger.debug(f"Tags: {', '.join(cita['tags'])}")
    autor_info = autores[cita['author']]
    logger.debug(f"Información del autor:")
    logger.debug(f"  Nacimiento: {autor_info['nacimiento']}")
    logger.debug(f"  Lugar: {autor_info['lugar']}")
    logger.debug(f"  Descripción: {autor_info['descripcion']}")
    logger.debug("\n")