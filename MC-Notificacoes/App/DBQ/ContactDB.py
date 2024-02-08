from sqlalchemy import create_engine, MetaData, Table, select, and_, insert, update
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
import os
import time

def create_engine_db():
    db_host = os.environ.get('DB_HOST')
    db_port = os.environ.get('DB_PORT')
    db_user = os.environ.get('DB_USER')
    db_pass = os.environ.get('DB_PASS')
    db_db = os.environ.get('DB_DB')
    con = f'mysql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_db}'
    retry = True
    metadata = MetaData()
    while retry:
        try:
            engine = create_engine(con)
            metadata.reflect(bind=engine)
            retry = False
        except OperationalError as e:
            print('A tentar ligação à base de dados novamente ') 
            time.sleep(3)
    return engine,metadata

def create_table(table_name):
    global metadata, engine 
    return Table(table_name, metadata, autoload_with=engine)

def load_tables():
    return {
        'notificacoes' : create_table('Notificacoes')
    }

def create_session():
    global engine
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def decode(clause,table):
    if clause[0] == 1:
        return table.c.idUser == str(clause[1])
    elif clause[0] == 2:
        return table.c.idNotificacao == clause[1]
    elif clause[0] == 3:
        return table.c.titulo == clause[1]
    else:
        return table.c.read == clause[1]

def select_fun(table_name,clauses):
    table = tables[table_name]
    where_cond = and_(*[ decode(clause,table)  for clause in clauses])
    session = create_session()
    select_statement = select(table).where(where_cond)
    result = session.execute(select_statement)
    session.close()
    return result.fetchall()

def insert_fun(table_name, new_elements):
    table = tables[table_name]
    session = create_session()
    select_statement = insert(table).values(new_elements)
    session.execute(select_statement)
    session.commit()
    session.close()
    return 0

def update_fun(table_name, clauses, new_elements):
    table = tables[table_name]
    where_cond = and_(*[ decode(clause,table)  for clause in clauses])
    session = create_session()
    select_statement = update(table).where(where_cond).values(new_elements)
    session.execute(select_statement)
    session.commit()
    session.close()
    return 0

def create_clauses():
    return []

def add_clause_idUser(idUser,current):
    current.append((1,idUser))
    return current

def add_clause_idNotificacao(idNotificacao,current):
    current.append((2,idNotificacao))
    return current

def add_clause_Titulo(titulo,current):
    current.append((3,titulo))
    return current

def add_clause_read(read,current):
    current.append((4,read))
    return current

def update_read(value):
    return {'read': value}

def update_titulo(value):
    return {'titulo': value}

def update_descricao(value):
    return {'descricao': value}

def create_new_value_notificacoes(idUser, idNotificacao, titulo, descricao, read):
    return {'idUser': idUser,
            'idNotificacao': idNotificacao,
            'titulo': titulo,
            'descricao': descricao,
            'read': read}

def teste():
    clauses = add_clause_idUser('PG1',create_clauses())
    clauses = add_clause_idNotificacao('N1',clauses)
    clauses = add_clause_read(False,clauses)
    update_fun('notificacoes',clauses,{'titulo': "Classificacao da Prova",
                                       'descricao': "A sua prova teve uma classificacao de 15"})

    for row in select_fun('notificacoes',clauses):
        print(row)


engine, metadata = create_engine_db()

# Reflect the existing database tables
tables = load_tables()

#teste()