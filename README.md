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
- Dependências do Projeto
- Arquivos build
- Banco de Dados
- Cronograma de Entregas
- Tecnologias Utilizadas

# Equipe

**Aline Cristiane Correa Costa**<br>
GitHub: https://github.com/acorreac          
Linkedin: https://www.linkedin.com/in/alinecorrea/<br><br>
**Ana Tainara da Silva Rosa**  
GitHub: https://github.com/anatainararosa          
Linkedin: https://www.linkedin.com/in/anatainararosa/<br><br>
**Eshilley Hiury Minicucci Vianna Barbosa**<br>
GitHub: https://github.com/EshilleyBa<br><br>
**Igor Pereira**<br> 
GitHub : https://github.com/igorpereira28<br><br>
**Isabela Silva**<br>
GitHub: https://github.com/Caris19<br><br>
**Vitor Garcez de Oliveira**<br>
GitHub: https://github.com/Vitaog                           
Linkedin: https://www.linkedin.com/in/vitorgarcezdeoliveira/<br>


## Instruções
1. No terminal clonar o repositorio do projeto com o comando git clone https://github.com/https-github-com-spicecorpdev/spicebank.git
2. Acessar a pasta do projeto clonado
3. Instale todos os pacotes python necessarios usando o comando: pip install -r requirements.txt
4. Se o sistema operacional for Windows, executar o arquivo usando o comando: build.bat
5. Se o sistema operacional for Linux, executar o arquivo usando o comando: sh build.sh
6. Instalar todos os programas para o devido funcionamento do projeto
7. Na pasta backend/database o arquivo 'command-sql.txt' contém um passo a passo de como criar e executar o banco de dados
8. Para inicializar o projeto entre na pasta backend e execute o seguinte comando: flask run
9. Acesse o aplicativo usando o link que aparecerá para visualização das páginas, geralmente localhost:5000

## Dependências do Projeto
- flask;
- flask session
- mariadb 1.0.1
- Python 3.8
- requirements.txt


## Arquivos build
O build é um arquivo que contém os comandos necessários para copiar arquivos HTML, CSS, imagens para pasta backend na qual se faz necessário tais arquivos para a correta execução e visualização da aplicação.


### Banco de Dados
Os passos para a utilização do banco de dados estão na pasta backend/database no arquivo commands-sql.txt

