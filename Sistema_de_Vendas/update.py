from tkinter import *
import sqlite3
import locale

# Configuração do locale para o Brasil
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

# Conexão com o banco de dados
conn = sqlite3.connect(r'C:\Users\marce\OneDrive\Área de Trabalho\SistemaDeVendasPython\Sistema_de_Vendas\Database\store.db')
c = conn.cursor()


class UpdateProduct:
    def __init__(self, master, *args, **kwargs):
        self.master = master
        self.heading = Label(master, text="Atualizar Produto", font=('arial 30 bold'), fg='steelblue')
        self.heading.place(x=400, y=0)

        # Campo para buscar o produto
        self.search_label = Label(master, text="ID do Produto:", font=('arial 18 bold'))
        self.search_label.place(x=250, y=70)  # Ajuste para centralizar o rótulo

        self.search_entry = Entry(master, width=15, font=('arial 18 bold'))  # Reduzido o width
        self.search_entry.place(x=450, y=70)  # Ajuste para centralizar o campo

        self.search_btn = Button(master, text="Buscar", width=10, height=1, bg='orange', fg='white', command=self.search_product)
        self.search_btn.place(x=700, y=70)  # Ajuste para centralizar o botão

        # Labels e campos para edição
        labels = [
            "Nome do produto:",
            "Estoque:",
            "Preço de Custo:",
            "Preço de Venda:",
            "Fornecedor:",
            "Telefone do Fornecedor:"
        ]
        self.entries = []

        for i, label in enumerate(labels):
            lbl = Label(master, text=label, font=('arial 18 bold'))
            lbl.place(x=0, y=150 + (i * 50))
            entry = Entry(master, width=25, font=('arial 18 bold'))
            entry.place(x=380, y=150 + (i * 50))
            self.entries.append(entry)

        # Botão para atualizar
        self.update_btn = Button(master, text="Atualizar Produto", width=25, height=2, bg='steelblue', fg='white', command=self.update_product)
        self.update_btn.place(x=520, y=550)

        # Caixa de mensagens
        self.tBox = Text(master, width=60, height=18)
        self.tBox.place(x=750, y=150)

    def search_product(self):
        """Busca o produto pelo ID informado."""
        try:
            product_id = self.search_entry.get()
            if not product_id.isdigit():
                self.tBox.insert(END, "\nErro: ID do produto deve ser um número válido.\n")
                return

            # Consultar o banco de dados
            c.execute("SELECT * FROM inventory WHERE id = ?", (product_id,))
            product = c.fetchone()

            if not product:
                self.tBox.insert(END, f"\nProduto com ID {product_id} não encontrado.\n")
                return

            # Preencher os campos com os dados do produto
            self.entries[0].delete(0, END)  # Nome do Produto
            self.entries[0].insert(0, str(product[1]))  # Índice 1 = name

            self.entries[1].delete(0, END)  # Estoque
            self.entries[1].insert(0, str(product[2]))  # Índice 2 = stock

            self.entries[2].delete(0, END)  # Preço de Custo
            self.entries[2].insert(0, str(product[3]))  # Índice 3 = cp (Preço de custo)

            self.entries[3].delete(0, END)  # Preço de Venda
            self.entries[3].insert(0, str(product[4]))  # Índice 4 = sp (Preço de venda)

            self.entries[4].delete(0, END)  # Fornecedor
            self.entries[4].insert(0, str(product[8]))  # Índice 8 = vendor (Fornecedor)

            self.entries[5].delete(0, END)  # Telefone do Fornecedor
            self.entries[5].insert(0, str(product[9]))  # Índice 9 = vendor_ph (Telefone do fornecedor)

            self.tBox.insert(END, f"\nProduto com ID {product_id} carregado para edição.\n")

        except Exception as e:
            self.tBox.insert(END, f"\nErro ao buscar o produto: {str(e)}\n")

    def update_product(self):
        """Atualiza os dados do produto no banco de dados."""
        try:
            product_id = self.search_entry.get()
            if not product_id.isdigit():
                self.tBox.insert(END, "\nErro: ID do produto deve ser um número válido.\n")
                return

            # Obter valores dos campos
            name = self.entries[0].get()
            stock = self.entries[1].get()
            cp = self.entries[2].get()
            sp = self.entries[3].get()
            vendor = self.entries[4].get()
            vendor_phone = self.entries[5].get()

            # Validações
            if not all([name, stock, cp, sp, vendor, vendor_phone]):
                self.tBox.insert(END, "\nErro: Preencha todos os campos para atualizar o produto.\n")
                return

            stock = int(stock)
            cp = locale.atof(cp)  # Converte preço de custo (formato brasileiro) para float
            sp = locale.atof(sp)  # Converte preço de venda (formato brasileiro) para float

            # Atualizar no banco de dados
            c.execute("""
                UPDATE inventory
                SET name = ?, stock = ?, cp = ?, sp = ?, vendor = ?, vendor_ph = ?
                WHERE id = ?
            """, (name, stock, cp, sp, vendor, vendor_phone, product_id))
            conn.commit()

            self.tBox.insert(END, f"\nProduto com ID {product_id} atualizado com sucesso.\n")
            self.clear_all()

        except Exception as e:
            self.tBox.insert(END, f"\nErro ao atualizar o produto: {str(e)}\n")

    def clear_all(self):
        """Limpa todos os campos de entrada."""
        for entry in self.entries:
            entry.delete(0, END)
        self.search_entry.delete(0, END)


# Inicialização da interface Tkinter
root = Tk()
app = UpdateProduct(root)

root.geometry("1366x768+0+0")
root.title("Atualizar Produtos")
root.mainloop()
