class AlunoResposta:
    def __init__(self, json):
        self.idAluno = json['idAluno']
        self.resposta = json['resposta']


class Questoes_Resposta:
    def __init__(self, json):
        self.idQuestao = json['idQuestao']
        self.resposta = json['resposta']
        self.classificacao_certa = json['classificacao_certa']
        self.classificacao_errada = json['classificacao_errada']
        self.alunos_resposta = list(map(lambda e : AlunoResposta(e),json['alunos_respostas']))
    
    def get_alunos_acertaram(self):
        alunos_certos = list(map(lambda e: e.idAluno,filter(lambda e : e.resposta == self.resposta ,self.alunos_resposta)))
        alunos_errados = list(map(lambda e: e.idAluno,filter(lambda e : e.idAluno not in alunos_certos ,self.alunos_resposta)))
        return (self.idQuestao,self.classificacao_certa,self.classificacao_errada,alunos_certos,alunos_errados)

class ClassificacaoAutomatica:
    def __init__(self, json):
        self.prova = json['prova']
        self.questoes_respostas = list(map(lambda e : Questoes_Resposta(e),json['questoes_respostas']))
    def get_alunos_acertaram(self):
        alunos_res_certas = list(map(lambda e : e.get_alunos_acertaram(),self.questoes_respostas))
        return list(map(lambda e : (self.prova,e[0],e[1],e[2],e[3],e[4]),alunos_res_certas))
    
class ClassificacaoQuestao:
    def __init__(self, json):
        self.idProva = json['idProva']
        self.idQuestao = json['idQuestao']
        self.idAluno = json['idAluno']
        self.classificacao = json['classificacao']

class ClassificacaoProva:
    def __init__(self, json):
        self.idProva = json['idProva']
        self.idAluno = json['idAluno']
        self.classificacao = json['classificacao']

class CriaInstancias:
    def __init__(self, json):
        self.idProva = json['idProva']
        self.idAluno = json['idAluno']
        self.idQuestoes = json['idQuestoes']
