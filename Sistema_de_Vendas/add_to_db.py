from tkinter import *
import sqlite3
import locale

# Configuração do locale para o Brasil
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

# Conexão com o banco de dados
conn = sqlite3.connect(r'C:\Users\marce\OneDrive\Área de Trabalho\SistemaDeVendasPython\Sistema_de_Vendas\Database\store.db')
c = conn.cursor()

# Consultar o maior ID na tabela
result = c.execute("SELECT MAX(id) FROM inventory")
for r in result:
    id = r[0] or 0  # Caso a tabela esteja vazia, id será None, então definimos como 0


class Database:
    def __init__(self, master, *args, **kwargs):
        self.master = master
        self.heading = Label(master, text="Cadastro de Produtos", font=('arial 40 bold'), fg='steelblue')
        self.heading.place(x=400, y=0)

        # Rótulos e Entradas para o formulário
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
            lbl.place(x=0, y=70 + (i * 50))
            entry = Entry(master, width=25, font=('arial 18 bold'))
            entry.place(x=380, y=70 + (i * 50))
            self.entries.append(entry)

        # Botões
        self.btn_add = Button(master, text="Cadastrar Produto", width=25, height=2, bg='steelblue', fg='white', command=self.get_items)
        self.btn_add.place(x=520, y=570)

        self.btn_clear = Button(master, text="Limpar Campos", width=18, height=2, bg='green', fg='white', command=self.clear_all)
        self.btn_clear.place(x=350, y=570)

        # Text Box
        self.tBox = Text(master, width=60, height=18)
        self.tBox.place(x=750, y=70)

    def get_items(self, *args, **kwargs):
        try:
            # Obter valores dos campos
            name = self.entries[0].get()
            stock = self.entries[1].get()
            cp = self.entries[2].get()
            sp = self.entries[3].get()
            vendor = self.entries[4].get()
            vendor_phone = self.entries[5].get()

            # Validações
            if not all([name, stock, cp, sp, vendor, vendor_phone]):
                self.tBox.insert(END, "\nPor favor, preencha todos os campos.")
                return

            stock = int(stock)
            cp = locale.atof(cp)  # Converte preço de custo (formato brasileiro) para float
            sp = locale.atof(sp)  # Converte preço de venda (formato brasileiro) para float

            totalcp = cp * stock
            totalsp = sp * stock
            profit = totalsp - totalcp

            # Inserir no banco de dados
            sql = "INSERT INTO inventory (name, stock, cp, sp, totalcp, totalsp, profit, vendor, vendor_ph) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
            c.execute(sql, (name, stock, cp, sp, totalcp, totalsp, profit, vendor, vendor_phone))
            conn.commit()

            # Formatar valores para exibir no formato brasileiro
            totalcp_brl = locale.currency(totalcp, grouping=True)
            totalsp_brl = locale.currency(totalsp, grouping=True)
            profit_brl = locale.currency(profit, grouping=True)

            self.tBox.insert(END, f"\nProduto '{name}' adicionado com sucesso!")
            self.tBox.insert(END, f"\nCusto Total: {totalcp_brl}, Preço Total: {totalsp_brl}, Lucro: {profit_brl}")
            self.clear_all()

        except ValueError:
            self.tBox.insert(END, "\nErro: Certifique-se de que a quantidade, preço de custo e preço de venda sejam números válidos.")

    def clear_all(self, *args, **kwargs):
        for entry in self.entries:
            entry.delete(0, END)


# Inicialização da interface Tkinter
root = Tk()
b = Database(root)

root.geometry("1366x768+0+0")
root.title("Adicionar ao Banco de Dados")
root.mainloop()
