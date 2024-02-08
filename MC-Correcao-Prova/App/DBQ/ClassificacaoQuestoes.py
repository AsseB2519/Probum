from DBQ import ContactDB

def correcaoAutomatica(alunos_certos):
    for elem in alunos_certos:
        prova = elem[0]
        questao = elem[1]
        classificacao_certa = elem[2]
        classificacao_errada = elem[3]
        alunos_certos = elem[4]
        alunos_errados = elem[5]
        print(alunos_certos)
        print(alunos_errados)
        for aluno in alunos_certos:
            updateNotaAluno(prova,aluno,questao,classificacao_certa)
        for aluno in alunos_errados:
            updateNotaAluno(prova,aluno,questao,-classificacao_errada)
    return 0

def novasQuestoes(provaID,alunoID,questoesIDs):
    new_entries = list(map(lambda questaoID : ContactDB.create_new_value_questoes(provaID,alunoID,questaoID,0),questoesIDs))
    return ContactDB.insert_fun('questoes',new_entries)

def updateNotaAluno(provaID, alunoID, questaoID,classificacao):
    clauses = ContactDB.create_clauses()
    clauses = ContactDB.add_clause_idProva(provaID,clauses)
    clauses = ContactDB.add_clause_idAluno(alunoID,clauses)
    clauses = ContactDB.add_clause_idQuestao(questaoID,clauses)
    ContactDB.update_fun('questoes',clauses,ContactDB.update_classificacao(classificacao))
    return 0

def getQuestoesNotasAluno(provaID,alunoID):
    clauses = ContactDB.create_clauses()
    clauses = ContactDB.add_clause_idProva(provaID,clauses)
    clauses = ContactDB.add_clause_idAluno(alunoID,clauses)
    result  = ContactDB.select_fun('questoes',clauses)
    if len(result) == 0: 
        result = None
    return result