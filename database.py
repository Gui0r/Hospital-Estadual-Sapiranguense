import mysql.connector
import configparser
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

# Lendo configurações adicionais
config = configparser.ConfigParser()
config.read("config.ini")

class Database:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        self.cursor = self.connection.cursor()

    def execute(self, query, values=None):
        self.cursor.execute(query, values or ())
        self.connection.commit()

    def fetch(self, query, values=None):
        self.cursor.execute(query, values or ())
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.connection.close()
