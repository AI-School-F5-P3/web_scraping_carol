import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.database import Base, Cita, insertar_autor, insertar_cita
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class TestFuncionesBD(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Crear una conexión a una base de datos de prueba
        cls.engine = create_engine('postgresql://postgres:1234@localhost/scraping')
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)

    @classmethod
    def tearDownClass(cls):
        # Eliminar todas las tablas después de las pruebas
        Base.metadata.drop_all(cls.engine)

    def setUp(self):
        # Crear una nueva sesión para cada prueba
        self.session = self.Session()

    def tearDown(self):
        # Cerrar la sesión después de cada prueba
        self.session.close()

    def test_insertar_autor(self):
        autor = insertar_autor(self.session, 'Autor de Prueba', '1 de enero de 1990', 'Ciudad de Prueba', 'Descripción de prueba')
        self.session.commit()

        self.assertIsNotNone(autor.id)
        self.assertEqual(autor.nombre, 'Autor de Prueba')
        self.assertEqual(autor.nacimiento, '1 de enero de 1990')
        self.assertEqual(autor.lugar, 'Ciudad de Prueba')
        self.assertEqual(autor.descripcion, 'Descripción de prueba')

if __name__ == '__main__':
    unittest.main()