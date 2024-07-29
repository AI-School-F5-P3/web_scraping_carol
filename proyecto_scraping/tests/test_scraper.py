import unittest
from unittest.mock import patch, MagicMock
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from src.scraper import EscrapeoCitas


class TestEscrapeoCitas(unittest.TestCase):

    @patch('src.scraper.Logger')
    def setUp(self, mock_logger):
        self.mock_logger = MagicMock()
        mock_logger.return_value = self.mock_logger
        self.scraper = EscrapeoCitas()

    def test_verificar_tablas(self):
        with patch('src.scraper.inspect') as mock_inspect, \
             patch('src.scraper.Base.metadata.create_all') as mock_create_all:
            
            mock_inspector = MagicMock()
            mock_inspector.get_table_names.return_value = ['citas']
            mock_inspect.return_value = mock_inspector

            resultado = self.scraper.verificar_tablas()

            self.assertTrue(resultado)
            mock_create_all.assert_called_once()
            self.mock_logger.info.assert_called_with("Tabla autores creada.")

    @patch('src.scraper.requests.get')
    def test_obtener_info_autor(self, mock_get):
        mock_response = MagicMock()
        mock_response.text = '''
        <html>
            <h3 class="author-title">Autor de Prueba</h3>
            <span class="author-born-date">1 de enero de 1990</span>
            <span class="author-born-location">Ciudad de Prueba, País de Prueba</span>
            <div class="author-description">Descripción de prueba</div>
        </html>
        '''
        mock_get.return_value = mock_response

        resultado = self.scraper.obtener_info_autor('http://prueba.com')
        
        self.assertEqual(resultado['nombre'], 'Autor de Prueba')
        self.assertEqual(resultado['nacimiento'], '1 de enero de 1990')
        self.assertEqual(resultado['lugar'], 'Ciudad de Prueba, País de Prueba')
        self.assertEqual(resultado['descripcion'], 'Descripción de prueba')

    @patch('src.scraper.requests.get')
    @patch('src.scraper.insertar_cita')
    @patch('src.scraper.insertar_autor')
    def test_scrapear_pagina(self, mock_insertar_autor, mock_insertar_cita, mock_get):
        mock_response = MagicMock()
        mock_response.text = '''
        <html>
            <div class="quote">
                <span class="text">Cita de prueba</span>
                <small class="author">Autor de Prueba</small>
                <a class="tag">etiqueta1</a>
                <a class="tag">etiqueta2</a>
                <a href="/author/autor-de-prueba">Sobre</a>
            </div>
        </html>
        '''
        mock_get.return_value = mock_response

        with patch.object(self.scraper, 'obtener_info_autor') as mock_obtener_info:
            mock_obtener_info.return_value = {
                'nombre': 'Autor de Prueba',
                'nacimiento': '1 de enero de 1990',
                'lugar': 'Ciudad de Prueba, País de Prueba',
                'descripcion': 'Descripción de prueba'
            }
            
            resultado = self.scraper.scrapear_pagina(1)

        self.assertTrue(resultado)
        self.assertEqual(len(self.scraper.citas), 1)
        self.assertEqual(self.scraper.citas[0]['texto'], 'Cita de prueba')
        self.assertEqual(self.scraper.citas[0]['autor'], 'Autor de Prueba')
        self.assertEqual(self.scraper.citas[0]['etiquetas'], ['etiqueta1', 'etiqueta2'])
        mock_insertar_cita.assert_called_once()
        mock_insertar_autor.assert_called_once()

    @patch.object(EscrapeoCitas, 'verificar_tablas')
    @patch.object(EscrapeoCitas, 'scrapear_pagina')
    def test_ejecucion(self, mock_scrapear_pagina, mock_verificar_tablas):
        mock_verificar_tablas.return_value = True
        mock_scrapear_pagina.side_effect = [True, True, False]

        self.scraper.ejecucion()

        self.assertEqual(mock_scrapear_pagina.call_count, 3)
        mock_verificar_tablas.assert_called_once()

if __name__ == '__main__':
    unittest.main()
