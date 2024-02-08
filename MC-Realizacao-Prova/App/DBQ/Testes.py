import Resposta_Aluno

provas_teste = [3,4]
alunos_teste = ['PG1','PG2']
questoes_teste = [1,2,3,4,5,6,7,8,9,10]
respostas_teste = ['A','B','123','V','F']

def insert():
    for prova_teste in provas_teste:
        for aluno_teste in alunos_teste:
            for questao_teste in questoes_teste:
                Resposta_Aluno.novaResposta(prova_teste,questao_teste,aluno_teste,respostas_teste[1])
                Resposta_Aluno.novasRespostas(prova_teste,questao_teste,aluno_teste,respostas_teste)

def update():
    for prova_teste in provas_teste:
        for aluno_teste in alunos_teste:
            for questao_teste in questoes_teste:
                Resposta_Aluno.updateResposta(prova_teste,questao_teste,aluno_teste,respostas_teste[2])

def select():
    for prova_teste in provas_teste:
        for aluno_teste in alunos_teste:
            for questao_teste in questoes_teste:
                respostas = list(map(lambda e : e[3],Resposta_Aluno.getRespostas(prova_teste,questao_teste,aluno_teste)))
                resposta = list(map(lambda e : (e[1],e[3]),Resposta_Aluno.getResposta(prova_teste,questao_teste,aluno_teste)))
                print(f'Respostas da prova {prova_teste}:\t{respostas}')
                print(f'Resposta à questão {questao_teste}:\t{resposta}')


# insert()
# update()
select()