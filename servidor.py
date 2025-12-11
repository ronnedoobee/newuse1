from flask import *
from utils.auxiliares import *
from dao.banco import init_db, Session
from dao.usuarioDAO import *
from dao.roupaDAO import *


app = Flask(__name__)

app.secret_key = 'KJH#45K45JHQASs'

roupas = []
calcados = []
vendedores = [['rome', '123']]
clientes = []
logado = False
cliente = False
vendedor = False
nomevendedor = ""
id = 0

init_db()

@app.before_request
def pegar_sessao():
    g.session = Session()

@app.teardown_appcontext
def encerrar_sessao(exception=None):
    Session.remove()

@app.route('/')
def pag_principal():

    itens_venda = []
    for roupa in roupas:
        itens_venda.append(roupa)

    for calcado in calcados:
        itens_venda.append(calcado)

    return render_template('paginainicial.html', itens = itens_venda)

@app.route('/cadastrarcalcado', methods=['post'])
def cadastro_calcado():

    global calcados, id

    if not session.get('logado') or session.get('tipo') != 'vendedor':
        return render_template('login.html')

    nome = request.form.get('nomecalcado')
    categoria = request.form.get('categoria')
    numeracao = request.form.get('numeracao')
    preco = request.form.get('preco')
    descricao = request.form.get('descricao')
    genero = request.form.get('genero')
    estoque = request.form.get('estoque')


    if not cadastrar_calcado(nome, categoria, numeracao, preco, descricao, nomevendedor, genero, id, calcados, estoque):
        msg = 'Preencha todos os campos!'
        print(calcados)
        return render_template('cadastrarcalcado.html', erro = msg)

    feedback = 'Calçado cadastrado com sucesso!'
    print(calcados)
    return render_template('cadastrarcalcado.html', retorno = feedback)

@app.route('/cadastro')
def cadastro():
    return render_template('cadastrousuario.html')

@app.route('/cadastrar', methods = ['post'])
def cadastrar():
    usuario_dao = UsuarioDAO(g.session)

    usuario = request.form.get('usuario')
    senha = request.form.get('senha')
    tipouser = request.form.get('tipouser')

    novo_usuario = Usuario(usuario, senha, tipouser)

    if usuario_dao.buscar_por_usuario(usuario) is None:
        usuario_dao.criar(novo_usuario)
        msg = 'Usuário cadastrado com sucesso!'
        return render_template('cadastrousuario.html', saida=msg)

    msg = 'Usuário já existe!'
    return render_template('cadastrousuario.html', saida=msg)


    ##msg = 'Usuário já existe!'
    ##return render_template('cadastrousuario.html', saida=msg)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/logar', methods=['post'])
def logar ():
    usuario = request.form.get('usuario')
    senha = request.form.get('senha')

    usuario_dao = UsuarioDAO(g.session)

    if usuario_dao.autenticar(usuario, senha) is None:
        msg = 'Usuário ou senha incorretos'
        return render_template('login.html', erro=msg)

    session['usuario'] = usuario_dao.buscar_por_usuario(usuario).tipo
    return render_template('paginainicial.html', usuario=usuario)


@app.route('/cadastraritem')
def cadastro_item():

    if not session.get('logado') or session.get('tipo') != 'vendedor':
        return render_template('login.html')

    return render_template('cadastraritem.html')


@app.route('/cadastrarroupa', methods=['post'])
def cadastro_roupa():

    if not session.get('logado') or session.get('tipo') != 'vendedor':
        return render_template('login.html')

    nome = request.form.get('nomeroupa')
    categoria = request.form.get('categoria')
    tamanho = request.form.get('tamanho')
    preco = request.form.get('preco')
    descricao = request.form.get('descricao')
    genero = request.form.get('genero')
    estoque = request.form.get('estoque')

    if not cadastrar_roupa(nome, categoria, tamanho, preco, descricao, nomevendedor, genero, id, roupas, estoque):
        msg = 'Preencha todos os campos!'
        print(roupas)
        return render_template('cadastrarroupa.html', erro = msg)

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

    if not session.get('logado') or session.get('tipo') != 'vendedor':
        return render_template('login.html')

    meusitens = []

    exibir_itens(nomevendedor, roupas, meusitens)
    exibir_itens(nomevendedor, calcados, meusitens)

    print(meusitens)
    return render_template('meusitens.html', lista = meusitens)

@app.route('/detalhes')
def detalhes_itens():

    if not session.get('logado') or session.get('tipo') != 'vendedor':
        return render_template('login.html')

    vendedor = request.values.get('vendedor')
    nome = request.values.get('nome')
    item = None

    for roupa in roupas:
        if roupa[0] == nome and roupa[5] == vendedor:
            item = roupa
            break

    return render_template('detalhesroupa.html', roupa=item)

@app.route('/remover', methods = ['post'])
def remover_item():

    if not session.get('logado') or session.get('tipo') != 'vendedor':
        return render_template('login.html')

    idroupa = request.form.get('id')
    global roupas, calcados

    deletar_item(idroupa, roupas)
    deletar_item(idroupa, calcados)

    meusitens = []

    exibir_itens(nomevendedor, roupas, meusitens)
    exibir_itens(nomevendedor, calcados, meusitens)

    print(meusitens)
    return render_template('meusitens.html', lista=meusitens)



if __name__ == '__main__':
    app.run()