import tkinter as tk
from tkinter import ttk, messagebox
from database import Database
from tkcalendar import DateEntry
from datetime import datetime, timedelta

class ConsultaApp:
    def __init__(self):
        self.root = tk.Toplevel()
        self.root.title("Agendamento de Consultas")
        self.root.geometry("1200x500")
        self.root.resizable(False, False)

        # Frame principal
        main_frame = ttk.Frame(self.root, padding=15)
        main_frame.pack(expand=True, fill="both")

        # Frame para agendamento
        agenda_frame = ttk.LabelFrame(main_frame, text="Agendar Consulta", padding=10)
        agenda_frame.pack(fill="x", pady=5)

        # Seleção de paciente
        ttk.Label(agenda_frame, text="Paciente:").grid(row=0, column=0, sticky="w", pady=5)
        self.paciente_cb = ttk.Combobox(agenda_frame, width=40)
        self.paciente_cb.grid(row=0, column=1, padx=5, pady=5)

        # Seleção de médico
        ttk.Label(agenda_frame, text="Médico:").grid(row=1, column=0, sticky="w", pady=5)
        self.medico_cb = ttk.Combobox(agenda_frame, width=40)
        self.medico_cb.grid(row=1, column=1, padx=5, pady=5)
        self.medico_cb.bind('<<ComboboxSelected>>', self.atualizar_horarios)

        # Data da consulta
        ttk.Label(agenda_frame, text="Data:").grid(row=2, column=0, sticky="w", pady=5)
        self.data_entry = DateEntry(agenda_frame, width=20, locale='pt_BR')
        self.data_entry.grid(row=2, column=1, sticky="w", padx=5, pady=5)

        # Horário
        ttk.Label(agenda_frame, text="Horário:").grid(row=3, column=0, sticky="w", pady=5)
        self.horario_cb = ttk.Combobox(agenda_frame, width=10)
        self.horario_cb.grid(row=3, column=1, sticky="w", padx=5, pady=5)

        # Motivo da consulta
        ttk.Label(agenda_frame, text="Motivo:").grid(row=4, column=0, sticky="w", pady=5)
        self.motivo_text = tk.Text(agenda_frame, height=3, width=40)
        self.motivo_text.grid(row=4, column=1, padx=5, pady=5)

        # Botão de agendar
        ttk.Button(agenda_frame, text="Agendar Consulta", command=self.agendar_consulta).grid(
            row=5, column=0, columnspan=2, pady=15
        )

        # Frame para lista de consultas
        list_frame = ttk.LabelFrame(main_frame, text="Consultas Agendadas", padding=10)
        list_frame.pack(fill="both", expand=True, pady=5)

        # Treeview para listar consultas
        self.tree = ttk.Treeview(list_frame, columns=("data", "hora", "paciente", "medico", "motivo"), show="headings")
        self.tree.heading("data", text="Data")
        self.tree.heading("hora", text="Hora")
        self.tree.heading("paciente", text="Paciente")
        self.tree.heading("medico", text="Médico")
        self.tree.heading("motivo", text="Motivo")
        
        self.tree.column("data", width=100)
        self.tree.column("hora", width=70)
        self.tree.column("paciente", width=150)
        self.tree.column("medico", width=150)
        self.tree.column("motivo", width=200)
        
        self.tree.pack(fill="both", expand=True)

        # Carregar dados
        self.carregar_pacientes()
        self.carregar_medicos()
        self.atualizar_lista_consultas()

    def carregar_pacientes(self):
        db = Database()
        pacientes = db.fetch("SELECT id, nome FROM pacientes ORDER BY nome")
        db.close()
        
        if not pacientes:
            messagebox.showwarning("Atenção", "Não há pacientes cadastrados!\n"
                                 "Cadastre um paciente primeiro.")
            return
        
        self.pacientes_dict = {f"{p[1]} (ID: {p[0]})": p[0] for p in pacientes}
        self.paciente_cb['values'] = list(self.pacientes_dict.keys())

    def carregar_medicos(self):
        db = Database()
        medicos = db.fetch("SELECT id, nome, especialidade FROM medicos ORDER BY nome")
        db.close()
        
        if not medicos:
            messagebox.showwarning("Atenção", "Não há médicos cadastrados!\n"
                                 "Cadastre um médico primeiro.")
            return
        
        self.medicos_dict = {f"{m[1]} - {m[2]} (ID: {m[0]})": m[0] for m in medicos}
        self.medico_cb['values'] = list(self.medicos_dict.keys())

    def agendar_consulta(self):
        paciente = self.paciente_cb.get()
        medico = self.medico_cb.get()
        data = self.data_entry.get_date()
        horario = self.horario_cb.get()
        motivo = self.motivo_text.get("1.0", "end-1c")

        if not all([paciente, medico, horario, motivo]):
            messagebox.showwarning("Atenção", "Preencha todos os campos!")
            return

        try:
            # Verificar se o paciente existe no banco
            if paciente not in self.pacientes_dict:
                messagebox.showerror("Erro", "Paciente não encontrado! Selecione um paciente da lista.")
                return
            
            # Verificar se o médico existe no banco
            if medico not in self.medicos_dict:
                messagebox.showerror("Erro", "Médico não encontrado! Selecione um médico da lista.")
                return

            paciente_id = self.pacientes_dict[paciente]
            medico_id = self.medicos_dict[medico]
            data_hora = f"{data.strftime('%Y-%m-%d')} {horario}:00"

            db = Database()
            # Verificar se já existe consulta no mesmo horário
            existing = db.fetch("""
                SELECT COUNT(*) FROM consultas 
                WHERE medico_id = %s AND data_consulta = %s
            """, (medico_id, data_hora))

            if existing[0][0] > 0:
                messagebox.showerror("Erro", "Já existe uma consulta agendada neste horário!")
                db.close()
                return

            # Inserir a consulta
            db.execute("""
                INSERT INTO consultas (paciente_id, medico_id, data_consulta, motivo)
                VALUES (%s, %s, %s, %s)
            """, (paciente_id, medico_id, data_hora, motivo))
            db.close()

            messagebox.showinfo("Sucesso", "Consulta agendada com sucesso!")
            self.atualizar_lista_consultas()
            self.limpar_campos()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao agendar consulta: {str(e)}\n\n"
                                "Verifique se:\n"
                                "1. Há pacientes cadastrados\n"
                                "2. Há médicos cadastrados\n"
                                "3. O banco de dados está conectado")

    def atualizar_lista_consultas(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        db = Database()
        consultas = db.fetch("""
            SELECT c.data_consulta, p.nome, m.nome, c.motivo 
            FROM consultas c
            JOIN pacientes p ON c.paciente_id = p.id
            JOIN medicos m ON c.medico_id = m.id
            ORDER BY c.data_consulta
        """)
        db.close()

        for consulta in consultas:
            data_hora = datetime.strptime(str(consulta[0]), '%Y-%m-%d %H:%M:%S')
            data = data_hora.strftime('%d/%m/%Y')
            hora = data_hora.strftime('%H:%M')
            self.tree.insert("", "end", values=(data, hora, consulta[1], consulta[2], consulta[3]))

    def limpar_campos(self):
        self.paciente_cb.set('')
        self.medico_cb.set('')
        self.horario_cb.set('')
        self.motivo_text.delete("1.0", "end")

    def atualizar_horarios(self, event=None):
        medico = self.medico_cb.get()
        if not medico or medico not in self.medicos_dict:
            self.horario_cb['values'] = []
            return

        db = Database()
        result = db.fetch(
            "SELECT horario_atendimento FROM medicos WHERE id = %s",
            (self.medicos_dict[medico],)
        )
        db.close()

        if not result:
            return

        horario_atendimento = result[0][0]
        inicio, fim = horario_atendimento.split()
        
        # Converte strings para datetime
        hora_inicio = datetime.strptime(inicio, "%H:%M")
        hora_fim = datetime.strptime(fim, "%H:%M")
        
        # Gera lista de horários disponíveis em intervalos de 30 minutos
        horarios = []
        hora_atual = hora_inicio
        while hora_atual < hora_fim:
            horarios.append(hora_atual.strftime("%H:%M"))
            hora_atual += timedelta(minutes=30)

        self.horario_cb['values'] = horarios
        if horarios:
            self.horario_cb.set(horarios[0])

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    ConsultaApp()
    root.mainloop() 