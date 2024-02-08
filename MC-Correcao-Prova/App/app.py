# Create a file named app.py
from flask import Flask, request, jsonify
import json
from DBQ import ClassificacaoProvas
from DBQ import ClassificacaoQuestoes
import classes

app = Flask(__name__)

# 1 - X
@app.route('/auto_classificacao/' ,methods=['POST'])
def autoClassificacao():
    try: 
        body = request.get_json()
        ca = classes.ClassificacaoAutomatica(body)
        ClassificacaoQuestoes.correcaoAutomatica(ca.get_alunos_acertaram())
        return jsonify({'idProva':ca.prova})
    except Exception as e:
        # Custom error handler for this route
        return jsonify({'message':'Dados incorretos '}), 404

# 1 - 
@app.route('/classificacao/alunos/<string:idAluno>/<int:idProva>/', methods=['GET'])
def getClassificacaoAluno(idAluno,idProva):
    try:
        # Aluno consulta a sua nota
        nota_prova = ClassificacaoProvas.getProvaNotaAluno(idProva,idAluno)
        nota_questoes = ClassificacaoQuestoes.getQuestoesNotasAluno(idProva,idAluno)
        classificacoes_res = list(map(lambda e : {'idQuestao':e[1],'classificacao':e[3]},nota_questoes))
        return jsonify({'idProva':idProva,'classificacao':nota_prova,'idAluno':idAluno,'classificacoes_respostas':classificacoes_res})
    except Exception as e:
        # Custom error handler for this route
        return jsonify({'message':'Aluno ou Prova não existe'}), 404

# 1 - 
@app.route('/classificacao/alunos/<string:idAluno>/', methods=['GET'])
def getProvasAluno(idAluno):
    try:
        # Sistema busca provas que um aluno tem provas
        provas = ClassificacaoProvas.getProvasAluno(idAluno)
        result = list(map(lambda p : {'idProva':p[0],'publica':p[3]},provas))
        return jsonify(result)
    except Exception as e:
        # Custom error handler for this route
        return jsonify({'message':'Aluno não existe'}), 404

# 1 - X
# 2 - X
@app.route('/classificacao/alunos/', methods=['PUT', 'POST'])
def classificacaoAlunos():
    try:
        if request.method == 'POST':
            # Adiciona novas entradas
            body = request.get_json()
            ci = classes.CriaInstancias(body)
            ClassificacaoProvas.novaProva(ci.idProva,ci.idAluno)
            ClassificacaoQuestoes.novasQuestoes(ci.idProva,ci.idAluno,ci.idQuestoes)
            nota_prova = ClassificacaoProvas.getProvaNotaAluno(ci.idProva,ci.idAluno)
            return jsonify({'idProva':ci.idProva,'idAluno': ci.idAluno,'classificacao':nota_prova})
        else:
            # Atualiza as notas de um aluno
            body = request.get_json()
            cq = classes.ClassificacaoQuestao(body)
            ClassificacaoQuestoes.updateNotaAluno(cq.idProva,cq.idAluno,cq.idQuestao,cq.classificacao)
            nota_prova = ClassificacaoProvas.getProvaNotaAluno(cq.idProva,cq.idAluno)
            return jsonify({'idProva':cq.idProva,'idAluno':cq.idAluno,'classificacao':nota_prova})
    except Exception as e:
        # Custom error handler for this route
        return jsonify({'message':'Dados incorretos '}), 404

# 1 - X
# 2 - 
@app.route('/classificacao/provas/<int:idProva>', methods=['GET', 'POST'])
def classificacaoProvas(idProva):
    try:
        if request.method == 'POST':
            # Publica as notas de uma prova
            ClassificacaoProvas.publicaNotas(idProva)
            return jsonify({'idProva':idProva})
        else:
            # Verifica se as notas estão públicadas
            value = ClassificacaoProvas.notasProvaPublicadas(idProva)
            return jsonify({'result':value})
    except Exception as e:
        # Custom error handler for this route
        return jsonify({'message':'Prova não existe'}), 404
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
