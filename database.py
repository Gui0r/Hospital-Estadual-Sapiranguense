import mysql.connector
import configparser
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

# Lendo configurações adicionais
config = configparser.ConfigParser()
config.read("config.ini")

class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        self.cursor = self.conn.cursor()

    def execute(self, query, params=None):
        self.cursor.execute(query, params or ())
        self.conn.commit()

    def fetch(self, query, params=None):
        self.cursor.execute(query, params or ())
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()
