from DBQ import ContactDB
from datetime import datetime

# GET

# Obter uma prova pelo o seu ID
def getProva(provaID,ver):
    clauses = ContactDB.create_clauses()
    clauses = ContactDB.add_clause_id(provaID, clauses)
    clauses = ContactDB.add_clause_versao(ver, clauses)

    result = ContactDB.select_fun('provas', clauses)

    if len(result) == 0:
        results = None
    else:
        #results = list(map(lambda e : (e[0],e[1],e[2],e[3],e[4],e[5],e[6],e[7],e[8]),result))
        results = list(result[:9])
    return results

# Obter as questoes de uma prova
def getQuestoes(provaID,ver):
    clauses = ContactDB.create_clauses()
    clauses = ContactDB.add_clause_prova_id(provaID,clauses)
    clauses = ContactDB.add_clause_prova_versao(ver, clauses)
    
    des = ContactDB.select_fun('questaoDes',clauses)
    em = ContactDB.select_fun('questaoEM',clauses)
    vf = ContactDB.select_fun('questaoVF',clauses)
    esp = ContactDB.select_fun('questaoEsp',clauses)

    if (len(des) == 0) and (len(em) == 0) and (len(vf) == 0) and (len(esp) == 0):
        result = None
    else:
        des = list(map(lambda e: (e[0], e[1], e[2], e[3], e[4], e[5], e[6], e[7], e[8]), des))
        em = list(map(lambda e: (e[0], e[1], e[2], e[3], e[4], e[5]), em))
        vf = list(map(lambda e: (e[0], e[1], e[2], e[3], e[4], e[5]), vf))
        esp = list(map(lambda e: (e[0], e[1], e[2], e[3], e[4], e[5]), esp))
        result = {'Desen' : des, 'EM' : em, 'VF' : vf, 'Esp' : esp}
    
    return result

# Obter as respostas automaticas de uma prova
def getRespostasAutomaticas(provaID,ver):
    clauses = ContactDB.create_clauses()
    clauses = ContactDB.add_clause_prova_id(provaID,clauses)
    clauses = ContactDB.add_clause_prova_versao(ver, clauses)
    
    em = ContactDB.select_fun('questaoEM',clauses)
    vf = ContactDB.select_fun('questaoVF',clauses)
    esp = ContactDB.select_fun('questaoEsp',clauses)

    if (len(em) == 0) and (len(vf) == 0) and (len(esp) == 0):
        return None
    
    alEM = {}
    alVF = {}
    espacos = {}

    for q in em:
        als = getAlineas(q[0])
        alEM[str(q[0])] = []
        for a in als:
            # id, questao, correto, pontos_acerto, pontos_erro, questao_id, questao_pos
            alEM[str(q[0])].append((a[0],a[2],a[3],a[4]))
    
    for q in vf:
        als = getAlineas(q[0])
        alVF[str(q[0])] = []
        for a in als:
            # id, questao, correto, pontos_acerto, pontos_erro, questao_id, questao_pos
            alVF[str(q[0])].append((a[0],a[2],a[3],a[4]))

    for q in esp:
        als = getEspacos(q[0])
        espacos[str(q[0])] = []
        for e in als:
            # id, n_espaco, correto, texto, questao_id
            espacos[str(q[0])].append((e[0],e[1],e[2],e[3]))

    result = {'EM' : alEM, 'VF' : alVF, 'Esp' : espacos}
    
    return result

# Obter uma questao de uma prova
def getQuestao(qID,provaID,tipo,ver):
    clauses = ContactDB.create_clauses()
    clauses = ContactDB.add_clause_prova_id(provaID,clauses)
    clauses = ContactDB.add_clause_id(qID,clauses)
    clauses = ContactDB.add_clause_prova_versao(ver, clauses)

    if tipo == 1:
        result = ContactDB.select_fun('questaoDes',clauses)
    elif tipo == 2:
        result = ContactDB.select_fun('questaoEM',clauses)
    elif tipo == 3:
        result = ContactDB.select_fun('questaoVF',clauses)
    elif tipo == 4:
        result = ContactDB.select_fun('questaoEsp',clauses)
    else:
        return None
    
    if len(result) == 0:
        return None
    else:
        result = list(map(lambda e: (e[0], e[1], e[2], e[3], e[4], e[5]), result))
        return result
    
