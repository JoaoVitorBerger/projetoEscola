from flask import Flask, render_template, request, redirect, url_for,jsonify
import mysql.connector
from models.secretaria import *

app = Flask(__name__)

# Configuração do MySQL
db_config = {
    'host': 'localhost',
    'user': 'root',
    'passwd': '',
    'database': 'cursosbd'
}

# Função para conectar ao banco de dados
def conectar():
    return mysql.connector.connect(**db_config)
#Homepage
@app.route('/')
def index():
    return render_template('index.html')

#Rota para exibir todas as secretarias
#O nome no href do index tem que ser o mesmo do app.route
# As chamadas de arquivos e redirecionamento de urls`s tem que ser feito no app.py
@app.route('/secretarias')
def exibir_secretarias():
    conn = conectar()
    result = secretarias(conn)
    if isinstance(result, str):  # Verifica se houve erro
        return render_template('erro.html', mensagem=result)
    return render_template('Secretarias/secretarias.html', secretarias=result)


#Rota para exibir formulário secretarias
@app.route('/secretarias-form')
def adicionar_secretaria():
    conn = conectar()
    result = secretaria_form(conn)
    if isinstance(result, str):  # Verifica se houve erro
        return render_template('erro.html', mensagem=result)
    return render_template('Secretarias/secretarias-form.html')


#Rota para adicionar uma secretaria
@app.route('/secretarias', methods=['POST'])
def inserir_secretaria():
    conn = conectar()
    result = add_secretaria(conn)
    if isinstance(result, str):  # Verifica se houve erro
        return render_template('erro.html', mensagem=result)
    return render_template('index.html')


#Rota para editar uma secretaria
@app.route('/editar-valores-secretarias/<int:secretaria_id>', methods=['GET', 'POST'])
def edit_secretaria_valores(secretaria_id):
    conn=conectar()
    result = edit_secretaria(secretaria_id, conn)
    if isinstance(result, str):  # Verifica se houve erro
        return render_template('erro.html', mensagem=result)
    if request.method == 'POST':
        # Redireciona para a rota '/secretarias'
        return redirect('/secretarias')
    return render_template('Secretarias/editar-valores-secretarias.html')

    
@app.route('/excluir-secretaria', methods=['POST'])
def excluir_secretarias():
    try:
        data = request.json
        print('dados recebidos', data)
        secretaria_id = data.get('secretaria_id')
        conn = conectar()
        cursor = conn.cursor()
        data_exclusao = datetime.now()  # Obtém a data e hora atuais
        cursor.execute('''UPDATE secretarias SET deletado_em = %s WHERE id = %s;
                       ''', (data_exclusao, secretaria_id))
        conn.commit()
        return jsonify({"message": "Secretaria excluída com sucesso"})
    except mysql.connector.Error as err:
        return jsonify({"error": f'Erro ao excluir secretaria: {err}'})




# Rota para visualizar todas as pessoas
@app.route('/pessoas')
def pessoas():
    try:
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM pessoas')
        pessoas = cursor.fetchall()
        return render_template('pessoas.html', pessoas=pessoas)
    except mysql.connector.Error as err:
        return render_template('erro.html', mensagem=f'Erro ao buscar pessoas: {err}')
# Rota para exibir o formulário de adicionar pessoa
@app.route('/pessoas-form')
def pessoa_form():
    return render_template('pessoas-form.html')
# Rota para adicionar uma nova pessoa
@app.route('/pessoas', methods=['POST'])
def add_pessoa():
    try:
        conn = conectar()
        cursor = conn.cursor()
        nome = request.form['nome'].upper()
        cpf = request.form['cpf']
        data_nasc = request.form['data_nasc']
        endereco = request.form['endereco'].upper()
        sexo = request.form['sexo']
        nome_social = request.form['nome_social'].upper()
        if nome_social is None:
            nome_social = 'None'
        cursor.execute('INSERT INTO pessoas (nome, cpf, data_nasc, endereco, sexo, nome_social) VALUES (%s, %s, %s, %s, %s,%s )', 
                       (nome, cpf, data_nasc, endereco, sexo, nome_social))
        conn.commit()
        return redirect(url_for('pessoas'))
    except mysql.connector.Error as err:
        return render_template('erro.html', mensagem=f'Erro ao adicionar pessoa: {err}')
    
