import datetime
from flask import jsonify, session, redirect, url_for, request
from _init import main
from scripts import post_dados,get_dados,delete_dados,put_dados,post_dados_2

########################## Variaveis globais ##############################

MC_users = "http://localhost:7002"
MC_recursos = "http://localhost:7005"
MC_provas = "http://localhost:7010"
MC_Realizar_Prova = "http://localhost:7001"
MC_notificacoes = "http://localhost:7004"
MC_Correçao_Prova = "http://localhost:7003"

############################################################################

#Users
@main.route('/user/docente', methods=['POST'])
def register_Docente():
    data = request.get_json()
    target_server_url = MC_users+"/docente"

    return post_dados(target_server_url,data)
    
@main.route('/user/aluno', methods=['POST'])
def register_aluno(): 
    data = request.get_json()
    target_server_url = MC_users +"/aluno"

    return post_dados(target_server_url,data)

@main.route('/user/login', methods=['GET'])
def login(): 
    # data = request.get_json()
    target_server_url = MC_users+"/login"
    username = request.args.get('username')
    password = request.args.get('password')
    user_type = request.args.get('user_type')
    return post_dados(target_server_url,{'username':username,'password':password, 'user_type':user_type})

@main.route('/user/logout', methods=['POST'])
def logout(): 
    data = request.get_json()
    target_server_url = MC_users+"/logout"

    return post_dados(target_server_url,data)

@main.route('/user/<username>', methods=['GET','PUT','DELETE'])
def info_user(username):
    target_server_url = MC_users +f"/utilizador/{username}"
    if request.method == 'GET':
        return get_dados(target_server_url)
    elif request.method == 'PUT':
        data = request.get_json()
        return put_dados(target_server_url,data)
    elif request.method == 'DELETE':
        return delete_dados(target_server_url)

#Recursos

@main.route('/recursos', methods=['POST'])
def create_recurso():
    data = request.get_json()
    target_server_url = MC_recursos +"/recursos"

    return post_dados(target_server_url,data)

@main.route('/recursos/<id_recursos>', methods=['GET','PUT','DELETE'])
def info_recurso(id_recursos):
    target_server_url = MC_recursos +f"/recursos/reservas/{id_recursos}"
    if request.method == 'GET':
        return get_dados(target_server_url)
    elif request.method == 'PUT':
        data = request.get_json()
        return put_dados(target_server_url,data)
    elif request.method == 'DELETE':
        return delete_dados(target_server_url)


#Provas

@main.route('/prova', methods=['GET'])
def all_provas():
    #HARDCODE
    return [], 200
    # ele entra aqui
    target_server_url= MC_provas +'/prova'
    return get_dados(target_server_url)

@main.route('/prova/aluno', methods=['GET'])
def all_provas_aluno():
    username = request.args.get('username')
    target_server_url= MC_provas +'/provas/aluno/' + username
    return get_dados(target_server_url)

@main.route('/prova/docente', methods=['GET'])
def all_provas_docente():
    username = request.args.get('username')
    target_server_url= MC_provas +'/provas/prof/' + username
    return get_dados(target_server_url)

#é preciso validar primeiro o agendamento ou entao criar uma nova rota para isso
@main.route('/prova', methods=['POST'])
def create_prova():
    target_server_url= MC_provas +'/prova'
    data = request.get_json()
    return post_dados(target_server_url,data)

@main.route('/prova/<id_prova>/<id_versao>', methods=['GET','PUT','DELETE','POST'])
def search_prova(id_prova,id_versao):
    target_server_url = MC_provas +"/prova/"+id_prova+'/'+id_versao
    if request.method == 'GET':
        return get_dados(target_server_url)
    elif request.method == 'POST':#criar versao
        data = request.get_json()
        return post_dados(target_server_url,data)
    elif request.method == 'PUT':
        data = request.get_json()
        return put_dados(target_server_url,data)
    elif request.method == 'DELETE':
        return delete_dados(target_server_url)

@main.route('/prova/<id_prova>/share', methods=['POST'])
def share_prova(id_prova):
    data = request.get_json()
    target_server_url = MC_provas +"/prova/"+str(id_prova)
    (info,code)= post_dados(target_server_url,data)
    if code ==200:
        data=data['list_Teachers']
        target_server_url = 'MC-Notificaçoes'+"/prova/"+str(id_prova)
        return post_dados(target_server_url,data)
    else: 
        return (info,code)


