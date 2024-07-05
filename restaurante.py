import queue

# Cria a classe produto
class Produto:
    # Construtor
    def __init__(self, nome, preco):
        self._nome = nome
        self._preco = preco

    # Getters e setters
    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, nome):
        self._nome = nome

    @property
    def preco(self):
        return self._preco

    @preco.setter
    def preco(self, preco):
        self._preco = preco

    # Descrição
    def descricao(self):
        return f"{self.nome}, Preço: R${self.preco:.2f}"

# Cria a classe cardápio
class Cardapio:
    # Construtor
    def __init__(self):
        self._produtos = []

    # Getter e setter
    @property
    def produtos(self):
        return self._produtos

    @produtos.setter
    def produtos(self, produtos):
        self._produtos = produtos

    # Método para adicionar produtos ao cardápio
    def adicionar_produto(self, produto):
        self.produtos.append(produto)

    # Método para remover produtos do cardápio
    def remover_produto(self, nome_produto):
        self.produtos = [produto for produto in self.produtos if produto.nome != nome_produto]

    # Método para listar os produtos do cardápio
    def listar_produtos(self):
        for produto in self.produtos:
            print(produto.descricao())


# Cria a classe pedido
class Pedido:
    #Cria lista de estados dos pedidos
    ESTADOS = ['PEDIDO', 'EM PREPARAÇÃO', 'ENTREGUE']

    # Construtor
    def __init__(self, id_pedido, produtos):
        self.id_pedido = id_pedido
        self.produtos = produtos  # Lista de produtos
        self.estado_atual = 0  # Índice do estado inicial 'Pedido'

    # Getters e setters
    @property
    def id_pedido(self):
        return self._id_pedido

    @property
    def produtos(self):
        return self._produtos

    @property
    def estado_atual(self):
        return self._estado_atual

    @id_pedido.setter
    def id_pedido(self, id_pedido):
        self._id_pedido = id_pedido

    @produtos.setter
    def produtos(self, produtos):
        self._produtos = produtos

    @estado_atual.setter
    def estado_atual(self, estado_atual):
        self._estado_atual = estado_atual

    # Método para avançar estado dos pedidos
    def avancar_estado(self):
        if self.estado_atual < len(self.ESTADOS) - 1:
            self.estado_atual += 1

    # Método para obter o estado dos pedidos
    def obter_estado(self):
        return self.ESTADOS[self.estado_atual]

    # Método para calcular o valor total do pedido
    def calcular_valor_total(self):
        return sum(produto.preco for produto in self.produtos)

    # Cria descrição do pedido
    def descricao(self):
        produtos_descricao = ", ".join(produto.descricao() for produto in self.produtos)
        return f"{self.obter_estado()} - Nro {self.id_pedido}: {produtos_descricao} - Total: R${self.calcular_valor_total():.2f}"


# Cria a classe relatório de vendas
class RelatorioDeVendas:
    # Construtor
    def __init__(self):
        self._produtos_vendidos = {}

    # Getter e setter
    @property
    def produtos_vendidos(self):
        return self._produtos_vendidos

    @produtos_vendidos.setter
    def produtos_vendidos(self, produtos_vendidos):
        self._produtos_vendidos = produtos_vendidos

    # Registrar venda
    def registrar_venda(self, pedido):
        for produto in pedido.produtos:
            if produto.nome in self.produtos_vendidos:
                self.produtos_vendidos[produto.nome]['quantidade'] += 1
                self.produtos_vendidos[produto.nome]['faturamento'] += produto.preco
            else:
                self.produtos_vendidos[produto.nome] = {
                    'quantidade': 1,
                    'faturamento': produto.preco
                }

    # Calcula a quantidade vendida de cada item
    def quantidade_vendida_total(self):
        print("\nQuantidade vendida de cada produto:")
        for nome, dados in self.produtos_vendidos.items():
            print(f"{nome}: {dados['quantidade']} unidades")

    # Calcula o faturamento total
    def faturamento_total(self):
        total = sum(dados['faturamento'] for dados in self.produtos_vendidos.values())
        print(f"\nFaturamento total do estabelecimento: R${total:.2f}")


# Cria a classe do gerenciador de pedidos
class GerenciadorDePedidos:
    # Construtor
    def __init__(self):
        self.fila_pedido = queue.Queue()
        self.fila_preparacao = queue.Queue()
        self.fila_entregue = queue.Queue()
        self.contador_pedidos = 0
        self.relatorio_de_vendas = RelatorioDeVendas()

    # Getters e setters
    @property
    def fila_pedido(self):
        return self._fila_pedido

    @property
    def fila_preparacao(self):
        return self._fila_preparacao

    @property
    def fila_entregue(self):
        return self._fila_entregue

    @property
    def contador_pedidos(self):
        return self._contador_pedidos

    @property
    def relatorio_de_vendas(self):
        return self._relatorio_de_vendas

    @fila_pedido.setter
    def fila_pedido(self, fila_pedido):
        self._fila_pedido = fila_pedido

    @fila_preparacao.setter
    def fila_preparacao(self, fila_preparacao):
        self._fila_preparacao = fila_preparacao

    @fila_entregue.setter
    def fila_entregue(self, fila_entregue):
        self._fila_entregue = fila_entregue

    @contador_pedidos.setter
    def contador_pedidos(self, contador_pedidos):
        self._contador_pedidos = contador_pedidos

    @relatorio_de_vendas.setter
    def relatorio_de_vendas(self, relatorio_de_vendas):
        self._relatorio_de_vendas = relatorio_de_vendas

    # Método para adicionar um novo pedido à fila inicial
    def adicionar_pedido(self, pedido):
        pedido.estado_atual = 0
        self.fila_pedido.put(pedido)

    # Método para setar o status do pedido como "EM PRODUÇÃO" e passar para a fila de pedidos em produção
    def colocar_em_producao(self):
        if not self.fila_pedido.empty():
            pedido = self.fila_pedido.get()
            pedido.avancar_estado()
            self.fila_preparacao.put(pedido)

    # Método para setar o status do pedido como "ENTREGUE" e passar para a fila de pedidos entregues
    def entregar(self):
        if not self.fila_preparacao.empty():
            pedido = self.fila_preparacao.get()
            pedido.avancar_estado()
            self.fila_entregue.put(pedido)
            self.relatorio_de_vendas.registrar_venda(pedido)

    # Listar pedidos de cada uma das filas
    def listar_pedidos(self):
        print("Pedidos:")
        pedidos = list(self.fila_pedido.queue)
        for pedido in pedidos:
            print(pedido.descricao())

        print("\nEm preparação:")
        preparacao = list(self.fila_preparacao.queue)
        for pedido in preparacao:
            print(pedido.descricao())

        print("\nEntregues:")
        entregues = list(self.fila_entregue.queue)
        for pedido in entregues:
            print(pedido.descricao())

    # Métodos dos relatórios
    def quantidade_vendida_total(self):
        self.relatorio_de_vendas.quantidade_vendida_total()

    def faturamento_total(self):
        self.relatorio_de_vendas.faturamento_total()
