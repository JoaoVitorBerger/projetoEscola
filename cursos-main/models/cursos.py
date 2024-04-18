import mysql.connector
from flask import request
from datetime import datetime
from unidecode import unidecode


def resultados_cursos_pesquisados(conn):
    nome_curso = unidecode(request.form['nome_curso'].upper())
    secretaria_curso = request.form['id_secretaria']
    print(secretaria_curso)
    try:
        
        cursor = conn.cursor(dictionary=True)
        query = '''
            SELECT 
                   cursos.id AS curso_id,
                   cursos.nome AS nome_curso,
                   cursos.descricao AS curso_descricao,
                   secretarias.nome AS nome_secretaria
            FROM 
                cursos
			JOIN 
				secretarias ON secretarias.id = cursos.id_secretaria
            WHERE
                cursos.deletado_em IS NULL
            AND 
                secretarias.deletado_em IS NULL
		 '''
        params = ()

        if nome_curso:
            query += ' AND cursos.nome LIKE %s'
            params += (f'%{nome_curso}%',)  # Adiciona o parâmetro à tupla
        
        if secretaria_curso:
            query += ' AND secretarias.id LIKE %s'
            params += (f'%{secretaria_curso}%',)  # Adiciona o parâmetro à tupla
        
        cursor.execute(query, params) 
         
        cursos = cursor.fetchall()
        return cursos
    except mysql.connector.Error as err:
        return f'Erro ao buscar cursos: {err}'

def pesquisar_secretarias(conn):
    try:   
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT id, nome FROM secretarias')
        cursos = cursor.fetchall()
        return cursos
    except mysql.connector.Error as err:
        return f'Erro ao buscar cursos: {err}'
    
def add_cursos(conn):
    try:
        cursor = conn.cursor()
        nome = unidecode(request.form['nome_curso'].upper())
        descricao = unidecode(request.form['descricao'].upper())
        id_secretaria = request.form['id_secretaria']
        cursor.execute('INSERT INTO cursos (nome, descricao, id_secretaria, criado_em) VALUES (%s, %s, %s,%s)', 
                       (nome, descricao, id_secretaria,datetime.now()))
        conn.commit()
        return 
    except mysql.connector.Error as err:
        return f'Erro ao adicionar curso: {err}'

def editar_cursos(conn, curso_id):
    cursor =conn.cursor(dictionary = True)
    
    try:
        nome_curso = unidecode(request.form['nome_curso'].upper())
        secretaria_curso = request.form['id_secretaria']
        descricao_curso = unidecode(request.form['descricao'].upper())

        query = '''UPDATE cursos
                   SET cursos.nome = %s,
                       cursos.id_secretaria= %s,
                       cursos.descricao = %s,
                       cursos.modificado_em = %s
                   WHERE cursos.id = %s
                    '''
        cursor.execute(query,(nome_curso, secretaria_curso, descricao_curso, datetime.now(), curso_id))
        conn.commit()
        return
    except mysql.connector.Error as err:
            print ('Erro ao editar curso: {err}')
            conn.rollback()

def excluir_curso(conn,curso_id):
    try:
        cursor = conn.cursor()
        cursor.execute('''UPDATE cursos SET cursos.deletado_em = %s, ativo_flag = 0 WHERE cursos.id = %s;
                       ''', (datetime.now(), curso_id))
        conn.commit()
        return
    except mysql.connector.Error as err:
        return ({"error": f'Erro ao excluir curso: {err}'})