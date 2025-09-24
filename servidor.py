from flask import *

app = Flask(__name__)

roupas = []
calcados = []
vendedores = [['rome', '123']]
clientes = []
logado = False
cliente = False
vendedor = False
nomevendedor = ""



@app.route('/')
def pag_principal():
    return render_template('paginainicial.html')

@app.route('/cadastrarcalcado', methods=['post'])
def cadastro_calcado():

    global calcados

    if  logado and vendedor:

        nome = request.form.get('nomecalcado')
        categoria = request.form.get('categoria')
        numeracao = request.form.get('numeracao')
        preco = request.form.get('preco')
        descricao = request.form.get('descricao')

        if nome == None or nome == '' or preco == None or preco == '':
    
            msg = 'Preencha todos os campos!'
            print(calcados)
            return render_template('cadastrarcalcado.html', erro = msg)


        calcado = [nome, categoria, numeracao, preco, descricao, nomevendedor]

        
        calcados.append(calcado)

        feedback = 'Calçado cadastrado com sucesso!'
        print(calcados)
        return render_template('cadastrarcalcado.html', retorno = feedback)
    
    else: return render_template('login.html')

@app.route('/cadastro')
def cadastro():
    return render_template('cadastrousuario.html')

@app.route('/cadastrar', methods = ['post'])
def cadastrar():
    usuario = request.form.get('usuario')
    senha = request.form.get('senha')
    tipouser = request.form.get('tipouser')
    msg = ''
    login = [usuario, senha]
    repetido = False

    global vendedores, clientes

    if tipouser == 'vendedor':
        for vendedor in vendedores:
            if usuario == vendedor[0]:
                repetido = True

        if repetido:
            msg = "Usuário já existe."
            return render_template('cadastrousuario.html', saida=msg)

        else:
            vendedores.append(login)
            msg = 'Usuário cadastrado com sucesso!'

        print(vendedores)
        return render_template('cadastrousuario.html', saida = msg)

    else:
        for cliente in clientes:
            if usuario == cliente[0]:
                repetido = True

        if repetido:
            msg = "Usuário já existe."
            return render_template('cadastrousuario.html', saida=msg)

        else:
            clientes.append(login)
            msg = 'Usuário cadastrado com sucesso!'
        print(clientes)
        return render_template('cadastrousuario.html', saida = msg)


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/logar', methods=['post'])
def logar ():
    usuario = request.form.get('usuario')
    senha = request.form.get('senha')
    global logado, cliente, vendedor, nomevendedor
    for cliente in clientes:
        if usuario == cliente[0] and senha == cliente[1]:
            logado = True
            cliente = True
            vendedor = False
            return render_template('paginainicial.html')
        
    for vendedor in vendedores:
        if usuario == vendedor[0] and senha == vendedor[1]:
            logado = True
            vendedor = True
            cliente = False
            nomevendedor = usuario
            return render_template('paginainicial.html')

    msg = 'Usuário ou senha incorretos'
    return render_template('login.html', erro = msg)

@app.route('/cadastraritem')
def cadastro_item():
    
    if logado and vendedor:

        return render_template('cadastraritem.html')
    
    else: return render_template('login.html')

@app.route('/cadastrarroupa', methods=['post'])
def cadastro_roupa():

    if logado and vendedor:
        nome = request.form.get('nomeroupa')
        categoria = request.form.get('categoria')
        tamanho = request.form.get('tamanho')
        preco = request.form.get('preco')
        descricao = request.form.get('descricao')
        global roupas

        if nome == None or preco == None:
    
            msg = 'Preencha todos os campos!'
            print(roupas)
            return render_template('cadastrarroupa.html', erro = msg)

        roupa = [nome, categoria, tamanho, preco, descricao, nomevendedor]

        roupas.append(roupa)
        msg = "Roupa cadastrada com sucesso!"

        print(roupas)
        return render_template('cadastrarroupa.html', retorno = msg)


@app.route('/pesquisar', methods=['post'])
def pesquisar():
    pesquisas = []
    pesquisar = request.form.get('pesquisar')
    if pesquisar:
        for roupa in roupas:
            if pesquisar.lower() == roupa[0].lower():
                pesquisas.append(roupa)
        for calcado in calcados:
            if pesquisar.lower() == calcado[0].lower():
                pesquisas.append(calcado)
    print(f"Resultados: {pesquisas}")
    return render_template('pesquisa.html', lista = pesquisas)

@app.route('/meusitens', methods=['post'])
def meus_itens():
    meusitens = []

    for roupa in roupas:
        if roupa[5] == nomevendedor:
            meusitens.append(roupa)

    for calcado in calcados:
        if calcado[5] == nomevendedor:
            meusitens.append(calcado)

    print(meusitens)
    return render_template('meusitens.html', lista = meusitens)

if __name__ == '__main__':
    app.run()