class User:
    def __init__(self, json):
        self.nome = json['nome']
        self.num = json['num']
        self.email = json['email']
        self.password = json['password']

class UserMicroserviceClasses:
    def __init__(self, json):
        self.idNotificacao = json['idNotificacao']
        self.idUser = json['idUser']
        self.titulo = json['titulo']
        self.descricao = json['descricao']
        self.read = json['read']