@main.route('/prova/<id_prova>/questao/<id_questao>', methods=['GET','PUT','DELETE'])
def search_questao(id_prova,id_questao):
    target_server_url = MC_provas +f"/prova/{id_prova}/{id_questao}"
    if request.method == 'GET':
        return get_dados(target_server_url)
    elif request.method == 'PUT':
        data = request.get_json()
        return put_dados(target_server_url,data)
    elif request.method == 'DELETE':
        return delete_dados(target_server_url)

#Realizaçao de provas

@main.route('/realizar/<id_prova>', methods=['GET', 'POST'])
def start_prova(id_prova):
    if request.method == 'GET':
        target_server_url = MC_Realizar_Prova+f"/provas/{id_prova}"
        return get_dados(target_server_url)
    else:
        data = request.get_json()
        target_server_url = MC_Realizar_Prova +f"/provas/{id_prova}"
        # data = {idProva,idAluno,idQuestoes}
        post_dados(MC_Correçao_Prova +f"/classificacao/alunos/",dados=data)
        return post_dados(target_server_url,data)

#####tenho de verificar isto
# @main.route('/realizar/<id_prova>', methods=['POST'])
# def submit_prova(id_prova):
#     data = request.get_json()
#     target_server_url = MC_Realizar_Prova +f"/provas/{id_prova}"
#     # data = {idProva,idAluno,idQuestoes}
#     post_dados(MC_Correçao_Prova +f"/classificacao/alunos/",dados=data)
#     return post_dados(target_server_url,data)

@main.route('/realizar/<id_prova>/<id_versao>/questao/<id_questao>', methods=['GET','POST','PUT'])
def questoes(id_prova,id_versao,id_questao):
    target_server_url1 = MC_Realizar_Prova +f"/provas/{id_prova}/questoes/{id_questao}"
    target_server_url2 = MC_provas +f'/prova/{id_prova}/{id_versao}/questions'
    if request.method == 'GET':
        print('entrou aqui')
        return get_dados(target_server_url2)
    elif request.method == 'PUT':
        data = request.get_json()
        return put_dados(target_server_url1,data)
    elif request.method == 'POST':
        idAluno = request.args.get('username')
        resposta = request.args.get('resposta')
        return post_dados_2(target_server_url1,{'idProva':id_prova,'idQuestao':id_questao,'idAluno':idAluno,'resposta':resposta})


#Correçao de provas



@main.route('/resolucao', methods=['GET'])
def search_resolucao():
    #HARDCODE
    return [], 200
    target_server_url = MC_Correçao_Prova +f"/classificacao/provas"
    return get_dados(target_server_url)

@main.route('/resolucao/<id_prova>', methods=['GET'])
def search_resolucoes(id_prova):
    target_server_url = MC_Correçao_Prova +f"/classificacao/provas/{id_prova}"
    return get_dados(target_server_url)

def get_questoes(json):
    em  = list(json['EM'].keys())
    vf  = list(json['VF'].keys())
    esp = list(json['ESP'].keys())
    return em + vf + esp

def associa_respostas_questoes_aux(questoes,respostas,type):
    res = []
    for q in questoes.keys():
        obj = {}
        respostas_alunos = []
        for r in respostas:
            if r['idQuestao'] == q:
                respostas_alunos = r['alunos_respostas']  
                break 
        obj['alunos_respostas'] = respostas_alunos
        obj['classificacao_certa'] = 0
        obj['classificacao_errada'] = 0
        obj['resposta'] = ''
        obj['idQuestao'] = q
        if type < 2:
            resposta_questao = questoes[q]
            for r in resposta_questao:
                obj['classificacao_certa']  += questoes[q]['pontos_acerto']
                obj['classificacao_errada'] -= questoes[q]['pontos_erro']
                if type == 0:
                    obj['resposta'] += questoes[q]['id'] + ';'
                else:
                    obj['resposta'] += questoes[q]['valor'] + ';'
        else:
            resposta_questao = questoes[q]
            for r in resposta_questao:
                obj['classificacao_certa'] += questoes[q]['cotacao']
                obj['resposta'] += questoes[q]['texto'] + ';'

        obj['resposta'] = obj['resposta'][:-1]
        res.append(obj)
    return res

