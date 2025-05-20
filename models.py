from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Country(Base):
    __tablename__ = 'countries'

    id = Column(Integer, primary_key=True)
    nome_comum = Column(String)
    nome_oficial = Column(String)
    capital = Column(String)
    continente = Column(String)
    regiao = Column(String)
    subregiao = Column(String)
    populacao = Column(Integer)
    area = Column(Float)
    moeda = Column(String)
    idioma = Column(String)
    fuso_horario = Column(String)
    bandeira_url = Column(String)


class Livros(Base):
    __tablename__ = 'livros'

    id = Column(Integer, primary_key=True)
    titulo = Column(String)
    preco = Column(Float)
    avaliacao = Column(String)
    disponibilidade = Column(String)

engine = create_engine('sqlite:///paises.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
