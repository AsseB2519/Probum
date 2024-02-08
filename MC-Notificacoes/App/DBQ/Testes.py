import Notificacoes

users_teste = ['PG1','PG2']
notificacoes_teste = [1,2,3,4]
titulos_teste = ['Classificação da Prova',
                 'Sala reservada para Prova'
                 'Inscrição na Prova',
                 'Registo do Usuário']
descricao_teste = ['A sua classificação na Prova A foi 16 valores'
                   'A sala reserva para a Prova B é G0.06'
                   'Inscrição concluída na Prova B'
                   'Registo com sucesso do utilizador']

def insert():
    Notificacoes.criaNotificacao(users_teste[0], notificacoes_teste[0], titulos_teste[0], descricao_teste[0], False)
    Notificacoes.criaNotificacao(users_teste[1], notificacoes_teste[1], titulos_teste[1], descricao_teste[1], False)
    Notificacoes.criaNotificacao(users_teste[1], notificacoes_teste[2], titulos_teste[2], descricao_teste[2], False)
    Notificacoes.criaNotificacao(users_teste[1], notificacoes_teste[3], titulos_teste[3], descricao_teste[3], True)

def update():
    Notificacoes.updateNotificacao(notificacoes_teste[1],
                                   'Sala reservada para Prova',
                                   'A sala reserva para a Prova B muda para a sala G0.20')
    Notificacoes.readNotificacao(notificacoes_teste[2])

def select():
    user = 'PG2'
    id = 2
    titulo = 'Registo do Usuário'

    notificacao = Notificacoes.getNotificacao(user, id)
    print(f'Notificação com ID {id} do user {user}:\n{notificacao}')
    
    usernoti = list(map(lambda e : (e[2],e[3]),Notificacoes.getUserNoti(user)))
    print(f'Notificações do user {user}:\n{usernoti}')

    titulonoti = list(map(lambda e : (e[2],e[3]),Notificacoes.getUserNoti(user, titulo)))
    print(f'Notificações do user {user} sobre {titulo}:\n{titulonoti}')

    notivisto = list(map(lambda e : (e[2],e[3]),Notificacoes.getNotificacaoRead(user, False)))
    print(f'Notificação não vistas do user {user}:\n{notivisto}')

    

#insert()
#update()
#select()