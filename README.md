# Projeto: Sabores Pelo Mundo

## Contexto do Problema de Negócio

A Sabores Pelo Mundo é uma empresa de marketplace de restaurantes, cujo objetivo principal é conectar clientes e  restaurantes de maneira eficiente. Por meio da plataforma, os restaurantes podem se cadastrar e disponibilizar informações como tipo de culinária servida e nota de avaliação recebida pelos clientes.

O CEO da Sabores Pelo Mundo, Kleiton Guerra, foi recentemente contratado e precisa de uma compreensão detalhada sobre o negócio para tomar decisões estratégicas e alavancar a empresa. Para isso, é necessária uma análise dos dados disponíveis na empresa e a criação de dashboards que apresentem respostas para perguntas chaves relacionadas aos restaurantes, países, cidades, tipos de culinária e outros aspectos relevantes.

## Objetivo do Projeto

Desenvolver uma solução baseada em dados para responder às principais perguntas do CEO da Sabores Pelo Mundo e criar um dashboard interativo que permita a visualização das informações de forma clara e objetiva.

### Perguntas a Serem Respondidas:

### Geral:

Quantos restaurantes únicos estão registrados?

Quantos países únicos estão registrados?

Quantas cidades únicas estão registradas?

Qual o total de avaliações feitas?

Qual o total de tipos de culinária registrados?

### Países:

Qual o nome do país que possui mais cidades registradas?

Qual o nome do país que possui mais restaurantes registrados?

Qual o nome do país que possui, na média, a maior quantidade de avaliações registrada?

Qual a média de preço de um prato para dois por país?

### Cidades:

Qual o nome da cidade que possui mais restaurantes registrados?

Qual o nome da cidade que possui mais restaurantes com nota média acima de 4?

Qual o nome da cidade que possui mais restaurantes com nota média abaixo de 2.5?

Qual o nome da cidade que possui a maior quantidade de tipos de culinária distintas?

###  Culinárias:

Qual o nome do restaurante que possui a maior quantidade de avaliações?

Qual o nome do restaurante com a maior nota média?

Qual o nome do restaurante que possui o maior valor de um prato para duas pessoas?


## Premissas assumidas para a análise:

Marketplace foi o modelo de negócio assumido.
As 4 principais visões do negócio foram: Visão Geral, Visão Países, Visão Cidades e Visão Culinárias.


## Estratégia da solução:

O painel estratégico foi desenvolvido utilizando as métricas que refletem as 4 principais visões do modelo de negócio da empresa:
- Visão Geral
- Visão Países
- Visão Cidades
- Visão Culinárias

### Visão geral:
- Restaurantes cadastrados
- Países cadastrados
- Cidades cadastradas
- Total de avaliações na plataforma
- Total de culinárias oferecidas


### Visão Países:
- Restaurantes cadastrados por país
- Cidades cadastradas por país
- Média de avaliação feitas por país
- Média de preço de um prato para duas pessoas por país

### Visão Cidades:
- Top 10 cidades com mais restaurantes na base de dados
- Top 7 cidades com restaurantes com média de avaliação acima de 4
- Top 7 cidades com restaurantes com média de avaliação abaixo de 2,5
- Top 10 cidades com mais restaurantes com tipo culinários distintos

### Visão Culinárias:
- 5 melhores restaurantes dos principais tipos culinários
- Top 10 restaurantes
- Top 10 melhores tipos de culinárias
- Top 10 piores tipos de culinárias


## Top 3 insights de dados

- Brasília e Rio de Janeiro lideram o ranking dos top 7 restaurantes que possuem avaliação média abaixo de 2,5/5.0.

- A Índia possui a maior quantidade de restaurantes cadastrados com 36,2%. Já a Indonesia aparece em último com apenas 0,8%.

- Mint Leaf Of London é o restaurante que possui a maior média de avaliações 4.9/5.0 e possui a maior quantidade de votos 2092.


## O produto final do projeto

Painel online, hospedado em um Cloud e disponível para acesso em qualquer dispositivo conectado à internet.
O painel pode ser acesso através desse link: https://saborespelomundo.streamlit.app/


## Conclusão

O objetivo desse projeto é criar um conjunto de gráficos e/ou tabelas que exibam essas métricas da melhor forma possível para o CEO.
Da visão Países, podemos concluir que a Indonesia e Austrália lideram o ranking na categoria Média de Preço mais caro em prato para duas pessoas. Já Canadá e England possuem a média de preço mais econômica em prato para duas pessoas.

## Próximos passos

- Gerar métricas temporais para acompanhamento.
- Criar novos filtros.
- Adicionar novas visões de negócio.

