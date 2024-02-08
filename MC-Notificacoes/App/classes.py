class Notificacao:
    def __init__(self, json):
        self.idNotificacao = json['idNotificacao']
        self.idUser = json['idUser']
        self.titulo = json['titulo']
        self.descricao = json['descricao']
        self.read = json['read']

class CriaInstancias:
    def __init__(self, json):
        self.idNotificacao = json['idNotificacao']
        self.idUser = json['idUser']
        self.titulo = json['titulo']
        self.descricao = json['descricao']
        self.read = json['read']
