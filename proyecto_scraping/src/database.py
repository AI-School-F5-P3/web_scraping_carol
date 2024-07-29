from sqlalchemy import create_engine, ForeignKey, Column, Integer, Text, String, ARRAY
from sqlalchemy.orm import sessionmaker, relationship, declarative_base

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

# Crear la conexión a la base de datos
engine = create_engine('postgresql://postgres:1234@localhost/scraping')
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