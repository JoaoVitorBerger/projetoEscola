from flask import Flask, render_template, request, redirect, url_for,jsonify
import mysql.connector
from models.secretaria import *
from models.pessoa import *
from models.alunos import *
from models.professores import *
from models.inscricoes import *
from models.cursos import *
from models.turmas import *
from models.turmas_professores import *
from models.matriculas import *
from models.planosAula import *
from models.faltas import *


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

################################################    SECRETARIAS   ###################################################################################
@app.route('/secretarias')
def exibir_secretarias():
    conn = conectar()
    result = secretarias(conn)
    if isinstance(result, str):  # Verifica se houve erro
        return render_template('erro.html', mensagem=result)
    return render_template('Secretarias/secretarias.html', secretarias=result)


#Rota para exibir formulário secretarias
@app.route('/secretarias/form', methods=['POST','GET'])
def adicionar_secretaria():
    conn = conectar()
    mensagem = False    
    if request.method == 'POST':
        result = add_secretaria(conn)
        if isinstance(result, str):  # Verifica se houve erro
            return render_template('erro.html', mensagem=result)
        mensagem = True
    return render_template('Secretarias/secretarias-form.html', mensagem = mensagem)

#Rota para editar uma secretaria
@app.route('/editar-valores-secretarias/<int:secretaria_id>', methods=['GET', 'POST'])
def edit_secretaria_valores(secretaria_id):
    conn=conectar()
    mensagem = False
    result = edit_secretaria(secretaria_id, conn)
    if isinstance(result, str):  # Verifica se houve erro
        return render_template('erro.html', mensagem=result)
    if request.method == 'POST':
        # Redireciona para a rota '/secretarias'
        mensagem = True
    return render_template('Secretarias/editar-valores-secretarias.html', mensagem = mensagem)

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
        mensagem = "Secretaria excluida com sucesso."
        return mensagem
    except mysql.connector.Error as err:
        return jsonify({"error": f'Erro ao excluir secretaria: {err}'})
        
################################################    PESSOAS  ###################################################################################
# Rota para exibir o formulário de adicionar pessoa
@app.route('/pessoas/form',  methods=['POST','GET'])
def pessoa_form():
    conn = conectar()
    mensagem = False    
    if request.method == 'POST':
        result = add_pessoa(conn)
        if isinstance(result, str):  # Verifica se houve erro
          return render_template('erro.html', mensagem=result)
        mensagem = True
    return render_template('Pessoas/pessoas-form.html',mensagem= mensagem)

# Rota para pesquisar pessoas
@app.route('/pessoas/pesquisar')
def exibindo_pessoas():
    return render_template('Pessoas/pesquisar-pessoas.html')

#Exibe uma página com a resposta da pesquisa e coloca as opções edtar e excluir
@app.route('/pessoas/pesquisar/resultados', methods=['POST'])
def exibir_resultados_pesquisa_pessoas():
    conn = conectar()
    if request.method == 'POST':
        result = resultado_pesquisa(conn)
        if isinstance(result, str):
            mensagem = False  # Verifica se houve erro
            return render_template('Pessoas/resultado-pesquisa-pessoas.html', mensagem= mensagem)
    return render_template('Pessoas/resultado-pesquisa-pessoas.html',pessoas=result )

#Opção editar valores pessoa
@app.route('/pessoas/editar/<int:pessoa_id>', methods=['GET', 'POST'])
def edit_valores_pessoas(pessoa_id):
    conn = conectar()
    mensagem = False
    if request.method == 'POST':
        result = edit_pessoa(conn,pessoa_id)
        if isinstance(result, str):  # Verifica se houve erro
            return render_template('erro.html', mensagem=result)
        # Redireciona para a rota '/resultados
        mensagem = True
    return render_template('Pessoas/editar-valores-pessoas.html', mensagem = mensagem)

#Opção para excluir pessoa
@app.route('/pessoas/excluir', methods=['POST'])
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

#Opção para sugestão de nomes de pessoas
@app.route('/professor/nome', methods=['GET','POST'])
def pesquisar_nomes():
    conn = conectar()
    dados = request.json  # Acesse os dados enviados no corpo da solicitação
    print(dados)
    result = pesquisar_nomes_proximos(conn,dados)
    return jsonify(result)

