class Prova:
    def __init__(self, json):
        self.id = json.get('id','')
        self.name = json['name']
        self.version = json['version']
        self.canBack = json['canBack']
        self.randOrder = json['randOrder']
        self.horario = json['horario']
        self.duracao = json['duracao']
        self.timeAdmi = json['timeAdmi']
        self.creator = json['creator']
        #self.questoes = json['questoes']
        #self.docentes = json['docentes'] 
        #self.alunosInc = json['alunosInc']

class QuestaoVF:
    def __init__(self, json):
        self.id = json['id']
        self.enunciado = json['enunciado']
        self.img = json['img']
        self.pos = json['pos']
        self.alineas = list(map(lambda e : Alinea(e),json['alineas']))

class QuestaoEM:
    def __init__(self, json):
        self.id = json['id']
        self.enunciado = json['enunciado']
        self.img = json['img']
        self.pos = json['pos']
        self.alineas = list(map(lambda e : Alinea(e),json['alineas']))

class QuestaoDesen:
    def __init__(self, json):
        self.id = json['id']
        self.enunciado = json['enunciado']
        self.img = json['img']
        self.min = json['min']
        self.max = json['max']
        self.crit = json['crit']
        self.pos = json['pos']

class QuestaoEsp:
    def __init__(self, json):
        self.id = json['id']
        self.enunciado = json['enunciado']
        self.img = json['img']
        self.text = json['text']
        self.spaces = list(map(lambda e : Espaco(e),json['spaces']))
        self.pos = json['pos']

class Alinea:
    def __init__(self, json):
        self.id = json['id']
        self.enun = json['enun']
        self.value = json['value']
        self.cotR = json['cotR']
        self.cotW = json['cotW']
        self.pos = json['pos']

class Espaco:
    def __init__(self,json):
        self.id = json['id']
        self.n_espaco = json['n_espaco']
        self.value = json['value']
        self.texto = json['texto']
        #self.questao_id = json['questao_id']