# Obter as alineas de uma questao
def getAlineas(qID):
    clauses = ContactDB.create_clauses()
    clauses = ContactDB.add_clause_questao_id(qID,clauses)
    
    result = ContactDB.select_fun('alinea',clauses)

    if len(result) == 0:
        return None
    else:
        result = list(map(lambda e: (e[0], e[1], e[2], e[3], e[4], e[5], e[6]), result))
        return result

# Obter os espaços da questão de preencher espaços
def getEspacos(qID):
    clauses = ContactDB.create_clauses()
    clauses = ContactDB.add_clause_questao_id(qID,clauses)
    
    result = ContactDB.select_fun('espacos',clauses)

    if len(result) == 0:
        return None
    else:
        result = list(map(lambda e: (e[0], e[1], e[2], e[3], e[4]), result))
        return result

"""
# Obter os critérios dos espaços da questão de preencher espaços
def getCriteriosEspacos(qID):
    clauses = ContactDB.create_clauses()
    clauses = ContactDB.add_clause_questao_id(qID,clauses)
    
    result = ContactDB.select_fun('criterioEsp',clauses)

    if len(result) == 0:
        return None
    else:
        return result
"""
# Obter os professores que tem a acesso a uma prova pelo o seu ID
def getProvaProfs(id_prova): 
    clauses = ContactDB.create_clauses()
    clauses = ContactDB.add_clause_id_prova(id_prova, clauses)

    result = ContactDB.select_fun('profPro', clauses)

    if len(result) == 0:
        result = None
    else:
        result = list(map(lambda e: (e[0]), result))
    return result


# Obter os alunos inscritos numa prova pelo o seu ID
def getProvaAlunos(id_prova,versao_id):
    clauses = ContactDB.create_clauses()
    clauses = ContactDB.add_clause_id_prova(id_prova, clauses)
    clauses = ContactDB.add_clause_prova_versao(versao_id, clauses)

    result = ContactDB.select_fun('alunoPro', clauses)

    if len(result) == 0:
        result = None
    else:
        result = list(map(lambda e: (e[0]), result))
    return result    

# Obter um aluno_prova pelo o seu ID
def getAluno_prova(id_aluno,prova_id,prova_versao):
    clauses = ContactDB.create_clauses()
    clauses = ContactDB.add_clause_id_aluno(id_aluno, clauses)
    clauses = ContactDB.add_clause_prova_id(prova_id, clauses)
    clauses = ContactDB.add_clause_prova_versao(prova_versao, clauses)

    result = ContactDB.select_fun('alunoPro', clauses)

    if len(result) == 0:
        result = None

    return result

# Obter um prof_prova pelo o seu ID
def getProf_prova(id_prof,prova_id):
    clauses = ContactDB.create_clauses()
    clauses = ContactDB.add_clause_id_prof(id_prof, clauses)
    clauses = ContactDB.add_clause_prova_id(prova_id, clauses)

    result = ContactDB.select_fun('profPro', clauses)

    if len(result) == 0:
        result = None

    return result

# Obter provas futuras por iD de aluno
def getProvas_aluno(id_aluno):

    clauses = ContactDB.create_clauses()
    clauses = ContactDB.add_clause_id_aluno(id_aluno, clauses)

    ids = ContactDB.select_fun('alunoPro', clauses)
    result = []
    for i in ids:
        p = getProva(i[1],i[2])
        p2 = p[0]
        result.append(list(p2))

    if len(result) == 0:
        result = None

    return result

# Obter provas futuras por iD de prof
def getProvas_prof(id_prof):

    clauses = ContactDB.create_clauses()
    clauses = ContactDB.add_clause_id_prof(id_prof, clauses)

    ids = ContactDB.select_fun('profPro', clauses)
    result = []
    for i in ids:
        p = getProva(i[1],1)
        p2 = p[0]
        result.append(list(p2))
        
    if len(result) == 0:
        result = None

    return result        

# INSERT

# Criar uma nova prova
def createProva(id,versao,nome,criador,data,duracao,tempo_admissao,aleatorio,retrocesso):
    elem = ContactDB.create_new_value_prova(id,versao,nome,criador,data,duracao,tempo_admissao,aleatorio,retrocesso)
    return ContactDB.insert_fun('provas',elem)

# Criar um novo aluno_prova
def createAluno_prova(id_aluno, id_prova, id_versao):
    elem = ContactDB.create_new_value_aluno_prova(id_aluno, id_prova, id_versao)
    return ContactDB.insert_fun('alunoPro',elem)

