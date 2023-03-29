# cuisines_around_world
this repository was made for evaluation of restaurants and types of cuisines
'Cuisine Around the World' é uma plataforma  de análise sobre culinária e restaurantes pelo mundo. Ou seja, é uma ferramenta que facilita a pesquisa sobre tipos de culinária e restaurantes em vários países. Essa plataforma foi desenvolvida para atender a empresa Fome Zero.

# 1. Problema de negócio
A empresa Fome Zero é uma marketplace de restaurantes. Ou seja, seu core business é facilitar o encontro e negociações de clientes e restaurantes. Os restaurantes fazem o cadastro dentro da plataforma da Fome Zero, que disponibiliza informações como endereço, tipo de culinária servida, se possui reservas, se faz entregas, preço do prato servido e também uma nota de avaliação dos serviços e produtos dos restaurantes, dentre outras informações.

O desafio foi entender melhor o negócio para conseguir tomar as melhores decisões estratégicas e alavancar ainda mais a
Fome Zero fidelizando os restaurantes na plataforma, melhorando a performance dos restaurantes e para isso, foi feita uma análise nos dados das empresas cadastradas e gerar dashboards interativos.

O CEO Guerra também foi recém contratado e precisa tomar as melhores decisões estratégicas e a partir dessas análises, ele gostaria de ver algumas métricas e precisa responder às seguintes perguntas:

## Geral
1. Quantos restaurantes únicos estão registrados?
2. Quantos países únicos estão registrados?
3. Quantas cidades únicas estão registradas?
4. Qual o total de avaliações feitas?
5. Qual o total de tipos de culinária registrados?

## Países
1. Qual o nome do país que possui mais cidades registradas?
2. Qual o nome do país que possui mais restaurantes registrados?
3. Qual o nome do país que possui mais restaurantes com o nível de preço tipo gourmet registrados?
4. Qual o nome do país que possui a maior quantidade de tipos de culinária distintos?
5. Qual o nome do país que possui a maior quantidade de avaliações feitas?
6. Qual o nome do país que possui a maior quantidade de restaurantes que fazem entrega?
7. Qual o nome do país que possui a maior quantidade de restaurantes que aceitam reservas?
8. Qual o nome do país que possui, na média, a maior quantidade de avaliações registrada?
9. Qual o nome do país que possui, na média, a maior nota média registrada?
10. Qual o nome do país que possui, na média, a menor nota média registrada?
11. Qual a média de preço de um prato para dois por país?

## Cidades
1. Qual o nome da cidade que possui mais restaurantes registrados?
2. Qual o nome da cidade que possui mais restaurantes com nota média acima de 4?
3. Qual o nome da cidade que possui mais restaurantes com nota média abaixo de 2.5?
4. Qual o nome da cidade que possui o maior valor médio de um prato para dois?
5. Qual o nome da cidade que possui a maior quantidade de tipos de culinária distintas?
6. Qual o nome da cidade que possui a maior quantidade de restaurantes que fazem reservas?
7. Qual o nome da cidade que possui a maior quantidade de restaurantes que fazem entregas?
8. Qual o nome da cidade que possui a maior quantidade de restaurantes que aceitam pedidos online?

## Restaurantes
1. Qual o nome do restaurante que possui a maior quantidade de avaliações?
2. Qual o nome do restaurante com a maior nota média?
3. Qual o nome do restaurante que possui o maior valor de uma prato para duas pessoas?
4. Qual o nome do restaurante de tipo de culinária brasileira que possui a menor média de avaliação?
5. Qual o nome do restaurante de tipo de culinária brasileira, e que é do Brasil, que possui a maior média de avaliação?
6. Os restaurantes que aceitam pedido online são também, na média, os restaurantes que mais possuem avaliações registradas?
7. Os restaurantes que fazem reservas são também, na média, os restaurantes que possuem o maior valor médio de um prato para duas pessoas?
8. Os restaurantes do tipo de culinária japonesa dos Estados Unidos da América possuem um valor médio de prato para duas pessoas maior que as churrascarias americanas (BBQ)?

