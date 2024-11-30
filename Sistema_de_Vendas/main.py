from tkinter import *
from tkinter import ttk
import sqlite3
import tkinter.messagebox
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image, ImageTk
import os

# Obtenha a data atual e formate-a
date = datetime.datetime.now().strftime("%d/%m/%Y")

# Conexão com o banco de dados
conn = sqlite3.connect(r'C:\Users\marce\OneDrive\Área de Trabalho\SistemaDeVendasPython\Sistema_de_Vendas\Database\store.db')
c = conn.cursor()


class Application:
    def __init__(self, master, *args, **kwargs):
        self.master = master

        # Carregar as imagens de fundo
        self.left_bg = PhotoImage(file=r"C:\Users\marce\OneDrive\Área de Trabalho\SistemaDeVendasPython\Sistema_de_Vendas\imagens\back04.png")
        self.right_bg = PhotoImage(file=r"C:\Users\marce\OneDrive\Área de Trabalho\SistemaDeVendasPython\Sistema_de_Vendas\imagens\back01.png")

        # Frame esquerdo
        self.left = Frame(master, width=700, height=760, bg='white')
        self.left.pack(side=LEFT, fill=BOTH)

         # Label para o background esquerdo
        self.left_bg_label = Label(self.left, image=self.left_bg)
        self.left_bg_label.place(x=0, y=0, relwidth=1, relheight=1)


        # Frame direito
        self.right = Frame(master, width=666, height=768, bg='lightblue', relief=RIDGE, borderwidth=2)
        self.right.pack(side=RIGHT, fill=BOTH)

        # Label para o background direito
        self.right_bg_label = Label(self.right, image=self.right_bg)
        self.right_bg_label.place(x=0, y=0, relwidth=1, relheight=1)


        # Carregar a imagem da logomarca
        logo_image = Image.open(r"C:\Users\marce\OneDrive\Área de Trabalho\SistemaDeVendasPython\Sistema_de_Vendas\imagens\mercado-todo-dia-logo.png")  # Atualize com o caminho correto
        logo_image = logo_image.resize((700, 100))  # Redimensione para o tamanho desejado
        self.logo_photo = ImageTk.PhotoImage(logo_image)

        # Substituir o título por uma logomarca
        self.logo_label = Label(self.left, image=self.logo_photo, bg='red')
        self.logo_label.place(x=10, y=0)  # Ajuste as coordenadas conforme necessário

        self.enterid = Label(self.left, text="ID do Produto:", font=('arial 18 bold'), fg='black', bg='white')
        self.enterid.place(x=0, y=120)

        self.enteride = Entry(self.left, width=25, font=('arial 18 bold'), bg='lightblue')
        self.enteride.place(x=190, y=120)

        self.search_btn = Button(self.left, text="Pesquisar", width=22, height=2, bg='steelblue', fg='white', command=self.jx)
        self.search_btn.place(x=350, y=160)

        self.productname = Label(self.left, text="", font=('arial 18 bold'), fg='black', bg='white')
        self.productname.place(x=0, y=200)

        self.pprice = Label(self.left, text="", font=('arial 18 bold'), fg='black', bg='white')
        self.pprice.place(x=0, y=250)

        # Campo para valor pago e troco
        self.total_paid_label = Label(self.left, text="Total Pago:", font=('arial 18 bold'), fg='black', bg='white')
        self.total_paid_label.place(x=0, y=480)

        self.total_paid_entry = Entry(self.left, width=25, font=('arial 18 bold'), bg='lightblue')
        self.total_paid_entry.place(x=190, y=480)

        self.calculate_change_btn = Button(self.left, text="Calcular Troco", width=22, height=2, bg='green', fg='white', command=self.calculate_change)
        self.calculate_change_btn.place(x=350, y=520)

        self.change_label = Label(self.left, text="", font=('arial 18 bold'), fg='black', bg='white')
        self.change_label.place(x=0, y=580)

        # Botão para gerar recibo
        self.bill_btn = Button(self.left, text="Gerar Recibo", width=22, height=2, bg='red', fg='white', command=self.generate_receipt)
        self.bill_btn.place(x=350, y=640)

        # Data
        self.date_l = Label(self.right, text="Data: " + date, font=('arial 16 bold'), fg='white', bg='red')
        self.date_l.place(x=20, y=10)

        # Total
        self.total_l = Label(self.right, text="Total: R$ 0.00", font=('arial 27 bold'), fg='white', bg='red')
        self.total_l.place(x=20, y=60)

        # Estilo para Treeview
        style = ttk.Style()
        style.configure("Treeview", font=('Arial', 14), rowheight=30)
        style.configure("Treeview.Heading", font=('Arial', 16, 'bold'))

        # Tabela (Treeview)
        self.cart_table = ttk.Treeview(
            self.right,
            columns=("Produto", "Quantidade", "Preço Total"),
            show='headings',
            height=10,
            selectmode="extended"
        )
        self.cart_table.heading("Produto", text="Produto")
        self.cart_table.heading("Quantidade", text="Quantidade")
        self.cart_table.heading("Preço Total", text="Preço Total")
        self.cart_table.column("Produto", anchor=CENTER, width=200)
        self.cart_table.column("Quantidade", anchor=CENTER, width=150)
        self.cart_table.column("Preço Total", anchor=CENTER, width=150)
        self.cart_table.place(x=20, y=120, width=600, height=300)

        # Área de recibo
        self.receipt_area = Text(self.right, width=40, height=10, font=('arial', 12), bg='white', fg='black')
        self.receipt_area.place(x=20, y=450)

    def jx(self, *args, **kwargs):
        try:
            self.get_id = self.enteride.get()
            query = "SELECT * FROM inventory WHERE id=?"
            result = c.execute(query, (self.get_id,))
            record = result.fetchone()  # Obtém apenas o primeiro registro encontrado

            if record:
                self.get_id = record[0]
                self.get_name = record[1]
                self.get_stock = record[2]
                self.get_price = record[3]

                self.productname.configure(text="Produto: " + str(self.get_name))
                self.pprice.configure(text="Preço: R$ " + str(self.get_price))

                # Campos adicionais para entrada de quantidade e desconto
                self.quantity_l = Label(self.left, text="Quantidade", font=('arial 18 bold'), fg='black', bg='white')
                self.quantity_l.place(x=0, y=330)

                self.quantity_e = Entry(self.left, width=25, font=('arial 18 bold'), bg='lightblue')
                self.quantity_e.place(x=190, y=330)
                self.quantity_e.focus()

                self.discount_l = Label(self.left, text="Desconto", font=('arial 18 bold'), fg='black', bg='white')
                self.discount_l.place(x=0, y=390)

                self.discount_e = Entry(self.left, width=25, font=('arial 18 bold'), bg='lightblue')
                self.discount_e.place(x=190, y=390)
                self.discount_e.insert(END, 0)

                self.add_to_cart_btn = Button(self.left, text="Adicionar ao Carrinho", width=22, height=2, bg='steelblue', fg='white', command=self.add_to_cart)
                self.add_to_cart_btn.place(x=350, y=430)

            else:
                tkinter.messagebox.showinfo("Erro", "Produto não encontrado!")

        except Exception as e:
            tkinter.messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

    def add_to_cart(self, *args, **kwargs):
        try:
            self.quantity_value = int(self.quantity_e.get())
            if self.quantity_value > int(self.get_stock):
                tkinter.messagebox.showinfo("Erro", "Quantidade solicitada maior que o estoque")
            else:
                desconto = float(self.discount_e.get())
                self.final_price = (float(self.quantity_value) * float(self.get_price)) - desconto

                self.cart_table.insert("", END, values=(self.get_name, self.quantity_value, f"R$ {self.final_price:.2f}"))

                cart_price.append(self.final_price)
                self.total_l.configure(text="Total: R$ " + f"{sum(cart_price):.2f}")

                self.quantity_l.destroy()
                self.quantity_e.destroy()
                self.discount_l.destroy()
                self.discount_e.destroy()
                self.productname.configure(text="")
                self.pprice.configure(text="")
                self.add_to_cart_btn.destroy()

        except Exception as e:
            tkinter.messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

    def calculate_change(self, *args, **kwargs):
        try:
            total_paid = float(self.total_paid_entry.get())
            total_cart = sum(cart_price)
            if total_paid < total_cart:
                self.change_label.configure(text="Valor pago insuficiente!", fg="red")
            else:
                change = total_paid - total_cart
                self.change_label.configure(text=f"Troco: R$ {change:.2f}", fg="green")
        except ValueError:
            tkinter.messagebox.showerror("Erro", "Digite um valor válido para o total pago.")
         
    def generate_receipt(self, *args, **kwargs):
        total = sum(cart_price)
        self.receipt_area.delete(1.0, END)
        self.receipt_area.insert(END, f"Supermercado Todo Dia\n")
        self.receipt_area.insert(END, f"Data: {date}\n")
        self.receipt_area.insert(END, f"{'-'*60}\n")
        self.receipt_area.insert(END, f"Produto\t\tQtd\tPreço Total\n")
        self.receipt_area.insert(END, f"{'-'*60}\n")

        pdf_data = [["Produto", "Quantidade", "Preço Total"]]

        for item in self.cart_table.get_children():
            produto, quantidade, preco_total = self.cart_table.item(item, "values")
            self.receipt_area.insert(END, f"{produto}\t\t{quantidade}\t{preco_total}\n")
            pdf_data.append([produto, quantidade, preco_total])

        self.receipt_area.insert(END, f"{'-'*60}\n")
        self.receipt_area.insert(END, f"TOTAL: R$ {total:.2f}\n")
        self.receipt_area.insert(END, f"{'-'*60}\n")
        self.receipt_area.insert(END, f"Obrigado e volte sempre!\n")

        # Gerar o recibo em PDF
        pdf_path = os.path.join(os.getcwd(), "recibo.pdf")
        pdf_canvas = canvas.Canvas(pdf_path, pagesize=letter)
        pdf_canvas.setFont("Helvetica", 12)
        y = 750  # Coordenada inicial no eixo Y

        pdf_canvas.drawString(50, y, "Supermercado Tabajara")
        y -= 20
        pdf_canvas.drawString(50, y, f"Data: {date}")
        y -= 20
        pdf_canvas.drawString(50, y, "-" * 60)
        y -= 20

        # Adicionando os itens ao PDF
        for linha in pdf_data:
            linha_texto = f"{linha[0]:<20} {linha[1]:<10} {linha[2]:<10}"
            pdf_canvas.drawString(50, y, linha_texto)
            y -= 20
            if y < 50:  # Evitar ultrapassar o limite da página
                pdf_canvas.showPage()
                pdf_canvas.setFont("Helvetica", 12)
                y = 750

        pdf_canvas.drawString(50, y, "-" * 60)
        y -= 20
        pdf_canvas.drawString(50, y, f"TOTAL: R$ {total:.2f}")
        y -= 20
        pdf_canvas.drawString(50, y, "-" * 60)
        y -= 20
        pdf_canvas.drawString(50, y, "Obrigado e volte sempre!")

        pdf_canvas.save()

        tkinter.messagebox.showinfo("Recibo Gerado", f"Recibo salvo em: {pdf_path}")

if __name__ == "__main__":
    root = Tk()
    cart_price = []
    app = Application(root)
    root.geometry("1366x768+0+0")
    root.mainloop()
