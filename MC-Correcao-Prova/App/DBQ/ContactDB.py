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
        'provas' : create_table('ClassificacaoProvas'),
        'questoes' : create_table('ClassificacaoQuestoes')
    }

def create_session():
    global engine
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def decode(clause,table):
    if clause[0] == 1:
        return table.c.idProva == clause[1]
    elif clause[0] == 2:
        return table.c.idAluno == clause[1]
    elif clause[0] == 3:
        return table.c.idQuestao == clause[1]
    elif clause[0] == 4:
        return table.c.publica == clause[1]
    else:
        return table.c.classificacao < clause[1]

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

def add_clause_idProva(idProva,current):
    current.append((1,idProva))
    return current

def add_clause_idAluno(idAluno,current):
    current.append((2,idAluno))
    return current

def add_clause_idQuestao(idQuestao,current):
    current.append((3,idQuestao))
    return current

def add_clause_publica(value,current):
    current.append((4,value))
    return current

def add_clause_lower_classificacao(value,current):
    current.append((5,value))
    return current

def update_visibilidade(value):
    return {'publica': value}

def update_classificacao(value):
    return {'classificacao': value}

def create_new_value_provas(idProva,idAluno,classificacao,publica):
    return {'idProva': idProva, 'idAluno': idAluno, 'classificacao': classificacao, 'publica': publica}

def create_new_value_questoes(idProva,idAluno,idQuestao,classificacao):
    return {'idProva': idProva, 'idAluno': idAluno, 'idQuestao': idQuestao, 'classificacao': classificacao}

def teste():
    clauses = add_clause_idAluno('PG1',create_clauses())
    clauses = add_clause_idProva('P1',clauses)
    for row in select_fun('provas',clauses):
        print(row)
    # insert_fun('provas', create_new_value_provas('P3','PG1',20,False))

    clauses = add_clause_publica(True,create_clauses())
    update_fun('provas',clauses,{'publica': False})
    clauses = add_clause_idAluno('PG1',create_clauses())
    clauses = add_clause_idProva('P1',create_clauses())
    clauses = add_clause_idQuestao('Q1',create_clauses())
    update_fun('questoes',clauses,{'classificacao': 10})

    clauses = add_clause_idAluno('PG1',create_clauses())
    for row in select_fun('provas',clauses):
        print(row)



engine, metadata = create_engine_db()

# Reflect the existing database tables
tables = load_tables()
