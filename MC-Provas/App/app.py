# Create a file named app.py
from flask import Flask, request, jsonify
import json
from DBQ import Provas
import classes
from datetime import datetime

app = Flask(__name__)

# Criaçao de Provas
@app.route('/prova/' ,methods=['POST'])
def postProva():
    try: 
        body = request.get_json()
        p = classes.Prova(body)
        Provas.createProva(p.id,p.version,p.name,p.creator,p.horario,p.duracao,p.timeAdmi,p.randOrder,p.canBack)
        return jsonify({'idProva':p.id,'idVersao':p.version})
    except Exception as e:
        # Custom error handler for this route
        return jsonify({'message':'Dados incorretos '}), 404

# Criaçao de Provas   
@app.route('/prova/<int:provaID>/' ,methods=['POST'])
def postProvaVersion(provaID):
    body = request.get_json()
    try:
        p = classes.Prova(body)
    except Exception as e:
        return jsonify({'message':'p'}), 404
    try:    
        Provas.createProva(provaID,p.version,p.name,p.creator,p.horario,p.duracao,p.timeAdmi,p.randOrder,p.canBack)
        return jsonify({'idProva':provaID,'idVersao':p.version})
    except Exception as e:
        return jsonify({'message':'Dados incorretos '}), 404    

# Criaçao/Edicao/Observacao de Provas
@app.route('/prova/<int:provaId>/<int:versaoId>/questions', methods=['POST','PUT','GET'])
def provaQuestions(provaId,versaoId):
    try:
        if request.method == 'POST':
            # Deve ser um json com 4 campos (um para cada tipo de pergunta), cujo valor é
            # a lista com todas perguntas, e os seus campos respetivos, desse resptivo tipo
            # da prova correspondente
            body = request.get_json()
            try:
                for q in body["Desen"]:
                    try:
                        p = classes.QuestaoDesen(q)
                        Provas.createQuestaoDesen(p.id, p.enunciado, p.img, p.min, p.max, p.crit, provaId, versaoId, p.pos)
                    except Exception as ex:
                        return jsonify({'message':'p or desen1'}), 404
            except Exception as ex:
                return jsonify({'message':'desen2'}), 404
            for q in body["EM"]:
                try:
                    p = classes.QuestaoEM(q)
                except Exception as ex:
                    return jsonify({'message':'p EM'}), 404
                try:
                    Provas.createQuestaoEM(p.id, p.enunciado, p.img, provaId, versaoId, p.pos)
                except Exception as ex:
                    return jsonify({'message': 'questao'}), 404
                try:
                    for a in p.alineas:
                        Provas.createAlinea(a.id, a.enun, a.value, a.cotR, a.cotW, p.id, a.pos)
                except Exception as ex:
                    return jsonify({'message':[a.id, a.enun, a.value, a.cotR, a.cotW, p.id, a.pos]}), 404
            for q in body["VF"]:
                p = classes.QuestaoVF(q)
                Provas.createQuestaoVF(p.id, p.enunciado, p.img, provaId, versaoId, p.pos)
                for a in p.alineas:
                    Provas.createAlinea(a.id, a.enun, a.value, a.cotR, a.cotW, p.id, a.pos)

            for q in body["Esp"]:
                try:
                    p = classes.QuestaoEsp(q)
                except Exception as ex:
                    return jsonify({'message':'p'}), 404
                try:
                    Provas.createQuestaoEsp(p.id, p.enunciado, p.img, provaId, versaoId, p.pos)
                except Exception as ex:
                    return jsonify({'message':'esp'}), 404
                try:
                    for e in p.spaces:
                        Provas.createEspacos(e.id,e.n_espaco,e.value,e.texto,p.id)
                except Exception as ex:
                    return jsonify({'message':'alinea'}), 404
                
            return jsonify({'idProva': provaId,'idVersao':versaoId})
        elif request.method == 'PUT':
            # Deve ser um json com 4 campos (um para cada tipo de pergunta), cujo valor é
            # a lista com todas perguntas, e os seus campos respetivos, desse resptivo tipo
            # da prova correspondente
            body = request.get_json()

            for q in body["Desen"]:
                p = classes.QuestaoDesen(q)
                Provas.updateQuestaoDesen(p.id, p.enunciado, p.img, p.min, p.max, p.crit, provaId, versaoId, p.pos)

            for q in body["EM"]:
                p = classes.QuestaoEM(q)
                Provas.updateQuestaoEM(p.id, p.enunciado, p.img, provaId, versaoId, p.pos)
                for a in p.alineas:
                    Provas.updateAlinea(a.id, a.enun, a.value, a.cotR, a.cotW, p.id, a.pos)
            
                for q in body["VF"]:
                    p = classes.QuestaoVF(q)
                    Provas.updateQuestaoVF(p.id, p.enunciado, p.img, provaId, versaoId, p.pos)
                    for a in p.alineas:
                        Provas.updateAlinea(a.id, a.enun, a.value, a.cotR, a.cotW, p.id, a.pos)

                for q in body["Esp"]:
                    p = classes.QuestaoEsp(q)
                    Provas.updateQuestaoEsp(p.id, p.enunciado, p.img, provaId, versaoId, p.pos)
                    for e in p.spaces:
                        Provas.updateEspacos(e.id,e.n_espaco,e.value,e.texto,p.id)
            return jsonify({'idProva': provaId,'idVersao':versaoId})

        else:
            questoes = Provas.getQuestoes(provaId,versaoId)
            des = [{'id': e[0], 'descricao': e[1], 'imagem': e[2], 'min_palavras': e[3], 'max_palavras': e[4], 'criterio_avaliacao': e[5], 'prova_id': e[6], 'prova_versao': e[7], 'prova_pos': e[8]} for e in questoes['Desen']]
            em = [{'id': e[0], 'descricao': e[1], 'imagem': e[2], 'prova_id': e[3], 'prova_versao': e[4], 'prova_pos': e[5], 'alineas': Provas.getAlineas(e[0])} for e in questoes['EM']]
            vf = [{'id': e[0], 'descricao': e[1], 'imagem': e[2], 'prova_id': e[3], 'prova_versao': e[4], 'prova_pos': e[5], 'alineas': Provas.getAlineas(e[0])} for e in questoes['VF']]
            esp = [{'id': e[0], 'descricao': e[1], 'imagem': e[2], 'prova_id': e[3], 'prova_versao': e[4], 'prova_pos': e[5], 'espacos' : Provas.getEspacos(e[0])} for e in questoes['Esp']]
            return jsonify({'Desen' : des, 'EM' : em, 'VF' : vf, 'Esp' : esp})
    except Exception as ex:
        # Custom error handler for this route
        return jsonify({'message':'Dados incorretos'}), 404

