from sqlalchemy import create_engine, MetaData, Table, select, and_, insert, update
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
import os
import time

# Create MySQL database engine
#def create_engine_db():
#    user = ''
#    password = ''
#    host = '127.0.0.1'
#    db = 'RAS_Prova'
#    return create_engine(f'mysql://{user}:{password}@{host}/{db}')

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
            print('Agora vais dormir um soninho')  
            time.sleep(60)
    return engine,metadata

# Function to create a table object based on the provided table name
def create_table(table_name):
    global metadata, engine 
    return Table(table_name, metadata, autoload_with=engine)

# Function to load tables into a dictionary
def load_tables():
    return {
        'provas' : create_table('prova'),
        'alunoPro' : create_table('aluno_prova'),
        'profPro' : create_table('prof_prova'),
        'questaoDes' : create_table('questao_desenvolvimento'),
        'questaoEM' : create_table('questao_escolha_multipla'),
        'questaoVF' : create_table('questao_vf'),
        'alinea' : create_table('alinea'),
        'questaoEsp' : create_table('questao_espacos'),
        'espacos' : create_table('espacos')
        #'criterioEsp' : create_table('critero_questao_espacos')
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
        return table.c.id == clause[1]
    elif clause[0] == 2:
        return table.c.id_aluno == clause[1]
    elif clause[0] == 3:
        return table.c.id_prof == clause[1]
    elif clause[0] == 4:
        return table.c.versao == clause[1]
    elif clause[0] == 5:
        return table.c.prova_id == clause[1]
    elif clause[0] == 6:
        return table.c.questao_id == clause[1]
    elif clause[0] == 8:
        return table.c.id_prova == clause[1]
    elif clause[0] == 9:
        return table.c.data == clause[1]
    else:
        return table.c.prova_versao == clause[1] 
    
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
def add_clause_id(id, current):
    current.append((1, id))
    return current

def add_clause_id_aluno(id_aluno, current):
    current.append((2, id_aluno))
    return current 

def add_clause_id_prof(id_prof, current):
    current.append((3, id_prof))
    return current 

def add_clause_versao(versao, current):
    current.append((4, versao))
    return current

def add_clause_prova_id(prova_id, current):
    current.append((5, prova_id))
    return current

def add_clause_questao_id(questao_id, current):
    current.append((6, questao_id))
    return current

def add_clause_prova_versao(prova_versao, current):
    current.append((7, prova_versao))
    return current

def add_clause_id_prova(id_prova, current):
    current.append((8, id_prova))
    return current

def add_clause_data(data, current):
    current.append((9, data))
    return current

# Function to create a dictionary for an update operation
def update_nome(value):
    return {'nome': value}

def update_criador(value):
    return {'criador': value}

def update_data(value):
    return {'data': value}

def update_duracao(value):
    return {'duracao': value}

def update_tempo_admissao(value):
    return {'tempo_admissao': value}

def update_aleatorio(value):
    return {'aleatorio': value}

def update_retrocesso(value):
    return {'retrocesso': value}

def update_descricao(value):
    return {'descricao': value}

def update_imagem(value):
    return {'imagem': value}

def update_prova_pos(value):
    return {'prova_pos': value}

def update_n(value):
    return {'n': value}

def update_texto(value):
    return {'texto': value}

def update_n_espaco(value):
    return {'n_espaco': value}

def update_criterio(value):
    return {'criterio': value}

def update_min_palavras(value):
    return {'min_palavras': value}

def update_max_palavras(value):
    return {'max_palavras': value}

def update_correto(value):
    return {'correto': value}

def update_questao(value):
    return {'questao': value}

def update_pontos_acerto(value):
    return {'pontos_acerto': value}

def update_pontos_erro(value):
    return {'pontos_erro': value}

def update_questao_pos(value):
    return {'questao_pos': value}

def update_criterio_avaliacao(value):
    return {'criterio_avaliacao': value}

# Function to create a dictionary for a new row in a table
def create_new_value_prova(id,versao,nome,criador,data,duracao,tempo_admissao,aleatorio,retrocesso):
    return {'id': id, 'versao': versao,'nome': nome,'criador': criador,'data': data,'duracao':duracao ,'tempo_admissao': tempo_admissao,
            'aleatorio': aleatorio,'retrocesso': retrocesso}

def create_new_value_aluno_prova(id_aluno, id_prova, prova_versao):
    return {'id_aluno': id_aluno, 'id_prova': id_prova, 'prova_versao': prova_versao}

def create_new_value_prof_prova(id_prof, id_prova):
    return {'id_prof': id_prof, 'id_prova': id_prova}

def create_new_value_questao_esp(id, descricao, imagem, prova_id, prova_versao, prova_pos):
    return {'id': id, 'descricao': descricao, 'imagem': imagem, 'prova_id': prova_id, 'prova_versao': prova_versao, 'prova_pos': prova_pos}

def create_new_value_texto_quest_esp(id, n, texto, questao_id):
    return {'id': id, 'n': n, 'texto': texto, 'questao_id': questao_id}

def create_new_value_questao_desen(id, descricao, imagem, min_palavras, max_palavras, criterio_avaliacao, prova_id, prova_versao, prova_pos):
    return {'id': id, 'descricao': descricao, 'imagem': imagem, 'min_palavras': min_palavras, 'max_palavras': max_palavras,
             'criterio_avaliacao': criterio_avaliacao, 'prova_id': prova_id, 'prova_versao': prova_versao, 'prova_pos': prova_pos}

def create_new_value_questao_EM(id, descricao, imagem, prova_id, prova_versao, prova_pos):
    return {'id': id, 'descricao': descricao, 'imagem': imagem, 'prova_id': prova_id, 'prova_versao': prova_versao, 'prova_pos': prova_pos}

def create_new_value_questao_VF(id,descricao, imagem, prova_id, prova_versao, prova_pos):
    return {'id': id, 'descricao': descricao,'imagem': imagem, 'prova_id': prova_id, 'prova_versao': prova_versao, 'prova_pos': prova_pos}

def create_new_value_espaco(id, n_espaco, correto, texto, questao_id):
    return {'id': id, 'n_espaco': n_espaco, 'correto': correto, 'texto': texto ,'questao_id': questao_id}

def create_new_value_alinea(id, questao, correto, pontos_acerto, pontos_erro, questao_id, questao_pos):
    return {'id': id, 'questao': questao, 'correto': correto, 'pontos_acerto': pontos_acerto, 'pontos_erro': pontos_erro, 'questao_id': questao_id, 'questao_pos': questao_pos}

# Test function to demonstrate the usage of the defined functions
#def teste():

# Create a database engine and reflect existing database tables
#engine = create_engine_db()
#metadata = MetaData()
#metadata.reflect(bind=engine)
#tables = load_tables()

#teste()

engine, metadata = create_engine_db()

# Reflect the existing database tables
tables = load_tables()