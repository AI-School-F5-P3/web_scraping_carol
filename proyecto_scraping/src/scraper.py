from bs4 import BeautifulSoup
import requests
from src.logger import Logger
from src.database import Base, engine, Session, insertar_autor, insertar_cita
from sqlalchemy import inspect
import time

class EscrapeoCitas:
    def __init__(self):
        self.logger = Logger("ScrapeQuotes")
        self.BASE_URL = 'https://quotes.toscrape.com'
        self.page_website = 'https://quotes.toscrape.com/page/{}/'
        self.citas = []
        self.autores = {}
        self.session = Session()

    def verificar_tablas(self):
        inspector = inspect(engine)
        tablas_necesarias = ['citas', 'autores']
        tablas_existentes = inspector.get_table_names()
        
        tablas_faltantes = [tabla for tabla in tablas_necesarias if tabla not in tablas_existentes]
        
        if tablas_faltantes:
            Base.metadata.create_all(engine)
            for tabla in tablas_faltantes:
                self.logger.info(f"Tabla {tabla} creada.")
            return True
        return True

    def obtener_info_autor(self, url):
        self.logger.info(f"Obteniendo información del autor desde: {url}")
        time.sleep(1)
        try:
            respuesta = requests.get(url)
            respuesta.raise_for_status()
            soup = BeautifulSoup(respuesta.text, "html.parser")
            
            info = {
                'nombre': soup.find('h3', class_='author-title').get_text(strip=True) if soup.find('h3', class_='author-title') else None,
                'nacimiento': soup.find('span', class_='author-born-date').get_text(strip=True) if soup.find('span', class_='author-born-date') else None,
                'lugar': soup.find('span', class_='author-born-location').get_text(strip=True) if soup.find('span', class_='author-born-location') else None,
                'descripcion': soup.find('div', class_='author-description').get_text(strip=True) if soup.find('div', class_='author-description') else None
            }
            
            return info
        except requests.RequestException as e:
            self.logger.error(f"Error al obtener la información del autor: {e}")
            return None

    def scrapear_pagina(self, page_number):
        URL = self.page_website.format(page_number)
        self.logger.info(f'Scrapeando la página: {URL}')
        time.sleep(1)
        respuesta_url = requests.get(URL)
        soup = BeautifulSoup(respuesta_url.text, "html.parser")

        for cita in soup.find_all('div', class_='quote'):
            texto = cita.find('span', class_='text').get_text(strip=True)
            autor_nombre = cita.find('small', class_='author').get_text(strip=True)
            etiquetas = [tag.get_text(strip=True) for tag in cita.find_all('a', class_='tag')]
            
            nueva_cita = {
                'texto': texto,
                'autor': autor_nombre,
                'etiquetas': etiquetas
            }
            
            if nueva_cita not in self.citas:
                self.citas.append(nueva_cita)
                self.logger.info(f"Nueva cita de {autor_nombre} incluida correctamente")

                try:
                    insertar_cita(self.session, texto, autor_nombre, etiquetas)
                    self.logger.info(f"Cita de {autor_nombre} insertada correctamente en la base de datos")
                except Exception as e:
                    self.logger.error(f"Error al insertar cita en la base de datos: {e}")
                    self.session.rollback()

            if autor_nombre not in self.autores:
                about_link = cita.find('a', href=True)['href']
                autor_url = self.BASE_URL + about_link
                self.logger.info(f"Obteniendo información del autor: {autor_nombre} desde {autor_url}")
                info_autor = self.obtener_info_autor(autor_url)
                if info_autor:
                    self.autores[autor_nombre] = info_autor
                    self.logger.info(f"Información obtenida para {autor_nombre}")
                    try:
                        insertar_autor(self.session, info_autor['nombre'], info_autor['nacimiento'], 
                                        info_autor['lugar'], info_autor['descripcion'])
                        self.logger.info(f"Autor {autor_nombre} insertado correctamente en la base de datos")
                    except Exception as e:
                        self.logger.error(f"Error al insertar autor en la base de datos: {e}")
                        self.session.rollback()
            else:
                self.logger.info(f"Información del autor {autor_nombre} ya obtenida previamente")

        return bool(soup.find_all('div', class_='quote'))

    def ejecucion(self):
        if not self.verificar_tablas():
            self.logger.error("No se puede continuar debido a problemas con la estructura de la base de datos.")
            return

        try:
            for page_number in range(1, 11):
                if not self.scrapear_pagina(page_number):
                    self.logger.info("No se encontraron más citas. Finalizando el scraping")
                    break
            self.session.commit()
            self.logger.info("Commit realizado con éxito")
        except Exception as e:
            self.logger.error(f"Error durante el scraping: {e}")
            self.session.rollback()
        finally:
            self.session.close()

        self.logger.info(f"Total de citas recopiladas: {len(self.citas)}")
        self.logger.info(f"Total de autores recopilados: {len(self.autores)}")

if __name__ == "__main__":
    scraper = EscrapeoCitas()
    scraper.ejecucion()