# Ediçao de provas
@app.route('/prova/<int:provaId>/<int:versaoId>/', methods=['PUT','GET'])
def provaVersion(provaId,versaoId):
    try:
        if request.method == 'PUT':
            body = request.get_json()
            p = classes.Prova(body)
            Provas.updateProva(provaId,versaoId,p.name,p.creator,p.horario,p.duracao,p.timeAdmi,p.randOrder,p.canBack)
            try:
                provaT = Provas.getProva(provaId,versaoId)
                prova = provaT[0]
            except Exception as e:
                return jsonify({'message':'pro crl '}), 404
            return jsonify({'idProva':prova[0],'idVersao':prova[1],'nome': prova[2],'criador': prova[3],
                            'data': prova[4], 'duracao':prova[5] ,'tempo_admissao': prova[6],
                            'aleatorio': prova[7],'retrocesso': prova[8]})
        else:
            provaT = Provas.getProva(provaId,versaoId)
            prova = provaT[0]
            return jsonify({'idProva':prova[0],'idVersao':prova[1],'nome': prova[2],'criador': prova[3],
                            'data': prova[4], 'duracao':prova[5] ,'tempo_admissao': prova[6],
                            'aleatorio': prova[7],'retrocesso': prova[8]})
    except Exception as e:
        # Custom error handler for this route
        return jsonify({'message':'Dados incorretos '}), 404

