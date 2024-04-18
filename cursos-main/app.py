from flask import Flask, render_template, request, redirect, url_for,jsonify
import mysql.connector
from models.secretaria import *
from models.pessoa import *
from models.alunos import *
from models.professores import *
from models.inscricoes import *
from models.cursos import *
from models.turmas import *

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
         # Obtém a data e hora atuais
        cursor.execute('''UPDATE secretarias SET deletado_em = %s, ativo_flag = 0 WHERE id = %s;
                       ''', (datetime.now(), secretaria_id))
        conn.commit()
        return jsonify({"message": "Secretaria excluída com sucesso"})
    except mysql.connector.Error as err:
        return jsonify({"error": f'Erro ao excluir secretaria: {err}'})
        

# Rota para exibir o formulário de adicionar pessoa
@app.route('/pessoas-form')
def pessoa_form():
    return render_template('Pessoas/pessoas-form.html')

# Rota para adicionar uma nova pessoa
@app.route('/pessoas', methods=['POST'])
def cadastrar_pessoa():
    conn = conectar()
    result = add_pessoa(conn)
    if isinstance(result, str):  # Verifica se houve erro
        return render_template('erro.html', mensagem=result)
    return redirect('/')

# Rota para pesquisar pessoas
@app.route('/pesquisar-pessoas')
def exibindo_pessoas():
    return render_template('Pessoas/pesquisar-pessoas.html')

#Exibe uma página com a resposta da pesquisa e coloca as opções edtar e excluir
@app.route('/resultado-pesquisa-pessoas', methods=['POST'])
def exibir_resultados_pesquisa_pessoas():
    conn = conectar()
    if request.method == 'POST':
        result = resultado_pesquisa(conn)
        print(result)
        if isinstance(result, str):  # Verifica se houve erro
            return render_template('erro.html', mensagem=result)
    return render_template('Pessoas/resultado-pesquisa-pessoas.html',pessoas=result)

#Opção editar valores pessoa
@app.route('/editar-valores-pessoas/<int:pessoa_id>', methods=['GET', 'POST'])
def edit_valores_pessoas(pessoa_id):
    conn = conectar()
    result = edit_pessoa(conn,pessoa_id)
    if isinstance(result, str):  # Verifica se houve erro
        return render_template('erro.html', mensagem=result)
    if request.method == 'POST':
        # Redireciona para a rota '/resultados
        return redirect('/')
    return render_template('Pessoas/editar-valores-pessoas.html')

#Opção para excluir pessoa
@app.route('/excluir-pessoa', methods=['POST'])
def excluir_pessoa():
    try:
        data = request.json
        print('dados recebidos', data)
        pessoa_id = data.get('pessoa_id')
        conn = conectar()
        cursor = conn.cursor()
         # Obtém a data e hora atuais
        cursor.execute('''UPDATE pessoas SET deletado_em = %s, ativo_flag = 0 WHERE id = %s;
                       ''', (datetime.now(), pessoa_id))
        conn.commit()
        return jsonify({"message": "Secretaria excluída com sucesso"})
    except mysql.connector.Error as err:
        return jsonify({"error": f'Erro ao excluir secretaria: {err}'})
     
@app.route('/nomes-proximos', methods=['GET','POST'])
def pesquisar_nomes():
    conn = conectar()
    dados = request.json  # Acesse os dados enviados no corpo da solicitação
    print(dados)
    result = pesquisar_nomes_proximos(conn,dados)
    return jsonify(result)

# Rota para exibir o formulário de adicionar aluno
@app.route('/alunos-form')
def aluno_form():
    conn = conectar()
    result = formulario_adicionar_alunos(conn)
    if isinstance(result, str):  # Verifica se houve erro
        return render_template('erro.html', mensagem=result)
    return render_template('Alunos/alunos-form.html',  secretarias=result)

# Rota para adicionar um novo aluno
@app.route('/alunos-envio', methods=['POST'])
def add_aluno():
        conn = conectar()
        result = enviar_valores_alunos(conn)
        if isinstance(result, str):  # Verifica se houve erro
            return render_template('erro.html', mensagem=result)
        return redirect('/')

#Rota para pesquisar alunos
@app.route('/alunos-pesquisa')
def pesquisar():
    return render_template('Alunos/alunos-pesquisa.html')   

@app.route('/resultado-pesquisa-alunos', methods=['POST'])
def resultado(): 
    conn = conectar ()
    result = resultados_alunos_pesquisados(conn)
    if isinstance(result, str):  # Verifica se houve erro
            return render_template('erro.html', mensagem=result)
    return render_template('Alunos/resultado-pesquisa-alunos.html',alunos=result)

