import tkinter as tk
from tkinter import ttk, messagebox
from database import Database
from dashboard import Dashboard
from theme import aplicar_tema

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login - Hospital Estadual Sapiranguense")
        self.root.geometry("320x200")
        self.root.resizable(False, False)

        aplicar_tema(self.root)

        frame = ttk.Frame(root, padding=20)
        frame.pack(expand=True)

        ttk.Label(frame, text="Usuário:").grid(row=0, column=0, pady=5, sticky="w")
        self.entry_user = ttk.Entry(frame, width=25)
        self.entry_user.grid(row=0, column=1, pady=5)

        ttk.Label(frame, text="Senha:").grid(row=1, column=0, pady=5, sticky="w")
        self.entry_pass = ttk.Entry(frame, width=25, show="*")
        self.entry_pass.grid(row=1, column=1, pady=5)

        self.btn_login = ttk.Button(frame, text="Entrar", command=self.verify_login)
        self.btn_login.grid(row=2, column=0, columnspan=2, pady=10)

    def verify_login(self):
        db = Database()
        user, password = self.entry_user.get(), self.entry_pass.get()

        if not user or not password:
            messagebox.showwarning("Atenção", "Preencha todos os campos!")
            return

        result = db.fetch("SELECT tipo FROM usuarios WHERE nome=%s AND senha=%s", (user, password))
        db.close()

        if result:
            role = result[0][0]
            self.root.destroy()
            Dashboard(role)
        else:
            messagebox.showerror("Erro", "Usuário ou senha inválidos!")

if __name__ == "__main__":
    root = tk.Tk()
    LoginApp(root)
    root.mainloop()
