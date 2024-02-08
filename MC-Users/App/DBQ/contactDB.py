from sqlalchemy import create_engine, MetaData, Table, select, and_, insert, update, delete
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
import os
import time


# Replace 'mysql://user:password@localhost/dbname' with your MySQL connection string
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
        'users': create_table('Utilizadores'),
    }

def create_session():
    global engine
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def decode(clause, table):
    if clause[0] == 1:
        return table.c.numero == clause[1]
    elif clause[0] == 2:
        return table.c.email == clause[1]
    elif clause[0] == 3:
        return table.c.password == clause[1]
    elif clause[0] == 4:
        return table.c.classifications == clause[1]
    elif clause[0] == 5:  # Added clause for user_type
        return table.c.user_type == clause[1]
    else:
        # Add additional conditions as needed
        return None


def select_fun(table_name,clauses):
    table = tables[table_name]
    where_cond = and_(*[ decode(clause,table)  for clause in clauses])
    session = create_session()
    select_statement = select(table).where(where_cond)
    result = session.execute(select_statement)
    session.close()
    return result.fetchall()

def insert_fun(table_name, tables, new_elements):
    table = tables[table_name]
    session = create_session(engine)
    select_statement = insert(table).values(new_elements)
    session.execute(select_statement)
    session.commit()
    session.close()
    return 0

def update_fun(table_name, tables, clauses, new_elements):
    table = tables[table_name]
    where_cond = and_(*[decode(clause, table) for clause in clauses])
    session = create_session(engine)
    select_statement = update(table).where(where_cond).values(new_elements)
    session.execute(select_statement)
    session.commit()
    session.close()
    return 0

def create_clauses():
    return []

def add_clause_user_id(user_id, current):
    current.append((1, user_id))
    return current

def add_clause_email(email, current):
    current.append((2, email))
    return current

def add_clause_pass(password,current):
    current.append((3),password)
    return current

def add_clause_classif(classifications,current):
    current.append((4),classifications)
    return current

def add_clause_user_type(user_type, current):
    current.append((5, user_type))
    return current


def validate_credentials(username, password):
    try:
        clauses = [(1, username), (3, password)]
        res = select_fun('users',clauses)
        return len(res) > 0

    except Exception as e:
        print(f"Error validating credentials: {e}")
        return False



def get_user_profile(user_id, user_type):
    try:
        users_table = tables['users']
        clauses = [(1, user_id), (5, user_type)]
        session = create_session()
        query = select([users_table]).where(and_(*[decode(clause, users_table) for clause in clauses]))
        result = session.execute(query)
        user_data = result.fetchone()

        if user_data:
            return {"numero": user_data[0], "nome": user_data[1], "email": user_data[2]}
        else:
            return None

    except Exception as e:
        print(f"Error getting user profile: {e}")
        return None

def update_email(user_id, new_email):
    try:
        users_table = tables['users']
        session = create_session()
        query = update(users_table).where(users_table.c.numero == user_id).values(email=new_email)
        session.execute(query)
        session.commit()
        return True

    except Exception as e:
        print(f"Error updating email: {e}")
        return False


def update_password(user_id, new_password):
    try:
        users_table = tables['users']
        session = create_session()
        query = update(users_table).where(users_table.c.numero == user_id).values(password=new_password)
        session.execute(query)
        session.commit()
        return True

    except Exception as e:
        print(f"Error updating password: {e}")
        return False

def register_user(name, user_id, email, password):
    try:
        users_table = tables['users']
        session = create_session()
        new_user = {'numero': user_id, 'nome': name, 'email': email, 'password': password}
        query = insert(users_table).values(new_user)
        session.execute(query)
        session.commit()
        return True

    except Exception as e:
        print(f"Error registering user: {e}")
        return False


def delete_user(user_id):
    try:
        users_table = tables['users']
        session = create_session()
        query = delete(users_table).where(users_table.c.numero == user_id)
        session.execute(query)
        session.commit()
        return True

    except Exception as e:
        print(f"Error deleting user: {e}")
        return False
    
'''
def teste(client: FlaskClient):
    # Assuming you have the app context pushed (which is usually done in a request)
    with app.app_context():
        # Register a student
        client.post('/receive_alunos_list', json={"alunos": [{"nome": "Student1", "num": "pg123", "email": "student1@example.com"}]})
        
        # Validate the student registration
        assert validate_credentials("pg123", "student1@example.com", "")

        # Get the profile of the student
        profile = get_user_profile("pg123")
        assert profile is not None
        assert profile["numero"] == "pg123"
        assert profile["nome"] == "Student1"
        assert profile["email"] == "student1@example.com"

        # Update the student's email
        update_email("pg123", "new_email@example.com")

        # Validate the updated email
        profile = get_user_profile("pg123")
        assert profile is not None
        assert profile["email"] == "new_email@example.com"

        # Clean up: Delete the student
        delete_user("pg123")

        # Validate that the student is deleted
        assert not validate_credentials("pg123", "new_email@example.com", "")


# Usage
with app.test_client() as client:
    teste(client)

'''

engine, metadata = create_engine_db()

# Reflect the existing database tables
tables = load_tables()
