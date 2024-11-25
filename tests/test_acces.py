from acess import Acess
import pytest
import asyncio
import json

@pytest.fixture
def login_valido():
    f = open('tests//credenciais.txt', 'r')
    login = f.read(11)
    f.seek(13)
    senha = f.read(8)
    f.close()

    return Acess(str(login), str(senha))

@pytest.fixture
def login_invalido():
    return Acess('1', '123')

def test_forceRequestToken_valido(login_valido):
    assert login_valido.forceRequestToken != -1

def test_forceRequestToken_invalido(login_invalido):
    assert login_invalido.forceRequestToken()  == -1

def test_requestTelemetricaAdotadaAsync_realiza_requisicao_valida(login_valido):
    acesso = login_valido

    headers = {'Authorization': 'Bearer {}'.format(acesso.forceRequestToken())}

    ListaListaRespostas = asyncio.run(acesso.requestTelemetricaDetalhadaAsync(76310000, '2024-01-01', '2024-01-03', headers))
    for resposta in ListaListaRespostas:
        for dia in resposta:
            contentDia = json.loads(dia) #dict
            if str(contentDia['status']) != 'OK':
                assert contentDia['code'] == 200
    assert True