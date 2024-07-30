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

# Instalar el cliente de PostgreSQL
RUN apt-get update && apt-get install -y postgresql-client

# Copiar el script de espera para PostgreSQL
COPY wait-for-postgres.sh /wait-for-postgres.sh
RUN chmod +x /wait-for-postgres.sh

# Comando por defecto para ejecutar tu aplicación
CMD ["/wait-for-postgres.sh", "python", "/proyecto_scraping/src/scraper.py"]
