# hidroaccess

![Alt](docs/images/ecotec.png "Identidade visual do grupo de pesquisa Ecotecnologias")
## Sumário
- [Sobre](#sobre)
- [Instalação](#instalação)
- [Uso](#uso)
    - [Access](#classe-access)
    - [safe_request_token](#método-safe_request_token)
    - [request_telemetrica](#método-request_telemetrica)
    - [atualizar_credenciais](#método-atualizar_credenciais-confirmar-código)

- [Contato](#contato)

# Sobre 
Esta biblioteca foi desenvolvida para facilitar a automatização do acesso aos dados hidrológicos disponibilizados pela Agência Nacional de Águas e Saneamento Básico (ANA) por meio de sua API e não possui nenhuma afiliação ou relação com a ANA.

# Instalação
A versão mais recente do pacote pode ser instalado através da ferramenta *pip* com o comando

```
pip install hidroaccess
```
Também é possível acessar o código fonte e as versões de desenvolvimento através do repositório no [Github](https://github.com/mBrond/hidroaccess).

# Uso
## Classe *Access*
A classe Access funciona como uma 'sessão', através dela as comunicações com a API são realizadas. Os parâmetros de inicialização são seus ID e Senhas adquiridos previamente.
```
from hidroaccess import access

sessao = access.Access("SEU_ID", "SUA_SENHA")
```

## Método *safe_request_token()*
Retorna um token (str) para validação de outras requisições. A obtenção do token é dependente das credencias utilizadas na criação do objetao Access. Caso alguma das credenciais sejam inválidas, retorna '-1'.
```
token = sessao.safe_request_token()
```
## Método *request_telemetrica()*
Obtem dados de uma estação telemétrica. Parâmetros:

- estacao_codigo (int): valor númerico de oito dígitos correspondente a estação para consulta desejada
- data_inicio (str): data inicial do período de consulta no formato YYYY-MM-DD
- data_fim (str): data final do período de consulta no formato YYYY-MM-DD
- token (str): token válido adquirido em *safe_request_token()* 
- tipo_dado ('Adotada' ou 'Detalhada'): Opcional, por padrão as requisições solicitam os dados Adotados. Os dados Detalhados retornam mais variáveis. 

Retorno: Lista de dicionários. Cada dicionário possui a chave 'Hora_Medicao' com a data e horário da medição correspondente.

```
estacao_codigo = 85900000
data_inicio = '2020-01-01'
data_fim = '2020-01-05'
tipo_dado = 'Detalhada'

retorno = sessao.request_telemetrica(estacao_codigo, data_inicio, data_fim, token, tipo_dado)
```

## Método *atualizar_credenciais()* CONFIRMAR CÓDIGO
Sobreescreve as credenciais utilizadas para criar o objeto.
```
sessao.atualizar_credenciais("NOVO ID", "NOVA SENHA")
```

# Contato
Para mais informações sobre o projeto, sugestões ou reportar erros:
- Desenvolvedor: brondani.miguel@gmail.com
- Grupo de Pesquisa: eco@ecotecnologias.org
- [Github](https://github.com/mBrond/hidroaccess)