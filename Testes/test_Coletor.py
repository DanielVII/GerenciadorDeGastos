import pytest

import mock

from Coletor import ColetarInfoGastos

from excecoes import ObjetoInvalido, DataInvalida, QuantidadeInvalida, ValorInvalido, RespostaInvalida

from datetime import datetime

ctrl = ColetarInfoGastos()


def mock_input(valor):
    return mock.patch("builtins.input", return_value=valor)


def mock_many_inputs(valor: list):
    return mock.patch("builtins.input", side_effect=valor)


# test valor
def test_deve_passar_quando_a_resposta_para_o_valor_for_decimal_positivo():
    with mock_input(1.0):
        ctrl.coletar_valor()
        assert ctrl.valor == 1.0


def test_deve_falhar_quando_a_resposta_para_o_valor_for_negativo():
    with pytest.raises(ValorInvalido):
        with mock_input(-1):
            ctrl.coletar_valor()


def test_deve_falhar_quando_a_resposta_para_o_valor_for_zero():
    with pytest.raises(ValorInvalido):
        with mock_input(0):
            ctrl.coletar_valor()


def test_deve_falhar_quando_a_resposta_para_o_valor_for_diferente_de_numeral():
    with pytest.raises(ValorInvalido):
        with mock_input("aloha2"):
            ctrl.coletar_valor()


# test nome
def test_deve_passar_quando_o_objeto_tiver_um_nome_qualquer():
    with mock_input(" al1o7h6a "):
        ctrl.coletar_objeto()
    assert ctrl.objeto == 'al1o7h6a'


def test_deve_falhar_quando_o_objeto_nao_tiver_nome():
    with pytest.raises(ObjetoInvalido):
        with mock_input(''):
            ctrl.coletar_objeto()


# test quantidade
def test_deve_passar_quando_a_resposta_para_quantidade_for_inteiro_maior_que_zero():
    with mock_input(' 1 '):
        ctrl.coletar_quantidade()
    assert ctrl.quantidade == '1'


def test_deve_falhar_quando_a_resposta_para_quantidade_for_inteiro_menor_que_zero():
    with pytest.raises(QuantidadeInvalida):
        with mock_input('-1'):
            ctrl.coletar_quantidade()


def test_deve_falhar_quando_a_resposta_para_quantidade_nao_for_numeral():
    with pytest.raises(QuantidadeInvalida):
        with mock_input('aloha'):
            ctrl.coletar_quantidade()


def test_deve_falhar_quando_a_resposta_para_quantidade_nao_for_inteiro():
    with pytest.raises(QuantidadeInvalida):
        with mock_input('1.5'):
            ctrl.coletar_quantidade()


# test data
def test_deve_retornar_true_quando_resposta_para_foi_hoje_for_s():
    with mock_input('s'):
        t_ou_f = ctrl.confirmar_se_foi_hoje()
    assert t_ou_f == True


def test_deve_retornar_false_quando_resposta_para_foi_hoje_for_n():
    with mock_input('n'):
        t_ou_f = ctrl.confirmar_se_foi_hoje()
    assert t_ou_f == False


def test_deve_falhar_quando_a_resposta_para_foi_hoje_for_diferente_de_s_ou_n():
    with pytest.raises(RespostaInvalida):
        with mock_input('j'):
            ctrl.confirmar_se_foi_hoje()


def test_deve_ter_o_ano_de_hoje_quando_resposta_para_foi_hoje_for_s():
    ano_hoje_dois_digitos = int(datetime.today().date().strftime("%y"))
    with mock_input('s'):
        ctrl.confirmar_se_foi_hoje()
    assert ctrl.ano == ano_hoje_dois_digitos


def test_deve_ter_o_mes_de_hoje_quando_resposta_para_foi_hoje_for_s():
    mes_hoje = int(datetime.today().date().strftime("%m"))
    with mock_input('s'):
        ctrl.confirmar_se_foi_hoje()
    assert ctrl.mes == mes_hoje


def test_deve_ter_o_dia_de_hoje_quando_resposta_para_foi_hoje_for_s():
    dia_hoje = int(datetime.today().date().strftime("%d"))
    with mock_input('s'):
        ctrl.confirmar_se_foi_hoje()
    assert ctrl.dia == dia_hoje


