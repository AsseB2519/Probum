import ClassificacaoProvas
import ClassificacaoQuestoes

provas_teste = [3,4]
alunos_teste = ['PG1','PG2']
questoes_teste = [1,2,3,4,5,6,7,8,9,10]

def insert():
    for prova_teste in provas_teste:
        for aluno_teste in alunos_teste:
            ClassificacaoProvas.novaProva(prova_teste,aluno_teste)
            ClassificacaoQuestoes.novasQuestoes(prova_teste,aluno_teste,questoes_teste)

def update():
    for prova_teste in provas_teste:
        for aluno_teste in alunos_teste:
            for questao_teste in questoes_teste:
                ClassificacaoQuestoes.updateNotaAluno(prova_teste,aluno_teste,questao_teste,1)

def select():
    for prova_teste in provas_teste:
        for aluno_teste in alunos_teste:
            provas = list(map(lambda e : e[0],ClassificacaoProvas.getProvasAluno(aluno_teste)))
            notasQuestoes = list(map(lambda e : (e[1],e[3]),ClassificacaoQuestoes.getQuestaoNotasAluno(prova_teste,aluno_teste)))
            notaProva     = ClassificacaoProvas.getProvaNotaAluno(prova_teste,aluno_teste)
            print(f'Provas aluno {aluno_teste}:\t{provas}')
            print(f'Notas questoes {prova_teste}:\t{notasQuestoes}')
            print(f'Nota prova {prova_teste}:\t\t{notaProva}')


# insert()
# update()
select()