################################################    ALUNOS   ###################################################################################
# Rota para exibir o formulário de adicionar aluno
@app.route('/alunos/form', methods=['POST','GET'])
def aluno_form():
    conn = conectar()
    secretarias = formulario_adicionar_alunos(conn)
    mensagem = False
    if request.method == 'POST':
        result = enviar_valores_alunos(conn)
        if isinstance(result, str):  # Verifica se houve erro
            return render_template('erro.html', mensagem=result)
        mensagem = True
    return render_template('Alunos/alunos-form.html',  secretarias=secretarias, mensagem = mensagem)

#Rota para pesquisar alunos
@app.route('/alunos/pesquisar')
def pesquisar():
    return render_template('Alunos/alunos-pesquisa.html')   

@app.route('/alunos/pesquisar/resultados', methods=['POST'])
def resultado(): 
    conn = conectar ()
    result = resultados_alunos_pesquisados(conn)
    if isinstance(result, str):  # Verifica se houve erro
            return render_template('Alunos/resultado-pesquisa-alunos.html', mensagem=result)
    return render_template('Alunos/resultado-pesquisa-alunos.html',alunos=result)

@app.route('/alunos/editar/alunos/<int:aluno_id>/<int:id_aluno>', methods=['GET', 'POST'])
def edit_aluno(aluno_id,id_aluno):
    conn = conectar()
    mensagem = False
    conn = conectar()
    if request.method == 'POST':
        result = editar_alunos(conn, aluno_id, id_aluno)
        if isinstance(result, str):  # Verifica se houve erro
            return render_template('erro.html', mensagem=result)
        # Redireciona para a rota '/resultados
        mensagem =True
    return render_template('Alunos/editar-valores-alunos.html', mensagem = mensagem)

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
        

################################################    PROFESSORES   ###################################################################################
@app.route('/professores/pesquisar', methods=['GET'])
def pesquisarProfessores():
    return render_template('Professores/professores-pesquisa.html')  
     

# Rota para visualizar todos os professores        
@app.route('/professores/pesquisar/resultados', methods=['POST'])
def professores():
        conn = conectar ()
        if request.method == 'POST':
            result = resultados_professores_pesquisados(conn)
            if isinstance(result, str):  # Verifica se houve erro
                return render_template('Professores/resultado-pesquisa-professores.html', mensagem = result)
        return render_template('Professores/resultado-pesquisa-professores.html', professores = result)

#Rota para editar os valores de professores
@app.route('/professores/editar/<int:professor_id>/<int:id_professor>', methods=['GET', 'POST'])
def editar_professor(professor_id ,id_professor):
    mensagem = False
    conn = conectar()
    secretarias = selecionar_secretaria(conn)
    if request.method == 'POST':
        result = editar_professores(conn, professor_id, id_professor)
        if isinstance(result, str):  # Verifica se houve erro
            return render_template('erro.html', mensagem=result)
        mensagem = True   
    return render_template('Professores/editar-valores-professores.html',secretarias_valores = secretarias, mensagem = mensagem)

@app.route('/professores/excluir', methods=['POST'])
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

# Rota para exibir o formulário e adicionar professor
@app.route('/professores/form', methods = ['GET', 'POST'])
def professor_form():
    mensagem = False
    conn = conectar()
    secretarias = exibir_formulario_professores(conn)
    if request.method =='POST':
        result = enviar_valores_professores(conn)
        if isinstance(result, str):  # Verifica se houve erro
            return render_template('erro.html', mensagem=result)
        mensagem = True
    return render_template('Professores/professores-form.html', secretarias=secretarias, mensagem = mensagem)





################################################    INSCRICOES  ###################################################################################


@app.route('/inscricoes/nomes/pesquisa', methods=['GET','POST'])
def pesquisar_nomes_pessoas():
    conn = conectar()
    dados = request.json  # Acesse os dados enviados no corpo da solicitação
    print(dados)
    result = pesquisar_nomes_proximos_pessoa(conn,dados)
    return jsonify(result)

