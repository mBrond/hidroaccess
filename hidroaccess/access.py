import json
import requests
import aiohttp
import asyncio
import warnings
import hidroaccess.decodes as decodes
from datetime import datetime, timedelta

class Access:
    def __init__(self, id: str, senha: str) -> None:
        self.__id = id
        self.__senha = senha
        self.urlApi = 'https://www.ana.gov.br/hidrowebservice/EstacoesTelemetricas'

    def _set_senha(self, senha=str()) -> None:
        self.__senha = senha

    def _set_id(self, id=str()) -> None:
        self.__id = id

    def atualizar_credenciais(self, id: str, senha: str) -> None:
        """Atualiza as credencias salvas no objeto

        Args:
            id (str, optional): _description_. Defaults to str().
            senha (str, optional): _description_. Defaults to str().
        """
        self._set_senha(senha)
        self._set_id(id)

    def _defineIntervaloBuscaLongo(self, qtdDiasDownload: int)->str:
        """Define o melhor parâmetro para o campo "Range Intervalo de Busca" para longos períodos

        Args:
            qtdDiasDownload (int): Quantidade total de dias desejados

        Returns:
            str: Parâmetro para requisição
        """
        intervalos = [
            (30, "DIAS_30"),
            (21, "DIAS_21"),
            (14, "DIAS_14"),
            (7, "DIAS_7"),
            (2, "DIAS_2"),
            (0, "HORA_24")
        ]
        for dias, intervalo in intervalos:
            if qtdDiasDownload >= dias:
                return intervalo

    def _criaParams(self, codEstacao: int, diaComeco: datetime, intervaloBusca="HORA_24", filtroData = "DATA_LEITURA", **kwargs) -> list:
        """
        !!OBSOLETO!!
        :param codEstacao: Codigo da estacao
        :param diaComeco:
        :param intervaloBusca: [OPCIONAL] 
        :param filtroData: [OPCIONAL]
        :param diaFinal: [OPCIONAL] Utilizado apenas quando é necessário parâmetros para mais de um dia. Data final, posterior à diaComeco.
        :param qtdMaxParams: [OPCIONAL] Utilizado em conjunto com com diaFinal. Máximo de parametrôs para aquele período  
        """

        diaFinal= kwargs.get('diaFinal')
        if not diaFinal:
            diaFinal = diaComeco + timedelta(days=1)

        paramsL = list()

        while diaComeco < diaFinal:
            params = {
                'Código da Estação': codEstacao,
                'Tipo Filtro Data': filtroData,
                'Data de Busca (yyyy-MM-dd)': datetime.strftime(diaComeco, "%Y-%m-%d"),
                'Range Intervalo de busca': intervaloBusca
            }
            paramsL.append(params)
            diaComeco = diaComeco + timedelta(days=1)

        return paramsL

    def _param_unico(self, codEstacao, filtroData, qtdDiasParam, dia):

        intervaloBusca = self._defineIntervaloBuscaLongo(qtdDiasParam)
        param = {
            'Código da Estação': codEstacao,
            'Tipo Filtro Data': filtroData,
            'Data de Busca (yyyy-MM-dd)': datetime.strftime(dia, "%Y-%m-%d"),
            'Range Intervalo de busca': intervaloBusca
        }
        return param

    def _defineQtdDownloadsAsync(self, maxRequests, qtdDownloads)->int:
        if qtdDownloads < maxRequests:
            return qtdDownloads
        else:
            return maxRequests

    def _defQtdDiasParam(self, dataComeco: datetime, dataFinal: datetime)->int:
        diferenca = (dataFinal - dataComeco).days

        if diferenca >=30:
            return 30
        elif diferenca >= 21:
            return 21
        elif diferenca >= 14:
            return 14
        elif diferenca >= 7:
            return 7
        elif diferenca >=5:
            return 5
        elif diferenca >= 2:
            return 2
        else:
            return 1

    def _validar_data(self, data: str) ->datetime:
        try:
            return datetime.strptime(data, "%Y-%m-%d")
        except:
            raise ValueError(f"Parâmetro 'data' inválido: {data}. Deve ser 'YYYY-MM-DD'.")

    def _criar_cabecalho(self, token: str) -> dict:
        """Cria o cabeçalho da requisição http

        Args:
            token (str): token de validação do usuário

        Returns:
            dict: Cebeçalho pronto para requisição
        """
        if token != '-1':
            return {'Authorization': f'Bearer {token}'}

        raise ValueError(f"Token inválido: {token}.")

    #deprecated
    def requestTelemetricaDetalhada(self, estacaoCodigo: int, data: str, token: str, intervaloBusca="HORA_24", filtroData = "DATA_LEITURA"):
        """
        !!!Utilizar requestTelemetricaDetalhadaAsync!!!
        :param estacaoCodigo: Código de 8 dígitos
        :param data: Data dos dados requisitados. Formato yyyy-MM-dd.
        :param token: AcessToken adquirido
        :param filtroData:
        :param intervaloBusca: Intervalo das medições.
        :return: Objeto 'response'.
        """

        warnings.warn("'requestTelemetricaDetalhada' é um método obsoleto e será removido!", category=DeprecationWarning, stacklevel=2)

        url = self.urlApi+ "/HidroinfoanaSerieTelemetricaDetalhada/v1"

        headers = {
            'Authorization': 'Bearer '+token
        }

        params = self._criaParams(estacaoCodigo)[0]

        return requests.get(url=url, headers = headers, params = params)

    #deprecated
    def requestTelemetricaAdotada(self, estacaoCodigo: int, data: str, token: str, intervaloBusca="HORA_24", filtroData = "DATA_LEITURA"):
        """
        !!!Utilizar versão requestTelemetricaAdotadaAsync!!!
        :param estacaoCodigo: Código de 8 dígitos
        :param data: Data dos dados requisitados. Formato yyyy-MM-dd.
        :param token: AcessToken adquirido
        :param filtroData:
        :param intervaloBusca: Intervalo das medições.
        :return: Objeto 'response'.
        """ 

        warnings.warn("'requestTelemetricaAdotada' é um método obsoleto e será removido!", category=DeprecationWarning, stacklevel=2)

        url = self.urlApi + "/HidroinfoanaSerieTelemetricaAdotada/v1"

        headers = {
            'Authorization': 'Bearer '+token
        }

        params = {
            'Código da Estação': estacaoCodigo,
            'Tipo Filtro Data': filtroData,
            'Data de Busca (yyyy-MM-dd)': data,
            'Range Intervalo de busca': intervaloBusca
        }

        return requests.get(url=url, headers = headers, params = params)
    
    def requestToken(self):
        """
        Requisita o token de autenticação da API com o ID e Senha
        :param id: Identificador cadastrado.
        :param password: Senha cadastrada.
        :return: Objeto 'response'.
        """
        url = self.urlApi + '/OAUth/v1'
        headers = {'Identificador': self.__id, 'Senha': self.__senha}
        return requests.get(url=url, headers=headers)

    def safe_request_token(self)->str:
        """Realiza requisições até conseguir um token válido. Credenciais utilizadas 

        Returns:
            str: '-1' caso as credenciais não sejam válidas, se não str de token válido.
        """
        tokenRequest = self.requestToken()
        tentativas = 1  #TODO melhorar lógica com TRY-EXCEPT (?)
        if (tokenRequest.status_code == 401): #Não autorizado, sem motivos tentar novamente.
            return '-1'

        while(tokenRequest.status_code!=200 and tentativas <5): #TODO recursividade 
            tokenRequest = self.requestToken()  
            tentativas = tentativas+1

        if(tokenRequest.status_code==200):
            token = json.loads(tokenRequest.content)
            itens = token['items']
            return itens['tokenautenticacao']

    #deprecated
    async def requestTelemetricaAdotadaAsync(self, estacaoCodigo: int, stringComeco: str, stringFinal: str, headers: dict, qtdDownloadsAsync=20):

        warnings.warn("'requestTelemetricaAdotadaAsync' é um método obsoleto e será removido! Utilize request_telemetrica.", category=DeprecationWarning, stacklevel=2)

        diaFinal = datetime.strptime(stringFinal, "%Y-%m-%d")
        diaComeco = datetime.strptime(stringComeco, "%Y-%m-%d")

        diasRestantesParaDownload = (diaFinal - diaComeco).days

        url = self.urlApi + "/HidroinfoanaSerieTelemetricaAdotada/v1"

        respostaLista = list()
        qtdDiasParam = qtdDownloadsAsync+1 #garante que é maior

        while diasRestantesParaDownload != 0 :
            blocoAsync = list()

            while (len(blocoAsync) <= qtdDownloadsAsync) and (diaComeco!=diaFinal):
                qtdDiasParam = self._defQtdDiasParam(diaComeco, diaFinal)
                diaComeco += timedelta(days=qtdDiasParam)
                blocoAsync.append(self._param_unico(estacaoCodigo, "DATA_LEITURA", qtdDiasParam, diaComeco - timedelta(days=1)))

            async with aiohttp.ClientSession(headers=headers) as session:
                tasks = list()
                for param in blocoAsync:
                    tasks.append(self._download_url(session, url, param))
                resposta = await asyncio.gather(*tasks)
                respostaLista.append(resposta)

            diasRestantesParaDownload = (diaFinal - diaComeco).days
            
        return respostaLista
    
    #deprecated
    async def requestTelemetricaDetalhadaAsync(self, estacaoCodigo: int, stringComeco: str, stringFinal: str, headers: dict, qtdDownloadsAsync=20) -> list:

        warnings.warn("'requestTelemetricaDetalhadaAsync' é um método obsoleto e será removido! Utilize request_telemetrica.", category=DeprecationWarning, stacklevel=2)


        diaFinal = datetime.strptime(stringFinal, "%Y-%m-%d")
        diaComeco = datetime.strptime(stringComeco, "%Y-%m-%d")

        diasRestantesParaDownload = (diaFinal - diaComeco).days

        url = self.urlApi + "/HidroinfoanaSerieTelemetricaDetalhada/v1"

        respostaLista = list()
        qtdDiasParam = qtdDownloadsAsync+1 #garante que é maior

        while diasRestantesParaDownload != 0 :
            blocoAsync = list()

            while (len(blocoAsync) <= qtdDownloadsAsync) and (diaComeco!=diaFinal):
                qtdDiasParam = self._defQtdDiasParam(diaComeco, diaFinal)
                diaComeco += timedelta(days=qtdDiasParam)
                blocoAsync.append(self._param_unico(estacaoCodigo, "DATA_LEITURA", qtdDiasParam, diaComeco - timedelta(days=1)))

            async with aiohttp.ClientSession(headers=headers) as session:
                tasks = list()
                for param in blocoAsync:
                    tasks.append(self._download_url(session, url, param))
                resposta = await asyncio.gather(*tasks)
                respostaLista.append(resposta)

            diasRestantesParaDownload = (diaFinal - diaComeco).days
            
        return respostaLista

    async def _main_request_telemetrica(self, estacaoCodigo: int, dataComeco: str, dataFinal: str, token: str, tipo='Adotada', qtdDownloadsAsync=20) -> list:
        """_summary_

        Args:
            estacaoCodigo (int): Código da estação para consulta.
            dataComeco (str): Data inicial do período a ser consultado.
            dataFinal (str): Data final do período a ser consultado.
            cabecalho (dict): _description_
            tipo (str, optional): _description_. Defaults to 'Adotada'.
            qtdDownloadsAsync (int, optional): _description_. Defaults to 20.

        Returns:
            list: _description_
        """
        if tipo not in {"Adotada", "Detalhada"}:
            raise ValueError(f"Parâmetro 'tipo' inválido: {tipo}. Deve ser 'Adotada' ou 'Detalhada'")

        diaFinal = self._validar_data(dataFinal)
        diaComeco = self._validar_data (dataComeco)

        cabecalho = self._criar_cabecalho(token)

        diasRestantesParaDownload = (diaFinal - diaComeco).days

        listaRespostaTasks = list()

        url = self.urlApi + f"/HidroinfoanaSerieTelemetrica{tipo}/v1"

        while diasRestantesParaDownload != 0 :
            blocoAsync = list()

            while (len(blocoAsync) <= qtdDownloadsAsync) and (diaComeco!=diaFinal):
                qtdDiasParam = self._defQtdDiasParam(diaComeco, diaFinal)
                diaComeco += timedelta(days=qtdDiasParam)
                blocoAsync.append(self._param_unico(estacaoCodigo, "DATA_LEITURA", qtdDiasParam, diaComeco - timedelta(days=1)))

            async with aiohttp.ClientSession(headers=cabecalho) as session:
                tasks = list()
                for param in blocoAsync:
                    tasks.append(self._download_url(session, url, param))
                respostaTasks = await asyncio.gather(*tasks)
                listaRespostaTasks.extend(respostaTasks)

            diasRestantesParaDownload = (diaFinal - diaComeco).days

        resposta = decodes.decode_list_bytes(listaRespostaTasks, tipo)

        return resposta

    def request_telemetrica(self, estacaoCodigo: int, dataComeco: str, dataFinal: str, token: str, tipo='Adotada', qtdDownloadsAsync=20) -> list:
        """_summary_

        Args:
            estacaoCodigo (int): Código da estação para consulta.
            dataComeco (str): Data inicial do período a ser consultado.
            dataFinal (str): Data final do período a ser consultado.
            cabecalho (dict): _description_
            tipo (str, optional): _description_. Defaults to 'Adotada'.
            qtdDownloadsAsync (int, optional): _description_. Defaults to 20.

        Returns:
            list: Lista de dicionários.
        """
        return asyncio.run(self._main_request_telemetrica(estacaoCodigo, dataComeco, dataFinal, token, tipo, qtdDownloadsAsync))

    async def _download_url(self, session, url, params): 
        async with session.get(url, params=params) as response:
            return await response.content.read()

if __name__ =='__main__':
    pass