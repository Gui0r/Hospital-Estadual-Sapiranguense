import tkinter as tk
from tkinter import ttk, messagebox
from database import Database
import re

class PacienteApp:
    def __init__(self):
        self.root = tk.Toplevel()
        self.root.title("Cadastro de Pacientes")
        self.root.geometry("500x400")  
        self.root.resizable(False, False)

        frame = ttk.Frame(self.root, padding=15)
        frame.pack(expand=True)
      
        ttk.Label(frame, text="Nome Completo:").grid(row=0, column=0, sticky="w")
        self.entry_nome = ttk.Entry(frame, width=40) 
        self.entry_nome.grid(row=0, column=1, pady=5)

        ttk.Label(frame, text="CPF:").grid(row=1, column=0, sticky="w")
        self.entry_cpf = ttk.Entry(frame, width=40)
        self.entry_cpf.grid(row=1, column=1, pady=5)
        self.entry_cpf.bind('<KeyRelease>', self.formatar_cpf)

        ttk.Label(frame, text="Telefone:").grid(row=2, column=0, sticky="w")
        self.entry_telefone = ttk.Entry(frame, width=40)
        self.entry_telefone.grid(row=2, column=1, pady=5)
        self.entry_telefone.bind('<KeyRelease>', self.formatar_telefone)

        endereco_frame = ttk.LabelFrame(frame, text="Endereço", padding=10)
        endereco_frame.grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")

        ttk.Label(endereco_frame, text="Rua:").grid(row=0, column=0, sticky="w")
        self.entry_rua = ttk.Entry(endereco_frame, width=40)
        self.entry_rua.grid(row=0, column=1, pady=5)

        ttk.Label(endereco_frame, text="Número:").grid(row=1, column=0, sticky="w")
        self.entry_numero = ttk.Entry(endereco_frame, width=10)
        self.entry_numero.grid(row=1, column=1, pady=5, sticky="w")

        ttk.Label(endereco_frame, text="Bairro:").grid(row=2, column=0, sticky="w")
        self.entry_bairro = ttk.Entry(endereco_frame, width=30)
        self.entry_bairro.grid(row=2, column=1, pady=5, sticky="w")

        ttk.Label(endereco_frame, text="Cidade:").grid(row=3, column=0, sticky="w")
        self.entry_cidade = ttk.Entry(endereco_frame, width=30)
        self.entry_cidade.grid(row=3, column=1, pady=5, sticky="w")

        self.btn_add = ttk.Button(frame, text="Salvar", command=self.add_paciente)
        self.btn_add.grid(row=4, column=0, columnspan=2, pady=20)

    def formatar_telefone(self, event=None):
        telefone = self.entry_telefone.get().replace("(", "").replace(")", "").replace("-", "").replace(" ", "")
        telefone = ''.join(filter(str.isdigit, telefone))
        
        formatted_tel = ""
        if len(telefone) > 0:
            if len(telefone) > 10:  # Celular
                formatted_tel = f"({telefone[:2]}) {telefone[2:7]}-{telefone[7:11]}"
            elif len(telefone) > 6:  # Fixo
                formatted_tel = f"({telefone[:2]}) {telefone[2:6]}-{telefone[6:]}"
            elif len(telefone) > 2:
                formatted_tel = f"({telefone[:2]}) {telefone[2:]}"
            else:
                formatted_tel = f"({telefone})"

        if formatted_tel != self.entry_telefone.get():
            self.entry_telefone.delete(0, tk.END)
            self.entry_telefone.insert(0, formatted_tel)

    def formatar_cpf(self, event=None):
        cpf = self.entry_cpf.get().replace(".", "").replace("-", "")
        cpf = ''.join(filter(str.isdigit, cpf))
        
        formatted_cpf = ""
        if len(cpf) > 0:
            if len(cpf) > 9:
                formatted_cpf = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:11]}"
            elif len(cpf) > 6:
                formatted_cpf = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:]}"
            elif len(cpf) > 3:
                formatted_cpf = f"{cpf[:3]}.{cpf[3:]}"
            else:
                formatted_cpf = cpf

        if formatted_cpf != self.entry_cpf.get():
            self.entry_cpf.delete(0, tk.END)
            self.entry_cpf.insert(0, formatted_cpf)

    def validar_cpf(self, cpf):
        if not re.fullmatch(r"\d{3}\.\d{3}\.\d{3}-\d{2}", cpf):
            return False
        return True

    def validar_telefone(self, telefone):
        # Aceita formato (XX) XXXXX-XXXX ou (XX) XXXX-XXXX
        return re.fullmatch(r"\(\d{2}\) \d{4,5}-\d{4}", telefone)

    def montar_endereco(self):
        rua = self.entry_rua.get().strip()
        numero = self.entry_numero.get().strip()
        bairro = self.entry_bairro.get().strip()
        cidade = self.entry_cidade.get().strip()
        
        partes = []
        if rua: partes.append(f"Rua {rua}")
        if numero: partes.append(f"Nº {numero}")
        if bairro: partes.append(f"Bairro {bairro}")
        if cidade: partes.append(cidade)
        
        return ", ".join(partes)

    def add_paciente(self):
        nome = self.entry_nome.get().strip()
        cpf = self.entry_cpf.get().strip()
        telefone = self.entry_telefone.get().strip()
        endereco = self.montar_endereco()

        if not nome or not cpf:
            messagebox.showwarning("Atenção", "Nome e CPF são obrigatórios!")
            return
        
        if not self.validar_cpf(cpf):
            cpf_numeros = ''.join(filter(str.isdigit, cpf))
            if len(cpf_numeros) != 11:
                messagebox.showerror("Erro", "CPF inválido! Digite 11 números.")
                return
            cpf = f"{cpf_numeros[:3]}.{cpf_numeros[3:6]}.{cpf_numeros[6:9]}-{cpf_numeros[9:]}"

        if telefone and not self.validar_telefone(telefone):
            messagebox.showerror("Erro", "Formato de telefone inválido!")
            return

        try:
            db = Database()
            db.execute(
                "INSERT INTO pacientes (nome, cpf, telefone, endereco) VALUES (%s, %s, %s, %s)",
                (nome, cpf, telefone, endereco)
            )
            db.close()
            messagebox.showinfo("Sucesso", "Paciente cadastrado!")
            self.root.destroy()
        except Exception as e:
            if "Duplicate entry" in str(e):
                messagebox.showerror("Erro", "CPF já cadastrado!")
            else:
                messagebox.showerror("Erro", f"Erro ao cadastrar: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    PacienteApp()
    root.mainloop()
