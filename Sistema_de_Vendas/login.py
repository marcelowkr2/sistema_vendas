import sqlite3
from tkinter import *
import tkinter.messagebox as tmsg
import subprocess


class LoginApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Tela de Login")
        self.master.geometry("400x300")
        self.master.config(bg="lightblue")

        # Conexão com o banco de dados
        self.db_path = r'C:\Users\marce\OneDrive\Área de Trabalho\SistemaDeVendasPython\Sistema_de_Vendas\Database\register.db'
        self.conn = sqlite3.connect(self.db_path)
        self.c = self.conn.cursor()

        # Verificar se a tabela de usuários existe
        self.create_user_table()

        # Interface gráfica
        self.heading = Label(master, text="Login", font=("Arial", 20, "bold"), bg="lightblue", fg="black")
        self.heading.pack(pady=20)

        self.username_label = Label(master, text="Usuário:", font=("Arial", 14), bg="lightblue")
        self.username_label.pack(pady=5)
        self.username_entry = Entry(master, font=("Arial", 14))
        self.username_entry.pack(pady=5)

        self.password_label = Label(master, text="Senha:", font=("Arial", 14), bg="lightblue")
        self.password_label.pack(pady=5)
        self.password_entry = Entry(master, font=("Arial", 14), show="*")
        self.password_entry.pack(pady=5)

        self.login_btn = Button(
            master, text="Entrar", font=("Arial", 14), width=15, bg="steelblue", fg="white", command=self.login
        )
        self.login_btn.pack(pady=20)

    def create_user_table(self):
        """Cria a tabela de usuários se não existir."""
        self.c.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def login(self):
        """Valida o login do usuário."""
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Verificar se o usuário e senha são válidos
        self.c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = self.c.fetchone()

        if user:
            tmsg.showinfo("Sucesso", f"Bem-vindo, {username}!")

            # Verificar se o usuário é admin
            if username == "admin" and password == "dU2q4Lpm12":  # Substitua por sua senha de admin
                self.master.destroy()  # Fecha a tela de login
                self.open_admin_screen()  # Abre a tela de admin
            else:
                self.master.destroy()  # Fecha a tela de login
                self.open_main_screen()  # Abre a tela principal
        else:
            tmsg.showerror("Erro", "Usuário ou senha incorretos.")

    def open_main_screen(self):
        """Abre a tela principal após login com sucesso."""
        try:
            tmsg.showinfo("Tela Principal", "Abrindo a tela principal...")
            subprocess.Popen(["python", r"C:\Users\marce\OneDrive\Área de Trabalho\SistemaDeVendasPython\Sistema_de_Vendas\main_menu.py"])
        except FileNotFoundError:
            tmsg.showerror("Erro", "Arquivo main_menu.py não encontrado. Verifique o caminho.")
        except Exception as e:
            tmsg.showerror("Erro", f"Erro ao abrir a tela principal: {e}")

    def open_admin_screen(self):
        """Abre a tela de admin para cadastrar usuários."""
        try:
            admin_root = Tk()
            AdminApp(admin_root)
            admin_root.mainloop()
        except Exception as e:
            tmsg.showerror("Erro", f"Erro ao abrir a tela de admin: {e}")


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

        if password == password2:
            self.c.execute("SELECT * FROM users WHERE username=?", (username,))
            if self.c.fetchone():
                tmsg.showerror("Erro", "Usuário já existe.")
            else:
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
    app = LoginApp(root)
    root.mainloop()
