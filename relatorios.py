import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from database import Database
from tkcalendar import DateEntry
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from datetime import datetime
import os

class RelatorioApp:
    def __init__(self):
        self.root = tk.Toplevel()
        self.root.title("Relatórios")
        self.root.geometry("600x400")
        self.root.resizable(False, False)

        frame = ttk.Frame(self.root, padding=15)
        frame.pack(expand=True, fill="both")

        filtros_frame = ttk.LabelFrame(frame, text="Filtros", padding=10)
        filtros_frame.pack(fill="x", pady=5)

        # Data inicial
        ttk.Label(filtros_frame, text="Data Inicial:").grid(row=0, column=0, padx=5, pady=5)
        self.data_inicial = DateEntry(filtros_frame, width=12, locale='pt_BR')
        self.data_inicial.grid(row=0, column=1, padx=5, pady=5)

        # Data final
        ttk.Label(filtros_frame, text="Data Final:").grid(row=0, column=2, padx=5, pady=5)
        self.data_final = DateEntry(filtros_frame, width=12, locale='pt_BR')
        self.data_final.grid(row=0, column=3, padx=5, pady=5)

        # Tipo de relatório
        ttk.Label(filtros_frame, text="Tipo:").grid(row=1, column=0, padx=5, pady=5)
        self.tipo_relatorio = ttk.Combobox(filtros_frame, width=20)
        self.tipo_relatorio['values'] = ['Consultas por Período', 'Médicos e Atendimentos', 'Pacientes Cadastrados']
        self.tipo_relatorio.grid(row=1, column=1, columnspan=2, padx=5, pady=5)
        self.tipo_relatorio.set('Consultas por Período')

        # Botões
        ttk.Button(filtros_frame, text="Gerar Relatório", command=self.gerar_relatorio).grid(
            row=2, column=0, columnspan=4, pady=15
        )

        # Frame para prévia
        previa_frame = ttk.LabelFrame(frame, text="Prévia", padding=10)
        previa_frame.pack(fill="both", expand=True, pady=5)

        # Treeview para prévia
        self.tree = ttk.Treeview(previa_frame, show="headings")
        self.tree.pack(fill="both", expand=True)

        self.configurar_treeview()

    def configurar_treeview(self):
        # Configuração inicial para Consultas por Período
        self.tree["columns"] = ("data", "hora", "paciente", "medico", "motivo")
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

    def gerar_relatorio(self):
        tipo = self.tipo_relatorio.get()
        data_ini = self.data_inicial.get_date().strftime('%Y-%m-%d')
        data_fim = self.data_final.get_date().strftime('%Y-%m-%d')

        if tipo == 'Consultas por Período':
            dados = self.get_dados_consultas(data_ini, data_fim)
            colunas = ['Data', 'Hora', 'Paciente', 'Médico', 'Motivo']
        elif tipo == 'Médicos e Atendimentos':
            dados = self.get_dados_medicos(data_ini, data_fim)
            colunas = ['Médico', 'Especialidade', 'Total Atendimentos']
        else:  # Pacientes Cadastrados
            dados = self.get_dados_pacientes()
            colunas = ['Nome', 'CPF', 'Telefone', 'Total Consultas']

        if not dados:
            messagebox.showinfo("Aviso", "Nenhum dado encontrado para o período selecionado!")
            return

        # Atualizar prévia
        self.atualizar_previa(dados, colunas)

        # Gerar PDF
        filename = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            title="Salvar Relatório"
        )

        if filename:
            self.gerar_pdf(filename, dados, colunas, tipo)
            messagebox.showinfo("Sucesso", "Relatório gerado com sucesso!")

    def get_dados_consultas(self, data_ini, data_fim):
        db = Database()
        dados = db.fetch("""
            SELECT 
                DATE_FORMAT(c.data_consulta, '%d/%m/%Y'),
                DATE_FORMAT(c.data_consulta, '%H:%i'),
                p.nome,
                m.nome,
                c.motivo
            FROM consultas c
            JOIN pacientes p ON c.paciente_id = p.id
            JOIN medicos m ON c.medico_id = m.id
            WHERE DATE(c.data_consulta) BETWEEN %s AND %s
            ORDER BY c.data_consulta
        """, (data_ini, data_fim))
        db.close()
        return dados

    def get_dados_medicos(self, data_ini, data_fim):
        db = Database()
        dados = db.fetch("""
            SELECT 
                m.nome,
                m.especialidade,
                COUNT(c.id) as total
            FROM medicos m
            LEFT JOIN consultas c ON m.id = c.medico_id
            AND DATE(c.data_consulta) BETWEEN %s AND %s
            GROUP BY m.id
            ORDER BY total DESC
        """, (data_ini, data_fim))
        db.close()
        return dados

    def get_dados_pacientes(self):
        db = Database()
        dados = db.fetch("""
            SELECT 
                p.nome,
                p.cpf,
                p.telefone,
                COUNT(c.id) as total
            FROM pacientes p
            LEFT JOIN consultas c ON p.id = c.paciente_id
            GROUP BY p.id
            ORDER BY total DESC
        """)
        db.close()
        return dados

    def atualizar_previa(self, dados, colunas):
        # Limpar treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Configurar colunas
        self.tree["columns"] = tuple(range(len(colunas)))
        for i, col in enumerate(colunas):
            self.tree.heading(i, text=col)
            self.tree.column(i, width=100)

        # Inserir dados
        for row in dados:
            self.tree.insert("", "end", values=row)

    def gerar_pdf(self, filename, dados, colunas, titulo):
        doc = SimpleDocTemplate(filename, pagesize=letter)
        elements = []

        # Estilos
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=30
        )

        # Título
        elements.append(Paragraph(titulo, title_style))
        elements.append(Spacer(1, 20))

        # Dados da tabela
        data = [colunas] + list(dados)
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))

        elements.append(table)
        doc.build(elements)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    RelatorioApp()
    root.mainloop() 