import requests
import json
import csv


USER_API = "Enzo2";
KEY_API = "47820d2e-28f4-45a0-9b13-8731c6956d1e";
url = 'https://pabx.azuton.com/pabx/api.php'


f = open('empresas.csv', 'w', newline='')
writer = csv.writer(f)
writer.writerow(['cliente_id', 'nome'])


payload_init = {
    "autenticacao": {
      "usuario": USER_API,
      "token": KEY_API
     },
    "acao": "listar_clientes",
    "cliente_id": 0,
    "nome": "",
    "pos_registro_inicial": 0
  }
res_init = requests.post(url, data=json.dumps(payload_init))
resposta_init = res_init.json()
qnt_registros = resposta_init[ "qtd_total_resultados"]


count = 0
pos_reg = 0
contatos =0
#busca os clientes
while pos_reg <= int(qnt_registros):
    payload = {
        "autenticacao": {
        "usuario": USER_API,
        "token": KEY_API
         },
        "acao": "listar_clientes",
        "cliente_id": 0,
        "nome": "",
        "pos_registro_inicial": pos_reg
        } 

    res = requests.post(url, data=json.dumps(payload))
    resposta = res.json()
    qnt_retornados = resposta["qtd_resultados_retornados"]
  
    while count <= (int(qnt_retornados) - 1):
        cliente_id = resposta["dados"][count]["cliente_id"]
        nome = resposta["dados"][count]["nome"]
        print(f'{contatos+1}/{int(qnt_registros)}: {nome}')
        cliente_registro = [cliente_id, nome ] #dados da exportação
        writer.writerow(cliente_registro)
        contatos = contatos+1
        count = count+1
    


    pos_reg = pos_reg + 20
    count = 0