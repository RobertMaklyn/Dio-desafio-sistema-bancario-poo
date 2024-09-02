from abc import ABC, abstractmethod
from datetime import datetime


class ClienteBase:
    def __init__(self, local_residencia):
        self.local_residencia = local_residencia
        self.lista_contas = []

    def efetuar_transacao(self, conta, tipo_transacao):
        tipo_transacao.executar(conta)

    def adicionar_nova_conta(self, conta):
        self.lista_contas.append(conta)


class Pessoa(ClienteBase):
    def __init__(self, nome_completo, nascimento, cpf, local_residencia):
        super().__init__(local_residencia)
        self.nome_completo = nome_completo
        self.nascimento = nascimento
        self.cpf = cpf


class ContaBancaria:
    def __init__(self, numero_conta, cliente):
        self.__saldo = 0.0
        self.__numero_conta = numero_conta
        self.__codigo_agencia = "0001"
        self.__cliente = cliente
        self.__registro_historico = Historico()

    @classmethod
    def criar_nova_conta(cls, cliente, numero_conta):
        return cls(numero_conta, cliente)

    @property
    def saldo(self):
        return self.__saldo

    @property
    def numero_conta(self):
        return self.__numero_conta

    @property
    def codigo_agencia(self):
        return self.__codigo_agencia

    @property
    def cliente(self):
        return self.__cliente

    @property
    def registro_historico(self):
        return self.__registro_historico

    def efetuar_saque(self, valor):
        if valor <= 0:
            print("\n-- Erro: Valor de saque não permitido. --")
            return False

        if valor > self.__saldo:
            print("\n-- Erro: Saldo indisponível. --")
            return False

        self.__saldo -= valor
        print("\n-- Saque realizado com sucesso! --")
        return True

    def efetuar_deposito(self, valor):
        if valor <= 0:
            print("\n-- Erro: Valor de depósito não permitido. --")
            return False

        self.__saldo += valor
        print("\n-- Depósito realizado com sucesso! --")
        return True


class ContaCorrente(ContaBancaria):
    def __init__(self, numero_conta, cliente, limite_diario=500, max_saques=3):
        super().__init__(numero_conta, cliente)
        self.__limite_diario = limite_diario
        self.__max_saques = max_saques
        self.__total_saques = 0

    def efetuar_saque(self, valor):
        if self.__total_saques >= self.__max_saques:
            print("\n-- Erro: Número máximo de saques atingido. --")
            return False

        if valor > self.__limite_diario:
            print("\n-- Erro: Valor do saque excede o limite diário. --")
            return False

        if super().efetuar_saque(valor):
            self.__total_saques += 1
            return True

        return False

    def __str__(self):
        return f"""\
        Agência: {self.codigo_agencia}
        Número da Conta: {self.numero_conta}
        Titular: {self.cliente.nome_completo}\
        """


class Historico:
    def __init__(self):
        self.__lista_transacoes = []

    @property
    def transacoes(self):
        return self.__lista_transacoes

    def adicionar_transacao(self, transacao):
        self.__lista_transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        })


class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def executar(self, conta):
        pass


class OperacaoSaque(Transacao):
    def __init__(self, valor):
        self.__valor = valor

    @property
    def valor(self):
        return self.__valor

    def executar(self, conta):
        if conta.efetuar_saque(self.__valor):
            conta.registro_historico.adicionar_transacao(self)


class OperacaoDeposito(Transacao):
    def __init__(self, valor):
        self.__valor = valor

    @property
    def valor(self):
        return self.__valor

    def executar(self, conta):
        if conta.efetuar_deposito(self.__valor):
            conta.registro_historico.adicionar_transacao(self)
