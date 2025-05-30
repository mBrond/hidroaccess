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


##confirmar se são essas as chaves !!!
#EstacaoCodigo;NivelConsistencia;Data;Hora;NumMedicao;DataLiq;HoraLiq;NumMedicaoLiq;Cota;Vazao;AreaMolhada;Largura;VelMedia;ConcentracaoMatSuspensao;CotaDeMedicao;TemperaturaDaAgua;ConcentracaoDaAmostraExtra;CondutividadeEletrica;Observacoes
@pytest.mark.parametrize('chaves_esperadas_sedimentos',[
    (set(
        ["Area_Molhada","Concentracao_PPM","Concentracao_da_Amostra_Extra",
        "Condutividade_Eletrica","Cota_cm","Cota_de_Mediacao","Data_Hora_Dado",
        "Data_Hora_Medicao_Liquida","Data_Ultima_Alteracao","Largura","Nivel_Consistencia",
        "Numero_Medicao","Numero_Medicao_Liquida","Observacoes","Temperatura_da_Agua",
        "Vazao_m3_s","Vel_Media","codigoestacao"]
    ))
])
def test_request_sedimentos(login_valido_fixture, chaves_esperadas_sedimentos):
    sessao = login_valido_fixture
    token = sessao.safe_request_token()

    retorno = sessao.request_sedimentos(72980000, '2000-01-01', '2000-12-31', token)
    
    chavesRetorno = set(retorno[0].keys())
    assert chaves_esperadas_sedimentos == chavesRetorno

@pytest.mark.parametrize('chaves_esperadas_cotas',[
    (set([
        "Cota_01", "Cota_01_Status", "Cota_02", "Cota_02_Status",
        "Cota_03", "Cota_03_Status", "Cota_04", "Cota_04_Status",
        "Cota_05", "Cota_05_Status", "Cota_06", "Cota_06_Status",
        "Cota_07", "Cota_07_Status", "Cota_08", "Cota_08_Status",
        "Cota_09", "Cota_09_Status", "Cota_10", "Cota_10_Status",
        "Cota_11", "Cota_11_Status", "Cota_12", "Cota_12_Status",
        "Cota_13", "Cota_13_Status", "Cota_14", "Cota_14_Status",
        "Cota_15", "Cota_15_Status", "Cota_16", "Cota_16_Status",
        "Cota_17", "Cota_17_Status", "Cota_18", "Cota_18_Status",
        "Cota_19", "Cota_19_Status", "Cota_20", "Cota_20_Status",
        "Cota_21", "Cota_21_Status", "Cota_22", "Cota_22_Status",
        "Cota_23", "Cota_23_Status", "Cota_24", "Cota_24_Status",
        "Cota_25", "Cota_25_Status", "Cota_26", "Cota_26_Status",
        "Cota_27", "Cota_27_Status", "Cota_28", "Cota_28_Status",
        "Cota_29", "Cota_29_Status", "Cota_30", "Cota_30_Status",
        "Cota_31", "Cota_31_Status",
        "Data_Hora_Dado", "Data_Ultima_Alteracao",
        "Dia_Maxima", "Dia_Minima", "Maxima", "Maxima_Status",
        "Media", "Media_Anual", "Media_Anual_Status",
        "Media_Status", "Mediadiaria", "Minima", "Minima_Status",
        "Tipo_Medicao_Cotas", "codigoestacao", "nivelconsistencia"]
    ))
])
def test_request_cota(login_valido_fixture, chaves_esperadas_cotas):
    sessao = login_valido_fixture
    token = sessao.safe_request_token()

    retorno = sessao.request_cota(72980000, '2000-01-01', '2000-12-31', token)

    if (len(retorno)>0):
        chaves_retorno = set(retorno[0].keys())
        assert chaves_esperadas_cotas == chaves_retorno
    else:
        assert False

@pytest.mark.parametrize('chaves_esperadas_chuvas',[
    (set(
        [
            "Chuva_01", "Chuva_01_Status", "Chuva_02", "Chuva_02_Status",
            "Chuva_03", "Chuva_03_Status", "Chuva_04", "Chuva_04_Status",
            "Chuva_05", "Chuva_05_Status", "Chuva_06", "Chuva_06_Status",
            "Chuva_07", "Chuva_07_Status", "Chuva_08", "Chuva_08_Status",
            "Chuva_09", "Chuva_09_Status", "Chuva_10", "Chuva_10_Status",
            "Chuva_11", "Chuva_11_Status", "Chuva_12", "Chuva_12_Status",
            "Chuva_13", "Chuva_13_Status", "Chuva_14", "Chuva_14_Status",
            "Chuva_15", "Chuva_15_Status", "Chuva_16", "Chuva_16_Status",
            "Chuva_17", "Chuva_17_Status", "Chuva_18", "Chuva_18_Status",
            "Chuva_19", "Chuva_19_Status", "Chuva_20", "Chuva_20_Status",
            "Chuva_21", "Chuva_21_Status", "Chuva_22", "Chuva_22_Status",
            "Chuva_23", "Chuva_23_Status", "Chuva_24", "Chuva_24_Status",
            "Chuva_25", "Chuva_25_Status", "Chuva_26", "Chuva_26_Status",
            "Chuva_27", "Chuva_27_Status", "Chuva_28", "Chuva_28_Status",
            "Chuva_29", "Chuva_29_Status", "Chuva_30", "Chuva_30_Status",
            "Chuva_31", "Chuva_31_Status", "Data_Hora_Dado", "Data_Ultima_Alteracao",
            "Dia_Maxima", "Maxima", "Maxima_Status", "Nivel_Consistencia",
            "Numero_Dias_de_Chuva", "Numero_Dias_de_Chuva_Status",
            "Tipo_Medicao_Chuvas", "Total", "Total_Anual", "Total_Anual_Status",
            "Total_Status", "codigoestacao"
        ]
    ))
])
def test_request_chuva(login_valido_fixture, chaves_esperadas_chuvas):
    sessao = login_valido_fixture
    token = sessao.safe_request_token()

    retorno = sessao.request_chuva(47000, '1964-01-01', '1964-02-01', token)

    if (len(retorno)>0):
        chaves_retorno = set(retorno[0].keys())
        assert chaves_esperadas_chuvas == chaves_retorno
    else:
        assert False