def test_deve_falhar_quando_ano_for_negativo():
    with pytest.raises(DataInvalida):
        with mock_input(-1):
            ctrl.coletar_ano()


def test_deve_falhar_quando_ano_for_igual_ou_maior_que_cem():
    with pytest.raises(DataInvalida):
        with mock_input(100):
            ctrl.coletar_ano()


def test_deve_falhar_quando_mes_for_menor_igual_a_zero():
    with pytest.raises(DataInvalida):
        with mock_input(0):
            ctrl.coletar_mes()


def test_deve_falhar_quando_mes_for_maior_igual_a_treze():
    with pytest.raises(DataInvalida):
        with mock_input(13):
            ctrl.coletar_mes()


def ano_valido_e_bissexto():
    with mock_input(4):
        ctrl.coletar_ano()


def ano_valido_nao_bissexto():
    with mock_input(3):
        ctrl.coletar_ano()


def mes_valido_e_fevereiro():
    with mock_input(2):
        ctrl.coletar_mes()


def test_deve_passar_quando_for_bissexto_fevereiro_vinte_nove():
    ano_valido_e_bissexto()
    mes_valido_e_fevereiro()
    with mock_input(29):
        ctrl.coletar_dia()
    assert ctrl.dia == 29


def test_deve_falhar_quando_nao_for_bissexto_e_for_fevereiro_vinte_nove():
    ano_valido_nao_bissexto()
    mes_valido_e_fevereiro()
    with pytest.raises(DataInvalida):
        with mock_input(29):
            ctrl.coletar_dia()


# test confirmação
def test_deve_retornar_true_quando_resposta_para_confirmar_os_itens_for_s():
    with mock_input("s"):
        t_ou_f = ctrl.confirmar_os_itens()
    assert t_ou_f == True


def test_deve_retornar_false_quando_resposta_para_confirmar_os_itens_for_n():
    with mock_input("n"):
        t_ou_f = ctrl.confirmar_os_itens()
    assert t_ou_f == False


def test_deve_falhar_quando_resposta_para_confirmar_os_itens_for_diferente_de_s_ou_n():
    with pytest.raises(RespostaInvalida):
        with mock_input("j"):
            ctrl.confirmar_os_itens()


# test escolhas de erro
def test_deve_retornar_uma_lista_em_ordem_crescente_quando_for_colocado_os_numeros_certos_em_definir_erros():
    with mock_input("4213"):
        listinha = ctrl.definir_erros()
    assert listinha == ["1", "2", "3", "4"]


def test_deve_falhar_quando_tiver_um_numero_diferente_do_range_de_um_a_quatro_em_definir_erros():
    with pytest.raises(RespostaInvalida):
        with mock_input("3154"):
            ctrl.definir_erros()


# test concertar erros
def test_deve_mudar_o_nome_do_objeto_quando_a_escolha_for_somente_um_em_concertar_erro():
    lista = ["1"]
    with mock_input("nominho"):
        ctrl.concertar_erros(lista)
    assert ctrl.objeto == "nominho"


def test_deve_mudar_o_valor_do_objeto_quando_a_escolha_for_somente_dois_em_concertar_erro():
    lista = ["2"]
    with mock_input(42):
        ctrl.concertar_erros(lista)
    assert ctrl.valor == 42


def test_deve_mudar_a_quantidade_do_objeto_quando_a_escolha_for_somente_tres_em_concertar_erro():
    lista = ["3"]
    with mock_input("76"):
        ctrl.concertar_erros(lista)
    assert ctrl.quantidade == "76"


def test_deve_mudar_a_data_do_objeto_quando_a_escolha_for_somente_quatro_em_concertar_erro():
    lista = ["4"]
    ano = 4
    mes = 2
    dia = 29
    with mock_many_inputs([ano, mes, dia]):
        ctrl.concertar_erros(lista)
    assert ctrl.ano == ano
    assert ctrl.mes == mes
    assert ctrl.dia == dia


def test_deve_funcionar_quando_tiver_mais_de_uma_requisicao_de_mudanca_em_concertar_erro():
    lista = ["1", "3"]
    with mock_many_inputs(["aloha", "20"]):
        ctrl.concertar_erros(lista)

    assert ctrl.objeto == "aloha"
    assert ctrl.quantidade == "20"
