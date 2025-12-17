from sqlalchemy import Column, String, Integer, Boolean, DateTime, Float, NotNullable
from sqlalchemy.ext.declarative import declarative_base

#é um modelo que vai  representar uma tabela no BD
Base = declarative_base()
class Usuario(Base):
    __tablename__ = 'usuarios'

    login = Column(String, primary_key=True)
    senha = Column(String)
    tipo = Column(String)

    def __init__(self, login, senha, tipo):
        self.login = login
        self.senha = senha
        self.tipo = tipo


    def __repr__(self):
        return f"<Usuario(login='{self.login}', senha='{self.senha}', tipo='{self.tipo}')>"


class Roupa(Base):
    __tablename__= 'roupas'

    nome = Column(String, nullable=False)
    categoria = Column(String, nullable=False)
    tamanho = Column(String, nullable=False)
    preco = Column(Float, nullable=False)
    descricao = Column(String)
    nomevendedor = Column(String, nullable=False)
    genero = Column(String, nullable=False)
    id = Column(Integer, primary_key=True, autoincrement=True)
    estoque = Column(Integer, nullable=False)

    def __init__(self, nome, categoria, tamanho, preco, descricao, nomevendedor, genero, estoque):
        self.nome = nome
        self.categoria = categoria
        self.tamanho = tamanho
        self.preco = preco
        self.descricao = descricao
        self.nomevendedor = nomevendedor
        self.genero = genero
        self.estoque = estoque

    def __repr__(self):
        return f"<Roupa(nome='{self.nome}', preco='{self.preco}')>"

class Calcado(Base):
    __tablename__= 'calcados'

    nome = Column(String, nullable=False)
    categoria = Column(String, nullable=False)
    numeracao = Column(String, nullable=False)
    preco = Column(Float, nullable=False)
    descricao = Column(String)
    nomevendedor = Column(String, nullable=False)
    genero = Column(String, nullable=False)
    id = Column(Integer, primary_key=True, autoincrement=True)
    estoque = Column(Integer, nullable=False)

    def __init__(self, nome, categoria, tamanho, preco, descricao, nomevendedor, genero, estoque):
        self.nome = nome
        self.categoria = categoria
        self.numeracao = tamanho
        self.preco = preco
        self.descricao = descricao
        self.nomevendedor = nomevendedor
        self.genero = genero
        self.estoque = estoque

    def __repr__(self):
        return f"<Calcado(nome='{self.nome}', preco='{self.preco}')>"