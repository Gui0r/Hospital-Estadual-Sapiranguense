import tkinter as tk
from tkinter import ttk
from theme import aplicar_tema
from pacientes import PacienteApp
from medicos import MedicoApp
from consultas import ConsultaApp
from relatorios import RelatorioApp

class Dashboard:
    def __init__(self, role):
        self.root = tk.Tk()
        self.root.title("Hospital Estadual Sapiranguense - Painel Principal")
        self.root.geometry("500x300")
        self.root.resizable(False, False)

        aplicar_tema(self.root)

        ttk.Label(self.root, text="Bem-vindo ao Hospital E.A", font=("Arial", 14)).pack(pady=10)

        frame = ttk.Frame(self.root, padding=10)
        frame.pack()

        botoes = [
            ("Pacientes", self.open_pacientes),
            ("Médicos", self.open_medicos),
            ("Consultas", self.open_consultas),
            ("Relatórios", self.open_relatorios),
        ]

        for i, (texto, comando) in enumerate(botoes):
            ttk.Button(frame, text=texto, width=20, command=comando).grid(row=i, column=0, pady=5)

        self.root.mainloop()

    def open_pacientes(self):
        PacienteApp()

    def open_medicos(self):
        MedicoApp()

    def open_consultas(self):
        ConsultaApp()

    def open_relatorios(self):
        RelatorioApp()
