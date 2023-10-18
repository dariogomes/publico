# import de pacotes necessários
import pandas as pd
import json
import requests
import csv
import time
from datetime import datetime

# função para consulta de endereço utilizando o site VIACEP
def fn_consulta_viacep(cep):
    url = 'https://viacep.com.br/ws/' + cep + '/json/'
    endereco = json.loads(requests.get(url).text)
    
    return endereco

# faz o teste função fn_consulta_viacep consultando um endereço
cep_origem = '01001000'
endereco = fn_consulta_viacep(cep_origem)

if len(endereco) == 0:
    print(f"A consulta VIACEP não retornou dados, verifique se a função esta funcionando e tente novamente.")
    exit()

# faz a leitura do arquivo de credenciais
dir_json = "credenciais.json"
file = open(dir_json, 'r')
credencial = json.load(file)

# variavel com a sua chave de acesso a API do Google
strKey = credencial['credenciais'][0]['GoogleAPI_strKey']

# a API possui alguns modos de viagem podendo ser: BICYCLING, DRIVING, TRANSIT, WALKING 
# vamos utilizar o modo TRANSIT
modo = 'DRIVING'

# função para consulta de CEP origem destino Google API
def fn_consulta_rota(origem, destino, modo):
    strOrigem = origem.replace(' ', '+')
    strDestino = destino.replace(' ', '+')
    #, language='pt-BR'
    return requests.get('https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&language=pt-BR&mode='+modo+'&origins='
                     +strOrigem+'&destinations='+strDestino+'&key='+strKey)

# faz o teste função fn_consulta_rota com o endereço obtido no webservice VIACEP para o museu do ipiranga
origem = endereco['logradouro'] + ' - ' + endereco['bairro'] + ', ' + endereco['localidade'] + ', ' + endereco['uf'] + ', ' + endereco['cep'] + ', Brazil'
destino = "Avenida Nazaré - Ipiranga, São Paulo, SP, 04263-000, Brasil"
modo = 'transit'
response = fn_consulta_rota(origem, destino, modo)
rota = response.json()

if len(rota) == 0:
    print(f"A consulta Google API não retornou dados, verifique se a função esta funcionando e tente novamente.")
    exit()

