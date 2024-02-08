from DBQ import ContactDB 

# Obter uma Notificacao pelo seu id
def getNotificacao(idUser, idNotificacao):
    clauses = ContactDB.create_clauses()
    clauses = ContactDB.add_clause_idUser(idUser, clauses)
    clauses = ContactDB.add_clause_idNotificacao(idNotificacao, clauses)

    result = ContactDB.select_fun('notificacoes', clauses)
    return result

# Obter uma Notificacao pelo seu id
def getNotiTitulo(idUser, titulo):
    clauses = ContactDB.create_clauses()
    clauses = ContactDB.add_clause_idUser(idUser, clauses)
    clauses = ContactDB.add_clause_Titulo(titulo, clauses)

    result = ContactDB.select_fun('notificacoes', clauses)
    return result

# Obter as Notificacoes do user
def getUserNoti(idUser):
    clauses = ContactDB.create_clauses()
    clauses = ContactDB.add_clause_idUser(idUser, clauses)

    result = ContactDB.select_fun('notificacoes', clauses)
    return result

# Cria uma nova Notificacao
def criaNotificacao(idUser, idNotificacao, titulo, descricao):
    newNoti = ContactDB.create_new_value_notificacoes(idUser, idNotificacao, titulo, descricao, False)
    return ContactDB.insert_fun('questoes', newNoti)

# Lê uma nova Notificacao, mudando o estado de visto
def readNotificacao(idNotificacao):
    clauses = ContactDB.create_clauses()
    clauses = ContactDB.add_clause_idNotificacao(idNotificacao,clauses)
    ContactDB.update_fun('notificacoes',clauses,ContactDB.update_read(True))
    return 0
    
# Obter uma Notificacao não vistas ou vistas
def getNotificacaoRead(idUser, read):
    clauses = ContactDB.create_clauses()
    clauses = ContactDB.add_clause_idUser(idUser, clauses)
    clauses = ContactDB.add_clause_read(read, clauses)

    result = ContactDB.select_fun('notificacoes', clauses)
    return result

# Modifica a Notificacao (i.e. titulo e descricao)
def updateNotificacao(idNotificacao, titulo, descricao):
    clauses = ContactDB.create_clauses()
    clauses = ContactDB.add_clause_idNotificacao(idNotificacao,clauses)
    ContactDB.update_fun('notificacoes',clauses,ContactDB.update_titulo(titulo))
    ContactDB.update_fun('notificacoes',clauses,ContactDB.update_descricao(descricao))
    return 0



# from DBQ import ContactDB

# class NotificacoesObservable:
#     def __init__(self):
#         self._observers = []

#     def add_observer(self, observer):
#         if observer not in self._observers:
#             self._observers.append(observer)

#     def remove_observer(self, observer):
#         self._observers.remove(observer)

#     def notify_observers(self, idNotificacao):
#         for observer in self._observers:
#             observer.update(idNotificacao)

# class Notificacoes(ContactDB, NotificacoesObservable):
#     def criaNotificacao(self, idUser, idNotificacao, titulo, descricao):
#         newNoti = ContactDB.create_new_value_notificacoes(idUser, idNotificacao, titulo, descricao, False)
#         result = ContactDB.insert_fun('questoes', newNoti)
#         if result == 0:
#             self.notify_observers(idNotificacao)
#         return result

#     def updateNotificacao(self, idNotificacao, titulo, descricao):
#         clauses = ContactDB.create_clauses()
#         clauses = ContactDB.add_clause_idNotificacao(idNotificacao, clauses)
#         ContactDB.update_fun('notificacoes', clauses, ContactDB.update_titulo(titulo))
#         ContactDB.update_fun('notificacoes', clauses, ContactDB.update_descricao(descricao))
#         self.notify_observers(idNotificacao)
#         return 0

# # Exemplo de um observador específico para notificações
# class NotificacoesObserver:
#     def update(self, idNotificacao):
#         print(f"Nova notificação com ID {idNotificacao}")

# # Uso do padrão Observer
# if __name__ == "__main__":
#     notificacoes = Notificacoes()

#     observer1 = NotificacoesObserver()
#     observer2 = NotificacoesObserver()

#     notificacoes.add_observer(observer1)
#     notificacoes.add_observer(observer2)

#     notificacoes.criaNotificacao(1, 101, "Título 1", "Descrição 1")
#     notificacoes.updateNotificacao(101, "Novo Título", "Nova Descrição")
