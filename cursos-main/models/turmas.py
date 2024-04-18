import mysql.connector
from flask import request
from datetime import datetime
from unidecode import unidecode


def resultados_turmas_pesquisados(conn):
    nome_turma = request.form['nome_turma']
    data_inicio = request.form['data_inicio']
    data_fim = request.form['data_fim']
    nome_curso = request.form['nome_curso']
    try:
        
        cursor = conn.cursor(dictionary=True)
        query = '''
                SELECT 
                    turmas.id,
		                turmas.nome,
                    turmas.capacidade,
                    turmas.data_inicio,
                    turmas.data_fim,
                    cursos.nome AS nome_curso
	              FROM 
                    turmas
                JOIN 
                    cursos on cursos.id = turmas.id_curso
                WHERE 
                    turmas.deletado_em IS NULL '''
        params = ()
        if nome_turma:
            query += ' AND turmas.nome LIKE  %s'
            params+= (f'%{nome_turma.upper()}%',)

        if data_inicio:
            query += ' AND turmas.data_inicio >= %s'
            params+= (f'%{data_inicio}%',)

        if data_fim:
            query += ' AND turmas.data_fim >= %s'
            params+= (f'%{data_fim}%',)

        if nome_curso:
            query += 'AND cursos.nome LIKE %s'
            params += (f'%{nome_curso}%',)
      
        cursor.execute(query, params) 
   
        turmas = cursor.fetchall()
        return turmas
    except mysql.connector.Error as err:
        return f'Erro ao buscar alunos: {err}'
    


def editar_valores_turma(conn, id_turma):
  cursor = conn.cursor(dictionary=True)

  try:
      novo_nome =unidecode(request.form['novo_nome'].upper()) 
      nova_descricao =unidecode(request.form['nova_descricao'].upper()) 
      nova_capacidade = request.form['nova_capacidade']
      nova_data_inicio = request.form['nova_data_inicio']
      nova_data_fim = request.form['nova_data_fim']
      id_curso = request.form['id_curso']

      query = '''UPDATE turmas
                 SET turmas.nome = %s,
                    turmas.descricao = %s,
                    turmas.capacidade = %s,
                    turmas.data_inicio = %s,
                    turmas.data_fim = %s,
                    turmas.id_curso = %s,
                    turmas.modificado_em = %s
                 WHERE turmas.id = %s'''
      cursor.execute(query,(novo_nome,nova_descricao,nova_capacidade,nova_data_inicio,nova_data_fim,id_curso,datetime.now(), id_turma))

      conn.commit()
      return
  except mysql.connector.Error as err:
    print("Erro ao atualizar dados:", err)
    

def excluir_turmas(conn, id_turma): 
    try:
        cursor = conn.cursor()
        cursor.execute('''UPDATE turmas SET deletado_em = %s, ativo_flag = 0 WHERE id = %s;
                       ''', (datetime.now(), id_turma))
        conn.commit()
        return
    except mysql.connector.Error as err:
        return ({"error": f'Erro ao excluir secretaria: {err}'})