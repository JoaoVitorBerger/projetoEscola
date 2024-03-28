
import mysql.connector
from flask import redirect, request, url_for,jsonify
from datetime import datetime

# Rota para exibir secretarias
def secretarias(conn):
    try:
      cursor = conn.cursor(dictionary=True)
      cursor.execute('''SELECT 
                            id, 
                            nome, 
                            criado_em, 
                            modificado_em, 
                            criado_por, 
                            modificado_por,
                            ativo_flag,
                            deletado_em,
                        CASE
                            WHEN ativo_flag = 1 THEN 'Ativo'
                            ELSE 'Desativado'
                        END AS ativo_flag
                        FROM 
                            secretarias
                        WHERE 
                            deletado_em IS NULL''')
      secretarias = cursor.fetchall()
      return secretarias
    except mysql.connector.Error as err:
      return f'Erro ao buscar secretarias: {err}'
    
# Rota para exibir o formulário de adicionar secretaria
def secretaria_form(conn):
    return

# Rota para adicionar uma nova secretaria
def add_secretaria(conn):
    try:
        cursor = conn.cursor()
        nome = request.form['nome'].upper()
        data_criacao = datetime.now()  # Obtém a data e hora atuais
        cursor.execute('INSERT INTO secretarias (nome, criado_em) VALUES (%s, %s)', (nome, data_criacao))
        conn.commit()
        return 
    except mysql.connector.Error as err:
        return f'Erro ao adicionar secretaria: {err}'
    
def edit_secretaria(secretaria_id,conn):

  cursor = conn.cursor(dictionary=True)
  if request.method =='POST':
    try:
       new_nome_secretaria = request.form['new_nome_secretaria'].upper()
       query='''UPDATE secretarias
                SET nome = %s,
                modificado_em = %s
                WHERE id = %s
       '''
       cursor.execute(query,(new_nome_secretaria, datetime.now(), secretaria_id))
       conn.commit()
       print('Estou enviando')

    except mysql.connector.Error as err:
        print ('Erro ao editar secretaria: {err}')
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


  
   


   

    
     
   
      
    
      
   
       
   