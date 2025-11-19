def logar_vendedor(usuario, senha, vendedores ):
    for vendedor in vendedores:
        if usuario == vendedor[0] and senha == vendedor[1]:
            return True
    return False

def logar_cliente(usuario, senha, clientes ):
    for cliente in clientes:
        if usuario == cliente[0] and senha == cliente[1]:
            return True
    return False

def cadastrar_roupa(nome, categoria, tamanho, preco, descricao, nomevendedor, genero, id, roupas):
    if nome == '' or preco == '' or preco is None or nome is None:
        return False

    id += 1
    roupa = [nome, categoria, tamanho, preco, descricao, nomevendedor, genero, id]

    roupas.append(roupa)
    return True

def exibir_itens(nome_vendedor, lista_verificar, lista_adicionar):
    for item in lista_verificar:
        if item[5] == nome_vendedor:
            lista_adicionar.append(item)
    return

def cadastrar_calcado(nome, categoria, numeracao, preco, descricao, nomevendedor, genero, id, calcados):
    if nome == '' or preco == '' or preco is None or nome is None:
        return False

    id += 1
    calcado = [nome, categoria, numeracao, preco, descricao, nomevendedor, genero, id]

    calcados.append(calcado)
    return True

def cadastro_usuario(usuario, senha, tipo_usuario, vendedores, clientes):

    for vendedor in vendedores:
        if usuario == vendedor[0]:
            return False

    for cliente in clientes:
        if usuario == cliente[0]:
            return False

    login = [usuario, senha]
    if tipo_usuario == 'vendedor':
        vendedores.append(login)
        return True

    clientes.append(login)
    return True

def deletar_item(idropa, lista):
    for item in lista:
        if idropa == str(item[7]):
            lista.remove(item)
            return True
    return None