# Documentação para Sistema de Vendas
Este projeto é uma aplicação simples de Sistema de Vendas para um supermercado, desenvolvido</br> com Python utilizando a biblioteca Tkinter para a interface gráfica e SQLite como banco de dados.

### Funcionalidades
1. Pesquisar Produto: Busca produtos no banco de dados pelo ID.</br> 
2. Adicionar ao Carrinho: Permite adicionar produtos ao carrinho com quantidade e desconto.</br> 
3. Calcular Troco: Calcula o troco com base no valor total e no valor pago.</br> 
4. Gerar Recibo: Gera um recibo detalhado, incluindo os produtos, quantidades, preço total e o total pago.</br> 
5. Exibição Dinâmica: Lista os produtos adicionados ao carrinho de forma organizada.</br> </br> 

### Estrutura da Interface
### Lado Esquerdo
- Campo para pesquisar produto pelo ID.
- Exibição do nome do produto e preço unitário.
- Campos para inserir quantidade e desconto.
- Botão para adicionar ao carrinho.
- Campo para total pago e botão para calcular o troco.
- Exibição do troco calculado.</br></br>

### Lado Direito
- Tabela do Carrinho: Lista os produtos adicionados ao carrinho com:
- Nome do produto
- Quantidade
- Preço total
- Área de Recibo: Exibe o recibo gerado com o resumo da compra.</br></br>

### Tecnologias Utilizadas
- Python: Linguagem principal para o desenvolvimento.
- Tkinter: Criação de interface gráfica.
- SQLite: Gerenciamento do banco de dados.</br></br>

### Requisitos de Instalação
1. Python 3.x instalado no sistema.</br>
2. Instalar o pacote SQLite, se ainda não estiver disponível:</br>
**pip install pysqlite3**</br></br>

### Estrutura do Banco de Dados
A tabela inventory é utilizada para armazenar os produtos e deve conter as seguintes colunas:</br>

- id: Identificador único do produto.
- name: Nome do produto.
- stock: Quantidade disponível no estoque.
- price: Preço unitário do produto.</br></br>

### Exemplo de Criação da Tabela
CREATE TABLE inventory (</br>
    id INTEGER PRIMARY KEY AUTOINCREMENT,</br>
    name TEXT NOT NULL,</br>
    stock INTEGER NOT NULL,</br>
    price REAL NOT NULL</br>
);</br></br>

### Inserção de Produtos
INSERT INTO inventory (name, stock, price) VALUES ('Banana', 50, 2.50);</br>
INSERT INTO inventory (name, stock, price) VALUES ('Maçã', 30, 3.00);</br>
INSERT INTO inventory (name, stock, price) VALUES ('Arroz', 20, 10.00);</br></br>

### Como Usar
### 1. Clonar o Repositório
git clone https://github.com/seu-usuario/sistema-vendas.git
cd sistema-vendas</br></br>

### 2. Executar o Projeto
Certifique-se de que o arquivo do banco de dados (store.db) está na pasta especificada no código.</br>
Em seguida, execute:
**python sistema_vendas.py**

### Capturas de Tela
### Tela Inicial Menu
<img src="Sistema_de_Vendas\imagens\tela02.png" width="500" height="300"></br></br>

### Carrinho e Recibo
<img src="Sistema_de_Vendas\imagens\tela01.png" width="500" height="300"></br></br>

### Cadastro de Produto
<img src="Sistema_de_Vendas\imagens\tela03.png" width="500" height="300"></br></br>





