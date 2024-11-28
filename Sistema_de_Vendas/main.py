from tkinter import *
from tkinter import ttk
import sqlite3
import tkinter.messagebox
import datetime

# Obtenha a data atual e formate-a
date = datetime.datetime.now().strftime("%d/%m/%Y")

# Conexão com o banco de dados
conn = sqlite3.connect(r'C:\Users\marce\OneDrive\Área de Trabalho\SistemaDeVendasPython\Sistema_de_Vendas\Database\store.db')
c = conn.cursor()

class Application:
    def __init__(self, master, *args, **kwargs):
        self.master = master

        self.left = Frame(master, width=700, height=760, bg='white')
        self.left.pack(side=LEFT)

        self.right = Frame(master, width=666, height=768, bg='lightblue')
        self.right.pack(side=RIGHT)

        # Componentes do lado esquerdo
        self.heading = Label(self.left, text="Supermercado Tabajara:", font=('arial 40 bold'), fg='steelblue', bg='white')
        self.heading.place(x=0, y=0)

        # Atualize o Label para exibir a data formatada
        self.date_l = Label(self.right, text="Data: " + date, font=('arial 16 bold'), fg='white', bg='lightblue')
        self.date_l.place(x=0, y=0)

        self.enterid = Label(self.left, text="ID do Produto:", font=('arial 18 bold'), fg='black', bg='white')
        self.enterid.place(x=0, y=80)

        self.enteride = Entry(self.left, width=25, font=('arial 18 bold'), bg='lightblue')
        self.enteride.place(x=190, y=80)

        self.search_btn = Button(self.left, text="Pesquisar", width=22, height=2, bg='steelblue', fg='white', command=self.jx)
        self.search_btn.place(x=350, y=120)

        self.productname = Label(self.left, text="", font=('arial 18 bold'), fg='black', bg='white')
        self.productname.place(x=0, y=200)

        self.pprice = Label(self.left, text="", font=('arial 18 bold'), fg='black', bg='white')
        self.pprice.place(x=0, y=250)

        # Total label
        self.total_l = Label(self.right, text="Total: R$ 0.00", font=('arial 27 bold'), fg='black', bg='lightblue')
        self.total_l.place(x=0, y=450)

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

        # Tabela (Treeview) para exibir produtos no carrinho
        self.cart_table = ttk.Treeview(self.right, columns=("Produto", "Quantidade", "Preço Total"), show='headings', height=15)
        self.cart_table.heading("Produto", text="Produto")
        self.cart_table.heading("Quantidade", text="Quantidade")
        self.cart_table.heading("Preço Total", text="Preço Total")
        self.cart_table.column("Produto", anchor=CENTER, width=150)
        self.cart_table.column("Quantidade", anchor=CENTER, width=100)
        self.cart_table.column("Preço Total", anchor=CENTER, width=120)
        self.cart_table.place(x=0, y=50)

        # Área para exibição do recibo
        self.receipt_area = Text(self.right, width=40, height=10, font=('arial', 12), bg='white', fg='black')
        self.receipt_area.place(x=0, y=500)

    def jx(self, *args, **kwargs):
        try:
            self.get_id = self.enteride.get()
            query = "SELECT * FROM inventory WHERE id=?"
            result = c.execute(query, (self.get_id,))
            record = result.fetchone()  # Obtém apenas o primeiro registro encontrado

            if record:
                # Ajuste o desempacotamento conforme a estrutura da tabela
                self.get_id = record[0]  # Supondo que a primeira coluna seja o ID
                self.get_name = record[1]  # Supondo que a segunda coluna seja o nome
                self.get_stock = record[2]  # Supondo que a terceira coluna seja o estoque
                self.get_price = record[3]  # Supondo que a quarta coluna seja o preço

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

    # Método para adicionar produtos ao carrinho
    def add_to_cart(self, *args, **kwargs):
        try:
            self.quantity_value = int(self.quantity_e.get())
            if self.quantity_value > int(self.get_stock):
                tkinter.messagebox.showinfo("Erro", "Quantidade solicitada maior que o estoque")
            else:
                desconto = float(self.discount_e.get())
                self.final_price = (float(self.quantity_value) * float(self.get_price)) - desconto

                # Adicionar os dados à tabela
                self.cart_table.insert("", END, values=(self.get_name, self.quantity_value, f"R$ {self.final_price:.2f}"))

                # Atualizar o total
                cart_price.append(self.final_price)
                self.total_l.configure(text="Total: R$ " + f"{sum(cart_price):.2f}")

                # Resetar campos
                self.quantity_l.destroy()
                self.quantity_e.destroy()
                self.discount_l.destroy()
                self.discount_e.destroy()
                self.productname.configure(text="")
                self.pprice.configure(text="")
                self.add_to_cart_btn.destroy()

        except Exception as e:
            tkinter.messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

    # Método para calcular o troco
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
         
         # Método para gerar o recibo
    def generate_receipt(self, *args, **kwargs):
        total = sum(cart_price)
        self.receipt_area.delete(1.0, END)
        self.receipt_area.insert(END, f"Supermercado Tabajara\n")
        self.receipt_area.insert(END, f"Data: {date}\n")
        self.receipt_area.insert(END, f"{'-'*40}\n")
        self.receipt_area.insert(END, f"Produto\t\tQtd\tPreço Total\n")
        self.receipt_area.insert(END, f"{'-'*40}\n")

        for item in self.cart_table.get_children():
            produto, quantidade, preco_total = self.cart_table.item(item, "values")
            self.receipt_area.insert(END, f"{produto}\t{quantidade}\t{preco_total}\n")

        self.receipt_area.insert(END, f"{'-'*40}\n")
        self.receipt_area.insert(END, f"TOTAL: R$ {total:.2f}\n")
        self.receipt_area.insert(END, f"{'-'*40}\n")
        self.receipt_area.insert(END, f"Obrigado e volte sempre!\n")

# Inicialização da interface Tkinter
root = Tk()
cart_price = []  # Lista para guardar os preços dos produtos no carrinho
b = Application(root)

root.geometry("1366x768+0+0")
root.title("Supermercado")
root.mainloop()
