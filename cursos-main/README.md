# Sistema Escolar

Este é um sistema escolar simples desenvolvido em Python usando Flask e MySQL. Ele permite gerenciar alunos, cursos, faltas, inscrições, matrículas, pessoas, planos de aula, professores, secretarias, turmas e turmas de professores.

## Requisitos

- Python 3.x
- Flask
- MySQL

## Configuração

1. Clone este repositório.
2. Crie um ambiente virtual Python.
3. Instale as dependências do Python: `pip install Flask` e `pip install mysql-connector-python`.
4. Configure o banco de dados MySQL no arquivo `app.py`.
5. Execute o arquivo `app.py` para iniciar o servidor Flask.

## Estrutura do Banco de Dados

O banco de dados MySQL possui as seguintes tabelas:

- alunos
- cursos
- faltas
- inscricoes
- matriculas
- pessoas
- planos
- professores
- secretarias
- turmas
- turmas_professores


DIA 28/03/2024
Feitos até agora
criação das páginas de inserção de secretarias, pessoas e trabalhando na inserção de alunos, a parte de visualização de alunos. modularizei pessoas e secretarias, logo logo irei modularizar alunos e fechar essa parte também

DIA 01/04/2024
Feitos até agora. Estou trabalhando em uma ferramenta em alunos que pesquisa os valores em um campo input e retorna um datalist(lista) com os nomes próximos ao pesquisado, está na aba alunos-form a criação da lógica e na rota nomes-proximos no arquivo app.py