##  Tipos de Culinária
1. Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do restaurante com a maior média de avaliação?
2. Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do restaurante com a menor média de avaliação?
3. Dos restaurantes que possuem o tipo de culinária americana, qual o nome do restaurante com a maior média de avaliação?
4. Dos restaurantes que possuem o tipo de culinária americana, qual o nome do restaurante com a menor média de avaliação?
5. Dos restaurantes que possuem o tipo de culinária árabe, qual o nome do restaurante com a maior média de avaliação?
6. Dos restaurantes que possuem o tipo de culinária árabe, qual o nome do restaurante com a menor média de avaliação?
7. Dos restaurantes que possuem o tipo de culinária japonesa, qual o nome do restaurante com a maior média de avaliação?
8. Dos restaurantes que possuem o tipo de culinária japonesa, qual o nome do restaurante com a menor média de avaliação?
9. Dos restaurantes que possuem o tipo de culinária caseira, qual o nome do restaurante com a maior média de avaliação?
10. Dos restaurantes que possuem o tipo de culinária caseira, qual o nome do restaurante com a menor média de avaliação?
11. Qual o tipo de culinária que possui o maior valor médio de um prato para duas pessoas?
12. Qual o tipo de culinária que possui a maior nota média?
13. Qual o tipo de culinária que possui mais restaurantes que aceitam pedidos online e fazem entregas?


# 2. Premissas assumidas para a análise
<p>a) Marketplace foi o modelo de negócio assumido.</p>
<p>b) A análise foi feita nos cincos continentes e nas principais cidades onde existe elevado padrão culinário.</p>
<p>c) Os restaurates tem tipos de culinárias apreciadas e prestigiadas em suas cidades.</p>
<p>d) Os restaurantes tem serviços cúlinários que são acessiveis e de fácil disposição aos clientes.</p> 


# 3. Estratégia da solução
As análises foram desenvolvidas utilizando as métricas que refletem da empresa Fome Zero. Visão de crescimento, Visão de fidelização, visão de qualidade e bom atendimento.

Cada visão é representado pelos seguintes conjuntos de métricas.

<p>- Visão de crescimento da empresa:</p>
<p>i. número de países atendidos;
ii. número de restaurantes cadastrados;
iii. número de cidades atendidas;
iv. número de resturantes cadastrados;</p>


<p>- Visão de fidelização:</p>
<p>i. número de restaurantes avaliados;
ii. número de tipos de culinárias avaliadas;</p>

<p>- Visão de qualidade e acessibilidade:</p>
<p>i. número de restuarantes bem avaliados;
ii. preço do prato e avaliação do tipo de culinária;
iii. tipos de culinária bem avaliadas
iv. número de restaurantes que fazem reservas;
v. número de restaurantes que fazem entregas;
vi. número de restaurantes com pedidos online;</p>


# 4. Top 3 Insights de dados

<p> a) Existe um número baixo de restaurantes que fazem reservas e entregas.</p>
<p> b) Existem cidades com poucas variedades de tipos de culinária.</p>
<p> c) Cidades onde os preços estam acima de 4 do tipo gourmet são as que mais tem variedades de resturantes.</p>
<p> d) Existem poucos países participantes da marketingplace do Fome Zero.</p>

# 5. O produto final do projeto
O  Dashboard 'Cuisine Around the World' hospedado em uma cloud e disponivel para acessos em qualquer dispositivo conectado a internet fornece uma rápida análise aos tomadores de decições e uma visão ampla sobre restaurantes e culinária pelo mundo.


# 6. Conclusão
O objetivo do projeto era criar uma resposta as métricas e perguntas para CEO para apoiar nas decisões estratégicas da em presa Fome Zero.
A empresa Fome Zero pode mostrar aos seus clientes as várias oportunidades de melhorias e diversidade de culinárias ainda não ofertadas em várias cidades. Temos muitos restaurantes com avalições insatisfatórias, cidades com poucas variedades de culinárias, tipos de culinárias que com preços muito diferentes na mesma cidade, grande número de restaurantes que ainda não fazem reservas e entregas. Ou seja, existem muitas oportunidades a serem exploradas.

# 7. Próximo passos
<p> a) Adicionar novas visões de negócio</p>
<p> c) Continuar acompanhando os restaurantes do marketingplace</p>
<p> d) Adicionar mais restaurante a empresa e aumentar o número de partcipantes</p>
