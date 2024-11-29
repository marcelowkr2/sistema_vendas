from tkinter import *
import tkinter.messagebox as tmsg
import sqlite3


class Database:
    def __init__(self, root):
        self.root = root
        self.root.title("Supermercado Tabajara - Cadastro de Usuário")
        self.root.geometry("800x400")
        self.root.config(bg="lightblue")

        # Conexão com o banco de dados
        self.conn = sqlite3.connect(
            r"C:\Users\marce\OneDrive\Área de Trabalho\SistemaDeVendasPython\Sistema_de_Vendas\Database\admin.db"
        )
        self.c = self.conn.cursor()

        # Criar a tabela de usuários, se não existir
        self.c.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
            """
        )
        self.conn.commit()

        # Interface do usuário
        self.create_widgets()

    def create_widgets(self):
        # Cabeçalho
        Label(self.root, text="Cadastro de Usuário", font=("Arial", 24, "bold"), bg="lightblue").pack(pady=10)

        # Nome de usuário
        Label(self.root, text="Usuário:", font=("Arial", 14), bg="lightblue").place(x=50, y=70)
        self.username_entry = Entry(self.root, width=30, font=("Arial", 14))
        self.username_entry.place(x=250, y=70)

        # Senha
        Label(self.root, text="Senha:", font=("Arial", 14), bg="lightblue").place(x=50, y=120)
        self.password_entry = Entry(self.root, width=30, font=("Arial", 14), show="*")
        self.password_entry.place(x=250, y=120)

        # Confirmação de senha
        Label(self.root, text="Confirme a senha:", font=("Arial", 14), bg="lightblue").place(x=50, y=170)
        self.password2_entry = Entry(self.root, width=30, font=("Arial", 14), show="*")
        self.password2_entry.place(x=250, y=170)

        # Botão de cadastro
        Button(
            self.root,
            text="Cadastrar Usuário",
            width=20,
            height=2,
            bg="steelblue",
            fg="white",
            font=("Arial", 14),
            command=self.register_user,
        ).place(x=300, y=250)

    def register_user(self):
        # Obter valores dos campos
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        password2 = self.password2_entry.get().strip()

        # Validações
        if not username or not password or not password2:
            tmsg.showerror("Erro", "Todos os campos devem ser preenchidos!")
            return

        if password != password2:
            tmsg.showerror("Erro", "As senhas não coincidem!")
            return

        try:
            # Inserir usuário no banco de dados
            self.c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            self.conn.commit()
            tmsg.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
            # Limpar campos
            self.clear_fields()
        except sqlite3.IntegrityError:
            tmsg.showerror("Erro", "O nome de usuário já existe!")

    def clear_fields(self):
        self.username_entry.delete(0, END)
        self.password_entry.delete(0, END)
        self.password2_entry.delete(0, END)


# Inicialização da aplicação
root = Tk()
b = Database(root)


root.title("Cadastro de Usuário")
root.mainloop()
