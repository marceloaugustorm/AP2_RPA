from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

BaseLivraria = declarative_base()

class Livro(BaseLivraria):
    __tablename__ = 'livros'
    id = Column(Integer, primary_key=True)
    titulo = Column(String)
    preco = Column(Float)
    avaliacao = Column(String)
    disponibilidade = Column(String)

engine_livraria = create_engine('sqlite:///livraria.db')
BaseLivraria.metadata.create_all(engine_livraria)
SessionLivraria = sessionmaker(bind=engine_livraria)
