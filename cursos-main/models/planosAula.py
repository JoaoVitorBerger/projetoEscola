import mysql.connector
from flask import request
from datetime import datetime
from unidecode import unidecode

def adicionar_plano_aula(conn):
    try:
        cursor = conn.cursor()
        data = request.form['data']
        conteudo = unidecode(request.form['conteudo']).upper()
        id_turma = request.form['id_turma_hidden']
        cursor.execute('''
            INSERT INTO planos (data, conteudo, id_turma, criado_em) 
            VALUES (%s, %s, %s,%s)''', (data, conteudo, id_turma, datetime.now()))
        conn.commit()
        return
    except mysql.connector.Error as err:
        return f'Erro ao adicionar plano de aula: {err}'


def pesquisar_plano_aula(conn):
    try:
        cursor = conn.cursor(dictionary=True)
        query = '''
                SELECT planos.id,
                planos.data as data_plano_de_aula,
                planos.conteudo as conteudo_plano_de_aula,
                turmas.nome as nome_turma,
                turmas.descricao as descricao_turma,
                turmas.capacidade as capacidade_turma,
                turmas.data_inicio as data_inicio_turma,
                turmas.data_fim as data_termino_turma,
                cursos.nome as nome_curso
                FROM planos
                JOIN turmas on turmas.id = planos.id_turma
                JOIN cursos on cursos.id = turmas.id_curso
                WHERE planos.deletado_em IS NULL
              '''
        
        
        data = request.form['data']
        id_turma = request.form['id_turma_hidden']
        params = ()
        if data:
            query += ' AND planos.data = %s'
            params += (data,)
        if id_turma:
            query += ' AND planos.id_turma = %s'
            params += (id_turma,)

        cursor.execute(query, params) 
         
        matriculas = cursor.fetchall()
        if not matriculas:
             return 'False'
    
        
        return matriculas
    except mysql.connector.Error as err:
        return f'Erro ao buscar plano de aula: {err}'
    
def editar_planos(conn, planos_id):
    try:
            cursor = conn.cursor(dictionary=True)
            data = request.form['data']
            conteudo = unidecode(request.form['conteudo']).upper()
            id_turma = request.form['id_turma_hidden']
            
           #checar esse select e mudar os nomes dos campos em valores-professores
            query = '''UPDATE planos
                        SET 
                            data = %s,
                            conteudo= %s,
                            id_turma = %s,
                            modificado_em = %s
                        WHERE planos.id = %s;
                                '''
            
            # Executa a consulta SQL
            cursor.execute(query, ( data, conteudo, id_turma, datetime.now(),planos_id))
             
            # Comita as alterações no banco de dados
            conn.commit()
    except mysql.connector.Error as err:
            print("Erro ao atualizar dados:", err)

def excluir_planos_aula(conn,planos_id):
    try:
        cursor = conn.cursor()
        cursor.execute('''UPDATE planos SET planos.deletado_em = %s, ativo_flag = 0 WHERE planos.id = %s;
                       ''', (datetime.now(), planos_id))
        conn.commit()
        return
    except mysql.connector.Error as err:
        return ({"error": f'Erro ao excluir plano de aula: {err}'})
          