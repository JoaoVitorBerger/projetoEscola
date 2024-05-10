import mysql.connector
from flask import request
from datetime import datetime

def resultados_professores_pesquisados(conn):
    
    nome = request.form['nome']
    print(nome)
    cpf = request.form['cpf']
    try:
        
        cursor = conn.cursor(dictionary=True)
        query = '''SELECT
                    pessoas.id,
                    pessoas.nome,
                    pessoas.cpf,
                    data_nasc,
                    professores.id AS id_professor,
                    secretarias.id AS secretaria_id,
                    secretarias.nome AS secretaria_nome
                    FROM pessoas 
                    JOIN professores on professores.id_pessoa = pessoas.id
                    JOIN secretarias on secretarias.id = professores.id_secretaria
                WHERE 
                    professores.deletado_em IS NULL '''
        params = ()
        if nome:
            query += '  AND pessoas.nome LIKE %s'
            params += (f'%{nome}%',)
        if cpf:
            query += '  AND pessoas.cpf = %s'
            params += (cpf,)

        cursor.execute(query, params) 
          
        professores = cursor.fetchall()
        return professores
    except mysql.connector.Error as err:
        return f'Erro ao buscar alunos: {err}'
    
def editar_professores(conn, professor_id, id_professor):

    cursor = conn.cursor(dictionary=True)
    try:
            new_nome = request.form['new_nome_professor'].upper()
            new_cpf = request.form['new_cpf_professor']
            new_data_nasc = request.form['new_data_nasc_professor']
            new_secretaria = request.form['id_secretaria']
            
           #checar esse select e mudar os nomes dos campos em valores-professores
            query = '''UPDATE professores 
                       JOIN pessoas ON pessoas.id = professores.id_pessoa
                       SET cpf = %s,
                           nome = %s,
                           data_nasc = %s,
                           professores.id_secretaria = %s,
                           professores.modificado_em = %s
                       WHERE professores.id_pessoa = %s AND 
                                professores.id = %s'''
            
            # Executa a consulta SQL
            cursor.execute(query, (new_cpf,new_nome,new_data_nasc,new_secretaria,datetime.now(),professor_id, id_professor))
            
            # Comita as alterações no banco de dados
            conn.commit()
    except mysql.connector.Error as err:
            print("Erro ao atualizar dados:", err)

def excluir_professores(conn, professor_id):
    try:
        cursor = conn.cursor()
        cursor.execute('''UPDATE professores SET professores.deletado_em = %s, ativo_flag = 0 WHERE professores.id = %s;
                       ''', (datetime.now(), professor_id))
        conn.commit()
        return
    except mysql.connector.Error as err:
        return ({"error": f'Erro ao excluir secretaria: {err}'})

def pesquisar_nomes_proximos_professor(conn,dados):
    #função que fornece um datalist com os nomes próximos ao valor digitado no input em adicionar aluno
    try:
        cursor = conn.cursor(dictionary=True)
        dados = request.json  # Acesse os dados enviados no corpo da solicitação
        print(dados)
        if dados['nome'].strip():  # Verifica se o valor não está vazio após remover espaços em branco
            nome_inserido = dados['nome'].strip().upper()
            cursor.execute('SELECT id , nome FROM pessoas WHERE nome LIKE %s', ('%' + nome_inserido + '%',))
            nomes_encontrados = cursor.fetchall()
            nomes_semelhantes = [(nome['id'], nome['nome']) for nome in nomes_encontrados]
            return nomes_semelhantes  # Certifique-se de que está retornando JSON
    except mysql.connector.Error as err:
          return f'Erro ao buscar dados: {err}'
    
def enviar_valores_professores(conn):
    try:
        cursor = conn.cursor()
        status = request.form['status']
        id_pessoa = request.form['id_professor_hidden']
        id_secretaria = request.form['id_secretaria']
        cursor.execute('INSERT INTO professores (status, id_pessoa, id_secretaria,criado_em) VALUES ( %s, %s, %s, %s)', 
                       ( status,id_pessoa,id_secretaria, datetime.now()))
        conn.commit()
        return 
    except mysql.connector.Error as err:
        return f'Erro ao adicionar aluno: {err}'
    
def selecionar_secretaria(conn):
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT id, nome FROM secretarias WHERE deletado_em IS NULL')
        secretarias = cursor.fetchall()
        return secretarias
    except mysql.connector.Error as err:
        return f'Erro ao buscar dados: {err}'
    

def exibir_formulario_professores(conn):
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT id, nome FROM secretarias WHERE deletado_em IS NULL')
        secretarias = cursor.fetchall()
        return secretarias 
    except mysql.connector.Error as err:
        return 'Erro ao buscar dados: {err}'