import unittest
from src.scraper import QuoteScraper

class TestQuoteScraper(unittest.TestCase):
    def setUp(self):
        self.scraper = QuoteScraper("http://quotes.toscrape.com")

    def test_scrape_quotes(self):
        quotes = self.scraper.scrape_quotes()
        self.assertIsInstance(quotes, list)
        self.assertTrue(len(quotes) > 0)
        for quote in quotes:
            self.assertIn('text', quote)
            self.assertIn('author', quote)
            self.assertIn('tags', quotes)

    def test_clean_data(self):
        test_quotes = [
            {'text': '"Test quote"', 'author': 'Test Author', 'tags': ['Tag1', 'Tag2']}
        ]
        cleaned_quotes = self.scraper.clean_data(test_quotes)
        self.assertEqual(clean_quotes[0]['text', 'Test quote'])
        self.assertEqual(clean_quotes[0]['tags'], ['tag1', 'TAG2'])

    if __name__ == '__main__'
        unittest.main()
