from sqlalchemy.orm import scoped_session
from modelos.modelos import Calcado

class CalcadoDAO:
    def __init__(self, session: scoped_session):
        self.session = session

    def criar(self, calcado):
        self.session.add(calcado)
        self.session.commit()

    def listar_por_vendedor(self, nomevendedor):
        return self.session.query(Calcado).filter_by(nomevendedor=nomevendedor).all()

    def buscar_por_id(self, id):
        return self.session.query(Calcado).filter_by(id=id).first()