# Rota para exibir o formulário de adicionar inscrição e inserir uma nova inscrição
@app.route('/inscricoes/form', methods=['GET','POST'])
def inscricao_form():
    conn = conectar()
    mensagem =False
    secretarias = inscricoes_form(conn)
    if request.method == 'POST':
        result = add_inscricao(conn)      
        if isinstance(result, str):  # Verifica se houve erro
            return render_template('erro.html', mensagem=result)
        mensagem = True
    return render_template('Inscricoes/inscricoes-form.html',secretarias = secretarias, mensagem = mensagem)

#Rota para pesquisar inscrições pelo nome ou secretaria
@app.route('/inscricoes/pesquisar') 
def pesquisar_inscricoes():
    conn = conectar ()
    result = secretarias(conn)
    if isinstance(result, str):  # Verifica se houve erro
            return render_template('erro.html', mensagem=result)
    return render_template('Inscricoes/pesquisar-inscricoes.html', secretarias=result)

@app.route('/inscricoes/pesquisa/resultados', methods=['POST'])
def resultado_pesquisa_inscricoes(): 
    conn = conectar ()
    result = pesquisar_incricoes(conn)
    if isinstance(result, str):  # Verifica se houve erro
            return render_template('Inscricoes/resultado-pesquisa-inscricoes.html', mensagem=result)
    return render_template('Inscricoes/resultado-pesquisa-inscricoes.html', inscricoes=result)
# Rota para visualizar todos os cursos

@app.route('/inscricao/editar/valores/<int:inscrito_id>',  methods=['GET', 'POST'])
def editar_valores_incricoes(inscrito_id):
    conn = conectar()
    mensagem = False
    secretarias = selecionar_secretaria(conn)    
    if request.method == 'POST':
        result = editar_inscricoes(conn,inscrito_id)
        if isinstance(result, str):  # Verifica se houve erro
            return render_template('erro.html', mensagem=result)
        mensagem = True 
    return render_template('Inscricoes/editar-valores-inscricoes.html',secretarias = secretarias, mensagem = mensagem)
     
@app.route('/inscricao/excluir', methods=['POST'])
def excluir_inscrito():
        data = request.json
        print('dados recebidos', data)
        inscricao_id = data.get('inscricao_id')
        print(inscricao_id)
        conn = conectar()
        result = excluir_inscricao(conn, inscricao_id)
        if isinstance(result, str):  # Verifica se houve erro
            return render_template('erro.html', mensagem=result)



################################################    CURSOS  ###################################################################################
@app.route('/cursos/pesquisar', methods=['GET'])
def cursos():
    conn = conectar()
    result = pesquisar_secretarias(conn)
    if isinstance(result, str):  # Verifica se houve erro
        return render_template('erro.html', mensagem= result)
    return render_template('Cursos/cursos.html',secretarias = result )
   
@app.route('/cursos/pesquisar/resultados', methods=['POST'])
def pesquisar_cursos():
    conn = conectar()
    result = resultados_cursos_pesquisados(conn)
    print(result)
    if isinstance(result, str):  # Verifica se houve erro
             return render_template('Cursos/resultado-pesquisa-cursos.html',mensagem = result)
    return render_template('Cursos/resultado-pesquisa-cursos.html',cursos = result)

# Rota para exibir o formulário e adicionar curso
@app.route('/cursos/form', methods=['POST', 'GET'])
def curso_form():
    conn = conectar()
    mensagem = False
    secretarias = pesquisar_secretarias(conn)
    if request.method == 'POST':
        result = add_cursos(conn)
        if isinstance(result, str):  # Verifica se houve erro
            return render_template('erro.html', mensagem= result)
        mensagem = True
    return render_template('Cursos/cursos-form.html', secretarias = secretarias, mensagem = mensagem)


@app.route('/cursos/editar/<int:curso_id>',methods=['GET', 'POST'])
def edit_cursos(curso_id):
    conn = conectar()
    mensagem = False
    secretarias = selecionar_secretaria(conn)  
    if request.method == 'POST':
        result =editar_cursos(conn, curso_id)
        if isinstance(result, str):  # Verifica se houve erro
            return render_template('erro.html', mensagem= result)
        mensagem = True
    return render_template('Cursos/editar-valores-cursos.html', secretarias = secretarias, mensagem = mensagem)    