@app.route('/editar-valores-alunos/<int:aluno_id>/<int:id_aluno>', methods=['GET', 'POST'])
def edit_aluno(aluno_id,id_aluno):
    conn = conectar()
    if request.method == 'POST':
        result = editar_alunos(conn, aluno_id, id_aluno)
        if isinstance(result, str):  # Verifica se houve erro
            return render_template('erro.html', mensagem=result)
        # Redireciona para a rota '/resultados
        return redirect('/')
    return render_template('Alunos/editar-valores-alunos.html')

@app.route('/excluir-alunos', methods=['POST'])
def deletar_alunos():
        data = request.json
        print('dados recebidos', data)
        aluno_id = data.get('aluno_id')
        print(aluno_id)
        conn = conectar()
        result = excluir_alunos(conn,aluno_id)
        if isinstance(result, str):  # Verifica se houve erro
            return render_template('erro.html', mensagem=result)
        redirect('/')
        
# Rota para visualizar todos os professores
@app.route('/professores')
def professores():
        return render_template('Professores/professores-pesquisa.html')

#Rota que mostra os resultados das pesquisas
@app.route('/resultado-pesquisa-professores', methods=['POST'])
def resultado_pesquisa_professores(): 
    conn = conectar ()
    result = resultados_professores_pesquisados(conn)
    if isinstance(result, str):  # Verifica se houve erro
            return render_template('erro.html', mensagem=result)
    return render_template('Professores/resultado-pesquisa-professores.html', professores=result)

#Rota para editar os valores de professores
@app.route('/editar-valores-professores/<int:professor_id>/<int:id_professor>', methods=['GET', 'POST'])
def editar_professor(professor_id ,id_professor):
    conn = conectar()
    if request.method == 'POST':
        result = editar_professores(conn, professor_id, id_professor)
        if isinstance(result, str):  # Verifica se houve erro
            return render_template('erro.html', mensagem=result)
        # Redireciona para a rota '/resultados
        return redirect('/')
    result = selecionar_secretaria(conn)    
    return render_template('Professores/editar-valores-professores.html',secretarias_valores = result)

@app.route('/excluir-professores', methods=['POST'])
def deletar_professor():
        data = request.json
        print('dados recebidos', data)
        professor_id = data.get('professor_id')
        secretaria_id = data.get('secretaria_id')
        print(professor_id, secretaria_id)
        conn = conectar()
        result = excluir_professores(conn,professor_id)
        if isinstance(result, str):  # Verifica se houve erro
            return render_template('erro.html', mensagem=result)
        return redirect('/')

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
        return render_template('Professores/professores-form.html', pessoas=pessoas, secretarias=secretarias)
    except mysql.connector.Error as err:
        return render_template('erro.html', mensagem=f'Erro ao buscar dados: {err}')
# Rota para adicionar um novo professor
    
#Rota para pesquisar um nome  
@app.route('/nomes-proximos-professor', methods=['GET','POST'])
def pesquisar_nomes_professor():
    conn = conectar()
    dados = request.json  # Acesse os dados enviados no corpo da solicitação
    print(dados)
    result = pesquisar_nomes_proximos_professor(conn,dados)
    return jsonify(result)

#Rota para enviar valores de professor
@app.route('/professores', methods=['POST'])
def add_professor():
        conn = conectar()
        result = enviar_valores_professores(conn)
        if isinstance(result, str):  # Verifica se houve erro
            return render_template('erro.html', mensagem=result)
        return redirect('/')

# Rota para visualizar todas as inscrições
@app.route('/inscricoes')
def inscricoes():
    try:
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM inscricoes')
        inscricoes = cursor.fetchall()
        return render_template('Inscricoes/inscricoes.html', inscricoes=inscricoes)
    except mysql.connector.Error as err:
        return render_template('erro.html', mensagem=f'Erro ao buscar inscrições: {err}')
    
@app.route('/nomes-proximos-pessoas', methods=['GET','POST'])
def pesquisar_nomes_pessoas():
    conn = conectar()
    dados = request.json  # Acesse os dados enviados no corpo da solicitação
    print(dados)
    result = pesquisar_nomes_proximos_pessoa(conn,dados)
    return jsonify(result)