# criaremos a função para realizar a consulta na API Distance Matrix do Google Maps e gerar o arquivo CSV com os resultados obtidos
def fn_consulta_api(df):
    
    # recebe o dataframe
    df = pd.DataFrame(data=df)
    
    # define as variável de apoio
    erros = 0

    # define o nome do arquivo conforme a data e hora de execução
    arquivo_id = datetime.today().strftime('%Y%m%d%H%M')
    arquivo = f"data\\ResultadoConsultaCEP_{arquivo_id}.csv"
    
    # lista a quantidade de registros para consultar em uma variável
    registros = len(df)

    # verifica se existe CEP para consultar
    if registros > 0:

        # cria o arquivo CSV com o resultado da consulta
        with open(arquivo, mode='w', newline='') as csv_file:
            writer = csv.DictWriter(
                csv_file
                , fieldnames=["ID"
                              , "CEP_ORIGEM"
                              , "CEP_DESTINO"
                              , "ENDERECO_ORIGEM"
                              , "ENDERECO_DESTINO"
                              , "LOCAL"
                              , "DISTANCIA"
                              , "DISTANCIA_VL"
                              , "TEMPO"
                              , "TEMPO_VL"
                              , "STATUS"
                              , "MODO"
                              , "LOGRADOURO"
                              , "BAIRRO"
                              , "CIDADE"
                              , "UF"
                              , "IBGE"
                              , "DDD"
                              , "OBSERVACAO"
                              , "ATUALIZADO EM"]
                , delimiter=';'
                , quotechar='"'
            )

            # escreve o cabeçalho no arquivo
            writer.writeheader()

            # faz a consulta da base de cpf
            print('Realizando a consulta...')
            # get da variaveis data hora inicio
            datatime_ini = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            print(f"Processo iniciado em: {datatime_ini}")

            # aplica um for para cada registro do dataframe
            for index, row in df_sample.iterrows():

                # flag variaveis
                atualizado_em = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                cep_origem = row['cep_origem'].replace('-', '').rstrip()
                cep_destino = row['cep_destino'].replace('-', '').rstrip()
                endereco_destino = row['endereco_destino']
                local = row['local']

                # consulta o endereço de origem em VIACEP
                endereco = fn_consulta_viacep(cep_origem)

                try:
                    endereco_origem = endereco['logradouro'] + ' - ' + endereco['bairro'] + ', ' + endereco['localidade'] + ' - ' + endereco['uf'] + ', '  + endereco['cep'] + ', Brazil'
                    status_endereco = 'OK'
                except:
                    status_endereco = 'ERRO'

                if status_endereco == 'OK':

                    # faz a consulta na API
                    try:                
                        # faz a consulta do CEP no Google API
                        # aguarda antes de executar o próximo passo
                        time.sleep(3)
                        response = fn_consulta_rota(endereco_origem, endereco_destino, modo)
                        rota = response.json()

                        # se a consulta retornar dados
                        if rota:

                            status = rota['rows'][0]['elements'][0]['status']

                            if status == 'NOT_FOUND' or status == 'ZERO_RESULTS':
                                status_rota = 'ERRO'
                                observacao = 'Falha ao realizar a consulta da rota NOT_FOUND/ZERO_RESULTS'
                            else:
                                status_rota = rota['rows'][0]['elements'][0]['status']
                                observacao = 'Rota OK'

                            try:
                                # grava o resultado no arquivo
                                writer.writerow({"ID": index
                                                , "CEP_ORIGEM": row['cep_origem']
                                                 , "CEP_DESTINO": row['cep_destino']
                                                 , "ENDERECO_ORIGEM": rota['origin_addresses'][0]
                                                 , "ENDERECO_DESTINO": rota['destination_addresses'][0]
                                                 , "LOCAL": row['local']
                                                 , "DISTANCIA": rota['rows'][0]['elements'][0]['distance']['text']
                                                 , "DISTANCIA_VL": str(rota['rows'][0]['elements'][0]['distance']['value'])
                                                 , "TEMPO": rota['rows'][0]['elements'][0]['duration']['text']
                                                 , "TEMPO_VL": str(rota['rows'][0]['elements'][0]['duration']['value'])
                                                 , "STATUS": rota['rows'][0]['elements'][0]['status']
                                                 , "MODO": modo
                                                 , "LOGRADOURO": endereco['logradouro']
                                                 , "BAIRRO": endereco['bairro']
                                                 , "CIDADE": endereco['localidade']
                                                 , "UF": endereco['uf']
                                                 , "IBGE": endereco['ibge']
                                                 , "DDD": endereco['ddd']
                                                 , "OBSERVACAO": observacao
                                                 , "ATUALIZADO EM": atualizado_em
                                            })
            
                            except Exception as e:
                                # falha ao gravar o resultado no arquivo
                                # acrescenta 1 a quantidade de erros e aguarda antes de executar o próximo passo
                                erros += 1
                                time.sleep(5) 
                                observacao = 'Falha ao gravar o resultado no arquivo'

                                # grava o resultado no arquivo
                                writer.writerow({"ID": index
                                                , "CEP_ORIGEM": row['cep_origem']
                                                 , "CEP_DESTINO": row['cep_destino']
                                                 , "ENDERECO_ORIGEM": endereco_origem
                                                 , "ENDERECO_DESTINO": endereco_destino
                                                 , "LOCAL": row['local']
                                                 , "DISTANCIA": "NULL"
                                                 , "DISTANCIA_VL": 0
                                                 , "TEMPO": "NULL"
                                                 , "TEMPO_VL": 0
                                                 , "STATUS": "ERRO"
                                                 , "MODO": modo
                                                 , "LOGRADOURO": endereco['logradouro']
                                                 , "BAIRRO": endereco['bairro']
                                                 , "CIDADE": endereco['localidade']
                                                 , "UF": endereco['uf']
                                                 , "IBGE": endereco['ibge']
                                                 , "DDD": endereco['ddd']
                                                 , "OBSERVACAO": observacao
                                                 , "ATUALIZADO EM": atualizado_em
                                            })

                        else:
                            erros += 1
                            time.sleep(5) # aguarda para realizar o próximo passo
                            print("Rota não definida")

                    except Exception as e:
                        # falha ao realizar a consulta na API Google
                        # acrescenta 1 a quantidade de erros e aguarda antes de executar o próximo passo
                        erros += 1
                        time.sleep(5)
                        print(f"[ERRO {index}] {e}")
                        print("Falha ao realizar a consulta na API Google")
                        print(str(index) + " [ERRO] Origem: " + cep_origem + " | Destino: " + cep_destino)
                        print(e)                    

                else:
                    # falha ao realizar a consulta na API VIACEP
                    # acrescenta 1 a quantidade de erros e aguarda antes de executar o próximo passo
                    erros += 1
                    time.sleep(5) 
                    
                    # grava o resultado no arquivo
                    writer.writerow({"ID": index
                                     , "CEP_ORIGEM": row['cep_origem']
                                     , "CEP_DESTINO": row['cep_destino']
                                     , "ENDERECO_ORIGEM": endereco_origem
                                     , "ENDERECO_DESTINO": endereco_destino
                                     , "LOCAL": row['local']
                                     , "DISTANCIA": "NULL"
                                     , "DISTANCIA_VL": 0
                                     , "TEMPO": "NULL"
                                     , "TEMPO_VL": 0
                                     , "STATUS": "ERRO"
                                     , "MODO": modo
                                     , "LOGRADOURO": "NULL"
                                     , "BAIRRO": "NULL"
                                     , "CIDADE": "NULL"
                                     , "UF": "NULL"
                                     , "IBGE": "NULL"
                                     , "DDD": "NULL"
                                     , "OBSERVACAO": "Falha ao realizar a consulta na API VIACEP"
                                     , "ATUALIZADO EM": atualizado_em
                                    })

    # flag data hora fim 
    datatime_fim = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    datatime_ini = datetime.strptime(datatime_ini, '%Y-%m-%d %H:%M:%S')
    datatime_fim = datetime.strptime(datatime_fim, '%Y-%m-%d %H:%M:%S')
    duracao = datatime_fim - datatime_ini

    # faz o print dos resultados
    print(f"Processo finalizado em: {datatime_fim}")
    print(f"Duração: {duracao}")
    print(f"Total de {str(registros)} registros atualizados e {str(erros)} erro(s)")
    print(f"Criado o arquivo {arquivo} com os dados da consulta")
    
    return

# abre o arquivo base excel
df = pd.read_excel('data\\Base CEP.xlsx', sheet_name='Base')

# vamos cria um dataframe de amostra randomica
df_sample = df.sample(n=100, random_state=42)

# a consulta será executada utilizando o dataframe de amostra e não a base completa 
fn_consulta_api(df_sample)