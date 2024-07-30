from sqlalchemy import create_engine, ForeignKey, Column, Integer, Text, String, ARRAY, text
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from sqlalchemy.exc import OperationalError
import os
import time

Base = declarative_base()

class Autor(Base):
    __tablename__ = 'autores'

    id = Column(Integer, primary_key=True)
    nombre = Column(Text, unique=True)
    nacimiento = Column(Text, nullable=True)
    lugar = Column(Text, nullable=True)
    descripcion = Column(Text, nullable=True)
    citas = relationship("Cita", back_populates="autor")

class Cita(Base):
    __tablename__ = 'citas'

    id = Column(Integer, primary_key=True)
    texto = Column(Text)
    autor_id = Column(Integer, ForeignKey('autores.id'))
    etiquetas = Column(ARRAY(String))
    autor = relationship("Autor", back_populates="citas")

host = os.environ.get('POSTGRES_HOST', 'localhost')
port = os.environ.get('POSTGRES_PORT', '5432')  # Incluye el puerto
user = os.environ.get('POSTGRES_USER', 'postgres')
password = os.environ.get('POSTGRES_PASSWORD', '1234')
database = os.environ.get('POSTGRES_DB', 'scraping')

DATABASE_URL = f'postgresql://{user}:{password}@{host}:{port}/{database}'

def get_engine(max_retries=5, retry_interval=5):
    for attempt in range(max_retries):
        try:
            engine = create_engine(DATABASE_URL, echo=True)  # echo=True para depuración
            # Intenta realizar una consulta simple para verificar la conexión
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            return engine
        except OperationalError as e:
            if attempt < max_retries - 1:
                print(f"Error al conectar a la base de datos. Reintentando en {retry_interval} segundos...")
                time.sleep(retry_interval)
            else:
                print("No se pudo conectar a la base de datos después de varios intentos.")
                raise e

# Crear el motor de base de datos
engine = get_engine()

# Configurar la base y la sesión
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def insertar_autor(session, nombre, nacimiento, lugar, descripcion):
    autor = session.query(Autor).filter_by(nombre=nombre).first()
    if not autor:
        autor = Autor(nombre=nombre, nacimiento=nacimiento, lugar=lugar, descripcion=descripcion)
        session.add(autor)
    else:
        # Actualizar información si es necesario
        if nacimiento:
            autor.nacimiento = nacimiento
        if lugar:
            autor.lugar = lugar
        if descripcion:
            autor.descripcion = descripcion
    session.flush()
        
    return autor

def insertar_cita(session, texto, autor_nombre, etiquetas):
    autor = insertar_autor(session, autor_nombre, None, None, None)
    nueva_cita = Cita(texto=texto, autor=autor, etiquetas=etiquetas)
    session.add(nueva_cita)