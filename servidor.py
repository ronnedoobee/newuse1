from flask import *
from utils.auxiliares import *
from dao.banco import init_db, Session
from dao.usuarioDAO import *
from dao.roupaDAO import *
from dao.calcadoDAO import *


app = Flask(__name__)

app.secret_key = 'KJH#45K45JHQASs'

roupas = []
calcados = []
vendedores = [['rome', '123']]
clientes = []

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

    session['logado'] = True
    session['usuario'] = usuario
    session['vendedor'] = usuario_dao.verificar_vendedor(usuario)

    print(session.get('usuario'))
    return render_template('paginainicial.html', usuario=usuario)

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

@app.route('/logout')
def logout():
    session.clear()
    return render_template('paginainicial.html')


@app.route('/meuperfil')
def meu_perfil():
    usuario_dao = UsuarioDAO(g.session)
    usuario = usuario_dao.buscar_por_usuario(session.get('usuario'))
    if not session.get('logado'):
        return render_template('login.html')

    if not session.get('vendedor'):
        return render_template('meu-perfil-cliente.html', usuario = usuario)

    return render_template('meu-perfil-vendedor.html', usuario = usuario)


@app.route('/cadastraritem')
def cadastro_item():

    usuario_dao = UsuarioDAO(g.session)

    if not session.get('logado') or not session.get('vendedor'):
        return redirect(url_for('login'))

    return render_template('cadastraritem.html')

@app.route('/cadastrarroupa', methods=['GET', 'POST'])
def cadastro_roupa():

    if request.method == 'GET':
        return render_template('cadastrarroupa.html')

    roupa_dao = RoupaDAO(g.session)

    if not session.get('logado') or not session.get('vendedor'):
        return render_template('login.html')

    nome = request.form.get('nomeroupa')
    categoria = request.form.get('categoria')
    tamanho = request.form.get('tamanho')
    preco = request.form.get('preco')
    descricao = request.form.get('descricao')
    nomevendedor = session.get('usuario')
    genero = request.form.get('genero')
    estoque = request.form.get('estoque')

    roupa = Roupa(nome, categoria, tamanho, preco, descricao, nomevendedor, genero, estoque)
    roupa_dao.criar(roupa)
    msg = "Roupa cadastrada com sucesso!"
    return render_template("cadastrarroupa.html", msg = msg)


@app.route('/cadastrarcalcado', methods=['GET', 'POST'])
def cadastro_calcado():

    if request.method == 'GET':
        return render_template('cadastrarcalcado.html')

    calcado_dao = CalcadoDAO(g.session)

    if not session.get('logado') or not session.get('vendedor'):
        return render_template('login.html')

    nome = request.form.get('nomecalcado')
    categoria = request.form.get('categoria')
    numeracao = request.form.get('numeracao')
    preco = request.form.get('preco')
    descricao = request.form.get('descricao')
    nomevendedor = session.get('usuario')
    genero = request.form.get('genero')
    estoque = request.form.get('estoque')

    calcado = Calcado(nome, categoria, numeracao, preco, descricao, nomevendedor, genero, estoque)
    calcado_dao.criar(calcado)
    msg = "Calçado cadastrada com sucesso!"
    return render_template("cadastrarcalcado.html", msg = msg)


@app.route('/meusitens')
def meus_itens():
    roupa_dao = RoupaDAO(g.session)
    calcado_dao = CalcadoDAO(g.session)
    if not session.get('logado') or not session.get('vendedor'):
        return render_template('login.html')

    roupas = roupa_dao.listar_por_vendedor(session.get('usuario'))
    calcados = calcado_dao.listar_por_vendedor(session.get('usuario'))

    for roupa in roupas:
        roupa.tipo = "roupa"

    for calcado in calcados:
        calcado.tipo = "calcado"

    lista = roupas + calcados

    return render_template('meusitens.html', lista=lista)


@app.route('/detalhes')
def detalhes_itens():

    if not session.get('logado') or not session.get('vendedor'):
        return render_template('login.html')

    tipo = request.args.get('tipo')
    id_item = request.args.get('id')

    if tipo == "roupa":
        dao = RoupaDAO(g.session)

    elif tipo == "calcado":
        dao = CalcadoDAO(g.session)

    item = dao.buscar_por_id(id_item)

    return render_template("detalhes.html", item = item, tipo = tipo)


if __name__ == '__main__':
    app.run()