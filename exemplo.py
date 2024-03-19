@app.route('/buscar/', methods=['GET'])
def buscar():
    nome = request.args.get('nome')
    documento = request.args.get('documento')
    data_nascimento_min = request.args.get('data_nascimento_min')
    data_nascimento_max = request.args.get('data_nascimento_max')
    bairro = request.args.get('bairro')
    endereco = request.args.get('endereco')

    conn = get_db_connection()
    cur = conn.cursor()

    query = """
    SELECT DISTINCT ON (favorecido.nome)
           favorecido.*, 
           fotoscidadao.item AS foto_item, 
           logradouro.descr AS endereco, 
           moradia.numero AS numero, 
           bairro.descr AS bairro, 
           moradia.complemento AS complemento 
    FROM favorecido 
    LEFT JOIN fotoscidadao ON favorecido.item = fotoscidadao.cidadao 
    LEFT JOIN moradia ON favorecido.ref_moradia = moradia.referencial 
    LEFT JOIN logradouro ON moradia.ref_logradouro = logradouro.item 
    LEFT JOIN bairro ON moradia.ref_bairro = bairro.item 
    WHERE 1=1
    """

    params = []

    if nome:
        partes_nome = nome.split()

        condicoes_nome = []
        for parte_nome in partes_nome:
            condicoes_nome.append("(unaccent(nome) ILIKE unaccent(%s))")
            params.append('%' + parte_nome + '%')

        query += " AND (" + " AND ".join(condicoes_nome) + ")"

    if documento:
        query += " AND (cpf ILIKE %s OR rg ILIKE %s)"
        params.extend(['%' + documento + '%', '%' + documento + '%'])

    if data_nascimento_min and data_nascimento_max:
        query += " AND dtnasc BETWEEN %s AND %s"
        params.extend([data_nascimento_min, data_nascimento_max])

    elif data_nascimento_min:
        query += " AND dtnasc >= %s"
        params.append(data_nascimento_min)

    elif data_nascimento_max:
        query += " AND dtnasc <= %s"
        params.append(data_nascimento_max)

    if bairro:
        bairro = bairro.upper()
        query += " AND bairro.descr = %s"
        params.append(bairro)

    if endereco:
        endereco = endereco.upper()
        query += " AND logradouro.descr = %s"
        params.append(endereco)

    query += " ORDER BY nome ASC"

    cur.execute(query, params)
    favorecidos = cur.fetchall()

    # Se alguma informação estiver vazia, vai ficar em branco ao invés de aparecer "none"
    favorecidos_limpos = []
    for favorecido in favorecidos:
        favorecido_limpo = [
            "" if value is None else value for value in favorecido]
        favorecidos_limpos.append(favorecido_limpo)

    conn.close()
    return render_template('resultado.html', favorecidos=favorecidos_limpos)