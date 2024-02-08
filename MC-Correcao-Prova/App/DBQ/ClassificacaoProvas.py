
from DBQ import ContactDB 

# Se resultado = None, devolver código 400
def getProvaNotaAluno(provaID,alunoID):
    clauses = ContactDB.create_clauses()
    clauses = ContactDB.add_clause_idProva(provaID,clauses)
    clauses = ContactDB.add_clause_idAluno(alunoID,clauses)
    result = ContactDB.select_fun('provas',clauses)
    if len(result) == 0: 
        result = None
    else:
        result = result[0][2]
    return result

def getProvasAluno(alunoID):
    clauses = ContactDB.create_clauses()
    clauses = ContactDB.add_clause_idAluno(alunoID,clauses)
    result = ContactDB.select_fun('provas',clauses)
    if len(result) == 0: 
        result = None
    else:
        result = list(map(lambda e : (e[0],e[1],e[2],e[3]==1),result))
    return result

def publicaNotas(provaID):
    clauses = ContactDB.create_clauses()
    clauses = ContactDB.add_clause_idProva(provaID,clauses)
    result = ContactDB.update_fun('provas',clauses,ContactDB.update_visibilidade(True))
    clauses = ContactDB.add_clause_lower_classificacao(0,clauses)
    ContactDB.update_fun('provas',clauses,ContactDB.update_classificacao(0))
    return result

def novaProva(provaID,alunoID):
    elem = ContactDB.create_new_value_provas(provaID,alunoID,0,False)
    return ContactDB.insert_fun('provas',elem)

def notasProvaPublicadas(provaID):
    clauses = ContactDB.create_clauses()
    clauses = ContactDB.add_clause_idProva(provaID,clauses)
    clauses = ContactDB.add_clause_publica(1,clauses)
    result = ContactDB.select_fun('provas',clauses)
    return len(result) > 0
