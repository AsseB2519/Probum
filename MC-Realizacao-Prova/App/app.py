from flask import Flask, request, jsonify
from DBQ import Resposta_Aluno
import classes

app = Flask(__name__)

'''
# Route to get responses from students for a specific exam
@app.route('/provas/<int:idProva>/respostas', methods=['GET'])
def getRespostas(idProva):
    try:
        # Get respostas de alunos de uma prova
        result = Resposta_Aluno.getRespostas(idProva)
        return jsonify(result)
    except Exception as e:
        # Custom error handler for this route
        return jsonify({'message':'Prova não existe'}), 404
    
# Route to get responses from students for a specific question in an exam
@app.route('/provas/<int:idProva>/questoes/<int:idQuestao>/respostas', methods=['GET'])
def respostas(idProva,idQuestao):
    try:
        # Get respostas de alunos de uma prova
        result = Resposta_Aluno.getRespostasAQuestoes(idProva,idQuestao)
        return jsonify(result)
    except Exception as e:
        # Custom error handler for this route
        return jsonify({'message':'Prova não existe'}), 404

# Route to handle responses for a specific question in an exam
@app.route('/provas/<int:idProva>/questoes/<int:idQuestao>/resposta', methods=['GET', 'POST'])
def resposta(idProva, idQuestao):
    try:
        if request.method == 'POST':
            # Adiciona novas entradas
            json_data = request.get_json()

            Resposta_Aluno.novaResposta(
                idProva,
                idQuestao,
                json_data['alunoID'],
                json_data['resposta']
            )

            return 'This is a POST request.'
        else:
            # Atualiza as notas de um aluno
            aluno_id = request.args.get('alunoID')
            result = Resposta_Aluno.getResposta(idProva, idQuestao, aluno_id)
            return jsonify(result)
    except Exception as e:
        # Custom error handler for this route
        return jsonify({'message':'Prova não existe'}), 404
    '''

# Route to get information about an exam CHECK ROUTES
@app.route('/provas/<int:idProva>', methods=['GET'])
def getProvaToDo(idProva):
    try:
        result = Resposta_Aluno.getProva(idProva)
        return jsonify(result)
    except Exception as e:
        # Custom error handler for this route
        return jsonify({'message':'Prova não existe'}), 404

# Route to get information about a question in an exam and submit a response CHECK
@app.route('/provas/<int:idProva>/questoes/<int:idQuestao>', methods=['GET','POST','PUT'])
def getQuestaoAndSubmit(idProva,idQuestao):
    try:
        if request.method == 'POST':
            json_data = request.get_json()
            c = classes.RespostaQuestao(json_data)
            Resposta_Aluno.novaResposta(idProva,
                idQuestao, c.idAluno, c.resposta
            )
            return jsonify({'prova':idProva,'questao':idQuestao,'aluno': c.idAluno,'resposta':c.resposta})
        elif request.method == 'GET':
            result = Resposta_Aluno.getQuestao(idProva,idQuestao)
            return jsonify(result)
        else: 
            json_data = request.get_json() 
            c = classes.RespostaQuestao(json_data)      
            Resposta_Aluno.updateResposta(idProva,idQuestao,
                                        c.idAluno, c.resposta)
            return jsonify({'prova':idProva,'questao':idQuestao,'aluno': c.idAluno,'resposta':c.resposta})
    except Exception as e:
        # Custom error handler for this route
        return jsonify({'message':'Questao não existe'}), 404   

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
