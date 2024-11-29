import sqlite3
from tkinter import *
import tkinter.messagebox as tmsg

class AdminApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Tela de Admin - Cadastro de Usuários")
        self.master.geometry("400x400")
        self.master.config(bg="lightblue")

        # Conexão com o banco de dados
        self.db_path = r'C:\Users\marce\OneDrive\Área de Trabalho\SistemaDeVendasPython\Sistema_de_Vendas\Database\register.db'
        self.conn = sqlite3.connect(self.db_path)
        self.c = self.conn.cursor()

        # Interface gráfica
        self.heading = Label(master, text="Cadastro de Usuários", font=("Arial", 20, "bold"), bg="lightblue", fg="black")
        self.heading.pack(pady=20)

        self.username_label = Label(master, text="Usuário:", font=("Arial", 14), bg="lightblue")
        self.username_label.pack(pady=5)
        self.username_entry = Entry(master, font=("Arial", 14))
        self.username_entry.pack(pady=5)

        self.password_label = Label(master, text="Senha:", font=("Arial", 14), bg="lightblue")
        self.password_label.pack(pady=5)
        self.password_entry = Entry(master, font=("Arial", 14), show="*")
        self.password_entry.pack(pady=5)

        self.password2_label = Label(master, text="Confirme a Senha:", font=("Arial", 14), bg="lightblue")
        self.password2_label.pack(pady=5)
        self.password2_entry = Entry(master, font=("Arial", 14), show="*")
        self.password2_entry.pack(pady=5)

        # Botão para cadastrar o usuário
        self.register_btn = Button(
            master, text="Cadastrar Usuário", font=("Arial", 14), width=20, bg="steelblue", fg="white", command=self.register_user
        )
        self.register_btn.pack(pady=20)

    def register_user(self):
        """Cadastra o novo usuário no banco de dados."""
        username = self.username_entry.get()
        password = self.password_entry.get()
        password2 = self.password2_entry.get()

        # Verificar se as senhas são iguais
        if password == password2:
            # Verificar se o nome de usuário já existe
            self.c.execute("SELECT * FROM users WHERE username=?", (username,))
            if self.c.fetchone():
                tmsg.showerror("Erro", "Usuário já existe.")
            else:
                # Inserir o novo usuário no banco de dados
                self.c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                self.conn.commit()
                tmsg.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
        else:
            tmsg.showerror("Erro", "As senhas não coincidem!")

        # Limpar campos
        self.username_entry.delete(0, END)
        self.password_entry.delete(0, END)
        self.password2_entry.delete(0, END)

# Inicializar a aplicação
if __name__ == "__main__":
    root = Tk()
    app = AdminApp(root)
    root.mainloop()