@app.route('/cursos/excluir',methods=['POST'])
def excl_curso():
    data = request.json
    print('dados recebidos', data)
    curso_id = data.get('curso_id')
    print(curso_id)
    conn = conectar()
    result = excluir_curso(conn,curso_id)
    if isinstance(result, str):  # Verifica se houve erro
            return render_template('erro.html', mensagem=result)
    return 'SUCCESS'




################################################    TURMAS  ###################################################################################
# Rota para exibir o formulário de adicionar turma
@app.route('/turmas/form', methods =['POST', 'GET'])
def turma_form():
    conn = conectar()
    mensagem = False
    cursos= exibir_formulario_turmas(conn)
    if request.method == 'POST':
        result = adicionar_turma(conn)
        if isinstance(result, str):  # Verifica se houve erro
            return render_template('erro.html', mensagem=result)
        mensagem = True
    return render_template('Turmas/turmas-form.html', cursos=cursos, mensagem = mensagem)
    
#Rota para pesquisar e exibir os resultados de pesquisa de turmas
@app.route('/turmas/pesquisar', methods=['GET','POST'])
def pesquisar_turma():
    conn = conectar()
    if request.method == 'POST':
        result = resultados_turmas_pesquisados(conn)
        if isinstance(result, str):  # Verifica se houve erro
            return render_template('Turmas/resultado-pesquisa-turma.html',mensagem = result)
        return render_template('Turmas/resultado-pesquisa-turma.html', turmas = result)
    return render_template ('Turmas/turmas-pesquisa.html')

@app.route('/turmas/editar/<int:id_turma>', methods= ['GET','POST'])
def editar_turma(id_turma):
    conn = conectar()
    mensagem = False
    turmas = exibir_formulario_turmas(conn)
    if request.method == 'POST':
        result = editar_valores_turma(conn,id_turma)  
        if isinstance(result, str):  # Verifica se houve erro
            return render_template('erro.html', mensagem= result)
        mensagem = True
    return render_template('Turmas/editar-valores-turma.html', cursos = turmas, mensagem = mensagem)

@app.route('/turmas/excluir', methods=['POST'])
def excl_turma():
    data = request.json
    id_turma = data.get('turma_id')
    conn = conectar()
    result = excluir_turmas(conn,id_turma)
    if isinstance(result, str):  # Verifica se houve erro
            return render_template('erro.html', mensagem= result)
    return 'SUCCESS'




################################################    TURMAS-PROFESSORES   ###################################################################################
# Rota para visualizar todas as turmas dos professores
@app.route('/turmas/professores/pesquisa', methods = ['POST', 'GET'])
def turmas_professores():
    if request.method == 'POST':
        conn = conectar()
        result = resultados_turmas_professores_pesquisados(conn)
        if isinstance(result, str):  
            return render_template('Turmas_professores/resultado-pesquisa-turmas-professores.html', mensagem = result)
        return render_template('Turmas_professores/resultado-pesquisa-turmas-professores.html', turmas_professores = result)
    return render_template('Turmas_professores/turmas-professores-pesquisa.html')

# Rota para adicionar uma nova turma para professor
@app.route('/turmas/professores/form', methods=['POST','GET'])
def add_turma_professor():
    conn = conectar()
    mensagem = False
    if request.method == 'POST':
        result = enviar_valores_turmas_professores(conn)
        if isinstance(result, str):  # Verifica se houve erro
            return render_template('erro.html', mensagem=result)
        mensagem = True
    return render_template('Turmas_professores/turmas-professores-form.html',mensagem = mensagem)

@app.route('/turmas/professores/proximos', methods=['GET','POST'])
def pesquisar_nomes_professor_turma():
    conn = conectar()
    dados = request.json  # Acesse os dados enviados no corpo da solicitação
    print(dados)
    result = pesquisar_nomes_proximos_professores_turma(conn,dados)
    print(result)
    return jsonify(result)



