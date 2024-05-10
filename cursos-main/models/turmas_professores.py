import mysql.connector
from flask import request
from datetime import datetime
from unidecode import unidecode

def resultados_turmas_professores_pesquisados(conn):
    #LEMBRAR DE COLOCAR COMO UNIDECODE QUANDO TERMINAR A PARTE DE 
    #ADICIONAR ALUNOS
    professor_nome =  unidecode(request.form['nome_professor'].upper())
    turma = request.form['id_turma']
    print(professor_nome)
    print(turma)

    try:
        
        cursor = conn.cursor(dictionary=True)
        query = '''
            SELECT
                pessoas.nome AS nome_professor,
                turmas.nome AS nome_turma,
                turmas.descricao AS descricao_turma,
                turmas.capacidade AS capacidade_turma,
                turmas.data_inicio,
                turmas.data_fim,
                turmas.id AS id_turma,
                turmas.id_curso,
                cursos.nome AS nome_curso,
                cursos.descricao AS descricao_curso,
                turmas_professores.id AS id_turma_professor
                FROM turmas_professores
                JOIN professores on professores.id = turmas_professores.id_professor
                JOIN pessoas on pessoas.id = professores.id_pessoa
                JOIN turmas on turmas.id = turmas_professores.id_turma
                JOIN cursos on cursos.id = turmas.id_curso
                WHERE turmas_professores.deletado_em IS NULL '''
        
        params = ()
        if professor_nome:
            query += ' AND pessoas.nome LIKE %s'
            params+= (f'%{professor_nome}%',)

        if turma:
            query += ' AND turmas.id = %s'
            params+= (turma,)
      
        cursor.execute(query, params) 

        turmas_professor = cursor.fetchall()
        print(turmas_professor)
        return turmas_professor
    except mysql.connector.Error as err:
        return f'Erro ao buscar alunos: {err}'
    


def pesquisar_nomes_proximos_professores_turma(conn,dados):
    #função que fornece um datalist com os nomes próximos ao valor digitado no input em adicionar aluno
    try:
        cursor = conn.cursor(dictionary=True)
        dados = request.json  # Acesse os dados enviados no corpo da solicitação
        print(dados)
        if dados['nome'].strip():  # Verifica se o valor não está vazio após remover espaços em branco
            nome_inserido = dados['nome']
            cursor.execute('''SELECT 
                            MAX(turmas_professores.id) AS id_turma_professor,
                            pessoas.nome AS nome_professor,
                            MAX(turmas.id) AS id_turma,
                            MAX(turmas.nome) AS nome_turma,
                            MAX(turmas.descricao) AS descricao_turma
                            FROM 
                                turmas_professores
                            JOIN 
                                professores ON professores.id = turmas_professores.id_professor
                            JOIN 
                                pessoas ON pessoas.id = professores.id_pessoa 
                            JOIN 
                                turmas ON turmas.id = turmas_professores.id_turma
                            WHERE 
                                pessoas.nome LIKE %s 
                            GROUP BY 
                                pessoas.nome,
                                turmas.nome ''', ('%' + nome_inserido + '%',))
            nomes_encontrados = cursor.fetchall()
            nomes_semelhantes = [(nome['nome_turma'], nome['nome_professor'], nome['id_turma']) for nome in nomes_encontrados]
           
            return nomes_semelhantes  # Certifique-se de que está retornando JSON
    except mysql.connector.Error as err:
          return f'Erro ao buscar dados: {err}'
    

