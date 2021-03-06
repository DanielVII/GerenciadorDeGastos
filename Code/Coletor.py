from decimal import Decimal, InvalidOperation

from excecoes import ObjetoInvalido, DataInvalida, QuantidadeInvalida, ValorInvalido, RespostaInvalida

from datetime import datetime


class ColetarInfoGastos:

    def __init__(self):

        self.__valor = Decimal()
        self.__objeto = str()
        self.__quantidade = str()
        self.__ano = int()
        self.__mes = int()
        self.__dia = int()

    def coletar_valor(self):
        try:
            self.__valor = Decimal(input("Valor do objeto "
                                         "(use o ponto (.) para separar os centavos e apenas duas casas decimais): "))
        except InvalidOperation:
            self.__erro_valor_invalido()

        self.__checar_valor_dado()

    def coletar_objeto(self):
        self.__objeto = input("Nome do produto: ").strip().lower()
        self.__checar_objeto_dado()

    def coletar_quantidade(self):
        self.__quantidade = input("Quantidade da compra (apenas números inteiros): ").strip()
        self.__checar_quantidade_dada()

    def confirmar_se_foi_hoje(self):

        comprou_hoje = input("A compra foi realizada hoje, sim ou não (S/N): ").strip().lower()

        if comprou_hoje == "s":
            self.__ano = int(datetime.today().date().strftime("%y"))
            self.__mes = int(datetime.today().date().strftime("%m"))
            self.__dia = int(datetime.today().date().strftime("%d"))
            return True

        elif comprou_hoje == "n":
            return False

        else:
            raise RespostaInvalida("Só é aceito s(sim) ou n(não).")

    def coletar_ano(self):
        try:
            self.__ano = int(input("Ano da compra (dois ultimos digitos): "))
        except ValueError:
            self.__erro_ano_invalido()

        self.__checar_ano_dado()

    def coletar_mes(self):
        try:
            self.__mes = int(input("Mês da compra, em numeral (1-12): "))
        except ValueError:
            self.__erro_mes_invalido()

        self.__checar_mes_dado()

    def coletar_dia(self):
        try:
            self.__dia = int(input("Dia da compra, em numeral (1-último dia do mês desejado): "))
        except ValueError:
            self.__erro_dia_invalido()

        self.__checar_dia_dado()

    def __coletar_data(self):
        self.coletar_ano()
        self.coletar_mes()
        self.coletar_dia()

    def confirmar_os_itens(self):
        """Pedirá uma confirmação do usuário para saber se as informações entregues estão corretas."""

        resposta = input(f'O objeto (\033[1;31m{self.__objeto}\033[m), '
                         f'o valor (R$: \033[1;31m{self.__valor}\033[m),\n'
                         f'a quantidade (\033[1;31m{self.__quantidade}\033[m) e/ou'
                         f' a data (\033[1;31mD-{self.__dia}/M-{self.__mes}/A-{self.__ano}\033[m),\n '
                         f'estão corretos? S/N: ').lower().strip()

        if resposta != 's' and resposta != 'n':
            raise RespostaInvalida('Só é possivel responder s(sim) ou n(não) nessa questão.')

        retornar = {'s': True, 'n': False}

        return retornar[resposta]

    @staticmethod
    def definir_erros():
        """Perguntará ao usuário qual erro ele quer corrrigir."""

        achar_errado = input('Digite o(s) número(s) do(s) item(ns) que você deseja concertar,'
                             ' \nsendo o \033[1;31mobjeto igual a 1, valor(2), quantidade(3) e data(4).\033[m\n'
                             'Você pode escolher mais de um pra corrigir.\n'
                             'Exemplos: 4 ou 12 ou 123 ou 23 etc. Sua escolha:').strip()

        set_check = {'1', '2', '3', '4'}
        set_resposta = set(achar_errado)

        if not set_resposta <= set_check:
            raise RespostaInvalida('As únicas respostas válidas são; 1, 2, 3 e 4.')

        lista_erros = sorted(list(set_resposta))

        return lista_erros

    def concertar_erros(self, lista_erros):
        """Direcionará o erro a ser corrigido ao método apropriado."""

        direcionador = {'1': self.coletar_objeto, '2': self.coletar_valor,
                        '3': self.coletar_quantidade, '4': self.__coletar_data}

        for erro in lista_erros:
            direcionador[erro]()
            print("_" * 100)

    def __checar_objeto_dado(self):
        if self.__objeto == '':
            raise ObjetoInvalido('O objeto precisa ter um nome.')

    def __checar_valor_dado(self):
        if self.__valor <= 0:
            self.__erro_valor_invalido()

    def __checar_quantidade_dada(self):
        if not self.__quantidade.isnumeric() or int(self.__quantidade) <= 0:
            raise QuantidadeInvalida('A quantidade deve ser um inteiro maior que zero.')

    def __checar_ano_dado(self):
        if not -1 < self.__ano < 100:
            self.__erro_ano_invalido()

    def __checar_mes_dado(self):
        if not 0 < self.__mes < 13:
            self.__erro_mes_invalido()

    def __checar_dia_dado(self):
        if not self.__dia_eh_valido():
            self.__erro_dia_invalido()

    def __dia_eh_valido(self):
        total_dias_cada_mes = ColetarInfoGastos.__retornar_dias_dos_meses()

        bissexto = self.__ano % 4 == 0
        if bissexto:
            total_dias_cada_mes['2'] = 29

        return 0 < self.__dia <= total_dias_cada_mes[str(self.__mes)]

    def __erro_valor_invalido(self):
        raise ValorInvalido('O valor não pode ser zero ou negativo e deve está na forma numeral.')

    def __erro_ano_invalido(self):
        raise DataInvalida('O ano deve estar na forma númerica e ter apenas os dois últimos digitos.')

    def __erro_mes_invalido(self):
        raise DataInvalida("o mês deve está em forma númerica (1-12).")

    def __erro_dia_invalido(self):
        raise DataInvalida('O dia deve está em forma númerica (1-último dia do mês).')

    @staticmethod
    def __retornar_dias_dos_meses():

        """Retornará um dict para informar quantos dias cada mês tem."""

        mes_dias = {'1': 31, '2': 28, '3': 31, '4': 30, '5': 31, '6': 30,
                    '7': 31, '8': 31, '9': 30, '10': 31, '11': 30, '12': 31}
        return mes_dias

    @property
    def valor(self):
        return self.__valor

    @property
    def objeto(self):
        return self.__objeto

    @property
    def quantidade(self):
        return self.__quantidade

    @property
    def ano(self):
        return self.__ano

    @property
    def mes(self):
        return self.__mes

    @property
    def dia(self):
        return self.__dia
