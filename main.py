from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import sessionmaker
Base = declarative_base()
database_url = 'mysql+pymysql://root:Senac2021@localhost:3306/locadora'

class Filme(Base):
    __tablename__ = 'filme'
    id = Column(Integer, autoincrement=True, primary_key=True)
    titulo = Column(String(100), nullable=False)
    genero = Column(String(100), nullable=False)
    ano = Column(Integer, nullable=False)

    def __repr__(self):
        return f'Filme [Título: {self.titulo}, Gênero: {self.genero}, Ano: {self.ano}]'



def create_database():
    engine = create_engine(database_url, echo=True)
    try:
        engine.connect()
    except Exception as e:
        if '1049' in str(e):
            engine = create_engine(database_url.rsplit('/', 1)[0], echo=True)
            conn = engine.connect()
            conn.execute('CREATE DATABASE locadora')
            conn.close()
            print('Banco locadora criado com sucesso')
        else:
            raise e

create_database()

#Configurações
engine = create_engine(database_url, echo=True)
conn = engine.connect()
Session = sessionmaker(bind=engine)
session = Session()

def create_table():
    Base.metadata.create_all(engine)
    print('Tabela filme criada com sucesso!')

create_table()
#inserção no banco
data_insert = Filme(titulo = 'Batman', ano = '2022', genero = 'ação')
session.add(data_insert)
session.commit()
data_insert = Filme(titulo = 'Emanuelle', ano = '1985', genero = 'terror')
session.add(data_insert)
session.commit()
session.close()
data_insert = Filme(titulo = 'robinson', ano = '1987', genero = 'comédia')
session.add(data_insert)
session.commit()
session.close()

#remoção do banco
session.query(Filme).filter(Filme.id == '7').delete()
session.commit()

session.close()

#atualização de dados
session.query(Filme).filter(Filme.titulo == 'Batman').update({'titulo' : 'Bátima'})
session.commit()

session.close()

#consulta de dados
data = session.query(Filme).all()

print(f'Filmes{data}')
session.close()