def associa_respostas_questoes(questoes,respostas):
    em = associa_respostas_questoes_aux(questoes['EM'] ,respostas,0)
    vf = associa_respostas_questoes_aux(questoes['VF'] ,respostas,1)
    esp = associa_respostas_questoes_aux(questoes['ESP'],respostas,2)
    return em + vf + esp


@main.route('/resolucao/auto', methods=['PUT'])
def corrigir_automaticamente():
    data = request.get_json()
    provaid = data['idProva']
    target_server_url1 = MC_provas + f'getquestoesautomaticas'
    target_server_url2 = MC_Realizar_Prova + f'/provas/{provaid}/respostas'
    target_server_url3 = MC_Correçao_Prova +f"/auto_classificacao/"
    # {idQuestao:{resposta:,classificacao_certa}}
    questoes = get_dados(target_server_url1,data=data)[0]
    # [{idQuestao:,alunos_respostas:[{idAluno:,resposta:}]}]
    questoes_ids = get_questoes(questoes)
    respostas = get_dados(target_server_url2,data={'idProva':provaid,'questoes':questoes_ids})[0]
    # [{idQuestao:,resposta:, classificacao_certa:,,alunos_respostas:[{idAluno:,resposta:}]}]
    respostas_final = associa_respostas_questoes(questoes,respostas)
    return put_dados(target_server_url3,data={'prova':provaid,'questoes_respostas':respostas_final})

@main.route('/resolucao/manual', methods=['PUT'])
def corrigir_manualmente():
    target_server_url = MC_Correçao_Prova +f"/classificacao/alunos/"
    data = request.get_json()['body']
    return put_dados(target_server_url,data)


@main.route('/resolucao/publica/<idprova>', methods=['POST'])
def publica_notas(idprova):
    target_server_url = MC_Correçao_Prova +f"/classificacao/provas/"+idprova
    return post_dados(target_server_url,{})


#Notificaçoes

@main.route('/notificacoes', methods=['GET'])
def search_notificacoes():
    username = request.args.get('username')
    target_server_url = MC_notificacoes+"/notificacoes?username="+username
    return get_dados(target_server_url)

############### todas as notifs de um user no formato [titulo, id] ######################################
@main.route('/notificacoes/<username>', methods=['GET'])
def search_notificacoes_byuser(username):
    response = []
    target_server_url = MC_notificacoes+f"/notificacoes/{username}"
    (dados,code)= get_dados(target_server_url)
    if code == 200:
        for notifi in dados:
            titulo = notifi.get('titulo')
            id = notifi.get('id')
            response.append((titulo,id))
    return (response,code)

############### um user devolva todos os seus testes ja corrigidos no formato [nome do teste, nota, id do teste] ######################################
@main.route('/corrigidos/<username>', methods=['GET'])
def search_testescorrigidos(username):
    response=[]
    target_server_url = MC_Correçao_Prova +f"/classificacao/alunos/{username}/"
    (dados,code) = get_dados(target_server_url)
    if code == 200:
        Provas = dados
        for prova in Provas:
            provaid = prova['idProva']
            publica = prova['publica']


            target_server_url = MC_provas +f"/prova/{provaid}"
            (dados1,code1)= get_dados(target_server_url)

            if (code1 == 200 and publica):
                target_server_url = MC_Correçao_Prova +f"/classificacao/alunos/{username}/{provaid}"
                (dados3,code3)= get_dados(target_server_url)

                if code3 == 200:
                    nome = dados1.get('nome')
                    classificacao = dados3.get('classificacao')
                    response.append({
                        'name': nome,
                        'classificacao':classificacao,
                        'provaID' : provaid
                    })
        return (jsonify(response),200)
    return (response,code)

############## um user devolva todos os seus testes futuros no formato [nome do teste, data do teste, id do teste] ##############################3

@main.route('/provas/por_realizar/<username>', methods=['GET'])
def search_provas_por_realizar(username):
    response=[]
    target_server_url = MC_users +f"/utilizador/{username}"
    (dados,code) = get_dados(target_server_url)
    if code == 200:
        Provas = dados.get('Provas')
        for prova in Provas:
            target_server_url = MC_provas +f"/prova/{prova}"
            (dados1,code1)= get_dados(target_server_url)

            if code1 == 200:
                nome = dados1.get('nome')
                data = dados1.get('classificacao')
                if data >= datetime.now() :
                    response.append((nome,data,prova))
        return (jsonify(response),200)
    return (response,code)