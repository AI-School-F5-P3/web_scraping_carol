import requests
from bs4 import BeautifulSoup
from src.logger import Logger

class QuoteScraper:
    def __init__(self, url):
        self.url = url
        self.logger = Logger(__name__)

    def scrape_quotes(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            quotes = []

            all_quote_blockquotes = soup.find_all('blockquote')

            self.logger.info(f"Número total de blockquotes de citas encontrados: {len(all_quote_blockquotes)}")

            for i, quote_block in enumerate(all_quote_blockquotes, 1):
                text = quote_block.find('p')
                author = quote_block.find('footer')
                tags_element = quote_block.find('p', text=lambda x: x and x.startswith('Tags:'))

                if text and author:
                    text = text.get_text(strip=True).strip('"')
                    author = author.get_text(strip=True).strip('—')
                    tags = tags_element.get_text(strip=True).replace('Tags:', '').split(', ') if tags_element else []

                    quotes.append({
                        'text': text,
                        'author': author,
                        'tags': tags
                    })
                    self.logger.info(f"Cita {i} añadida - Autor: {author}, Tags: {tags}")
                else:
                    self.logger.warning(f"Advertencia: No se encontró texto o autor para una cita en el blockquote {i}")

            self.logger.info(f"{len(quotes)} citas scrapeadas con éxito")
            return quotes
        except requests.RequestException as e:
            self.logger.error(f"Error al scrapear las citas: {str(e)}")
            return []

    def clean_data(self, quotes):
        cleaned_quotes = []
        for quote in quotes:
            cleaned_quote = {
                'text': quote['text'].strip(),
                'author': quote['author'].strip(),
                'tags': [tag.lower() for tag in quote['tags']]
            }
            cleaned_quotes.append(cleaned_quote)
        return cleaned_quotes

if __name__ == "__main__":
    scraper = QuoteScraper("https://quotes.toscrape.com/")
    quotes = scraper.scrape_quotes()
    print(f"Número total de citas scrapeadas: {len(quotes)}")
    cleaned_quotes = scraper.clean_data(quotes)
    for i, quote in enumerate(cleaned_quotes, 1):
        print(f"\nCita {i}:")
        print(f"Texto: {quote['text']}")
        print(f"Autor: {quote['author']}")
        print(f"Etiquetas: {quote['tags']}")
                