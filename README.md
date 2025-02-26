# Sobre 
Esta biblioteca foi desenvolvida para facilitar o acesso aos dados hidrológicos disponibilizados pela Agência Nacional de Águas e Saneamento Básico (ANA) por meio de sua API e não possui nenhuma afiliação ou relação com a ANA.

# Como requisitar dados
Snipet de código

```
    from hidroapi import Access

    sessao =  Access("ID", "SENHA")
    acesso = login_valido_fixture
    token = acesso.safe_request_token()
    tipo = 'Adotada'
    retorno = asyncio.run(acesso.request_telemetrica(85900000, '2020-01-01', '2020-01-5', token, tipo))
```