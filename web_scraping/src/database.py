import sqlite3
from src.logger import Logger

class Database: 
    def __init__(self, db_name):
        self.db_name = db_name
        self.logger = Logger(__name__)

    def create_tables(self):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS quotes (
                    id INTEGER PRIMARY KEY,
                    text TEXT NOT NULL,
                    author TEXT NOT NULL
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tags (
                    id INTEGER PRIMARY KEY,
                    quote_id INTEGER,
                    tag TEXT NOT NULL,
                    FOREIGN KEY (quote_id) REFERENCES quotes (id)
                )
            ''')

            conn.commit()
        except sqlite3.Error as e:
            self.logger.error(f"Error al crear tablas: {e}")
        finally:
            conn.close()

    def insert_quotes(self, quotes):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            for quote in quotes:
                cursor.execute('INSERT INTO quotes (text, author) VALUES (?, ?)', (quote['text'], quote['author']))
                quote_id = cursor.lastrowid
                for tag in quote['tags']:
                    cursor.execute('INSERT INTO tags (quote_id, tag) VALUES (?, ?)', (quote_id, tag))
            conn.commit()
            self.logger.info(f"{len(quotes)} citas insertadas en la base de datos")
        except sqlite3.Error as e:
            self.logger.error(f"Error al insertar citas: {e}")
        finally:
            conn.close()

    def get_all_quotes(self):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT q.id, q.text, q.author, GROUP_CONCAT(t.tag, ',') as tags
                FROM quotes q
                LEFT JOIN tags t ON q.id = t.quote_id
                GROUP BY q.id
            ''')
            quotes = [{'id': row[0], 'text': row[1], 'author': row[2], 'tags': row[3].split(',') if row[3] else []} for row in cursor.fetchall()]
            return quotes
        except sqlite3.Error as e:
            self.logger.error(f"Error al obtener citas: {e}")
            return []
        finally:
            conn.close()