# Rota para visualizar todos os alunos
@app.route('/alunos')
def alunos():
    try:
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM alunos')
        alunos = cursor.fetchall()
        return render_template('alunos.html', alunos=alunos)
    except mysql.connector.Error as err:
        return render_template('erro.html', mensagem=f'Erro ao buscar alunos: {err}')
# Rota para exibir o formulário de adicionar aluno
@app.route('/alunos-form')
def aluno_form():
    try:
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT id, nome FROM pessoas')
        pessoas = cursor.fetchall()
        cursor.execute('SELECT id, nome FROM secretarias')
        secretarias = cursor.fetchall()
        return render_template('alunos-form.html', pessoas=pessoas, secretarias=secretarias)
    except mysql.connector.Error as err:
        return render_template('erro.html', mensagem=f'Erro ao buscar dados: {err}')
# Rota para adicionar um novo aluno
@app.route('/alunos', methods=['POST'])
def add_aluno():
    try:
        conn = conectar()
        cursor = conn.cursor()
        ra = request.form['ra']
        status = request.form['status']
        id_pessoa = request.form['id_pessoa']
        id_secretaria = request.form['id_secretaria']
        cursor.execute('INSERT INTO alunos (ra, status, id_pessoa, id_secretaria) VALUES (%s, %s, %s, %s)', 
                       (ra, status, id_pessoa, id_secretaria))
        conn.commit()
        return redirect(url_for('alunos'))
    except mysql.connector.Error as err:
        return render_template('erro.html', mensagem=f'Erro ao adicionar aluno: {err}')

# Rota para visualizar todos os professores
@app.route('/professores')
def professores():
    try:
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM professores')
        professores = cursor.fetchall()
        return render_template('professores.html', professores=professores)
    except mysql.connector.Error as err:
        return render_template('erro.html', mensagem=f'Erro ao buscar professores: {err}')
# Rota para exibir o formulário de adicionar professor
@app.route('/professores-form')
def professor_form():
    try:
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT id, nome FROM pessoas')
        pessoas = cursor.fetchall()
        cursor.execute('SELECT id, nome FROM secretarias')
        secretarias = cursor.fetchall()
        return render_template('professores-form.html', pessoas=pessoas, secretarias=secretarias)
    except mysql.connector.Error as err:
        return render_template('erro.html', mensagem=f'Erro ao buscar dados: {err}')
# Rota para adicionar um novo professor
@app.route('/professores', methods=['POST'])
def add_professor():
    try:
        conn = conectar()
        cursor = conn.cursor()
        status = request.form['status']
        id_pessoa = request.form['id_pessoa']
        id_secretaria = request.form['id_secretaria']
        cursor.execute('INSERT INTO professores (status, id_pessoa, id_secretaria) VALUES (%s, %s, %s)', 
                       (status, id_pessoa, id_secretaria))
        conn.commit()
        return redirect(url_for('professores'))
    except mysql.connector.Error as err:
        return render_template('erro.html', mensagem=f'Erro ao adicionar professor: {err}')

# Rota para visualizar todas as inscrições
@app.route('/inscricoes')
def inscricoes():
    try:
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM inscricoes')
        inscricoes = cursor.fetchall()
        return render_template('inscricoes.html', inscricoes=inscricoes)
    except mysql.connector.Error as err:
        return render_template('erro.html', mensagem=f'Erro ao buscar inscrições: {err}')
