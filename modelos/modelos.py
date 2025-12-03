from sqlalchemy import Column, String, Integer, Boolean, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base

#é um modelo que vai  representar uma tabela no BD
Base = declarative_base()
class Usuario(Base):
    __tablename__ = 'usuarios'


    login = Column(String, primary_key=True)
    senha = Column(String)
    tipo = Column(String)

    def __repr__(self):
        return f"<Usuario(login='{self.login}', senha='{self.senha}', tipo='{self.tipo}')>"



