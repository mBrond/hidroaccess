# Notas de atualização
## Métodos obsoletos removidos:
- _requestTelemetricaDetalhadaAsync_
- _requestTelemetricaAdotadaAsync_
- _requestTelemetricaAdotada_
- _requestTelemetricaDetalhada_


## Access
- Criado atributo _max_dias_convencional_ para controlar a maior data que requisicoes de Sedimentos e Convencional conseguem realizar 
- Método privado __seleciona_url_convencionais_ para selecionar o URL do endpoint de acordo com o tipo da estação.

### requests
- Adicionado __request_sedimentos()_ , __request_cota()_ , __request_chuva()_ para requisitar dados de sedimentos, cotas e chuvas de estações convencionais.

## Arquivo decodes
- Implementado __decode_request_cota_, __decode_request_chuva_ __decode_request_sedimento_, __decode_request_adotada_, __decode_request_detalhada_. Recebem um objeto _request_ e retornam um dicionário com as informações da estação do tipo correspondente a função.
- Criado _decode_list_bytes_ para receber listas das requisições e chamar as funções __decode_request_ correspondentes ao tipo informado.
- Lógica certamente será melhorada em patchs futuros.
