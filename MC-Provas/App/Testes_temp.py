from datetime import datetime
from DBQ import Provas

# Obter uma prova pelo o seu ID
# getProva(provaID,ver):

# Obter as questoes de uma prova
# getQuestoes(provaID,ver)

# Obter as respostas automaticas de uma prova
# getRespostasAutomaticas(provaID,ver):

# Obter uma questao de uma prova
# getQuestao(qID,provaID,tipo,ver):
    
# Obter as alineas de uma questao
# def getAlineas(qID)

# Obter os espaços da questão de preencher espaços
# getEspacos(qID)
   
# Obter os professores que tem a acesso a uma prova pelo o seu ID
# getProvaProfs(prova_id):

# Obter os alunos inscritos numa prova pelo o seu ID
# getProvaAlunos(prova_id,versao_id)

# Obter um aluno_prova pelo o seu ID
# getAluno_prova(id_aluno,prova_id,prova_versao):
   
# Obter um prof_prova pelo o seu ID
# getProf_prova(id_prof,prova_id):


###INSERT###

dt = datetime.now()

def insert():
    Provas.createProva(1,1,'Prova 1','Ze Manel',dt,90,10,1,1)
    Provas.createProva(2,1,'Prova 2','Joao Manel',dt,45,5,1,1)
    Provas.createAluno_prova(1, 1, 1)
    Provas.createAluno_prova(3, 1, 1)
    Provas.createAluno_prova(5, 1, 1)
    Provas.createAluno_prova(2, 2, 1)
    Provas.createAluno_prova(4, 2, 1)
    Provas.createAluno_prova(6, 2, 1)
    Provas.createProf_prova(11, 1)
    Provas.createProf_prova(33, 1)
    Provas.createProf_prova(22, 2)
    Provas.createProf_prova(44, 2)
    Provas.createQuestaoDesen(11, 'esta é a questao desenvolvimento teste 1', 'path imagem', 250, 500, 'criterio de correcao', 1, 1, 1)
    Provas.createQuestaoEM(12, 'questao EM', 'pathimagem', 1, 1, 2)
    Provas.createAlinea(1, 'isto esta certo?', 1, 2, 2, 12, 1)
    Provas.createAlinea(2, 'e isto?', 0, 2, 2, 12, 2)
    Provas.createQuestaoVF(21, 'questao VF','pathimagem', 2, 2, 1)
    Provas.createAlinea(3, 'isto esta certo?', 1, 2, 2, 21, 1)
    Provas.createAlinea(4, 'e isto?', 0, 2, 2, 21, 2)
    Provas.createQuestaoEsp(22, 'questao espacos', 'pathimagem', 2, 1, 2)
    Provas.createEspacos(1, 1, 'isto esta correto', 'blablabla', 22)
    Provas.createEspacos(2, 2, 'isto esta correto', 'blebleble', 22)

insert()
