class RespostaQuestao:
    def __init__(self, json):
        self.idAluno = json['idAluno']
        self.resposta = json['resposta']

class RespostasProva:
    def __init__(self, json):
        self.idProva = json['idProva']
        self.idAluno = json['idAluno']
        self.respostas = json['respostas']

class CriaInstancias:
    def __init__(self, json):
        self.idProva = json['idProva']
        self.idAluno = json['idAluno']
        self.idQuestoes = json['idQuestoes']
        self.resposta = json['resposta']

