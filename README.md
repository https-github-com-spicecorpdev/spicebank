# Spicebank
## Introdução
Este repositório é utilizado para compartilhar o desenvolvimento e entregas do projeto integrado das disciplinas “Design Digital ”, “Desenvolvimento Web I” e “Engenharia de Software I”, realizado na Faculdade de Tecnologia de São José dos Campos (FATEC) - Professor Jassen Vidal. 

## Objetivo

O objetivo do projeto é criar um sistema para gerenciamento de transações em um banco digital fictício, visando monitorar e controlar operações bancárias de um banco digital, reduzindo as interações presenciais.

# Índice
- Introdução
- Objetivo
- Equipe
- Instruções
- Arquivos build
- Banco de Dados
- Product Backlog Atual
- Product Backlog Total
- Minimum Viable Product(MVP) 3ªSprint
- Cronograma de Entregas
- Tecnologias Utilizadas

# Equipe
||Integrantes|<div align="center"><img src="https://user-images.githubusercontent.com/86271800/194735815-b3fc4048-bce9-4a70-af44-36583c8ca0e7.png" width=115></div>|<div align="center"><img src="https://user-images.githubusercontent.com/86271800/194737247-64ed8ec4-2b71-46ff-8d22-539b4015d7be.png" width=115></div>|
|--|-----------|------|--------|
|<div align="center"><img src="https://user-images.githubusercontent.com/86271800/194735729-e1a6aea7-ec46-4318-83b1-51a4958f6fc1.jpeg" width=50></div>|**Aline Cristiane Correa Costa**|<div align="center">[GitHub](https://github.com/acorreac)</div>|<div align="center">[Linkedin](www.linkedin.com/in/alinecorrea)</div>|
|<div align="center"><img src="https://user-images.githubusercontent.com/86271800/194737529-8081336b-55c0-48fe-a852-b26fe1e15246.jpeg" width=50></div>|**Ana Tainara da Silva Rosa**|<div align="center">[GitHub](https://github.com/anatainararosa)</div>|<div align="center">[Linkedin](https://www.linkedin.com/in/anatainararosa/)</div>|
|<div align="center"><img src="https://user-images.githubusercontent.com/86271800/194737614-116ff444-4c9b-4448-b0b3-8dad2d650c4d.jpeg" width=50></div>|**Eshilley Hiury Minicucci Vianna Barbosa**|<div align="center">[GitHub](https://github.com/EshilleyBa)</div>|<div align="center">[]()</div>|
|<div align="center"><img src="https://user-images.githubusercontent.com/86271800/194737664-ca9340f1-9ed0-4c20-8230-0573abcca4dc.jpeg" width=50></div>|**Igor Pereira**|<div align="center">[GitHub](https://github.com/igorpereira28)</div>|<div align="center">[Linkedin](https://www.linkedin.com/mwlite/in/igor-da-silva-pereira-119794159)</div>|
|<div align="center"><img src="https://user-images.githubusercontent.com/86271800/194737706-47003b65-a94d-4562-8d9d-86c2fee022ba.jpeg" width=50></div>|Isabela Silva|<div align="center">[GitHub](https://github.com/Caris19)</div>|<div align="center">[]()</div>|
|<div align="center"><img src="https://user-images.githubusercontent.com/86271800/194737727-491badc5-6dfb-4648-af3e-1ba7be0d5a4d.jpeg" width=50></div>|**Vitor Garcez de Oliveira**|<div align="center">[GitHub](https://github.com/Vitaog)</div>|<div align="center">[Linkedin](https://www.linkedin.com/in/vitorgarcezdeoliveira/)</div>|




## Instruções
### Para utilizar o projeto será necessário seguir os seguintes passos:
Tenha instalado em sua máquina o Python 3.10 e o MariaDB 10.11; <br>
Vide o tópico Banco de Dados para inicialização do banco de dados criado <br>
1. No terminal, clone o repositório do projeto utilizando o comando: <br>
`git clone https://github.com/https-github-com-spicecorpdev/spicebank.git`<br>
1.1 Após realizar o “clone” do repositório, você pode criar um ambiente virtual* seguindo os seguintes comandos no terminal de sua máquina: <br>
`py-3 -m venv venv(criando um ambiente virtual com o nome venv`<br>
`python –m venv venv`<br>
*Ative o ambiente virtual de sua máquina com o comando:*<br>
`venv\Scripts\activate`<br>
**Essa etapa é opcional.*
2. No editor de código de sua preferência, abra a pasta do projeto clonado e instale as bibliotecas necessárias com os comandos:<br>
`pip install -r requirements.txt`
3. Se o sistema operacional for **Windows**, executar o arquivo usando o comando:
`$ build.bat`<br>
Se o sistema operacional for **Linux**, executar o arquivo usando o comando: 
`$ sh build.sh`<br>
4. Na pasta “backend/database” o arquivo “db-spicebank.sql” contém o script para criar e executar o banco de dados;
5. Para inicializar o projeto, entre na pasta “backend” e execute os seguintes comandos, cada comando em um terminal diferente:<br>
`flask run`<br>
`flask --app manager_app run --port 5001`
6. Acesse o aplicativo usando o link que que aparecerá no terminal para visualização das páginas, localhost:5000 e localhost:5001 <br>
**É necessário instalar todos os programas para o devido funcionamento do projeto!** 
7. *Informações da matricula e senha para login dos gerentes administrativos*

|Tipo|Matrícula|Senha|
|----|---------|-----|
|Gerente Geral|1000|123|
|Gerente de agência|1001|123|


## Arquivos build
O build é um arquivo que contém os comandos necessários para copiar arquivos HTML, CSS, imagens para pasta backend na qual se faz necessário tais arquivos para a correta execução e visualização da aplicação.


### Banco de Dados
Os passos para a utilização do banco de dados estão na pasta backend/database no arquivo commands-sql.txt

# Product Backlog Atual
<div align="center">
<img src="https://user-images.githubusercontent.com/86271800/203446332-0b6a6e9f-4f2e-4083-aac6-2c9e8d1d1341.png" width="1000px", height="610px", />
</div>

# Product Backlog Total
|Sprint|Requisitos|
|------|----------|
|1|Cadastro de Usuário|
|1|Login de Usuário|
|1|Operações de Depósito|
|1|Operações de Saque|
|2|Confirmação de Depósito e Saque|
|2|Comprovante de Depósito e Saque|
|2|Acompanhamento de Solicitação de Abertura de Conta|
|3|Extrato do Usuário|
|3|Alteração de Dados Cadastrais|
|3|Encerramento de Conta|
|3|Operações de Transferência|
|3|Funcionalidades Administrativas do Gerente de Agência|
|3|Comprovantes de Depósito, Saque e Transferência|
|3|Definição do Capital Inicial do Banco|
|3|Funcionalidades do Gerente Geral|
|4|Cadastro de Gerente de Agência|
|4|Criação de Agência|
|4|Gerenciamento de Agências|
|4|Atribuição de Agência e Conta ao Cadastrar o Usuário|
|4|Tipos de conta ( Conta Corrente e Conta Poupança)
|4|Alteração de Taxas Bancárias|
|4|Juros Compostos|

# Minimum Viable Product(MVP) 4ªSprint
- Cadastro de Gerente de Agência
- Criação de Agência
- Gerenciamento de Agências
- Atribuição de Agência e Conta ao Cadastrar o Usuário
- Tipos de Conta (Conta Corrente e Conta Poupança)
- Alteração de Taxas Bancárias
- Juros Compostos 

Gerente Geral
<div align="center">
<img src="https://user-images.githubusercontent.com/86271800/200212216-c498c5db-f595-4f19-ad5d-a271d366e817.png" width="1000px", height="500px", />
</div>
Gerente de agência
<div align="center">
<img src="https://user-images.githubusercontent.com/86271800/200212224-1082ad47-c162-419a-b1bc-320cb24e74c1.png" width="1000px", height="500px", />
</div>
Usuário comum
<div align="center">
<img src="https://user-images.githubusercontent.com/86271800/200212229-4ec75752-a0c0-43b9-8e12-5ed6ad4e3b62.png" width="1000px", height="500px", />
</div>


# Cronograma de Entregas* 
Foi utilizado o arquivo Product Backlog para validação das estregas de acordo com as prioridades do cliente, sendo elas: 
- Entrega I 18/9
- Entrega II 9/10
- Entrega III 6/11
- Entrega IV 27/11

# Tecnologias Utilizadas
  <img src="https://user-images.githubusercontent.com/86271800/194738779-f117d6f3-852b-40c1-a5ea-8fec628c3a15.png" width=115px>
  <img src="https://user-images.githubusercontent.com/86271800/194738843-7a2b8a5c-e9e1-48ba-88ac-d0a880f98878.png" width=115px>
  <img src="https://user-images.githubusercontent.com/86271800/194738872-9317607d-e5ab-42dc-8715-4091cf252ed4.png" width=115px>
  <img src="https://user-images.githubusercontent.com/86271800/194738913-a6d23a32-ee53-4958-b62e-bafdb78b79d3.png" width=115px>
  <img src="https://user-images.githubusercontent.com/86271800/194738937-05603160-1c22-490f-ab26-d49f3e87a400.png" width=115px>
  <img src="https://user-images.githubusercontent.com/86271800/203760512-54a6b091-ccbf-4b20-af20-57d6da50378d.png" width=115px>


