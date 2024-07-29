# Utilizar una imagen base de Python
FROM python:3.12-slim

# Instalar dependencias del sistema necesarias para psycopg2 y otras bibliotecas
RUN apt-get update && \
    apt-get install -y git gcc libc6-dev libpq-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Establecer el directorio de trabajo
WORKDIR /proyecto_scraping

# Copiar los archivos del proyecto al contenedor
COPY . /proyecto_scraping/

# Instalar las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Comando por defecto para ejecutar tu aplicación
CMD ["python", "/proyecto_scraping/src/scraper.py", "/proyecto_scraping/src/database.py", "/proyecto_scraping/src/logger.py"]
