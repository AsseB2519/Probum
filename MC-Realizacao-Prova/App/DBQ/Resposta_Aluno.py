from DBQ import ContactDB 

# API Gateway
# 1
# Obter uma Prova pelo seu ID 
def getProva(provaID):
    # Create clauses for filtering
    clauses = ContactDB.create_clauses()
    clauses = ContactDB.add_clause_idProva(provaID, clauses)

    # Perform SELECT query
    result = ContactDB.select_fun('respostas', clauses)

    # Check if the result is empty
    if len(result) == 0:
        result = None
    else: result = {'prova' : result[0][0], 'questao': result[0][1]}

    return result

# Obter uma questao pelo seu ID 
def getQuestao(provaID, questaoID):
    # Create clauses for filtering
    clauses = ContactDB.create_clauses()
    clauses = ContactDB.add_clause_idProva(provaID, clauses)
    clauses = ContactDB.add_clause_idQuestao(questaoID, clauses)

    # Perform SELECT query
    result = ContactDB.select_fun('respostas', clauses)

    # Check if the result is empty
    if len(result) == 0:
        result = None
    else: result = {'prova' : result[0][0], 'questao': result[0][1]}

    return result

# 2 ??
# Submeter as respostas a uma dada prova que foi realizada
def novasRespostas(provaID,questaoID,alunoID,respostasIDs):
    new_entries = list(map(lambda respostaID : ContactDB.create_new_value_respostas(provaID,alunoID,questaoID,respostaID),respostasIDs))
    return ContactDB.insert_fun('respostas',new_entries)

# 3 
# Obter uma questão de uma prova pelo seu id para realização
def getResposta(provaID, questaoID, alunoID):
    # Create clauses for filtering
    clauses = ContactDB.create_clauses()
    clauses = ContactDB.add_clause_idProva(provaID, clauses)
    clauses = ContactDB.add_clause_idQuestao(questaoID, clauses)
    clauses = ContactDB.add_clause_idAluno(alunoID, clauses)

    # Perform SELECT query
    result = ContactDB.select_fun('respostas', clauses)

    # Check if the result is empty
    if len(result) == 0:
        result = None

    return result

# 4
# Submeter a resposta a uma dada questão de uma prova a ser realizada
def novaResposta(provaID,questaoID,alunoID,resposta):
    elem = ContactDB.create_new_value_respostas(provaID,questaoID,alunoID,resposta)
    return ContactDB.insert_fun('respostas',elem)


# 5
# Atualizar a resposta dada a uma questão de uma prova a ser realizada
def updateResposta(provaID, alunoID, questaoID, resposta):
    clauses = ContactDB.create_clauses()
    clauses = ContactDB.add_clause_idProva(provaID,clauses)
    clauses = ContactDB.add_clause_idAluno(alunoID,clauses)
    clauses = ContactDB.add_clause_idQuestao(questaoID,clauses)
    ContactDB.update_fun('respostas',clauses,ContactDB.update_resposta(resposta))
    return 0


# MS RealizarProva

# 1
# Get respostas de alunos de uma prova
def getRespostas(provaID):
    clauses = ContactDB.create_clauses()
    clauses = ContactDB.add_clause_idProva(provaID,clauses)
    result = ContactDB.select_fun('respostas',clauses)
    if len(result) == 0: 
        result = None
    else:
        result = list(map(lambda e : (e[0],e[1],e[2],bool(e[3])),result))
    return result

def getRespostasAQuestoes(provaID,questaoID):
    clauses = ContactDB.create_clauses()
    clauses = ContactDB.add_clause_idProva(provaID,clauses)
    clauses = ContactDB.add_clause_idProva(questaoID,clauses)
    result = ContactDB.select_fun('respostas',clauses)
    if len(result) == 0: 
        result = None
    else:
        result = list(map(lambda e : (e[0],e[1],e[2],bool(e[3])),result))
    return result

# 2
# Seleciona a resposta de um aluno para uma questão de uma prova
# def getResposta(provaID, questaoID, alunoID):

# 3
# Guarda a resposta de um aluno para uma questão de uma prova
# def novaResposta(provaID,questaoID,alunoID,resposta):




