import mysql.connector
from flask import request
from datetime import datetime
from unidecode import unidecode


# def pesquisar_aluno_matriculado(conn):
     
def pesquisar_nome_conteudo(conn, dados):
    try:
        cursor = conn.cursor(dictionary=True)
        dados = request.json  # Acesse os dados enviados no corpo da solicitação
        print(dados)
        if dados['nome'].strip():  # Verifica se o valor não está vazio após remover espaços em branco
            nome_inserido = dados['nome'].strip().upper()
            cursor.execute('''SELECT planos.conteudo AS conteudo_aula,planos.id AS identificacao_plano
                              FROM planos
                              WHERE planos.conteudo LIKE %s
                              GROUP BY planos.conteudo
                         
                             ''', ('%' + nome_inserido + '%',))
            nomes_encontrados = cursor.fetchall()
            nomes_semelhantes = [(nome['conteudo_aula'], nome['identificacao_plano']) for nome in nomes_encontrados]
            return nomes_semelhantes  # Certifique-se de que está retornando JSON
    except mysql.connector.Error as err:
          return f'Erro ao buscar dados: {err}'

def adicionar_falta(conn):
    try:
        cursor = conn.cursor()
        status_presenca = request.form['falta']
        justificativa = unidecode(request.form['justificativa']).upper()
        id_conteudo = request.form['id_conteudo_hidden']
        id_matricula = request.form['id_inscrito_hidden']
        cursor.execute('''
            INSERT INTO faltas (falta,justificativa, id_plano, id_matricula,criado_em) 
            VALUES (%s,%s, %s, %s,%s)''', (status_presenca,justificativa, id_conteudo, id_matricula, datetime.now()))
        conn.commit()
        return
    except mysql.connector.Error as err:
        return 'Erro ao registrar falta: {err}'
    
def pesquisar_faltas(conn):
    status = request.form['falta']
    conteudo = request.form['id_conteudo_hidden']
    inscrito = request.form['id_inscrito_hidden']
    try:
        
        cursor = conn.cursor(dictionary=True)
        query = '''SELECT 
                    CASE WHEN faltas.falta  = 1 THEN 'PRESENTE' ELSE 'NAO PRESENTE' END AS status_presenca,
                    faltas.id,
                    planos.data AS data_do_plano_de_aula,
                    planos.conteudo AS conteudo_plano_de_aula,
                    turmas.nome AS nome_turma,
                    turmas.descricao AS descricao_turma,
                    cursos.nome AS nome_curso,
                    secretarias.nome AS nome_secretaria,
                    pessoas.nome AS nome_aluno
                    FROM faltas
                    JOIN planos on planos.id = faltas.id_plano
                    JOIN turmas on turmas.id = planos.id_turma
                    JOIN cursos on cursos.id = turmas.id_curso
                    JOIN matriculas on matriculas.id = faltas.id_matricula
                    JOIN inscricoes on inscricoes.id = matriculas.id_inscricao
                    JOIN alunos on alunos.id = inscricoes.id_aluno
                    JOIN pessoas on pessoas.id = alunos.id_pessoa
                    JOIN secretarias on secretarias.id = alunos.id_secretaria
                    WHERE 1=1 AND faltas.deletado_em IS NULL
                     '''
        params = ()
        if status:
            query += '  AND faltas.falta = %s'
            params += (status,)
        if conteudo:
            query += '  AND faltas.id_plano = %s'
            params += (conteudo,)
        if inscrito:
            query += '  AND faltas.id_matricula = %s'
            params += (inscrito,)

        query += ' GROUP BY pessoas.nome'
        cursor.execute(query, params) 
          
        faltas = cursor.fetchall()

        if not faltas:
             return 'False'
        return faltas
    except mysql.connector.Error as err:
        return f'Erro ao buscar faltas: {err}'
    

def editar_faltas(conn,faltas_id):
    try:
            cursor = conn.cursor(dictionary=True)
            status_presenca = request.form['falta']
            justificativa = unidecode(request.form['justificativa']).upper()
            id_conteudo = request.form['id_conteudo_hidden']
            id_matricula = request.form['id_inscrito_hidden']
            
           #checar esse select e mudar os nomes dos campos em valores-professores
            query = '''UPDATE faltas 
                        SET
                            falta = %s,
                            justificativa = %s,
                            id_plano = %s,
                            id_matricula = %s,
                            modificado_em = %s
                        WHERE faltas.id = %s;
                                '''
            
            # Executa a consulta SQL
            cursor.execute(query, ( status_presenca, justificativa, id_conteudo,id_matricula, datetime.now(),faltas_id))
            
            # Comita as alterações no banco de dados
            conn.commit()
    except mysql.connector.Error as err:
            print("Erro ao atualizar dados:", err)

def excluir_falta(conn,faltas_id):
    try:
        cursor = conn.cursor()
        cursor.execute('''UPDATE faltas SET faltas.deletado_em = %s WHERE faltas.id = %s;
                       ''', (datetime.now(), faltas_id))
        conn.commit()
        return
    except mysql.connector.Error as err:
        return ({"error": f'Erro ao excluir secretaria: {err}'})
          



def pesquisar_nome_matriculado(conn, dados):
    try:
        cursor = conn.cursor(dictionary=True)
        dados = request.json  # Acesse os dados enviados no corpo da solicitação
        print(dados)
        if dados['nome'].strip():  # Verifica se o valor não está vazio após remover espaços em branco
            nome_inserido = dados['nome'].strip().upper()
            cursor.execute(''' SELECT
                    matriculas.id AS matricula_id,
                    pessoas.nome AS nome_pessoa
                    FROM matriculas
                    JOIN inscricoes on inscricoes.id = matriculas.id_inscricao
                    JOIN alunos on alunos.id = inscricoes.id_aluno
                    JOIN pessoas on pessoas.id = alunos.id_pessoa
                    WHERE matriculas.deletado_em IS NULL
                    AND pessoas.nome LIKE %s
                    GROUP BY pessoas.nome
                    ''', ('%' + nome_inserido + '%',))
            nomes_encontrados = cursor.fetchall()
            nomes_semelhantes = [(nome['matricula_id'], nome['nome_pessoa']) for nome in nomes_encontrados]
            return nomes_semelhantes  # Certifique-se de que está retornando JSON
    except mysql.connector.Error as err:
          return f'Erro ao buscar dados: {err}'
          