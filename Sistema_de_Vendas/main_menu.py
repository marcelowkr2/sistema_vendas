from tkinter import *
import subprocess

class MainMenu:
    def __init__(self, master):
        self.master = master
        self.master.title("Sistema de Vendas - Menu Principal")
        self.master.geometry("400x450")
        self.master.config(bg="lightblue")

        # Cabeçalho
        self.heading = Label(master, text="Menu Principal", font=("Arial", 24, "bold"), bg="lightblue", fg="black")
        self.heading.pack(pady=20)

        # Botão para abrir a tela de adicionar produtos
        self.add_product_btn = Button(
            master, text="Cadastrar Produtos", font=("Arial", 14),
            width=20, height=2, bg="steelblue", fg="white", command=self.open_add_to_db
        )
        self.add_product_btn.pack(pady=10)

        # Botão para abrir a tela de atualizar produtos
        self.update_product_btn = Button(
            master, text="Atualizar Produtos", font=("Arial", 14),
            width=20, height=2, bg="green", fg="white", command=self.open_update
        )
        self.update_product_btn.pack(pady=10)

        # Botão para abrir a tela de realizar vendas
        self.sales_btn = Button(
            master, text="Realizar Venda", font=("Arial", 14),
            width=20, height=2, bg="red", fg="white", command=self.open_main
        )
        self.sales_btn.pack(pady=10)

        # Botão para abrir a tela de cadastro de usuários
        self.register_btn = Button(
            master, text="Cadastrar Usuário", font=("Arial", 14),
            width=20, height=2, bg="blue", fg="white", command=self.open_register
        )
        self.register_btn.pack(pady=10)

    def open_add_to_db(self):
        subprocess.Popen(["python", r"C:\Users\marce\OneDrive\Área de Trabalho\SistemaDeVendasPython\Sistema_de_Vendas\add_to_db.py"])

    def open_update(self):
        subprocess.Popen(["python", r"C:\Users\marce\OneDrive\Área de Trabalho\SistemaDeVendasPython\Sistema_de_Vendas\update.py"])

    def open_main(self):
        subprocess.Popen(["python", r"C:\Users\marce\OneDrive\Área de Trabalho\SistemaDeVendasPython\Sistema_de_Vendas\main.py"])

    def open_register(self):
        subprocess.Popen(["python", r"C:\Users\marce\OneDrive\Área de Trabalho\SistemaDeVendasPython\Sistema_de_Vendas\register.py"])    


# Inicialização da interface
if __name__ == "__main__":
    root = Tk()
    app = MainMenu(root)
    root.mainloop()