# Rota para exibir o formulário de adicionar inscrição
@app.route('/inscricoes-form')
def inscricao_form():
    try:
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT 
                alunos.id AS id_aluno,
                pessoas.nome AS nome_aluno
            FROM alunos
            JOIN pessoas ON alunos.id_pessoa = pessoas.id
        ''')
        alunos = cursor.fetchall()
        cursor.execute('SELECT id, nome FROM secretarias')
        secretarias = cursor.fetchall()
        return render_template('inscricoes-form.html', alunos=alunos, secretarias=secretarias)
    except mysql.connector.Error as err:
        return render_template('erro.html', mensagem=f'Erro ao buscar dados: {err}')
# Rota para adicionar uma nova inscrição
@app.route('/inscricoes', methods=['POST'])
def add_inscricao():
    try:
        conn = conectar()
        cursor = conn.cursor()
        status = request.form['status']
        id_aluno = request.form['id_aluno']
        id_secretaria = request.form['id_secretaria']
        cursor.execute('INSERT INTO inscricoes (status, id_aluno, id_secretaria) VALUES (%s, %s, %s)', 
                       (status, id_aluno, id_secretaria))
        conn.commit()
        return redirect(url_for('inscricoes'))
    except mysql.connector.Error as err:
        return render_template('erro.html', mensagem=f'Erro ao adicionar inscrição: {err}')
    
# Rota para visualizar todos os cursos
@app.route('/cursos')
def cursos():
    try:
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT cursos.*, secretarias.nome AS secretaria
            FROM cursos
            JOIN secretarias ON cursos.id_secretaria = secretarias.id
        ''')
        cursos = cursor.fetchall()
        return render_template('cursos.html', cursos=cursos)
    except mysql.connector.Error as err:
        return render_template('erro.html', mensagem=f'Erro ao buscar cursos: {err}')
# Rota para exibir o formulário de adicionar curso
@app.route('/cursos-form')
def curso_form():
    try:
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT id, nome FROM secretarias')
        secretarias = cursor.fetchall()
        return render_template('cursos-form.html', secretarias=secretarias)
    except mysql.connector.Error as err:
        return render_template('erro.html', mensagem=f'Erro ao buscar dados: {err}')
# Rota para adicionar um novo curso
@app.route('/cursos', methods=['POST'])
def add_curso():
    try:
        conn = conectar()
        cursor = conn.cursor()
        nome = request.form['nome']
        descricao = request.form['descricao']
        id_secretaria = request.form['id_secretaria']
        cursor.execute('INSERT INTO cursos (nome, descricao, id_secretaria) VALUES (%s, %s, %s)', 
                       (nome, descricao, id_secretaria))
        conn.commit()
        return redirect(url_for('cursos'))
    except mysql.connector.Error as err:
        return render_template('erro.html', mensagem=f'Erro ao adicionar curso: {err}')
    
# Rota para visualizar todas as turmas
@app.route('/turmas')
def turmas():
    try:
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT turmas.*, cursos.nome AS curso_nome
            FROM turmas
            JOIN cursos ON turmas.id_curso = cursos.id
        ''')
        turmas = cursor.fetchall()
        return render_template('turmas.html', turmas=turmas)
    except mysql.connector.Error as err:
        return render_template('erro.html', mensagem=f'Erro ao buscar turmas: {err}')
# Rota para exibir o formulário de adicionar turma
@app.route('/turmas-form')
def turma_form():
    try:
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT id, nome FROM cursos')
        cursos = cursor.fetchall()
        return render_template('turmas-form.html', cursos=cursos)
    except mysql.connector.Error as err:
        return render_template('erro.html', mensagem=f'Erro ao buscar cursos: {err}')
# Rota para adicionar uma nova turma
@app.route('/turmas', methods=['POST'])
def add_turma():
    try:
        conn = conectar()
        cursor = conn.cursor()
        nome = request.form['nome']
        descricao = request.form['descricao']
        capacidade = request.form['capacidade']
        data_inicio = request.form['data_inicio']
        data_fim = request.form['data_fim']
        id_curso = request.form['id_curso']
        cursor.execute('''
            INSERT INTO turmas (nome, descricao, capacidade, data_inicio, data_fim, id_curso)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (nome, descricao, capacidade, data_inicio, data_fim, id_curso))
        conn.commit()
        return redirect(url_for('turmas'))
    except mysql.connector.Error as err:
        return render_template('erro.html', mensagem=f'Erro ao adicionar turma: {err}')

