from sqlalchemy import create_engine, MetaData, Table, select, and_, insert, update
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
import os
import time

# Function to create a MySQL database engine
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

# Function to create a table object based on the provided table name
def create_table(table_name):
    global metadata, engine
    return Table(table_name, metadata, autoload_with=engine)

# Function to load tables into a dictionary
def load_tables():
    return {
        'respostas': create_table('respostas_alunos')
    }

# Function to create a session for database interaction
def create_session():
    global engine
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

# Function to decode a clause and create a SQLAlchemy condition
def decode(clause, table):
    if clause[0] == 1:
        return table.c.idProva == clause[1]
    elif clause[0] == 2:
        return table.c.idAluno == str(clause[1]) # ID do aluno é uma String (pgXXXXX)
    elif clause[0] == 3:
        return table.c.idQuestao == clause[1]
    else: 
        return table.c.resposta == str(clause[1])

# Function to perform a SELECT query on the database
def select_fun(table_name, clauses):
    table = tables[table_name]
    where_cond = and_(*[decode(clause, table) for clause in clauses])
    session = create_session()
    select_statement = select(table).where(where_cond)
    result = session.execute(select_statement)
    session.close()
    return result.fetchall()

# Function to perform an INSERT query on the database
def insert_fun(table_name, new_elements):
    table = tables[table_name]
    session = create_session()
    select_statement = insert(table).values(new_elements)
    session.execute(select_statement)
    session.commit()
    session.close()
    return 0

# Function to perform an UPDATE query on the database
def update_fun(table_name, clauses, new_elements):
    table = tables[table_name]
    where_cond = and_(*[decode(clause, table) for clause in clauses])
    session = create_session()
    select_statement = update(table).where(where_cond).values(new_elements)
    session.execute(select_statement)
    session.commit()
    session.close()
    return 0

# Function to create an empty list of clauses
def create_clauses():
    return []

# Functions to add specific clauses to the list
def add_clause_idProva(idProva, current):
    current.append((1, idProva))
    return current

def add_clause_idAluno(idAluno, current):
    current.append((2, str(idAluno)))
    return current

def add_clause_idQuestao(idQuestao, current):
    current.append((3, idQuestao))
    return current

def add_clause_resposta(resposta, current):
    current.append((4, str(resposta)))
    return current

# Function to create a dictionary for an update operation
def update_resposta(value):
    return {'resposta': value}

# Function to create a dictionary for a new row in the 'respostas' table
def create_new_value_respostas(idProva, idQuestao, idAluno, resposta):
    return { 'idProva': idProva, 
             'idQuestao': idQuestao, 
             'idAluno': idAluno, 
             'resposta': resposta }

# Test function to demonstrate the usage of the defined functions
def teste():
    clauses = add_clause_idAluno('PG1', create_clauses())
    clauses = add_clause_idProva(1, clauses)
    for row in select_fun('respostas', clauses):
        print(row)

    update_fun('respostas', clauses, {'resposta': 'A'})

    clauses = add_clause_idAluno('PG1', create_clauses())
    clauses = add_clause_idProva(1, create_clauses())
    clauses = add_clause_idQuestao(1, create_clauses())
    update_fun('respostas', clauses, {'resposta': 'B'})

    clauses = add_clause_idAluno('PG1', create_clauses())
    for row in select_fun('respostas', clauses):
        print(row)

# Create a database engine and reflect existing database tables
engine, metadata = create_engine_db()

# Reflect the existing database tables
tables = load_tables()