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

## Configuração Tailwind

1. Execute o comando node -v em seu terminal para verificar se tem ele instalado.
2. Caso não tenha instalado, procure pelo node em seu navegador e faça a instalação.
3. Após a instalação do node, caso seja necessário, execute o comando npm init -y em seu terminal, ele deve criar um arquivo chamado package.json no seu diretório de pastas.
4. Agora vamos a instalação do tailwind em sua máquina.
5. https://tailwindcss.com/docs/installation nesse link você tem o guia de instalação do tailwind
6. No passo 2 do guia de instalação do tailwind coloque esse endereço "cursos-main/templates/**/*.{html,js}" dentro de content
7. Na pasta static, crie um arquivo .css e aplique os estilos que estão no passo 3 do guia de instalação do tailwind.
8. Após realizar essas ações, execute o seguinte script em seu terminal.
npx tailwindcss -i cursos-main/static/style.css -o cursos-main/static/output.css --watch.
9. Feio isso, o tailwind já deve estar instalado em sua máquina.
10. Agora voltando ao passo 3, abra o arquivo package.json e encontre a chave scripts e cole o seguinte comando dentro das chaves,
"tailwind":" npx tailwindcss -i cursos-main/static/style.css -o cursos-main/static/output.css --watch"
11. Após colar o comando, execute em seu terminal o script npm run tailwind.
12. Agora abra uma nova aba em seu terminal, clicando no + no canto superior direito da janela do terminal
13. De um cd cursos-main, de um enter, depois rode o seguinte script python app.py
14. Ele deve retornar um link de uma url

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

DIA 13/04/2024
Criei uma ferramenta para adicionar e pesquisar professores em que os não há obrigatoriedade dos campos na pesquisa.
A busca pode ser feita utilizando um ou mais campos.
Na parte de adicionar um novo professor, criei um campo input em que a pessoa deve inserir o nome e, uma lista de opções próximas ao valor em que ela digitou no campo. Isso deve otimizar as pesquisas ao banco, já que agora estamos pesquisando valore específicos da tabela.

DIA 15/04/2024
Criei uma ferramenta de pesquisa de cursos que tem um funcionamento semelhante ao de professores, onde os campos não são obrigatórios para pesquisa. Você pode pesquisar tanto pelo nome do curso quanto pela secretaria ou por ambos.
Na parte de adicionar um curso, criei restrições para que todos os campos estejam preenchidos ao enviar o formulário, caso os campos não estejam condizentes com a minha condição o formulário não é enviado.

DIA 16/04/2024
A ferramenta de turmas funciona basicmante da mesma maneira que a de cursos.