# Rota para visualizar todas as turmas dos professores
@app.route('/turmas-professores')
def turmas_professores():
    try:
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT turmas_professores.id, turmas_professores.data_inicio, turmas_professores.data_fim,
                   professores.id AS id_professor, pessoas.nome AS nome_professor,
                   turmas.id AS id_turma, turmas.nome AS nome_turma
            FROM turmas_professores
            JOIN professores ON turmas_professores.id_professor = professores.id
            JOIN turmas ON turmas_professores.id_turma = turmas.id
            JOIN pessoas ON professores.id_pessoa = pessoas.id
        ''')
        turmas_professores = cursor.fetchall()
        return render_template('turmas-professores.html', turmas_professores=turmas_professores)
    except mysql.connector.Error as err:
        return render_template('erro.html', mensagem=f'Erro ao buscar turmas dos professores: {err}')
# Rota para exibir o formulário de adicionar turma dos professores
@app.route('/turmas-professores-form')
def turmas_professores_form():
    try:
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT 
                professores.id AS id_professor,
                pessoas.nome AS nome_professor
            FROM professores
            JOIN pessoas ON professores.id_pessoa = pessoas.id
        ''')
        professores = cursor.fetchall()
        cursor.execute('SELECT id, nome FROM turmas')
        turmas = cursor.fetchall()
        return render_template('turmas-professores-form.html', professores=professores, turmas=turmas)
    except mysql.connector.Error as err:
        return render_template('erro.html', mensagem=f'Erro ao buscar dados: {err}')
# Rota para adicionar uma nova turma para professor
@app.route('/turmas-professores', methods=['POST'])
def add_turma_professor():
    try:
        conn = conectar()
        cursor = conn.cursor()
        data_inicio = request.form['data_inicio']
        data_fim = request.form['data_fim']
        id_professor = request.form['id_professor']
        id_turma = request.form['id_turma']
        cursor.execute('''
            INSERT INTO turmas_professores (data_inicio, data_fim, id_professor, id_turma) 
            VALUES (%s, %s, %s, %s)''', (data_inicio, data_fim, id_professor, id_turma))
        conn.commit()
        return redirect(url_for('turmas_professores'))
    except mysql.connector.Error as err:
        return render_template('erro.html', mensagem=f'Erro ao adicionar turma para professor: {err}')

