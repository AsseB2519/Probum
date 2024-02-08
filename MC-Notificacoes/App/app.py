from flask import Flask, request, jsonify
from DBQ import Notificacoes
import classes

app = Flask(__name__)

###########################################

@app.route('/notificacoes', methods=['GET','POST'])
def respostas():
    try:
        if request.method == 'GET':
            # Get notificações de user
            idUser = request.args.get('username')
            result = Notificacoes.getUserNoti(idUser)
            # result vem em tuplos
            # no caso ( idNotificacao idUser titulo descricao descricao)
            # converter para json
            result = list(map(lambda e : {
                'idNotificacao' : e[0],
                'idUser' : e[1],
                'titulo' : e[2],
                'descricao' : e[3],
                'read' : e[4]
            } ,result))
            return jsonify(result)
        else:
            idUser = request.args.get('username')
            json_data = request.get_json()
            ci = classes.CriaInstancias(json_data)
            # Post notificações no user
            result = Notificacoes.criaNotificacao(ci.idNotificacao,
                idUser, ci.titulo, ci.descricao, False
            )
            return 'This is a POST request'
    except Exception as e:
        # Custom error handler for this route
        return jsonify({'message':'Dados incorretos'}), 404

# @app.route('/notificacoes/<bool:read>', methods=['GET'])
# def notificacoesRead(read):
#     try:
#         # Get notificações de user não vistas ou vistas
#         idUser = request.args.get('username')
#         result = Notificacoes.getNotificacaoRead(idUser, read)
#         return jsonify(result)
#     except Exception as e:
#         # Custom error handler for this route
#         return jsonify({'message':'Dados incorretos'}), 404

@app.route('/notificacoes/<string:read>', methods=['GET'])
def notificacoesRead(read):
    try:
        # Convert the string 'read' to a boolean
        read_bool = read.lower() == 'true'

        # Get notificações de user não vistas ou vistas
        idUser = request.args.get('username')
        result = Notificacoes.getNotificacaoRead(idUser, read_bool)
        return jsonify(result)
    except Exception as e:
        # Custom error handler for this route
        return jsonify({'message':'Dados incorretos'}), 404
    
@app.route('/notificacoes/<int:idNotificacao>', methods=['GET'])
def notificacoesTitulo(idNotificacao):
    try:
        # Get notificação de user apartir do ID
        idUser = request.args.get('username')
        result = Notificacoes.getNotificacao(idUser, idNotificacao)
        Notificacoes.readNotificacao(idNotificacao)
        return jsonify(result)
    except Exception as e:
        # Custom error handler for this route
        return jsonify({'message':'Dados incorretos'}), 404


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
