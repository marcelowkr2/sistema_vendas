from tkinter import *
from PIL import Image, ImageTk
import subprocess

class MainMenu:
    def __init__(self, master):
        self.master = master
        self.master.title("Sistema de Vendas - Menu Principal")
        self.master.geometry("500x600")

        # Imagem de fundo
        self.background_image = Image.open(r"C:\Users\marce\OneDrive\Área de Trabalho\SistemaDeVendasPython\Sistema_de_Vendas\imagens\background.jpg")
        self.background_image = self.background_image.resize((500, 600), Image.Resampling.LANCZOS)  # Substitui ANTIALIAS
        self.bg_photo = ImageTk.PhotoImage(self.background_image)

        self.canvas = Canvas(self.master, width=500, height=600)
        self.canvas.create_image(0, 0, anchor=NW, image=self.bg_photo)
        self.canvas.pack(fill=BOTH, expand=True)

        # Cabeçalho
        self.heading = Label(
            self.master, text="Menu Principal", font=("Arial", 24, "bold"),
           bg="lightblue", fg="white"
        )
        self.heading.place(relx=0.5, y=40, anchor=CENTER)

        # Ícones para os botões
        self.add_icon = Image.open(r"Sistema_de_Vendas\imagens\cad_produtos.png")
        self.add_icon = self.add_icon.resize((50, 50), Image.Resampling.LANCZOS)
        self.add_icon_img = ImageTk.PhotoImage(self.add_icon)

        self.update_icon = Image.open(r"Sistema_de_Vendas\imagens\atualizar.png")
        self.update_icon = self.update_icon.resize((50, 50), Image.Resampling.LANCZOS)
        self.update_icon_img = ImageTk.PhotoImage(self.update_icon)

        self.sales_icon = Image.open(r"Sistema_de_Vendas\imagens\vender.png")
        self.sales_icon = self.sales_icon.resize((50, 50), Image.Resampling.LANCZOS)
        self.sales_icon_img = ImageTk.PhotoImage(self.sales_icon)

        self.user_icon = Image.open(r"Sistema_de_Vendas\imagens\cad_usuarios.png")
        self.user_icon = self.user_icon.resize((50, 50), Image.Resampling.LANCZOS)
        self.user_icon_img = ImageTk.PhotoImage(self.user_icon)

        # Botões com ícones
        self.add_product_btn = Button(
            self.master, text="Cadastrar Produtos", font=("Arial", 14),
            compound=LEFT, image=self.add_icon_img, width=250, height=60,
            bg="white", fg="black", command=self.open_add_to_db
        )
        self.add_product_btn.place(relx=0.5, y=120, anchor=CENTER)

        self.update_product_btn = Button(
            self.master, text="Atualizar Produtos", font=("Arial", 14),
            compound=LEFT, image=self.update_icon_img, width=250, height=60,
            bg="white", fg="black", command=self.open_update
        )
        self.update_product_btn.place(relx=0.5, y=200, anchor=CENTER)

        self.sales_btn = Button(
            self.master, text=" Realizar Vendas", font=("Arial", 14),
            compound=LEFT, image=self.sales_icon_img, width=250, height=60,
            bg="white", fg="black", command=self.open_main
        )
        self.sales_btn.place(relx=0.5, y=280, anchor=CENTER)

        self.register_btn = Button(
            self.master, text="Cadastrar Usuário", font=("Arial", 14),
            compound=LEFT, image=self.user_icon_img, width=250, height=60,
            bg="white", fg="black", command=self.open_register
        )
        self.register_btn.place(relx=0.5, y=360, anchor=CENTER)

    def open_add_to_db(self):
        subprocess.Popen(["python", r"C:\Users\marce\OneDrive\Área de Trabalho\SistemaDeVendasPython\Sistema_de_Vendas\add_product.py"])

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