# Rota para exibir o formulário de adicionar inscrição
@app.route('/inscricoes-form')
def inscricao_form():
    conn = conectar()
    result = inscricoes_form(conn)
    if isinstance(result, str):  # Verifica se houve erro
            return render_template('erro.html', mensagem=result)
    return render_template('Inscricoes/inscricoes-form.html',secretarias = result)

# Rota para adicionar uma nova inscrição
@app.route('/inscricoes', methods=['POST'])
def add_inscricao_pessoa():
    conn = conectar()
    result = add_inscricao(conn)
    if isinstance(result, str):  # Verifica se houve erro
            return render_template('erro.html', mensagem=result)
    return redirect('/')
 
# Rota para visualizar todos os cursos
@app.route('/cursos')
def cursos():
    conn = conectar()
    result = pesquisar_secretarias(conn)
    if isinstance(result, str):  # Verifica se houve erro
            return render_template('erro.html', mensagem= result)
    return render_template('Cursos/cursos.html',secretarias = result)
   
@app.route('/resultado-pesquisa-cursos', methods=['POST'])
def pesquisar_cursos():
    conn = conectar()
    result = resultados_cursos_pesquisados(conn)
    print(result)
    if isinstance(result, str):  # Verifica se houve erro
            return render_template('erro.html', mensagem= result)
    print(result)
    return render_template('Cursos/resultado-pesquisa-cursos.html',cursos = result)

# Rota para exibir o formulário de adicionar curso
@app.route('/cursos-form')
def curso_form():
    conn = conectar()
    result = pesquisar_secretarias(conn)
    if isinstance(result, str):  # Verifica se houve erro
            return render_template('erro.html', mensagem= result)
    return render_template('Cursos/cursos-form.html', secretarias = result)
# Rota para adicionar um novo curso
@app.route('/cursos', methods=['POST'])
def add_curso():
     conn = conectar()
     result = add_cursos(conn)
     if isinstance(result, str):  # Verifica se houve erro
            return render_template('erro.html', mensagem= result)
     return redirect('/')

@app.route('/editar-valores-cursos/<int:curso_id>',methods=['GET', 'POST'])
def edit_cursos(curso_id):
    conn = conectar()
    if request.method == 'POST':
        result =editar_cursos(conn, curso_id)
        if isinstance(result, str):  # Verifica se houve erro
            return render_template('erro.html', mensagem= result)
        return redirect('/')
    result = selecionar_secretaria(conn)      
    return render_template('Cursos/editar-valores-cursos.html', secretarias = result)    

@app.route('/excluir-cursos',methods=['POST'])
def excl_curso():
    data = request.json
    print('dados recebidos', data)
    curso_id = data.get('curso_id')
    print(curso_id)
    conn = conectar()
    result = excluir_curso(conn,curso_id)
    if isinstance(result, str):  # Verifica se houve erro
            return render_template('erro.html', mensagem=result)
    return redirect('/')


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
        print(turmas)
        return render_template('Turmas/turmas.html', turmas=turmas)
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
        return render_template('Turmas/turmas-form.html', cursos=cursos)
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
    

@app.route('/turmas-pesquisa', methods=['GET','POST'])
def pesquisar_turma():
    return render_template('Turmas/turmas-pesquisa.html')

@app.route('/resultado-pesquisa-turma', methods = ['POST'])
def pesquisar_turma_curso():
    conn = conectar()
    result = resultados_turmas_pesquisados(conn)
    print(result)
    if isinstance(result, str):  # Verifica se houve erro
            return render_template('erro.html', mensagem= result)
    print(result)
    return render_template('Turmas/resultado-pesquisa-turma.html',turmas = result)

@app.route('/editar_valores_turma/<int:id_turma>', methods= ['GET','POST'])
def editar_turma(id_turma):
    conn = conectar()
    if request.method == 'POST':
        result = editar_valores_turma(conn,id_turma)  
        if isinstance(result, str):  # Verifica se houve erro
            return render_template('erro.html', mensagem= result)
        return redirect('/')
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT id, nome FROM cursos')
    cursos = cursor.fetchall() 
    return render_template('Turmas/editar-valores-turma.html', cursos = cursos)
@app.route('/excluir-turmas', methods=['POST'])
def excl_turma():
    data = request.json
    id_turma = data.get('turma_id')
    conn = conectar()
    result = excluir_turmas(conn,id_turma)
    if isinstance(result, str):  # Verifica se houve erro
            return render_template('erro.html', mensagem= result)
    return redirect('/')
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
    


   


      

if __name__ == '__main__':
    app.run(debug=True)
