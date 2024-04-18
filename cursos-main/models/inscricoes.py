import mysql.connector
from flask import request
from datetime import datetime

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
        cursor.execute('SELECT id, nome FROM secretarias')
        secretarias = cursor.fetchall()
        return  secretarias
      except mysql.connector.Error as err:
        return f'Erro ao adicionar inscrição: {err}'