# Criar um novo ptof_prova
def createProf_prova(id_prof, id_prova):
    elem = ContactDB.create_new_value_prof_prova(id_prof, id_prova)
    return ContactDB.insert_fun('profPro',elem)

# Criar uma nova questao de desenvolvimento de uma prova
def createQuestaoDesen(id, descricao, imagem, min_palavras, max_palavras, criterio_avaliacao, prova_id, prova_versao, prova_pos):
    elem = ContactDB.create_new_value_questao_desen(id, descricao, imagem, min_palavras, max_palavras, criterio_avaliacao, prova_id, prova_versao, prova_pos)
    return ContactDB.insert_fun('questaoDes',elem)

# Criar uma nova questao de escolha multipla de uma prova
def createQuestaoEM(id, descricao, imagem, prova_id, prova_versao, prova_pos):
    elem = ContactDB.create_new_value_questao_EM(id, descricao, imagem, prova_id, prova_versao, prova_pos)    
    return ContactDB.insert_fun('questaoEM',elem)

# Criar uma nova questao de verdadeiro e falso de uma prova
def createQuestaoVF(id, descricao,imagem, prova_id, prova_versao, prova_pos):
    elem = ContactDB.create_new_value_questao_VF(id, descricao,imagem, prova_id, prova_versao, prova_pos)
    return ContactDB.insert_fun('questaoVF',elem)

# Criar nova alinea para uma dada questao VF/EM de uma prova
def createAlinea(id, questao, correto, pontos_acerto, pontos_erro, questao_id, questao_pos):
    elem = ContactDB.create_new_value_alinea(id, questao, correto, pontos_acerto, pontos_erro, questao_id, questao_pos)
    return ContactDB.insert_fun('alinea',elem)

# Criar uma nova questao de espaços de uma prova
def createQuestaoEsp(id, descricao, imagem, prova_id, prova_versao, prova_pos):
    elem = ContactDB.create_new_value_questao_esp(id, descricao, imagem, prova_id, prova_versao, prova_pos)
    return ContactDB.insert_fun('questaoEsp',elem)

# Criar novos espaços de texto para questoes de espaços de uma prova
def createEspacos(id, n_espaco, correto, texto, questao_id):
    elem = ContactDB.create_new_value_espaco(id, n_espaco, correto, texto, questao_id)
    return ContactDB.insert_fun('espacos',elem)

"""
# Criar novos espaços de texto para questoes de espaços de uma prova
def createEspacosTexto(id, n, texto, questao_id):
    elem = ContactDB.create_new_value_texto_quest_esp(id, n, texto, questao_id)
    return ContactDB.insert_fun('espacos',elem)

# Criar novos criterios para os espaços de uma questao de espaços de uma prova
def createCriteriosEsp(id, n_espaco, criterio, questao_id):
    elem = ContactDB.create_new_value_criterio_quest_esp(id, n_espaco, criterio, questao_id)
    return ContactDB.insert_fun('criterioEsp',elem)
"""

# UPDATE

# Atualizar os detalhes de uma prova
def updateProva(provaID,ver,nome,criador,data,duracao,tempo_admissao,aleatorio,retrocesso):
    clauses = ContactDB.create_clauses()
    clauses = ContactDB.add_clause_id(provaID, clauses)
    clauses = ContactDB.add_clause_versao(ver, clauses)
    
    updateDict = ContactDB.update_nome(nome) | ContactDB.update_criador(criador) | ContactDB.update_data(data) \
                 | ContactDB.update_duracao(duracao) | ContactDB.update_tempo_admissao(tempo_admissao) | ContactDB.update_aleatorio(aleatorio) \
                 | ContactDB.update_retrocesso(retrocesso)

    ContactDB.update_fun('provas',clauses,updateDict)

    return 0

# Atualizar os detalhes de uma questao de desenvolvimento
def updateQuestaoDesen(id, descricao, imagem, min_palavras, max_palavras, criterio_avaliacao, prova_id, prova_versao, prova_pos):
    clauses = ContactDB.create_clauses()
    clauses = ContactDB.add_clause_id(id,clauses)
    clauses = ContactDB.add_clause_prova_id(prova_id,clauses)
    clauses = ContactDB.add_clause_prova_versao(prova_versao,clauses)
    
    updateDict = ContactDB.update_descricao(descricao) | ContactDB.update_imagem(imagem) \
                 | ContactDB.update_min_palavras(min_palavras) | ContactDB.update_max_palavras(max_palavras) | ContactDB.update_criterio_avaliacao(criterio_avaliacao) \
                 | ContactDB.update_prova_pos(prova_pos)

    ContactDB.update_fun('questaoDes',clauses,updateDict)

    return 0