# MUDAR NO SWAGGER
@app.route('/prova/<int:provaId>/share/', methods=['PUT','GET'])
def shareProva(provaId):
    try:
        if request.method == 'PUT':
            # Deve ter os ids dos professores aos quais partilhar a prova
            body = request.get_json()
            for p in body['profs']:
                Provas.createProf_prova(p,provaId)
            profs = Provas.getProvaProfs(provaId)
            return jsonify({'idProva':provaId,'profs': profs})        
        else:
            profs = Provas.getProvaProfs(provaId)
            return jsonify({'idProva':provaId,'profs': profs})    
    except Exception as e:
        # Custom error handler for this route
        return jsonify({'message':'Dados incorretos '}), 404

# ADICIONAR NO SWAGGER    
@app.route('/prova/<int:provaId>/<int:versaoId>/signUp/', methods=['PUT','GET'])
def signUpProva(provaId,versaoId):
    try:
        if request.method == 'PUT':
            # Deve ter os ids dos professores aos quais partilhar a prova
            body = request.get_json()
            for a in body['alunos']:
                Provas.createAluno_prova(a,provaId,versaoId)
            alunos = Provas.getProvaAlunos(provaId,versaoId)
            return jsonify({'idProva':provaId,'idVersao':versaoId,'alunos': alunos})        
        else:
            alunos = Provas.getProvaAlunos(provaId,versaoId)
            return jsonify({'idProva':provaId,'idVersao':versaoId,'alunos': alunos})    
    except Exception as e:
        # Custom error handler for this route
        return jsonify({'message':'Dados incorretos '}), 404

# ADICIONAR NO SWAGGER    
@app.route('/prova/<int:provaId>/<int:versaoId>/answers/', methods=['GET'])
def respostasProva(provaId,versaoId):
    try:
        awn = Provas.getRespostasAutomaticas(provaId,versaoId)

        em = {}
        for i,als in awn['EM'].items():
            em[i] = {}
            for a in als:
                # Se alinea for certa
                if a[1] == 1:
                    em[i] = {'id':a[0],'pontos_acerto':a[2],'pontos_erro':a[3]}
        
        vf = {}
        for i,als in awn['VF'].items():
            vf[i] = {}
            for a in als:
                # Se for verdadeiro
                if a[1] == 1:
                    vf[i] = {'id':a[0],'valor':'V','pontos_acerto':a[2],'pontos_erro':a[3]}
                # Se for falso
                else:
                    vf[i] = {'id':a[0],'valor':'F','pontos_acerto':a[2],'pontos_erro':a[3]}
        
        esp = {}
        for i,als in awn['Esp'].items():
            esp[i] = {}
            for a in als:
                esp[i] = {'id':a[0],'n_espaco':a[1],'cotacao':a[2],'texto':a[3]}
        return jsonify({'EM' : em, 'VF' : vf, 'Esp' : esp})
    except Exception as e:
        # Custom error handler for this route
        return jsonify({'message':'Dados incorretos '}), 404
    
# Criaçao de Provas
@app.route('/provas/aluno/<string:username>/' ,methods=['GET'])
def getProvas_aluno(username):
    try: 
        lista = Provas.getProvas_aluno(username)
        result = {}
        for prova in lista:
            id = str(prova[0]) + str(prova[1])
            result[id]={'idProva':prova[0],'idVersao':prova[1],'nome': prova[2],'criador': prova[3],
                           'data': prova[4], 'duracao':prova[5] ,'tempo_admissao': prova[6],
                           'aleatorio': prova[7],'retrocesso': prova[8]}
        return jsonify(result)
    except Exception as e:
        # Custom error handler for this route
        return jsonify({'message':'Dados incorretos'}), 404
    
# Criaçao de Provas
@app.route('/provas/prof/<string:username>/' ,methods=['GET'])
def getProfFuture(username):
    try: 
        lista = Provas.getProvas_prof(username)
        result = {}
        for prova in lista:
            id = str(prova[0]) + str(prova[1])
            result[id]={'idProva':prova[0],'idVersao':prova[1],'nome': prova[2],'criador': prova[3],
                            'data': prova[4], 'duracao':prova[5] ,'tempo_admissao': prova[6],
                            'aleatorio': prova[7],'retrocesso': prova[8]}
        return jsonify(result)
    except Exception as e:
        # Custom error handler for this route
        return jsonify({'message':'Dados incorretos'}), 404
  
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')