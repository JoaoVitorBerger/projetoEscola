import mysql.connector
from flask import request
from datetime import datetime
from unidecode import unidecode

def pesquisar_nomes_proximos_turma(conn,dados):
    #função que fornece um datalist com os nomes próximos ao valor digitado no input em adicionar aluno
    try:
        cursor = conn.cursor(dictionary=True)
        dados = request.json  # Acesse os dados enviados no corpo da solicitação
        print(dados)
        if dados['nome'].strip():  # Verifica se o valor não está vazio após remover espaços em branco
            nome_inserido = dados['nome'].strip().upper()
            cursor.execute('SELECT nome AS nome_turma, id AS id_turma from turmas WHERE nome LIKE %s GROUP BY turmas.nome', ('%' + nome_inserido + '%',))
            nomes_encontrados = cursor.fetchall()
            nomes_semelhantes = [(nome['nome_turma'], nome['id_turma']) for nome in nomes_encontrados]
            return nomes_semelhantes  # Certifique-se de que está retornando JSON
    except mysql.connector.Error as err:
          return f'Erro ao buscar dados: {err}'
    
def pesquisar_nomes_proximos_inscrito(conn,dados):
    
    #função que fornece um datalist com os nomes próximos ao valor digitado no input em adicionar aluno
    try:
        cursor = conn.cursor(dictionary=True)
        dados = request.json  # Acesse os dados enviados no corpo da solicitação
        print(dados)
        if dados['nome'].strip():  # Verifica se o valor não está vazio após remover espaços em branco
            nome_inserido = dados['nome'].strip().upper()
            cursor.execute('''SELECT
						  id_inscricao AS numero_inscricao,
                          id_aluno,
                          pessoas.nome AS nome_inscrito
                          FROM matriculas
                          JOIN inscricoes on inscricoes.id = matriculas.id_inscricao
                          JOIN alunos on alunos.id = inscricoes.id_aluno
                          JOIN pessoas on pessoas.id = alunos.id_pessoa 
						  WHERE pessoas.nome LIKE %s
                          GROUP BY pessoas.nome ''', ('%' + nome_inserido + '%',))
            nomes_encontrados = cursor.fetchall()
            nomes_semelhantes = [(nome['numero_inscricao'], nome['nome_inscrito']) for nome in nomes_encontrados]
            return nomes_semelhantes  # Certifique-se de que está retornando JSON
    except mysql.connector.Error as err:
          return f'Erro ao buscar dados: {err}'
    
def enviar_valores_matricula(conn):
    try:
        cursor = conn.cursor()
        data_inicio = request.form['data_inicio']
        data_fim = request.form['data_fim']
        id_turma = request.form['id_turma_hidden']
        id_inscrito = request.form['id_inscrito_hidden']
        cursor.execute('INSERT INTO matriculas (data_inicio, data_fim, id_turma, id_inscricao,criado_em) VALUES ( %s, %s, %s, %s, %s)', 
                       ( data_inicio,data_fim,id_turma,id_inscrito, datetime.now()))
        conn.commit()
        return 
    except mysql.connector.Error as err:
        return f'Erro ao adicionar aluno: {err}'

def pesquisar_valores_matriculas(conn):
    try:
        
        cursor = conn.cursor(dictionary=True)
        query = '''SELECT 
                    pessoas.nome AS nome_pessoa, 
                    alunos.ra, 
                    pessoas.cpf,
                    turmas.nome AS nome_turma,
                    turmas.descricao AS descricao_turma,
                    turmas.capacidade,
                    turmas.data_inicio,
                    turmas.data_fim,
                    cursos.nome AS nome_curso,
                    cursos.descricao AS descricao_curso,
                    matriculas.id AS id_matricula,
					CASE WHEN matriculas.ativo_flag  = 1 THEN 'MATRICULADO' ELSE 'NAO MATRICULADO' END AS status_matricula
                    FROM matriculas
                    JOIN inscricoes on inscricoes.id = matriculas.id_inscricao
                    JOIN alunos on alunos.id = inscricoes.id_aluno
                    JOIN pessoas on pessoas.id = alunos.id_pessoa
                    JOIN turmas on turmas.id = matriculas.id_turma
                    JOIN cursos on cursos.id = turmas.id_curso
                    WHERE 1=1 AND matriculas.deletado_em IS NULL
                '''
        
        
        ra_aluno = request.form['ra_aluno']
        cpf_aluno = request.form['cpf_aluno']
        nome_turma = request.form['nome_turma']

        
        params = ()
        if ra_aluno:
            query += '  AND alunos.ra = %s'
            params += (ra_aluno,)
        if cpf_aluno:
            query += '  AND pessoas.cpf = %s'
            params += (cpf_aluno,)
        if nome_turma:
            query += '  AND turmas.id = %s'
            params += (nome_turma,)

        query+= 'GROUP BY pessoas.nome'
        cursor.execute(query, params) 
         
        matriculas = cursor.fetchall()
        if not matriculas:
             return f'Valor não encontrado ao buscar matrículas, certifique-se de que os valores estão sendo inseridos de maneira correta.'
    
        
        return matriculas
    except mysql.connector.Error as err:
        return f'Erro ao buscar matriculas: {err}'
    
def editar_matriculas(conn,matriculas_id):
    try:
            cursor = conn.cursor(dictionary=True)
            new_data_inicio = request.form['data_inicio']
            new_data_fim = request.form['data_fim']
            new_id_inscrito = request.form['id_inscrito_hidden']
            new_id_turma = request.form['id_turma_hidden']
            
           #checar esse select e mudar os nomes dos campos em valores-professores
            query = '''UPDATE matriculas
                        SET 
                            data_inicio = %s,
                            data_fim = %s,
                            id_turma = %s,
                            id_inscricao = %s,
                            modificado_em = %s
                        WHERE matriculas.id = %s;
                                '''
            
            # Executa a consulta SQL
            cursor.execute(query, ( new_data_inicio, new_data_fim, new_id_turma, new_id_inscrito,datetime.now(),matriculas_id))
             
            # Comita as alterações no banco de dados
            conn.commit()
    except mysql.connector.Error as err:
            print("Erro ao atualizar dados:", err)


def excluir_matriculas(conn, matriculas_id):
    try:
        cursor = conn.cursor()
        cursor.execute('''UPDATE matriculas SET matriculas.deletado_em = %s, ativo_flag = 0 WHERE matriculas.id = %s;
                       ''', (datetime.now(), matriculas_id))
        conn.commit()
        return
    except mysql.connector.Error as err:
        return ({"error": f'Erro ao excluir secretaria: {err}'})