# Rota para visualizar todas as matrículas
@app.route('/matriculas')
def matriculas():
    try:
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
                        SELECT matriculas.id, matriculas.data_inicio, matriculas.data_fim,
                        alunos.id AS id_aluno, alunos.ra AS ra_aluno,
                        turmas.id AS id_turma, turmas.nome AS nome_turma,
                        inscricoes.id AS id_inscricao, inscricoes.status AS status_inscricao
                        FROM matriculas
                        JOIN alunos ON matriculas.id = alunos.id
                        JOIN turmas ON matriculas.id = turmas.id
                        JOIN inscricoes ON matriculas.id = inscricoes.id
                        ORDER BY matriculas.id
                        ''')
        matriculas = cursor.fetchall()
        return render_template('matriculas.html', matriculas=matriculas)
    except mysql.connector.Error as err:
        return render_template('erro.html', mensagem=f'Erro ao buscar matrículas: {err}')
# Rota para exibir o formulário de adicionar matrícula
@app.route('/matriculas-form')
def matricula_form():
    try:
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT id, nome FROM turmas')
        turmas = cursor.fetchall()
        cursor.execute('''
                        SELECT inscricoes.id, pessoas.nome
                        FROM inscricoes
                        JOIN alunos ON inscricoes.id_aluno = alunos.id
                        JOIN pessoas ON alunos.id_pessoa = pessoas.id
                        LEFT JOIN matriculas ON inscricoes.id = matriculas.id_inscricao
                        WHERE matriculas.id IS NULL
                        ''')
        inscricoes = cursor.fetchall()
        return render_template('matriculas-form.html', turmas=turmas, inscricoes=inscricoes)
    except mysql.connector.Error as err:
        return render_template('erro.html', mensagem=f'Erro ao buscar dados: {err}')
# Rota para adicionar uma nova matrícula
@app.route('/matriculas', methods=['POST'])
def add_matricula():
    try:
        conn = conectar()
        cursor = conn.cursor()
        data_inicio = request.form['data_inicio']
        data_fim = request.form['data_fim']
        id_turma = request.form['id_turma']
        id_inscricao = request.form['id_inscricao']
        cursor.execute('''
            INSERT INTO matriculas (data_inicio, data_fim, id_turma, id_inscricao) 
            VALUES (%s, %s, %s, %s)''', (data_inicio, data_fim, id_turma, id_inscricao))
        conn.commit()
        return redirect(url_for('matriculas'))
    except mysql.connector.Error as err:
        return render_template('erro.html', mensagem=f'Erro ao adicionar matrícula: {err}')
    
# Rota para exibir todos os planos de aula
@app.route('/planos')
def planos():
    try:
        conn = conectar()  # Substitua conectar() pela função que conecta ao banco de dados
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM planos')
        planos = cursor.fetchall()
        return render_template('planos.html', planos=planos)
    except mysql.connector.Error as err:
        return render_template('erro.html', mensagem=f'Erro ao buscar planos de aula: {err}')
# Rota para exibir o formulário de planos de aula
@app.route('/planos-form')
def planos_form():
    try:
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT id, nome FROM turmas')
        turmas = cursor.fetchall()
        return render_template('planos-form.html', turmas=turmas)
    except mysql.connector.Error as err:
        return render_template('erro.html', mensagem=f'Erro ao buscar turmas: {err}')
# Rota para adicionar um novo plano de aula
@app.route('/planos', methods=['POST'])
def add_plano():
    try:
        conn = conectar()
        cursor = conn.cursor()
        data = request.form['data']
        conteudo = request.form['conteudo']
        id_turma = request.form['id_turma']
        cursor.execute('''
            INSERT INTO planos (data, conteudo, id_turma) 
            VALUES (%s, %s, %s)''', (data, conteudo, id_turma))
        conn.commit()
        return redirect(url_for('planos'))
    except mysql.connector.Error as err:
        return render_template('erro.html', mensagem=f'Erro ao adicionar plano de aula: {err}')

# Rota para exibir todas as faltas
@app.route('/faltas')
def faltas():
    try:
        conn = conectar()  # Substitua conectar() pela função que conecta ao banco de dados
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM faltas')
        faltas = cursor.fetchall()
        return render_template('faltas.html', faltas=faltas)
    except mysql.connector.Error as err:
        return render_template('erro.html', mensagem=f'Erro ao buscar faltas: {err}')
# Rota para exibir o formulário de registro de faltas
@app.route('/faltas-form')
def faltas_form():
    try:
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT id, nome FROM turmas')
        turmas = cursor.fetchall()
        cursor.execute('SELECT id, conteudo FROM planos')
        planos = cursor.fetchall()
        cursor.execute('''
            SELECT matriculas.id, pessoas.nome
            FROM matriculas
            JOIN inscricoes ON matriculas.id_inscricao = inscricoes.id
            JOIN alunos ON inscricoes.id_aluno = alunos.id
            JOIN pessoas ON alunos.id_pessoa = pessoas.id;
        ''')
        matriculas = cursor.fetchall()
        return render_template('faltas-form.html', turmas=turmas, planos=planos, matriculas=matriculas)
    except mysql.connector.Error as err:
        return render_template('erro.html', mensagem=f'Erro ao buscar dados: {err}')
# Rota para adicionar um registro de falta
@app.route('/faltas', methods=['POST'])
def add_falta():
    try:
        conn = conectar()
        cursor = conn.cursor()
        justificativa = request.form['justificativa']
        id_plano = request.form['id_plano']
        id_matricula = request.form['id_matricula']
        cursor.execute('''
            INSERT INTO faltas (justificativa, id_plano, id_matricula) 
            VALUES (%s, %s, %s)''', (justificativa, id_plano, id_matricula))
        conn.commit()
        return redirect(url_for('faltas'))
    except mysql.connector.Error as err:
        return render_template('erro.html', mensagem=f'Erro ao registrar falta: {err}')
    
@app.route('/alunos-secretarias')
def alunosSecretarias():
    try:
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(''' SELECT alunos.ra AS ra_aluno, pessoas.nome AS nome_aluno, secretarias.nome AS nome_secretaria, status,
                            CASE
                                WHEN status = 1 THEN 'Ativo'
                                ELSE 'Desativado'
                            END AS status
                            FROM alunos
                            JOIN pessoas ON alunos.id_pessoa = pessoas.id
                            JOIN secretarias ON secretarias.id = alunos.id_secretaria''')
        alunos = cursor.fetchall()
        return render_template('alunos-secretarias.html', alunos=alunos)
    except mysql.connector.Error as err:
        return render_template('erro.html', mensagem=f'Erro ao buscar alunos: {err}')
    
@app.route('/alunos-pesquisa')
def pesquisar():
    return render_template('alunos-pesquisa.html')   

@app.route('/resultado-pesquisa-alunos', methods=['POST'])
def resultado(): 
    nome = request.form['nome']
    ra = request.form['ra']
    cpf = request.form['cpf']
    

    try:
        conn = conectar ()
        cursor = conn.cursor(dictionary=True)
        query = '''SELECT
                    alunos.ra,
                    alunos.id,
                    pessoas.nome,
                    pessoas.cpf,
                    endereco,
                    data_nasc,
                    secretarias.nome AS secretaria_nome
                    FROM pessoas 
                    JOIN alunos on alunos.id_pessoa = pessoas.id
                    JOIN secretarias on secretarias.id = alunos.id_secretaria
                WHERE 1=1 '''
        if nome:
            query += ' AND pessoas.nome LIKE  %s'
            cursor.execute(query,(f'%{nome.upper()}%',))
        if ra:
            query += ' AND alunos.ra LIKE %s'
            cursor.execute(query,(f'%{ra}%',))
        if cpf:
            query += ' AND pessoas.cpf LIKE %s'
            cursor.execute(query,(f'%{cpf}%',))
      

   
        alunos = cursor.fetchall()
        return render_template('resultado-pesquisa-alunos.html',alunos=alunos)
    except mysql.connector.Error as err:
        return render_template('erro.html', mensagem=f'Erro ao buscar alunos: {err}')

@app.route('/editar-valores-alunos/<int:aluno_id>', methods=['GET', 'POST'])
def edit_aluno(aluno_id):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
        try:
            new_nome = request.form['new_nome'].upper()
            new_cpf = request.form['new_cpf']
            new_ra = request.form['new_ra']
            new_data_nasc = request.form['new_data_nasc']
            
            # Verifica se os campos estão vazios e define para None se estiverem
            if not new_nome:
                new_nome = None
            if not new_cpf:
                new_cpf = None
            if not new_ra:
                new_ra = None
            
            # Constrói a consulta SQL com os placeholders corretos
            query = '''UPDATE pessoas 
                       JOIN alunos ON alunos.id_pessoa = pessoas.id
                       SET cpf = %s,
                           nome = %s,
                           ra = %s,
                           data_nasc = %s
                       WHERE alunos.id = %s'''
            
            # Executa a consulta SQL
            cursor.execute(query, (new_cpf, new_nome, new_ra, new_data_nasc, aluno_id))
            
            # Comita as alterações no banco de dados
            conn.commit()
            
        except mysql.connector.Error as err:
            print("Erro ao atualizar dados:", err)
            conn.rollback()
        finally:
            # Fecha a conexão com o banco de dados
      
            cursor.close()
            conn.close()
        return redirect('/alunos-pesquisa')
    else:
        # Se o método da requisição não for POST, renderiza a página de edição
        return render_template('editar-valores-alunos.html')

   


      

if __name__ == '__main__':
    app.run(debug=True)
