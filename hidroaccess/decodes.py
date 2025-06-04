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
        elif tipo == 'Cota':
            retorno.extend(_decode_request_cota(request))
        elif tipo == 'Chuva':
            retorno.extend(_decode_request_chuva(request))

    return retorno
    
def _decode_request_chuva(request):
    content = json.loads(request.decode('latin-1'))
    itens = content.get('items')
    listaOrdenada = []

    chaves = chaves = [
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


    if itens is not None:
        for item in itens:
            dicionarioDiario = {chave: item.get(chave) for chave in chaves}
            listaOrdenada.append(dicionarioDiario)
    else:
        dicionarioDiario = {chave: None for chave in chaves}
        listaOrdenada.append(dicionarioDiario)

    return listaOrdenada
    

def _decode_request_cota(request):
    content = json.loads(request.decode('latin-1'))
    itens = content.get('items')
    listaOrdenada = []

    print(itens[0].keys())

    chaves =[
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
    "Tipo_Medicao_Cotas", "codigoestacao", "nivelconsistencia"
    ]


    if itens is not None:
        for item in itens:
            dicionarioDiario = {chave: item.get(chave) for chave in chaves}
            listaOrdenada.append(dicionarioDiario)
    else:
        dicionarioDiario = {chave: None for chave in chaves}
        listaOrdenada.append(dicionarioDiario)

    return listaOrdenada

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
