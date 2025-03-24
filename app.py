import tkinter as tk
from login import LoginApp
from database import Database
import sys
import mysql.connector

def verificar_conexao_banco():
    try:
        db = Database()
        db.close()
        return True
    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao banco de dados: {err}")
        return False

def main():
    if not verificar_conexao_banco():
        print("Não foi possível conectar ao banco de dados. Verifique as configurações em config.py")
        sys.exit(1)

    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 