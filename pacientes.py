import tkinter as tk
from tkinter import ttk, messagebox
from database import Database
import re

class PacienteApp:
    def __init__(self):
        self.root = tk.Toplevel()
        self.root.title("Cadastro de Pacientes")
        self.root.geometry("400x250")
        self.root.resizable(False, False)

        frame = ttk.Frame(self.root, padding=15)
        frame.pack(expand=True)

        ttk.Label(frame, text="Nome Completo:").grid(row=0, column=0, sticky="w")
        self.entry_nome = ttk.Entry(frame, width=30)
        self.entry_nome.grid(row=0, column=1, pady=5)

        ttk.Label(frame, text="CPF:").grid(row=1, column=0, sticky="w")
        self.entry_cpf = ttk.Entry(frame, width=30)
        self.entry_cpf.grid(row=1, column=1, pady=5)

        self.btn_add = ttk.Button(frame, text="Salvar", command=self.add_paciente)
        self.btn_add.grid(row=2, column=0, columnspan=2, pady=10)

    def validar_cpf(self, cpf):
        return re.fullmatch(r"\d{3}\.\d{3}\.\d{3}-\d{2}", cpf)

    def add_paciente(self):
        nome = self.entry_nome.get().strip()
        cpf = self.entry_cpf.get().strip()

        if not nome or not cpf:
            messagebox.showwarning("Atenção", "Preencha todos os campos!")
            return
        
        if not self.validar_cpf(cpf):
            messagebox.showerror("Erro", "CPF inválido! Formato esperado: 000.000.000-00")
            return

        db = Database()
        db.execute("INSERT INTO pacientes (nome, cpf) VALUES (%s, %s)", (nome, cpf))
        db.close()
        messagebox.showinfo("Sucesso", "Paciente cadastrado!")

if __name__ == "__main__":
    PacienteApp()
