import time
from src.scraper import QuoteScraper
from src.database import Database
from src.logger import Logger

class Updater:
    def __init__(self, url, db_name, interval):
        self.url = url
        self.db_name = db_name
        self.interval = interval
        self.logger = Logger(__name__)

    def run(self):
        while True:
            self.logger.info("Proceso de actualización iniciado")
            scraper = QuoteScraper(self.url)
            quotes = scraper.scrape_quotes()
            cleaned_quotes = scraper.clean_data(quotes)

            db = Database(self.db_name)
            db.insert_quotes(cleaned_quotes)

            self.logger.info(f"Actualización completada en {self.interval} segundos")
            time.sleep(self.interval)

if __name__ == "__main__":
    updater = Updater("http://quotes.toscrape.com", "quotes.db", 3600)
    updater.run()
