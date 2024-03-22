import mysql.connector
from flask import request
from datetime import datetime



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
        nome = request.form['nome'].upper()
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
        return
    except mysql.connector.Error as err:
        return f'Erro ao adicionar pessoa: {err}'