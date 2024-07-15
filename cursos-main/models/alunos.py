import mysql.connector
from flask import request
from datetime import datetime

def pesquisar_nomes_proximos(conn,dados):
    #função que fornece um datalist com os nomes próximos ao valor digitado no input em adicionar aluno
    try:
        cursor = conn.cursor(dictionary=True)
        dados = request.json  # Acesse os dados enviados no corpo da solicitação
        print(dados)
        if dados['nome'].strip():  # Verifica se o valor não está vazio após remover espaços em branco
            nome_inserido = dados['nome'].strip().upper()
            cursor.execute('SELECT DISTINCT id , nome FROM pessoas WHERE nome LIKE %s', ('%' + nome_inserido + '%',))
            nomes_encontrados = cursor.fetchall()
            nomes_semelhantes = [(nome['id'], nome['nome']) for nome in nomes_encontrados]
            return nomes_semelhantes  # Certifique-se de que está retornando JSON
    except mysql.connector.Error as err:
          return f'Erro ao buscar dados: {err}'
    
def formulario_adicionar_alunos(conn):
    try:
        cursor = conn.cursor(dictionary=True)      
        cursor.execute('SELECT id, nome FROM secretarias WHERE deletado_em IS NULL')
        secretarias = cursor.fetchall()
        return secretarias
    except mysql.connector.Error as err:
        return f'Erro ao buscar dados: {err}'
    
def enviar_valores_alunos(conn):
    try:
        cursor = conn.cursor()
        ra = request.form['ra']
        status = request.form['status']
        id_pessoa = request.form['id_pessoa_hidden']
        id_secretaria = request.form['id_secretaria']
        cursor.execute('INSERT INTO alunos (ra, status, id_pessoa, id_secretaria,criado_em) VALUES (%s, %s, %s, %s, %s)', 
                       (ra, status,id_pessoa,id_secretaria, datetime.now()))
        conn.commit()
        return 
    except mysql.connector.Error as err:
        return f'Erro ao adicionar aluno: {err}'
    
def resultados_alunos_pesquisados(conn):
    nome = request.form['nome']
    ra = request.form['ra']
    cpf = request.form['cpf']
    try:
        
        cursor = conn.cursor(dictionary=True)
        query = '''SELECT
                    alunos.ra,
                    alunos.id AS aluno_id,
                    pessoas.nome,
                    pessoas.cpf,
                    pessoas.id AS pessoa_id,
                    endereco,
                    data_nasc,
                    secretarias.nome AS secretaria_nome
                    FROM pessoas 
                    JOIN alunos on alunos.id_pessoa = pessoas.id
                    JOIN secretarias on secretarias.id = alunos.id_secretaria
                WHERE 
                    alunos.deletado_em IS NULL '''
        params = ()
        if nome:
            query += ' AND pessoas.nome LIKE  %s'
            params+= (f'%{nome.upper()}%',)
        if ra:
            query += ' AND alunos.ra LIKE %s'
            params+= (f'%{ra}%',)
        if cpf:
            query += ' AND pessoas.cpf LIKE %s'
            params+= (f'%{cpf}%',)
      
        cursor.execute(query, params) 
   
        alunos = cursor.fetchall()
        print(alunos)

        if not alunos:  # Verifica se a lista está vazia
            return 'False'
        return alunos
    except mysql.connector.Error as err:
        return f'Erro ao buscar alunos: {err}'

def editar_alunos(conn, aluno_id, id_aluno):
        cursor = conn.cursor(dictionary=True)
        try:
            new_nome = request.form['new_nome'].upper()
            new_cpf = request.form['new_cpf']
            new_ra = request.form['new_ra']
            new_data_nasc = request.form['new_data_nasc']
            
            # Constrói a consulta SQL com os placeholders corretos
            query = '''UPDATE alunos
            JOIN pessoas ON pessoas.id = alunos.id_pessoa
            SET cpf = %s,
                nome = %s,
                ra = %s,
                data_nasc = %s,
                alunos.modificado_em = %s
            WHERE alunos.id = %s AND
                  alunos.id_pessoa = %s
                  '''
            
            # Executa a consulta SQL
            cursor.execute(query, (new_cpf,new_nome,new_ra,new_data_nasc,datetime.now(),aluno_id, id_aluno))
            
            # Comita as alterações no banco de dados
            conn.commit()
            return
        except mysql.connector.Error as err:
            print("Erro ao atualizar dados:", err)

def excluir_alunos(conn, aluno_id):
    try:
        cursor = conn.cursor()
        cursor.execute('''UPDATE alunos SET deletado_em = %s, ativo_flag = 0 WHERE id = %s;
                       ''', (datetime.now(), aluno_id))
        conn.commit()
        return
    except mysql.connector.Error as err:
        return ({"error": f'Erro ao excluir secretaria: {err}'})