# Product Backlog Atual
|  ID    | Sprint  | User Story  |   Critério de Aceitação  |  Teste de Aceitação   |
| -------|---------|-------------|--------------------------|-----------------------|
| US05   |    2    | Eu, enquanto desenvolvedor, desejo ajustar as funcionalidades do saque, para que a visualização do saldo ao sacar seja de até duas casas decimais.| Realizar saque com valores com duas casas decimais.| Se sua operação for realizada com sucesso,  o saldo atual será visualizado com até duas casas decimais.|
|US06| 2  | Eu, enquanto desenvolvedor, desejo modificar o layout da tela de cadastro do usuário, para acrescentar dados do usuário ao se cadastrar.| Visualização da tela com os dados de usuário acrescentados.| Se os dados de usuário acrescentados forem visualizados, será possível realizar o cadastro dos usuários com os novos dados.|
|US07| 2| EU, enquanto desenvolvedor, desejo criar a tela de login do usuário especializado, para que seja possivel criar um gerente de agência e o mesmo possa realizar login.|Tela de Login para usuário especializado com validação de acesso através de agencia, conta e senha.|Se a funcionalidade de validação for implementada aparecerá print de validação de acesso no terminal do desenvolvedor e na tela de teste. Caso contrário aparecerá print de erro no terminal e na tela de teste do desenvolvedor para que o mesmo possa corrigi-lo.|
|US08|2| EU, enquanto gerente de agência, desejo solicitar abertura de conta,para fazer acesso a mesma.|Preencher nome completo, cpf, endereço, gênero, data de nascimento, senha.|Se preenchido tudo corretamente, deverá levar para página de acesso de conta. Caso contrário, deverá aparecer em destaque qual o erro digitado ou complemento faltante.|
|US09| 2| EU, enquanto gerente de agência, desejo acessar minha conta, para poder fazer transações.|Preencher usuário com agência, conta e senha, que foram solicitados na página cadastro.|Se preenchido corretamente o login e senha, deverá levar para página home; Caso contrário, deverá falar ''Senha/Agência ou conta Incorretos'' ou ''Cadastro Não Encontrado''.|
|US10|2|EU, enquanto gerente de agência, desejo ter acesso a tela de confirmação de conta, para validar abertura de contas de usuário comum.|Estar logado através de validação de agência, conta e senha.|Se o gerente de agência estiver validado o acesso através do login, o mesmo será direcionado a tela de confirmação de conta. Caso contrário será direcionado para a tela de login para efetuar a validação de acesso.|
|US11| 2| Eu, enquanto usuário, desejo visualizar a tela de confirmação de depósito, para ter segurança da operação que desejo efetuar.|Usuário deverá estar logado, e na tela de depósito deverá ser preenchido o valor de depósito maior que 0 reais, e clicado no botão de depositar.|Se a tela de confirmação de depósito for visualizada haverá um botão de confirmação da operação. Caso contrário aparecerá a mensagem de efetuar login, ou a mensagem de que o valor deverá ser maior que 0 reais.|
|US12| 2| Eu, enquanto usuário, desejo visualizar a tela de confirmação de saque, para ter segurança da operação que desejo efetuar.|Usuário deverá estar logado, e na tela de saque deverá ser preenchido o valor de saque maior que 0 reais, e clicado no botão de sacar.|Se a tela de confirmação de saque for visualizada haverá um botão de confirmação da operação. Caso contrário aparecerá a mensagem de efetuar login, ou a mensagem de que o valor deverá ser maior que 0 reais.|
|US13|2|Eu, enquanto usuário, desejo visualizar a tela de comprovante de depósito, para ter segurança da operação que desejo efetuar.|Usuário deverá estar logado, na tela de confirmação de depósito e ter clicado no botão de confirmar depósito.|Se a tela de comprovante for visualizada, o comprovante será mostrado na tela. Caso contrario será direcionado para tela de login.|
|US14| 2| Eu, enquanto usuário, desejo visualizar a tela de comprovante de saque, para ter segurança da operação que desejo efetuar.|Usuário deverá estar logado, na tela de confirmação de saque e ter clicado no botão de confirmar saque.|Se a tela de comprovante for visualizada, o comprovante será mostrado na tela. Caso contrario será direcionado para tela de login.|
|US15|2|Eu, enquanto usuário, desejo acessar a tela de extrato, para ver o histórico de movimentações.|Visualizar histórico de movimentações.|Se usuário logado o mesmo poderá acessar a tela de extrato.Caso contrário o usuário será direcionado para a tela de login para validação de acesso.|
|US16|2|Eu, enquanto usuário comum, desejo acompanhar minha solicitação de abertura de conta para após confirmado saber minha agência e conta.|O usuário deverá preencher com o CPF e senha e clicar no botão "Acompanhar abertura de conta".|Se os dados forem prenchidos corretamente e a solicitação de abertura for aprovada, a agência e conta será mostrada na tela. Caso contrário, uma mensagem dizendo que a solicitação está em analise será mostrada.|

# Product Backlog Total
<div align="center">
<img src="https://user-images.githubusercontent.com/86271800/194734847-efdff6b6-4333-44db-8a7b-91335cea0ede.png" width="1000px", height="10000px", />
</div>
<div align="center">
<img src="https://user-images.githubusercontent.com/86271800/194734995-38015285-74bf-4125-adaa-bc1f53817f72.png" width="1000px", height="10000px", />
</div>


# Minimum Viable Product(MVP) 2ªSprint
- Tela de Login de usuário personalizado (Navegavél e funcional)
- Tela Administrativas de Gerente de Agência (Navegavél e funcional)
- Tela de Comprovante de Saque e Depósito (Navegavél e funcional)
- Tela de Status de Solicitação de Conta (Navegavél e funcional)
- Tela de Extrato (Navegavél e funcional)


# Cronograma de Entregas 
Foi utilizado o arquivo Product Backlog para validação das estregas de acordo com as prioridades do cliente, sendo elas: 
- Entrega I 18/9
- Entrega II 9/10
- Entrega III 6/11
- Entrega IV 27/11

# Tecnologias Utilizadas
 - Flask
 - Python
 - MariaDB
 - HTML
 - CSS


