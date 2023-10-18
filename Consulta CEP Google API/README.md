# Coletar dados de tempo e distância através do CEP no Google Maps usando Python

### Introdução:
No mundo atual, dados precisos de tempo e distância são essenciais para uma ampla gama de aplicativos, desde logística até planejamento urbano. O Google Maps fornece um serviço poderoso chamado Distance Matrix API, que permite obter informações precisas sobre tempos de viagem e distâncias entre diferentes pontos. Neste artigo, você aprenderá como construir um processo para coletar esses dados utilizando Python e a API Distance Matrix do Google Maps.
Os dados obtidos são muito utilizados nas empresas para auxiliar na roteirização e demais aplicações que utilizam a geolocalização em seu negócio.

### Objetivo:
Será utilizado uma base de CEP com a origem e destino como referência para calcular o tempo e distância entre dois pontos, também enriquecer a base com os dados: BAIRRO, CIDADE, UF, IBGE e DDD.
No final será gerado um arquivo CSV com os dados obtidos para serem utilizados em um outro momento. A criação do arquivo será realizada através da função "writer.writerow" e pode muito bem ser modificada afim de simplificar o código com menos linhas de código algo do tipo.

### Configuração Inicial:

##### Distance Matrix
Antes de começar, você precisa ter uma conta no Google Cloud Platform (GCP) e criar um projeto para obter a chave de API necessária para acessar o serviço Distance Matrix. Siga as etapas de criação do projeto e geração da chave de API no console do GCP.
O serviço possui limitações no uso gratuito e pode haver cobranças caso a quantidade de requisições ultrapasse os limites estabelecidos, sugiro consultar a documentação para maiores detalhes em: https://developers.google.com/maps/documentation/javascript/distancematrix

##### VIACEP
Será utilizado o webservice gratuito para consultar o CEP através da url https://viacep.com.br/

##### Credenciais.json
Renomear o arquivo "credenciais-modelo.json" para "credenciais.json" e altere o valor da variável "GoogleAPI_strKey" com a chave de acesso ao serviço do GCP.
