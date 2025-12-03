from sqlalchemy.orm import scoped_session
from modelos.modelos import Usuario

class UsuarioDAO:
    #construtor da classe: instanciar um objeto, ele cria uma sessao
    def __init__(self, session: scoped_session):
        self.session = session

    def criar(self, usuario):
        #adiciona um objeto/modelo no banco de dados
        self.session.add(usuario)
        #autorizando modificações no banco/ gravando a alteração
        self.session.commit()

    def buscar_por_usuario(self, login):
        return self.session.query(Usuario).filter_by(login= login).first()

    def listar_usuarios(self):
        return self.session.query(Usuario).all()

    def autenticar(self, login, senha):
        user = self.buscar_por_usuario(login)
        if user and user.senha == senha:
            return user
        return None