def pesquisar_nomes_professores(conn,dados):
    try:
        cursor = conn.cursor(dictionary=True)
        dados = request.json  # Acesse os dados enviados no corpo da solicitação
        print(dados)
        if dados['nome'].strip():  # Verifica se o valor não está vazio após remover espaços em branco
            nome_inserido = dados['nome']
            cursor.execute('''
                           SELECT DISTINCT
                           pessoas.nome AS nome_professor,
                            professores.id AS professor_id
                            FROM professores
                            JOIN pessoas ON pessoas.id = professores.id_pessoa 
                            WHERE pessoas.nome LIKE %s''', ('%' + nome_inserido + '%',))
            nomes_encontrados = cursor.fetchall()
            nomes_semelhantes = [( nome['nome_professor'], nome['professor_id']) for nome in nomes_encontrados]
           
            return nomes_semelhantes  # Certifique-se de que está retornando JSON
    except mysql.connector.Error as err:
          return f'Erro ao buscar dados: {err}'
    

def pesquisar_nomes_proximos_turma(conn,dados):
    #função que fornece um datalist com os nomes próximos ao valor digitado no input em adicionar aluno
    try:
        cursor = conn.cursor(dictionary=True)
        dados = request.json  # Acesse os dados enviados no corpo da solicitação
        print(dados)
        if dados['nome'].strip():  # Verifica se o valor não está vazio após remover espaços em branco
            nome_inserido = dados['nome']
            cursor.execute('''SELECT DISTINCT					
                            turmas.id as id_turma,
                            turmas.nome AS nome_turma,
                            turmas.descricao AS descricao_turma
                            from turmas
                            WHERE turmas.nome LIKE %s''', ('%' + nome_inserido + '%',))
            nomes_encontrados = cursor.fetchall()
            nomes_semelhantes = [(nome['nome_turma'], nome['id_turma']) for nome in nomes_encontrados]
            return nomes_semelhantes  # Certifique-se de que está retornando JSON
    except mysql.connector.Error as err:
          return f'Erro ao buscar dados: {err}'
    
def enviar_valores_turmas_professores(conn):
    
    try:
        cursor = conn.cursor()
        data_inicio = request.form['data_inicio']
        data_fim = request.form['data_fim']
        id_professor = request.form['id_professor_hidden']
        id_turma = request.form['id_turma_hidden']
        cursor.execute('''
            INSERT INTO turmas_professores (data_inicio, data_fim, id_professor, id_turma, criado_em) 
            VALUES (%s, %s, %s, %s, %s)''', (data_inicio, data_fim, id_professor, id_turma, datetime.now()))
        conn.commit()
        return 
    except mysql.connector.Error as err:
        return 'Erro ao adicionar turma para professor: {err}'
    

def editar_valores_turmas_professores(conn, id_turma_professor):
    cursor = conn.cursor(dictionary=True)
    try:
            new_data_inicio = request.form['nova_data_inicio']
            new_data_fim = request.form['nova_data_fim']
            new_id_professor = request.form['novo_id_professor_hidden']
            new_id_turma = request.form['novo_id_turma_hidden']
            
           #checar esse select e mudar os nomes dos campos em valores-professores
            query = '''UPDATE turmas_professores 
                        JOIN turmas ON turmas.id = turmas_professores.id_turma
                        SET 
                            turmas_professores.id_professor = %s,
                            turmas_professores.id_turma = %s,
                            turmas_professores.modificado_em = %s,
                            turmas.data_inicio = %s,
                            turmas.data_fim = %s
                        WHERE turmas_professores.id = %s;
                                '''
            
            # Executa a consulta SQL
            cursor.execute(query, ( new_id_professor, new_id_turma, datetime.now(),new_data_inicio, new_data_fim,id_turma_professor))
            
            # Comita as alterações no banco de dados
            conn.commit()
    except mysql.connector.Error as err:
            print("Erro ao atualizar dados:", err)

def excluir_turmas_professores(conn,turmas_professores_id):
    try:
        cursor = conn.cursor()
        cursor.execute('''UPDATE turmas_professores SET deletado_em = %s, ativo_flag = 0 WHERE turmas_professores.id = %s;
                       ''', (datetime.now(),turmas_professores_id ))
        conn.commit()
        return
    except mysql.connector.Error as err:
        return ({"error": f'Erro ao excluir secretaria: {err}'})
    