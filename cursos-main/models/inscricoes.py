import mysql.connector
from flask import request
from datetime import datetime
from unidecode import unidecode

def pesquisar_nomes_proximos_pessoa(conn,dados):
    #função que fornece um datalist com os nomes próximos ao valor digitado no input em adicionar aluno
    try:
        cursor = conn.cursor(dictionary=True)
        dados = request.json  # Acesse os dados enviados no corpo da solicitação
        print(dados)
        if dados['nome'].strip():  # Verifica se o valor não está vazio após remover espaços em branco
            nome_inserido = dados['nome'].strip().upper()
            cursor.execute('''SELECT pessoas.id, pessoas.nome, alunos.id AS id_aluno
                            FROM pessoas
                            JOIN alunos ON alunos.id_pessoa = pessoas.id WHERE pessoas.nome LIKE %s''', ('%' + nome_inserido + '%',))
            nomes_encontrados = cursor.fetchall()
            print( nomes_encontrados)
            nomes_semelhantes = [(nome['id'], nome['nome'], nome['id_aluno']) for nome in nomes_encontrados]
            print(nomes_semelhantes)
            return nomes_semelhantes  # Certifique-se de que está retornando JSON
    except mysql.connector.Error as err:
          return f'Erro ao buscar dados: {err}'
    
def add_inscricao(conn):
      try:   
        cursor = conn.cursor()
        status = request.form['status']
        id_aluno = request.form['id_pessoa_hidden']
        print(id_aluno)
        id_secretaria = request.form['id_secretaria']
        cursor.execute('INSERT INTO inscricoes (status, id_aluno, id_secretaria, criado_em) VALUES (%s, %s, %s, %s)', 
                       (status, id_aluno, id_secretaria, datetime.now()))
        conn.commit()
        return 
      except mysql.connector.Error as err:
        return f'Erro ao adicionar inscrição: {err}'

def inscricoes_form(conn): 
      try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT id, nome FROM secretarias WHERE deletado_em IS NULL')
        secretarias = cursor.fetchall()
        return  secretarias
      except mysql.connector.Error as err:
        return f'Erro ao adicionar inscrição: {err}'
      
def pesquisar_incricoes(conn):

    try:
        
        cursor = conn.cursor(dictionary=True)
        query = '''SELECT
					          pessoas.id as id_pessoa,
				  	        pessoas.nome,
                    pessoas.data_nasc,
                    secretarias.id AS secretaria_id,
                    secretarias.nome AS secretaria_nome,
                    alunos.id AS id_aluno,
                    alunos.ra,
                    inscricoes.id,
                    CASE WHEN inscricoes.ativo_flag = 1 THEN 'INSCRITO' ELSE 'NAO INSCRITO' END AS status_inscricao
                    FROM inscricoes
                    JOIN alunos on alunos.id = inscricoes.id_aluno
                    JOIN secretarias on secretarias.id = inscricoes.id_secretaria
                    JOIN pessoas on pessoas.id = alunos.id_pessoa
                    WHERE inscricoes.deletado_em IS NULL'''
        
        
        nome_inscrito = unidecode(request.form['nome_pessoa'].upper())

        secretaria = request.form['id_secretaria']
        print(nome_inscrito)
        print(secretaria)
        
        params = ()
        if nome_inscrito:
            query += '  AND pessoas.nome LIKE %s'
            params += (f'%{nome_inscrito}%',)
        if secretaria:
            query += '  AND secretarias.id = %s'
            params += (secretaria,)

        cursor.execute(query, params) 
         
        inscricoes = cursor.fetchall()

        if not inscricoes:  # Verifica se a lista está vazia
            return 'False'
        return inscricoes
    except mysql.connector.Error as err:
        return f'Erro ao buscar inscricoes: {err}'
    

def editar_inscricoes(conn,inscrito_id):
      try:
       cursor = conn.cursor()
       nome_inscrito = request.form['id_pessoa_hidden']
       id_secretaria = request.form['id_secretaria']
       status = request.form['status']
       query='''UPDATE inscricoes
                SET id_aluno = %s,
                modificado_em = %s,
                id_secretaria = %s,
                ativo_flag = %s
                WHERE id = %s
       '''
       cursor.execute(query,(nome_inscrito, datetime.now(), id_secretaria, status, inscrito_id))
       conn.commit()
       print('Estou enviando')
      except mysql.connector.Error as err:
        return f'Erro ao adicionar secretaria: {err}'
      

def pesquisar_nomes_proximos_inscritos(conn,dados):
    #função que fornece um datalist com os nomes próximos ao valor digitado no input em adicionar aluno
    try:
        cursor = conn.cursor(dictionary=True)
        dados = request.json  # Acesse os dados enviados no corpo da solicitação
        print(dados)
        if dados['nome'].strip():  # Verifica se o valor não está vazio após remover espaços em branco
            nome_inserido = dados['nome'].upper()
            cursor.execute(''' SELECT
					          pessoas.id as id_pessoa,
					          pessoas.nome AS nome_pessoa,
                    secretarias.id AS secretaria_id,
                    alunos.id as id_aluno,
                    inscricoes.id
                    FROM inscricoes
                    JOIN secretarias on secretarias.id = inscricoes.id_secretaria
                    JOIN alunos on alunos.id = inscricoes.id_aluno
                    JOIN pessoas on pessoas.id = alunos.id_pessoa
                    WHERE pessoas.nome LIKE %s ''', ('%' + nome_inserido + '%',))
            nomes_encontrados = cursor.fetchall()
            print( nomes_encontrados)
            nomes_semelhantes = [(nome['id_pessoa'], nome['nome_pessoa'], nome['id_aluno']) for nome in nomes_encontrados]
            print(nomes_semelhantes)
            return nomes_semelhantes  # Certifique-se de que está retornando JSON
    except mysql.connector.Error as err:
          return f'Erro ao buscar dados: {err}'
    
def excluir_inscricao(conn, inscricao_id):
    try:
        cursor = conn.cursor()
        cursor.execute('''UPDATE inscricoes SET inscricoes.deletado_em = %s, ativo_flag = 0 WHERE inscricoes.id = %s;
                       ''', (datetime.now(), inscricao_id))
        conn.commit()
        return
    except mysql.connector.Error as err:
        return ({"error": f'Erro ao excluir secretaria: {err}'})