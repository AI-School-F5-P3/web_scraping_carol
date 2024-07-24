from src.scraper import QuoteScraper
from src.database import Database
from src.updater import Updater
from src.frontend import app
from src.logger import Logger
import threading

def main():
    logger = Logger(__name__)
    logger.info("Comenzando la app Scraper de Citas")

    # Inicializar y crear la base de datos
    db = Database('quotes.db')
    db.create_tables()

    # Iniciar el scraper y obtener citas iniciales
    scraper = QuoteScraper("http://quotes.toscrape.com")
    quotes = scraper.scrape_quotes()
    cleaned_quotes = scraper.clean_data(quotes)
    db.insert_quotes(cleaned_quotes)

    # Iniciar el actualizador en un hilo separado
    updater = Updater("http://quotes.toscrape.com", "quotes.db", 3600)  # Actualiza cada hora
    updater_thread = threading.Thread(target=updater.run)
    updater_thread.start()

    # Iniciar la aplicación web
    logger.info("Abriendo aplicación web")
    app.run(debug=True)

if __name__ == "__main__":
    main()