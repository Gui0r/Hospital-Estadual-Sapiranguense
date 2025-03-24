import tkinter as tk
from tkinter import ttk, messagebox
from database import Database
import re
from datetime import datetime, timedelta

class MedicoApp:
    def __init__(self):
        self.root = tk.Toplevel()
        self.root.title("Cadastro de Médicos")
        self.root.geometry("400x350")
        self.root.resizable(False, False)

        frame = ttk.Frame(self.root, padding=15)
        frame.pack(expand=True)

        ttk.Label(frame, text="Nome Completo:").grid(row=0, column=0, sticky="w")
        self.entry_nome = ttk.Entry(frame, width=40)
        self.entry_nome.grid(row=0, column=1, pady=5)

        ttk.Label(frame, text="CRM:").grid(row=1, column=0, sticky="w")
        self.entry_crm = ttk.Entry(frame, width=40)
        self.entry_crm.grid(row=1, column=1, pady=5)

        ttk.Label(frame, text="Especialidade:").grid(row=2, column=0, sticky="w")
        self.entry_especialidade = ttk.Entry(frame, width=40)
        self.entry_especialidade.grid(row=2, column=1, pady=5)

        horario_frame = ttk.LabelFrame(frame, text="Horário de Atendimento (formato 24h)", padding=10)
        horario_frame.grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")

        ttk.Label(horario_frame, text="Início (HH:MM):").grid(row=0, column=0, padx=5)
        self.hora_inicio = ttk.Entry(horario_frame, width=8)
        self.hora_inicio.grid(row=0, column=1, padx=5)
        self.hora_inicio.bind('<KeyRelease>', lambda e: self.formatar_hora(self.hora_inicio))

        ttk.Label(horario_frame, text="Fim (HH:MM):").grid(row=0, column=2, padx=5)
        self.hora_fim = ttk.Entry(horario_frame, width=8)
        self.hora_fim.grid(row=0, column=3, padx=5)
        self.hora_fim.bind('<KeyRelease>', lambda e: self.formatar_hora(self.hora_fim))

        ttk.Label(horario_frame, text="Exemplo: 08:30 17:00", foreground="gray").grid(
            row=1, column=0, columnspan=4, pady=(5,0)
        )

        self.btn_add = ttk.Button(frame, text="Salvar", command=self.add_medico)
        self.btn_add.grid(row=4, column=0, columnspan=2, pady=20)

    def formatar_hora(self, entry):
        texto = entry.get().replace(":", "")
        texto = ''.join(filter(str.isdigit, texto))
        
        if len(texto) > 4:
            texto = texto[:4]
        
        if len(texto) >= 2:
            horas = texto[:2]
            if int(horas) > 23:
                horas = "23"
            if len(texto) > 2:
                minutos = texto[2:4]
                if int(minutos) > 59:
                    minutos = "59"
                texto = f"{horas}:{minutos}"
            else:
                texto = f"{horas}:{texto[2:]}"
        
        if texto != entry.get():
            entry.delete(0, tk.END)
            entry.insert(0, texto)

    def validar_crm(self, crm):
        return re.fullmatch(r"\d{4,6}/[A-Z]{2}", crm)

    def validar_horario(self, horario):
        try:
            if not re.fullmatch(r"\d{2}:\d{2}", horario):
                return False
            horas, minutos = map(int, horario.split(":"))
            return 0 <= horas <= 23 and 0 <= minutos <= 59
        except:
            return False

    def add_medico(self):
        nome = self.entry_nome.get().strip()
        crm = self.entry_crm.get().strip()
        especialidade = self.entry_especialidade.get().strip()
        hora_inicio = self.hora_inicio.get().strip()
        hora_fim = self.hora_fim.get().strip()

        if not all([nome, crm, especialidade, hora_inicio, hora_fim]):
            messagebox.showwarning("Atenção", "Preencha todos os campos!")
            return

        if not self.validar_crm(crm):
            messagebox.showerror("Erro", "CRM inválido! Formato esperado: NÚMERO/UF (ex: 123456/SP)")
            return

        if not self.validar_horario(hora_inicio) or not self.validar_horario(hora_fim):
            messagebox.showerror("Erro", "Formato de horário inválido! Use HH:MM (ex: 08:30)")
            return

        try:
            hora_inicio_dt = datetime.strptime(hora_inicio, "%H:%M")
            hora_fim_dt = datetime.strptime(hora_fim, "%H:%M")
            if hora_inicio_dt >= hora_fim_dt:
                messagebox.showerror("Erro", "O horário de início deve ser anterior ao horário de fim!")
                return
        except:
            messagebox.showerror("Erro", "Horário inválido!")
            return

        horario_atendimento = f"{hora_inicio} {hora_fim}"

        try:
            db = Database()
            db.execute(
                "INSERT INTO medicos (nome, crm, especialidade, horario_atendimento) VALUES (%s, %s, %s, %s)",
                (nome, crm, especialidade, horario_atendimento)
            )
            db.close()
            messagebox.showinfo("Sucesso", "Médico cadastrado!")
            self.root.destroy()
        except Exception as e:
            if "Duplicate entry" in str(e):
                messagebox.showerror("Erro", "CRM já cadastrado!")
            else:
                messagebox.showerror("Erro", f"Erro ao cadastrar: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    MedicoApp()
    root.mainloop() 