import requests
import json
import csv
import os
from pathlib import Path

USER_API = "Enzo2";
KEY_API = "47820d2e-28f4-45a0-9b13-8731c6956d1e";
url = 'https://pabx.azuton.com/pabx/api.php'


#lista de empresas
arquivo = open('empresas.csv',encoding="ISO-8859-1")
empresas = csv.DictReader(arquivo)


empresas_sucesso = []
tot_registros = 0
done = 0
ano = input("Digite o ano a ser bucado: ")
new_header = input("Quer que crie um cabeçalho novo? Apenas se for a primeira vez que tiver rodando(y/n): ").lower().strip()
for empresa in empresas:

    
    Path('./empresas/'+empresa['nome']).mkdir(exist_ok=True) #cria a pasta
    #cria cabeçalho
    f = open('./empresas/'+empresa['nome']+'/chamadas.csv', 'a', newline='')
    writer = csv.writer(f)
    if new_header == 'y':
        writer.writerow(['cdr_id','cliente_id','regiao_id','data','origem','destino','recurso','preco',
                    'status','status_descricao','duracao_chamada','link_gravacao','chamada_id'])

    done = done +1
    mesInit = 1
    mesEnd = 2
    pesquisa = 1
    while mesEnd <= 12:
        payload = {
            "autenticacao": {
              "usuario": USER_API,
              "token": KEY_API
             },
            "acao": "listar_historico_chamada",
            "tronco_id": 0, #não mexer
            "cliente_id": empresa['cliente_id'],
            "data_inicial": "01/"+str(mesInit)+"/"+ano,
            "hora_inicial": "00:00",
            "data_final": "01/"+str(mesEnd)+"/"+ano,
            "hora_final": "00:00",
            "ramal_origem": "", #não mexer
            "ramal_destino": "", #não mexer
            "numero_origem": "", #não mexer
            "numero_destino": "", #não mexer
            "tipo_exibicao": "tela", #não mexer
            "status": 0, #não mexer
            "email": "", #não mexer
            "chamada_id": "", #não mexer
            "pos_registro_inicial": 0,
            "quantidade": 10
            }
        
        print(f"({  round(((done / 224)*100),1) }%) {empresa['nome']} - Resultado (1/{pesquisa}/{ano} à 1/{pesquisa+1}/{ano}):")
        res = requests.post(url, data=json.dumps(payload))
        resposta = res.json()
        if resposta['http_response_code'] == 404:
            print("Nenhuma chamada encontrada nesse período")
        else:
            total_resultados = resposta['qtd_total_resultados']
            print(f"Encontrado {total_resultados} chamadas")
            pos_reg = 0
            total = 0
            if empresa['nome'] not in empresas_sucesso:
                empresas_sucesso.append(empresa['nome'])
            while pos_reg <= total_resultados:
                payload2 = {
                    "autenticacao": {
                      "usuario": USER_API,
                      "token": KEY_API
                     },
                        "acao": "listar_historico_chamada",
                        "tronco_id": 0, #não mexer
                        "cliente_id": empresa['cliente_id'],
                        "data_inicial": "01/"+str(mesInit)+"/"+ano,
                        "hora_inicial": "00:00",
                        "data_final": "01/"+str(mesEnd)+"/"+ano,
                        "hora_final": "00:00",
                        "ramal_origem": "", #não mexer
                        "ramal_destino": "", #não mexer
                        "numero_origem": "", #não mexer
                        "numero_destino": "", #não mexer
                        "tipo_exibicao": "tela", #não mexer
                        "status": 0, #não mexer
                        "email": "", #não mexer
                        "chamada_id": "", #não mexer
                        "pos_registro_inicial": pos_reg,
                        "quantidade": 500
                        }
                res2 = requests.post(url, data=json.dumps(payload2))
                resposta2 = res2.json()
                # print(json.dumps(payload2, indent=4))
                # print(json.dumps(resposta2, indent=4))
                count = 0
                while count <= int(resposta2['qtd_resultados_retornados'])-1:
                    cdr_id = resposta2["dados"][count]["cdr_id"]
                    cliente_id = resposta2["dados"][count]["cliente_id"]
                    regiao_id = resposta2["dados"][count]["regiao_id"]
                    data = resposta2["dados"][count]["data"]
                    origem = resposta2["dados"][count]["origem"]
                    destino = resposta2["dados"][count]["destino"]
                    recurso = resposta2["dados"][count]["recurso"]
                    preco = resposta2["dados"][count]["preco"]
                    status = resposta2["dados"][count]["status"]
                    status_descricao = resposta2["dados"][count]["status_descricao"]
                    duracao_chamada = resposta2["dados"][count]["duracao_chamada"]
                    link_gravacao = resposta2["dados"][count]["link_gravacao"]
                    chamada_id = resposta2["dados"][count]["chamada_id"]
                    chamada_registro = [cdr_id,cliente_id,regiao_id,data,origem,destino,recurso,preco,
                                        status,status_descricao,duracao_chamada,link_gravacao,chamada_id]
                    writer.writerow(chamada_registro)
                    count = count +1
                    total = total +1
                    tot_registros = tot_registros +1
                    print(f'{total}/{total_resultados}')
                pos_reg = pos_reg +500


        mesEnd = mesEnd +1
        mesInit = mesInit +1
        pesquisa = pesquisa+1

        print('\n\n\n')
print(f'Foram encontrados {tot_registros} registros em {len(empresas_sucesso)} empresas!')
revelar = input("Deseja visualizar as empresas que foram exportadas? (y/n)")
if revelar == 'y':
    print(empresas_sucesso)