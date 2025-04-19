import json
import pandas as pd

def decode_list_bytes(listaRespostaTasks: list, tipo='Adotada')->list:
    retorno = list()
    for request in listaRespostaTasks:
        if tipo == 'Adotada':
            retorno.extend(_decode_request_adotada(request))
        elif tipo =='Detalhada':
            retorno.extend(_decode_request_detalhada(request))
        elif tipo == 'Sedimento':
            retorno.extend(_decode_request_sedimento(request))

    return retorno

def _decode_request_sedimento(request): #72980000 -> tem dado em 2000
    content = json.loads(request.decode('latin-1'))
    itens = content.get('items')
    listaOrdenada = []

    chaves = [
        "Area_Molhada",
        "Concentracao_PPM",
        "Concentracao_da_Amostra_Extra",
        "Condutividade_Eletrica",
        "Cota_cm",
        "Cota_de_Mediacao",
        "Data_Hora_Dado",
        "Data_Hora_Medicao_Liquida",
        "Data_Ultima_Alteracao",
        "Largura",
        "Nivel_Consistencia",
        "Numero_Medicao",
        "Numero_Medicao_Liquida",
        "Observacoes",
        "Temperatura_da_Agua",
        "Vazao_m3_s",
        "Vel_Media",
        "codigoestacao"
    ]

    if itens is not None:
        for item in itens:
            dicionarioDiario = {chave: item.get(chave) for chave in chaves}
            listaOrdenada.append(dicionarioDiario)
    else:
        dicionarioDiario = {chave: None for chave in chaves}
        listaOrdenada.append(dicionarioDiario)

    return listaOrdenada

def _decode_request_detalhada(request):
    content = json.loads(request.decode('latin-1'))
    itens = content['items']
    listaOrdenada = list()
    if itens != None:
        for item in itens:
            dicionarioDiario = dict()
            dicionarioDiario["Hora_Medicao"] = item['Data_Hora_Medicao']
            dicionarioDiario["Chuva_Acumulada"] = item["Chuva_Acumulada"]
            dicionarioDiario["Chuva_Adotada"] = item["Chuva_Adotada"]
            dicionarioDiario["Cota_Adotada"] = item["Cota_Adotada"]
            dicionarioDiario["Cota_Sensor"] = item["Cota_Sensor"]
            dicionarioDiario["Vazao_Adotada"] = item["Vazao_Adotada"]
            listaOrdenada.append(dicionarioDiario)
    else:
        dicionarioDiario = dict()
        dicionarioDiario["Hora_Medicao"] = None
        dicionarioDiario["Chuva_Acumulada"] = None
        dicionarioDiario["Chuva_Adotada"] = None
        dicionarioDiario["Cota_Adotada"] = None
        dicionarioDiario["Cota_Sensor"] = None
        dicionarioDiario["Vazao_Adotada"] = None
        listaOrdenada.append(dicionarioDiario)
    return listaOrdenada

def _decode_request_adotada(request: bytes) -> list:
    """_summary_

    Args:
        request (bytes): Resposta da requisição a API

    Returns:
        list: Lista de dicionarios com a data e medições correspondentes
    """
    content = json.loads(request.decode('latin-1'))
    itens = content['items']
    listaOrdenada = list()
    if itens != None:
        for item in itens:
            dicionarioDiario = dict()
            dicionarioDiario["Hora_Medicao"] = item["Data_Hora_Medicao"]
            dicionarioDiario["Chuva_Adotada"] = item["Chuva_Adotada"]
            dicionarioDiario["Cota_Adotada"] = item["Cota_Adotada"]
            dicionarioDiario["Vazao_Adotada"] = item["Vazao_Adotada"]
            listaOrdenada.append(dicionarioDiario)
    else:
        dicionarioDiario = dict()
        dicionarioDiario["Hora_Medicao"] = None
        dicionarioDiario["Chuva_Adotada"] = None
        dicionarioDiario["Cota_Adotada"] = None
        dicionarioDiario["Vazao_Adotada"] = None
        listaOrdenada.append(dicionarioDiario)
    return listaOrdenada
