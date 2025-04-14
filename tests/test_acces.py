from hidroaccess.access import Access
from datetime import datetime
import pytest

def login_valido():
    f = open('tests//credenciais.txt', 'r')
    login = f.read(11)
    f.seek(13)
    senha = f.read(8)
    f.close()
    return Access(str(login), str(senha))

@pytest.fixture
def login_valido_fixture():
    return login_valido()

@pytest.fixture
def estacao_valida():
    return 76310000

def login_invalido():
    return Access('1', '123')

@pytest.mark.parametrize("acesso, validade", [
    (login_valido(), True),
    (login_invalido(), False)
])

def test_safe_request_token(acesso, validade):
    if validade:
        assert acesso.safe_request_token() != '-1'#valor do token
    else:
        assert acesso.safe_request_token() == '-1'#valor erro

@pytest.mark.parametrize("chavesEsperadas, tipo", [
        (set(['Hora_Medicao', 'Chuva_Adotada', 'Cota_Adotada', 'Vazao_Adotada']), 'Adotada'),
        (set(['Hora_Medicao', 'Chuva_Adotada', 'Cota_Adotada', 'Vazao_Adotada', 'Chuva_Acumulada', 'Cota_Sensor']), 'Detalhada')
])
def test_request_telemetrica_valida(login_valido_fixture, chavesEsperadas, tipo):
    acesso = login_valido_fixture

    token = acesso.safe_request_token()

    retorno = acesso.request_telemetrica(85900000, '2020-01-01', '2020-01-5', token, tipo)
    for item in retorno:
        chavesRetorno = item.keys()
        if chavesEsperadas != set(chavesRetorno):
            assert False
    assert True

def test__criar_cabecalho():
    sessao = Access('a', 'b')
    token = "-1"
    with pytest.raises(ValueError, match="Token inválido: -1"):
        sessao._criar_cabecalho(token)

@pytest.mark.parametrize('diaInicio, diaFim, resultado', [
    ('2024-01-01', '2024-03-01', 30),
    ('2024-01-01', '2024-01-04', 2),
    ('2024-01-01', '2024-01-02', 1),
    ('2024-01-01', '2024-01-29', 21),
    ('2024-01-01', '2024-01-18', 14),
    ('2024-01-01', '2024-01-08', 7),
    ('2024-01-01', '2024-01-07', 5)
])
def test__defQtdDiasParam(diaInicio, diaFim, resultado):
    acesso = login_valido()

    resposta = acesso._defQtdDiasParam(datetime.strptime(diaInicio, "%Y-%m-%d"), datetime.strptime(diaFim, "%Y-%m-%d"))
    assert resposta == resultado

@pytest.mark.parametrize('data, validade', [
    ('2024-01-01', True),
    ('2024-01-32', False),
    ('2015-02-30', False),
    ('12-12-2024', False),
    (12, False),
    ('12/12/12', False),
    ('2024/12/12', False) 
])
def test__validar_data(data, validade):
    acesso = Access('a', 'a')
    try:
        acesso._validar_data(data)
    except ValueError:
        assert validade == False
    else:
        assert validade == True



#testa se os dias solicitados foram baixados
@pytest.mark.parametrize('diaInicial, diaFim, qtdDias',[
    ('2024-01-01', '2024-01-03', 2),
    ('2024-01-01', '2024-02-01', 31),
    ('2024-01-01', '2024-02-04', 34),
    ('2024-01-01', '2024-01-06', 5),
    ('2024-01-01', '2024-01-23', 22),
    ('2024-01-01', '2024-01-18', 17)

])
def test_request_telemetrica_dias_baixados(login_valido_fixture, diaInicial, diaFim, qtdDias):
    diasRetornados = set()
    acesso = login_valido_fixture

    token = acesso.safe_request_token()

    retorno = acesso.request_telemetrica(85900000, diaInicial, diaFim, token, 'Adotada')
    for item in retorno:
        diaHora = item['Hora_Medicao']
        dia = diaHora[:11]
        diasRetornados.add(dia)

    assert qtdDias == len(diasRetornados)