@app.route('/turmas/professores/nomes/proximos', methods=['GET','POST'])
def pesquisar_nomes_professores_turmas():
    conn = conectar()
    dados = request.json  # Acesse os dados enviados no corpo da solicitação
    print(dados)
    result = pesquisar_nomes_professores(conn,dados)
    print(result)
    return jsonify(result)

@app.route('/turmas/professores/nomes/turmas', methods=['GET','POST'])
def pesquisar_nomes_turmas():
    conn = conectar()
    dados = request.json  # Acesse os dados enviados no corpo da solicitação
    print(dados)
    result = pesquisar_nomes_proximos_turma(conn,dados)
    print(result)
    return jsonify(result)

@app.route('/turmas/professores/editar/<int:id_turma_professor>', methods=['GET','POST'])
def editar_turmas_professores(id_turma_professor):
            conn = conectar()
            mensagem = False
            if request.method == 'POST':
                result =editar_valores_turmas_professores(conn, id_turma_professor)
                if isinstance(result, str):  # Verifica se houve erro
                    return render_template('erro.html', mensagem= result)
                mensagem = True   
            return render_template('Turmas_professores/editar-valores-professores-turma.html',mensagem = mensagem) 

@app.route('/turmas/professores/excluir',methods=['POST'])
def excl_turma_professor():
    data = request.json
    print('dados recebidos', data)
    turmas_professores_id = data.get('turma_id')
    print(turmas_professores_id)
    conn = conectar()
    result = excluir_turmas_professores(conn,turmas_professores_id)
    if isinstance(result, str):  # Verifica se houve erro
            return render_template('erro.html', mensagem=result)




################################################    MATRICULAS   ###################################################################################
@app.route('/pesquisando-nome-turma-matricula', methods=['GET','POST'])
def pesquisando_turmas_matricula():
    conn = conectar()
    dados = request.json  # Acesse os dados enviados no corpo da solicitação
    print(dados)
    result = pesquisar_nomes_proximos_turma(conn,dados)
    print(result)
    return jsonify(result)

@app.route('/pesquisando-nomes-inscrito', methods=['GET','POST'])
def pesquisando_inscrito_matricula():
    conn = conectar()
    dados = request.json  # Acesse os dados enviados no corpo da solicitação
    print(dados)
    result = pesquisar_nomes_proximos_inscrito(conn,dados)
    print(result)
    return jsonify(result)

# Rota para visualizar todas as matrículas
@app.route('/matriculas')
def matriculas():
        return render_template('Matriculas/pesquisar-matriculas.html', matriculas=matriculas)
@app.route('/resultado-pesquisa-matricula',methods = ['POST'])
def pesquisar_matriculas():
     conn = conectar()
     result = pesquisar_valores_matriculas(conn)
     if isinstance(result, str):  # Verifica se houve erro
            return render_template('erro.html', mensagem=result)
     return render_template('Matriculas/resultado-pesquisa-matriculas.html', matriculas=result)
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
        return render_template('Matriculas/matriculas-form.html', turmas=turmas, inscricoes=inscricoes)
    except mysql.connector.Error as err:
        return render_template('erro.html', mensagem=f'Erro ao buscar dados: {err}')
# Rota para adicionar uma nova matrícula
@app.route('/matriculas', methods=['POST'])
def add_matricula():
        conn = conectar()
        result = enviar_valores_matricula(conn)
        if isinstance(result, str):  # Verifica se houve erro
            return render_template('erro.html', mensagem=result)
        return redirect('/')

@app.route('/editar-valores-matriculas/<int:matriculas_id>',methods = ['GET', 'POST'])
def edit_matriculas(matriculas_id):
    conn = conectar()
    if request.method == 'POST':
                result =editar_matriculas(conn, matriculas_id)
                if isinstance(result, str):  # Verifica se houve erro
                    return render_template('erro.html', mensagem= result)
                return redirect('/')     
    return render_template('Matriculas/editar-valores-matriculas.html') 
    

@app.route('/excluir-matriculas',methods = ['POST'])
def excl_matric():
     conn=conectar()
     data = request.json
     print('dados recebidos', data)
     matriculas_id= data.get('matricula_id')
     print(matriculas_id)
     result= excluir_matriculas(conn,matriculas_id)
     if isinstance(result, str):  # Verifica se houve erro
                    return render_template('erro.html', mensagem= result)
     return redirect('/')   


     