# Atualizar os detalhes de uma questao de escolha multipla
def updateQuestaoEM(id, descricao, imagem, prova_id, prova_versao, prova_pos):
    clauses = ContactDB.create_clauses()
    clauses = ContactDB.add_clause_id(id,clauses)
    clauses = ContactDB.add_clause_prova_id(prova_id,clauses)
    clauses = ContactDB.add_clause_prova_versao(prova_versao,clauses)
    
    updateDict = ContactDB.update_descricao(descricao) | ContactDB.update_imagem(imagem) | ContactDB.update_prova_pos(prova_pos)

    ContactDB.update_fun('questaoEM',clauses,updateDict)

    return 0

# Atualizar os detalhes de uma questao de verdadeiros e falsos
def updateQuestaoVF(id, descricao,imagem, prova_id, prova_versao, prova_pos):
    clauses = ContactDB.create_clauses()
    clauses = ContactDB.add_clause_id(id,clauses)
    clauses = ContactDB.add_clause_prova_id(prova_id,clauses)
    clauses = ContactDB.add_clause_prova_versao(prova_versao,clauses)
    
    updateDict = ContactDB.update_descricao(descricao) | ContactDB.update_imagem(imagem) | ContactDB.update_prova_pos(prova_pos)

    ContactDB.update_fun('questaoVF',clauses,updateDict)
    
    return 0

# Atualizar os detalhes de uma alinea de uma questao
def updateAlinea(id, questao, correto, pontos_acerto, pontos_erro, questao_id, questao_pos):
    clauses = ContactDB.create_clauses()
    clauses = ContactDB.add_clause_id(id,clauses)
    clauses = ContactDB.add_clause_questao_id(questao_id,clauses)
    
    updateDict = ContactDB.update_questao(questao) | ContactDB.update_correto(correto) | ContactDB.update_pontos_acerto(pontos_acerto) \
                 | ContactDB.update_pontos_erro(pontos_erro) | ContactDB.update_questao_pos(questao_pos)

    ContactDB.update_fun('alinea',clauses,updateDict)
    
    return 0

# Atualizar os detalhes de uma questao de espaços
def updateQuestaoEsp(id, descricao, imagem, prova_id, prova_versao, prova_pos):
    clauses = ContactDB.create_clauses()
    clauses = ContactDB.add_clause_id(id,clauses)
    clauses = ContactDB.add_clause_prova_id(prova_id,clauses)
    clauses = ContactDB.add_clause_prova_versao(prova_versao,clauses)
    
    updateDict = ContactDB.update_descricao(descricao) | ContactDB.update_imagem(imagem) | ContactDB.update_prova_pos(prova_pos)

    ContactDB.update_fun('questaoEsp',clauses,updateDict)

    return 0

# Atualizar os detalhes dos espaços de texto de uma questao de espaços
def updateEspacos(id, n_espaco, correto, texto, questao_id):
    clauses = ContactDB.create_clauses()
    clauses = ContactDB.add_clause_id(id,clauses)
    clauses = ContactDB.add_clause_questao_id(questao_id,clauses)

    updateDict = ContactDB.update_n_espaco(n_espaco) | ContactDB.update_texto(texto) | ContactDB.update_correto(correto)

    ContactDB.update_fun('espacos',clauses,updateDict)

    return 0

"""
# Atualizar os detalhes dos espaços de texto de uma questao de espaços
def updateEspacosTexto(id, n, texto, questao_id):
    clauses = ContactDB.create_clauses()
    clauses = ContactDB.add_clause_id(id,clauses)
    clauses = ContactDB.add_clause_questao_id(questao_id,clauses)

    updateDict = ContactDB.update_n(n) | ContactDB.update_texto(texto)

    ContactDB.update_fun('espacos',clauses,updateDict)

    return 0

# Atualizar os detalhes dos criterios dos espaços de uma questao de espaços
def updateCriteriosEsp(id, n_espaco, criterio, questao_id):
    clauses = ContactDB.create_clauses()
    clauses = ContactDB.add_clause_id(id,clauses)
    clauses = ContactDB.add_clause_questao_id(questao_id,clauses)

    updateDict = ContactDB.update_n_espaco(n_espaco) | ContactDB.update_criterio(criterio)

    ContactDB.update_fun('questaoEsp',clauses,updateDict)

    return 0
"""    