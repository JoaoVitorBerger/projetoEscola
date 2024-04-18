import mysql.connector
from flask import request
from datetime import datetime
from unidecode import unidecode



def exibir_pessoas(conn):
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM pessoas')
        pessoas = cursor.fetchall()
        return pessoas
    except mysql.connector.Error as err:
        return f'Erro ao buscar pessoas: {err}'

def add_pessoa(conn):
    try:
        cursor = conn.cursor()
        nome = unidecode(request.form['nome'].upper())
        cpf = request.form['cpf']
        data_nasc = request.form['data_nasc']
        endereco = request.form['endereco'].upper()
        sexo = request.form['sexo']
        nome_social = request.form['nome_social'].upper()
        nome_social = nome_social or None
        if nome_social is None:
            nome_social = 'None'
        cursor.execute('INSERT INTO pessoas (nome, cpf, data_nasc, endereco, sexo, nome_social, criado_em) VALUES (%s, %s, %s, %s, %s,%s,%s )', 
                       (nome, cpf, data_nasc, endereco, sexo, nome_social, datetime.now()))
        conn.commit()
    except mysql.connector.Error as err:
        return f'Erro ao adicionar pessoa: {err}'


def edit_pessoa(conn,pessoa_id):
    cursor = conn.cursor(dictionary=True)
    if request.method =='POST':
      try:
        new_nome = request.form['new_nome'].upper()
        new_cpf = request.form['new_cpf']
        new_data_nasc = request.form['new_data_nasc']
        new_endereco = request.form['new_endereco']
        new_nome_social = request.form['new_nome_social']
        new_nome_social = new_nome_social or None
        if new_nome_social is None:
            new_nome_social = 'None'

        query='''UPDATE pessoas
                SET nome = %s,
                    cpf = %s,
                    data_nasc = %s,
                    endereco = %s,
                    nome_social = %s
                WHERE id = %s'''
        cursor.execute(query,(new_nome, new_cpf, new_data_nasc, new_endereco, new_nome_social, pessoa_id ))
        conn.commit()
        print('Estou enviando')

      except mysql.connector.Error as err:
            print ('Erro ao editar pessoa: {err}')
            conn.rollback()
      finally:
            cursor.close()
            conn.close()


def resultado_pesquisa(conn): 
    nome = request.form['nome']
    cpf = request.form['cpf']
    try:
      
        cursor = conn.cursor(dictionary=True)
        query = '''SELECT
                    id,
                    nome,
                    cpf,
                    data_nasc,
                    endereco,
                    sexo,
                    nome_social
                    FROM pessoas 
                 WHERE 
                    deletado_em IS NULL '''
        params = ()
        if nome:
            query += ' AND pessoas.nome LIKE  %s'
            params+= (f'%{nome.upper()}%',)
        if cpf:
            query += ' AND pessoas.cpf LIKE %s'
            params+=(f'%{cpf}%',)
        cursor.execute(query, params) 

        pessoa = cursor.fetchall()
        return pessoa
    except mysql.connector.Error as err:
        return f'Erro ao buscar alunos: {err}'
    
