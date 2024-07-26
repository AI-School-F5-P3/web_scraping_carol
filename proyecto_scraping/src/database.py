from sqlalchemy import create_engine, Column, Integer, String, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Cita(Base):

    __tablename__ = 'citas'

    id = Column(Integer, primary_key=True)
    texto = Column(String[1500])
    autor = Column(String)
    etiquetas = Column(ARRAY(String))

#crear la conexión a la base de datos
engine = create_engine('postgresql://postgres:1234@localhost/scraping')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def insertar_cita(texto, autor, etiquetas):
    session = Session()
    nueva_cita = Cita(texto=texto, autor=autor, etiquetas=etiquetas)
    session.add(nueva_cita)
    session.commit()
    session.close()