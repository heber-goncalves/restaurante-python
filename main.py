import sys
# Importa as bibliotecas de widgets do PySide6
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QLineEdit, QListWidget, QLabel, QWidget
# Importa classes do arquivo restaurante.py
from restaurante import Produto, Cardapio, Pedido, GerenciadorDePedidos
# Importa o tema escuro
from qdarktheme import load_stylesheet


# Classe da janela
class MainWindow(QMainWindow):
    # Construtor
    def __init__(self):
        super().__init__()
        # Titulo e tamanho inicial da janela
        self.setWindowTitle("Gerenciador de Pedidos")
        self.setGeometry(100, 100, 800, 600)

        # Cria cardápio e gerenciador
        self.cardapio = Cardapio()
        self.gerenciador = GerenciadorDePedidos()

        # Cria listas
        self.lista_produtos = QListWidget()
        self.lista_pedidos = QListWidget()

        # Cria layout verticalizado e adiciona a lista de produtos criada
        layout = QVBoxLayout()
        layout.addWidget(self.lista_produtos)

        # Cria o input de produtos para a criação de pedidos com um label e adiciona ao layout
        self.input_pedido = QLineEdit(self)
        self.input_pedido.setPlaceholderText("Digite os índices dos produtos separados por espaço")
        layout.addWidget(self.input_pedido)

        # Cria botões, conecta eles com seus respectivos métodos e os adiciona ao layout
        botao_novo_pedido = QPushButton("Fazer novo pedido", self)
        botao_novo_pedido.clicked.connect(self.fazer_novo_pedido)
        layout.addWidget(botao_novo_pedido)

        layout.addWidget(self.lista_pedidos)

        botao_producao = QPushButton("Colocar em produção", self)
        botao_producao.clicked.connect(self.colocar_em_producao)
        layout.addWidget(botao_producao)

        botao_entregar = QPushButton("Entregar pedido", self)
        botao_entregar.clicked.connect(self.entregar)
        layout.addWidget(botao_entregar)

        # Botão para emitir os relatórios
        botao_relatorios = QPushButton("Emitir relatórios", self)
        botao_relatorios.clicked.connect(self.exibir_quantidade_vendida)
        botao_relatorios.clicked.connect(self.exibir_faturamento_total)
        layout.addWidget(botao_relatorios)

        # Cria exibição dos relatórios
        self.label_quantidade_vendida = QLabel("Quantidade vendida de cada produto:", self)
        layout.addWidget(self.label_quantidade_vendida)

        self.label_faturamento_total = QLabel("Faturamento total do estabelecimento:", self)
        layout.addWidget(self.label_faturamento_total)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    # Método para criar novos pedidos a partir dos produtos inseridos no input
    def fazer_novo_pedido(self):
        indices_produtos = self.input_pedido.text().split(" ")
        produtos = []

        for indice in indices_produtos:
            try:
                indice = int(indice.strip()) - 1
                if 0 <= indice < len(self.cardapio.produtos):
                    produto = self.cardapio.produtos[indice]
                    produtos.append(produto)
            except ValueError:
                continue

        if produtos:
            novo_pedido = Pedido(self.gerenciador.contador_pedidos + 1, produtos)
            self.gerenciador.contador_pedidos += 1
            self.gerenciador.adicionar_pedido(novo_pedido)
            self.lista_pedidos.addItem(novo_pedido.descricao())
            self.input_pedido.clear()

    # Método para alterar o status de um pedido para PRODUÇÃO
    def colocar_em_producao(self):
        self.gerenciador.colocar_em_producao()
        self.atualizar_lista_pedidos()

    # Método para alterar o status de um pedido para ENTREGUE
    def entregar(self):
        self.gerenciador.entregar()
        self.atualizar_lista_pedidos()

    # Médodo para atualizar a lista de pedidos
    def atualizar_lista_pedidos(self):
        self.lista_pedidos.clear()
        for pedido in list(self.gerenciador.fila_pedido.queue) + list(self.gerenciador.fila_preparacao.queue) + list(
                self.gerenciador.fila_entregue.queue):
            self.lista_pedidos.addItem(pedido.descricao())

    # Método para exibir o relatório de quantidades vendidas
    def exibir_quantidade_vendida(self):
        detalhes = "\nQuantidade vendida de cada produto:\n"
        for nome, dados in self.gerenciador.relatorio_de_vendas.produtos_vendidos.items():
            detalhes += f"{nome}: {dados['quantidade']} unidades\n"
        self.label_quantidade_vendida.setText(detalhes)

    # Método para exibir o relatório de faturamento total dos pedidos já finalizados
    def exibir_faturamento_total(self):
        total = sum(dados['faturamento'] for _, dados in self.gerenciador.relatorio_de_vendas.produtos_vendidos.items())
        self.label_faturamento_total.setText(f"Faturamento total do estabelecimento: R${total:.2f}")


# Run
if __name__ == "__main__":
    # Cria o app
    app = QApplication(sys.argv)
    # Seta tema
    app.setStyleSheet(load_stylesheet())
    # Cria janela instanciando um objeto da classe criada acima
    window = MainWindow()

    # Adiciona produtos ao cardápio
    produtos = [
        ("Prato pronto", 25.00),
        ("Prato kids", 20.00),
        ("Vegetariano", 22.00),
        ("Vegetariano kids", 18.00),
        ("Suco 250ml", 8.00),
        ("Refrigerante 340ml", 8.00),
        ("Água 500ml", 4.00)
    ]

    # Adiciona índices aos produtos
    for index, (nome, preco) in enumerate(produtos, start=1):
        produto = Produto(nome, preco)
        window.cardapio.adicionar_produto(produto)
        window.lista_produtos.addItem(f"{index}. {produto.descricao()}")

    # Exibe janela
    window.show()
    sys.exit(app.exec())