###########################################################   PLANOS DE AULA   ########################################################################
# Rota para exibir todos os planos de aula
@app.route('/planos-aula-pesquisa')
def pesquisar_planos():
     return render_template('PlanosAula/pesquisar-planos-aula.html')


@app.route('/resultados-pesquisa-plano-aula',methods=['POST'])
def planos():
    conn = conectar()
    result = pesquisar_plano_aula(conn)
    print(result)
    if isinstance(result, str):  # Verifica se houve erro
            return render_template('erro.html', mensagem= result)
    return render_template('PlanosAula/resultados-pesquisa-planos-aula.html',planos=result)
  


@app.route('/planos-form')
def planos_form():
    return render_template('PlanosAula/planos-form.html')


# Rota para adicionar um novo plano de aula
@app.route('/planos', methods=['POST'])
def add_plano():
        conn = conectar()
        result = adicionar_plano_aula(conn)
        if isinstance(result, str):  # Verifica se houve erro
                    return render_template('erro.html', mensagem= result)
        return redirect('/')

@app.route('/editar-valores-planos/<int:planos_id>', methods=['POST','GET'])
def edit_planos_aula(planos_id):
    conn = conectar()
    if request.method == 'POST':
                result =editar_planos(conn, planos_id)
                if isinstance(result, str):  # Verifica se houve erro
                    return render_template('erro.html', mensagem= result)
                return redirect('/')     
    return render_template('PlanosAula/editar-valores-planos.html') 

@app.route('/excluir-planos-aula', methods=['POST'])
def excl_planos_aula():
     conn=conectar()
     data = request.json
     print('dados recebidos', data)
     planos_id= data.get('planos_id')
     print(planos_id)
     result= excluir_planos_aula(conn,planos_id)
     if isinstance(result, str):  # Verifica se houve erro
                    return render_template('erro.html', mensagem= result)
     return redirect('/')   


############################################################################################################################################




###########################################################   FALTAS      ########################################################################

@app.route('/pesquisar-faltas')
def faltas():
   return render_template('Faltas/pesquisar-faltas.html')

@app.route('/faltas-form')
def faltas_form():
        return render_template('Faltas/faltas-form.html')

@app.route('/faltas', methods=['POST'])
def add_falta():
    conn = conectar()
    result = adicionar_falta(conn)
    if isinstance(result, str):  # Verifica se houve erro
            return render_template('erro.html', mensagem= result)
    return redirect('/')   
 
@app.route('/pesquisar-nome-conteudo', methods=['GET','POST'])
def pesquisar_conteudo():
    conn = conectar()
    dados = request.json  # Acesse os dados enviados no corpo da solicitação
    print(dados)
    result = pesquisar_nome_conteudo(conn,dados)
    print(result)
    return jsonify(result)
     
@app.route("/resultado-pesquisa-faltas",methods=['POST'])
def pesquisar_faltas_alunos():
     conn = conectar()
     result = pesquisar_faltas(conn)
     if isinstance(result, str):  # Verifica se houve erro
            return render_template('erro.html', mensagem= result)
     return render_template('Faltas/resultados-pesquisa-faltas.html',faltas=result)


@app.route('/editar-valores-faltas/<int:faltas_id>', methods=['POST','GET'])
def edit_faltas(faltas_id):
    conn = conectar()
    if request.method == 'POST':
                result =editar_faltas(conn, faltas_id)
                if isinstance(result, str):  # Verifica se houve erro
                    return render_template('erro.html', mensagem= result)
                return redirect('/')     
    return render_template('Faltas/editar-valores-faltas.html') 

@app.route('/excluir-faltas', methods=['POST'])
def excl_faltas():
     conn=conectar()
     data = request.json
     print('dados recebidos', data)
     faltas_id= data.get('faltas_id')
     print(faltas_id)
     result= excluir_falta(conn,faltas_id)
     if isinstance(result, str):  # Verifica se houve erro
                    return render_template('erro.html', mensagem= result)
     return redirect('/')   
      

if __name__ == '__main__':
    app.run(debug=True)
