# Importa o módulo textwrap, usado para manipular textos (como remover indentação).
import textwrap  

# Importa classes da biblioteca padrão abc (Abstract Base Classes), 
# para criar classes e métodos abstratos.
from abc import ABC, abstractmethod  

# Importa datetime para registrar data e hora das transações.
from datetime import datetime  


# Classe abstrata que define o contrato para qualquer transação.
class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @classmethod
    @abstractmethod
    def registrar(self, conta):
        pass


# Classe base que representa um cliente genérico do banco.
class Cliente:
    # Construtor: inicializa o endereço e uma lista de contas.
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    # Método que realiza uma transação chamando o método registrar.
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    # Método para adicionar uma nova conta ao cliente.
    def adicionar_conta(self, conta):
        self.contas.append(conta)


# Classe que herda de Cliente e representa uma pessoa física.
class PessoaFisica(Cliente):
    # Construtor: inicializa atributos específicos de pessoa física.
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


# Classe que representa uma conta bancária genérica.
class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0                     # Saldo da conta.
        self._numero = numero               # Número da conta.
        self._agencia = "0001"              # Código fixo da agência.
        self._cliente = cliente             # Cliente dono da conta.
        self._historico = Historico()       # Histórico de transações.

    # Método de classe para criar uma nova conta.
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    # Propriedades (getters) para acessar dados protegidos.
    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    # Método para sacar dinheiro.
    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        # Verifica se há saldo suficiente.
        if excedeu_saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

        # Se o valor for positivo e dentro do limite, realiza o saque.
        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True

        # Caso o valor seja inválido.
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

        return False

    # Método para depositar dinheiro.
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False

        return True


# Classe que representa uma conta corrente, com limites específicos.
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite               # Limite de valor por saque.
        self._limite_saques = limite_saques # Limite de número de saques.

    # Sobrescreve o método sacar, adicionando regras extras.
    def sacar(self, valor):
        # Conta quantos saques já foram feitos.
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        # Verifica limites.
        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")

        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

        else:
            return super().sacar(valor)

        return False

    # Representação em string da conta.
    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """


# Classe que registra o histórico de transações da conta.
class Historico:
    def __init__(self):
        self._transacoes = []  # Lista de dicionários com as transações.

    @property
    def transacoes(self):
        return self._transacoes

    # Adiciona uma transação ao histórico com tipo, valor e data.
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s"),
            }
        )


# Classe que representa uma operação de saque.
class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


# Classe que representa uma operação de depósito.
class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


# Valida um CPF conforme o algoritmo da Receita Federal.
# Remove caracteres não numéricos e confere os dígitos verificadores.
def validar_cpf(cpf: str) -> bool:
    cpf = ''.join(filter(str.isdigit, cpf))  # mantém apenas números

    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digito1 = (soma * 10 % 11) % 10

    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digito2 = (soma * 10 % 11) % 10

    return cpf[-2:] == f"{digito1}{digito2}"


# Exibe o menu principal e retorna a opção digitada pelo usuário.
def menu():
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [nu]\tNovo usuário
    [lc]\tListar contas
    [lu]\tListar usuários
    [lcu]\tListar contas por usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))


# Busca um cliente pelo CPF.
def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


# Retorna a conta do cliente (a primeira da lista).
def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return

    # FIXME: não permite cliente escolher a conta.
    return cliente.contas[0]


# Função para realizar depósito.
def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


# Função para realizar saque.
def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


# Exibe o extrato de transações e saldo da conta.
def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")


# Cria um novo cliente pessoa física.
def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\n@@@ Já existe cliente com esse CPF! @@@")
        return
    
    if not validar_cpf(cpf):
        print("\n@@@ CPF inválido! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    clientes.append(cliente)

    print("\n=== Cliente criado com sucesso! ===")


# Cria uma nova conta para um cliente existente.
def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado! @@@")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("\n=== Conta criada com sucesso! ===")


# Lista todas as contas cadastradas.
def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))


# Lista todos os usuários cadastrados no sistema.
def listar_usuarios(clientes):
    if not clientes:
        print("\n@@@ Nenhum cliente cadastrado! @@@")
        return

    print("\n=== Lista de Usuários Cadastrados ===")
    for cliente in clientes:
        print("=" * 100)
        print(f"Nome:\t\t{cliente.nome}")
        print(f"CPF:\t\t{cliente.cpf}")
        print(f"Nascimento:\t{cliente.data_nascimento}")
        print(f"Endereço:\t{cliente.endereco}")


# Lista todas as contas vinculadas a um cliente específico.
def listar_contas_por_usuario(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    if not cliente.contas:
        print(f"\n@@@ O cliente {cliente.nome} não possui contas cadastradas. @@@")
        return

    print(f"\n=== Contas do cliente: {cliente.nome} ===")
    for conta in cliente.contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))


# Função principal que controla o fluxo do programa.
def main():
    clientes = []  # Lista de clientes.
    contas = []    # Lista de contas.

    while True:
        opcao = menu()

        if opcao == "d":
            depositar(clientes)

        elif opcao == "s":
            sacar(clientes)

        elif opcao == "e":
            exibir_extrato(clientes)

        elif opcao == "nu":
            criar_cliente(clientes)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "lcu":
            listar_contas_por_usuario(clientes)

        elif opcao == "lu":
            listar_usuarios(clientes)

        elif opcao == "q":
            break

        else:
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")


# Chama a função principal para iniciar o programa.
main()
