import json
import requests
import aiohttp
import asyncio
from datetime import datetime, timedelta

class Acess:
    def __init__(self, id=str(), senha=str()) -> None:
        self._id = id
        self._senha = senha
        self.urlApi = 'https://www.ana.gov.br/hidrowebservice/EstacoesTelemetricas'
        self.pathResultados = '\\medicoes'
        self.pathConfigs = 'configs.json'

    def atualizarCredenciais(self, id=str(), senha=str()) -> None:
        """Atualiza as credencias salvas no objeto

        Args:
            id (str, optional): _description_. Defaults to str().
            senha (str, optional): _description_. Defaults to str().
        """
        self._senha = senha
        self._id=id

    def _criaParams(self, codEstacao: int, diaComeco: datetime, intervaloBusca="HORA_24", filtroData = "DATA_LEITURA", **kwargs) -> list:
        """
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

    def _defineQtdDownloadsSimultaneos(self, diasDownload):
        #Define a quantidade maxima de download simultaneos que serão realizados. 
        # Muitos downloads simultaneos podem gerar problema ?????
        # Valores arbitrários 
        if diasDownload <= 100:
            return 10
        else:
            return 20

    def requestTelemetricaDetalhada(self, estacaoCodigo: int, data: str, token: str, intervaloBusca="HORA_24", filtroData = "DATA_LEITURA"):
        """
        :param estacaoCodigo: Código de 8 dígitos
        :param data: Data dos dados requisitados. Formato yyyy-MM-dd.
        :param token: AcessToken adquirido
        :param filtroData:
        :param intervaloBusca: Intervalo das medições.
        :return: Objeto 'response'.
        """

        url = self.urlApi+ "/HidroinfoanaSerieTelemetricaDetalhada/v1"

        headers = {
            'Authorization': 'Bearer '+token
        }

        params = self._criaParams(estacaoCodigo)[0]

        return requests.get(url=url, headers = headers, params = params)

    def requestTelemetricaAdotada(self, estacaoCodigo: int, data: str, token: str, intervaloBusca="HORA_24", filtroData = "DATA_LEITURA"):
        """
        :param estacaoCodigo: Código de 8 dígitos
        :param data: Data dos dados requisitados. Formato yyyy-MM-dd.
        :param token: AcessToken adquirido
        :param filtroData:
        :param intervaloBusca: Intervalo das medições.
        :return: Objeto 'response'.
        """ 

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
        Realiza o login com o ID e senha cadastrados pela Agência Nacional de Águas.
        :param id: Identificador cadastrado.
        :param password: Senha cadastrada.
        :return: Objeto 'response'.
        """
        url = self.urlApi + '/OAUth/v1'
        headers = {'Identificador': self._id, 'Senha': self._senha}
        return requests.get(url=url, headers=headers)

    def forceRequestToken(self):

        token = self.requestToken()
        tentativas = 1  #melhorar lógica com TRY-EXCEPT (?)
        while(token.status_code!=200 and tentativas <5):
            token = self.requestToken()  
            tentativas = tentativas+1

        print(token.status_code)

        if(token.status_code==200):
            token = json.loads(token.content)
            itens = token['items']
            return itens['tokenautenticacao']
        else:
            print("Não foi possível requisitar o token. Finalizando aplicação")
            exit()

    async def requestTelemetricaAdotadaAsync(self, estacaoCodigo: int, stringComeco: str, stringFinal: str, headers: dict, qtdDownloadsAsync=None):

        diaFinal = datetime.strptime(stringFinal, "%Y-%m-%d")
        diaComeco = datetime.strptime(stringComeco, "%Y-%m-%d")

        #Total de dias que terão os dados baixados (se não exceder data atual. Ex: hoje ser dia 12/09 e tentar baixar até 31/12 pode dar erro)
        diasDownload = (diaFinal - diaComeco).days

        if qtdDownloadsAsync == None:
            qtdDownloadsAsync = self._defineQtdDownloadsSimultaneos(diasDownload)

        url = self.urlApi + "/HidroinfoanaSerieTelemetricaAdotada/v1"

        iteracao = 0
        respostaLista = list()
        while(iteracao * qtdDownloadsAsync <= diasDownload):
            params = self._criaParams(estacaoCodigo, diaComeco, diaFinal=diaComeco+timedelta(days=qtdDownloadsAsync))

            async with aiohttp.ClientSession(headers=headers) as session:
                tasks = []
                for param in params:
                    tasks.append(_download_url(session, url, param))
                resposta = await asyncio.gather(*tasks)
                respostaLista.append(resposta)

            diaComeco = diaComeco + timedelta(days=qtdDownloadsAsync)
            iteracao = iteracao + 1 
        return respostaLista
    
    async def requestTelemetricaDetalhadaAsync(self, estacaoCodigo: int, stringComeco: str, stringFinal: str, headers: dict, qtdDownloadsAsync=None) -> list:
        """_summary_

        Args:
            estacaoCodigo (int): Código da estação telemétrica
            stringComeco (str): Data do começo do período
            stringFinal (str): Data final do período (não incluida)
            headers (dict): Bearer Token

        Returns:
            list: Cada item da lista corresponde a um conjunto de tasks realizadas simultaneamente. Cada item é uma lista com dados de dias diferentes.
        """
        diaFinal = datetime.strptime(stringFinal, "%Y-%m-%d")
        diaComeco = datetime.strptime(stringComeco, "%Y-%m-%d")

        #Total de dias que terão os dados baixados (se não exceder data atual. Ex: hoje ser dia 12/09 e tentar baixar até 31/12 pode dar erro)
        diasDownload = (diaFinal - diaComeco).days

        if qtdDownloadsAsync == None:
            qtdDownloadsAsync = self._defineQtdDownloadsSimultaneos(diasDownload)

        url = self.urlApi + "/HidroinfoanaSerieTelemetricaDetalhada/v1"

        iteracao = 0
        respostaLista = list()
        while(iteracao * qtdDownloadsAsync <= diasDownload):
            params = self._criaParams(estacaoCodigo, diaComeco, diaFinal=diaComeco+timedelta(days=qtdDownloadsAsync))
            try:
                async with aiohttp.ClientSession(headers=headers) as session:
                    tasks = []
                    for param in params:
                        tasks.append(_download_url(session, url, param))
                    resposta = await asyncio.gather(*tasks)
                    respostaLista.append(resposta)

                diaComeco = diaComeco + timedelta(days=qtdDownloadsAsync)
                iteracao = iteracao + 1 
            except asyncio.TimeoutError as e:
                print("TIMEOUT")
                print(e)
            except ConnectionError as e:
                print('ERRO DE CONEXAO. CONFIRA INTERNET')
                print(e)
            except Exception as e:
                print(e) 
        return respostaLista

async def _download_url(session, url, params): 
    async with session.get(url, params=params) as response:
        return await response.content.read()

if __name__ =='__main__':
    pass