from datetime import datetime
from DBQ import Provas

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
    Provas.createQuestaoDesen(11, 'esta é a questao desenvolvimento teste 1', 'path imagem','ser ou n ser?', 250, 500, 'criterio de correcao', 1, 1, 1)
    Provas.createQuestaoEM(12, 'questao EM', 'pathimagem', 1, 1, 2)
    Provas.createAlinea(1, 'isto esta certo?', 1, 2, 2, 12, 1)
    Provas.createAlinea(2, 'e isto?', 0, 2, 2, 12, 2)
    Provas.createQuestaoVF(21, 'questao VF','pathimagem', 2, 1, 1)
    Provas.createAlinea(3, 'isto esta certo?', 1, 2, 2, 21, 1)
    Provas.createAlinea(4, 'e isto?', 0, 2, 2, 21, 2)
    Provas.createQuestaoEsp(22, 'questao espacos', 'pathimagem', 2, 1, 2)
    Provas.createEspacos(1, 1, 'isto esta correto', 'blablabla', 22)
    Provas.createEspacos(2, 2, 'isto esta correto', 'blebleble', 22)

def update():
    Provas.updateProva(1,1,'Prova update 1','Ze Josefino',dt,90,10,1,1)
    Provas.updateProva(2,1,'Prova update 2','Joao Patrao',dt,45,5,1,1)
    Provas.updateQuestaoDesen(11, 'esta e a questao atualizada desenvolvimento', 'novo_path imagem', 150, 400, 'criterio de correcao', 1, 1, 1)
    Provas.updateQuestaoEM(12, 'questao atualizada EM', 'pathimagem novo', 1, 1, 2)
    Provas.updateQuestaoVF(21, 'questao atualizada VF','pathimagem novo', 2, 1, 1)
    Provas.updateAlinea(1, 'isto esta muito certo?', 1, 2, 2, 12, 1)
    Provas.updateAlinea(2, 'e iiiisto?', 0, 2, 2, 12, 2)
    Provas.updateAlinea(3, 'isto esta muito certo?', 1, 2, 2, 21, 1)
    Provas.updateAlinea(4, 'e istoooo?', 0, 2, 2, 21, 2)
    Provas.updateQuestaoEsp(22, 'nova questao espacos', 'novo pathimagem', 2, 1, 2)
    Provas.updateEspacos(1, 1, 'isto esta muito correto', 'blobloblo', 22)
    Provas.updateEspacos(2, 2, 'isto esta muito correto', 'bliblibli', 22)

def select():
    #acessoProvaProfs = Provas.getProvaProfs(1)
    #alunosProva = Provas.getProvaAlunos(1,1)
    #prova = Provas.getProva(1,1)
    #alineas = Provas.getAlineas(12)
    #espacos = Provas.getEspacos(22)
    #questoesProva11 = Provas.getQuestoes(1,1)
    #questoesProva21 = Provas.getQuestoes(2,1)
    #print('Os profs que têm acesso à prova 1 são: ',acessoProvaProfs)
    #print()
    #print('Os alunos que têm acesso à prova 1, versao 1 são: ',alunosProva)
    #print()
    #print('Prova 1 versao 1:\n', prova)
    #print()
    #for alinea in alineas:
    #    print('Alinea da questao 12: ',alinea)
    #print()
    #for espaco in espacos:
    #    print('Espaco da questao 22: ',espaco)
    #print()
    #print('Questoes prova 1 versao 1:')
    #for key, value in questoesProva11.items():
    #    for v in value:
    #        print(f'{key}: {v}')
    #print()
    #print('Questoes prova 2 versao 1:')
    #for key, value in questoesProva21.items():
    #    for v in value:
    #        print(f'{key}: {v}')
    #print('provas_aluno:\n')
    #print(Provas.getProvas_aluno('PG123'))
    #print('provas_prof:\n')
    #print(Provas.getProvas_prof('PG123'))
#
    print(Provas.getRespostasAutomaticas(1,1))


#insert()
#update()
select()
