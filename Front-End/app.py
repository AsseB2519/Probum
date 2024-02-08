from datetime import datetime, timedelta
from flask import Flask, request, jsonify, render_template, redirect
import requests
import jwt
from functools import wraps


########################################    GLOBAL  VARS    ########################################

app = Flask(__name__)

# Secret key for JWT (replace with your secret key)
SECRET_KEY = "N44hg083HrB8h1"

# Global variables for the API gateway IP and port
GATEWAY_IP = "localhost"
GATEWAY_PORT = 5001 

# API Gateway URL
GATEWAY_URL = f'http://{GATEWAY_IP}:{GATEWAY_PORT}'

############################################## ROUTES ##############################################

# Decorator to require authentication
def requires_auth(user_type):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            token = request.args.get('token')
            if not token:
                return redirect('/user/login')  # Adjust the route accordingly

            try:
                # Decode the token
                decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
                
                # Check user type from the token
                if decoded_token.get('user_type') not in user_type:
                    return render_template('error.html', current_user={'token':token}, error_message='Unauthorized')

                # Attach the decoded token to the request object for later use
                request.current_user = decoded_token
                request.current_user['token'] = token
            except jwt.ExpiredSignatureError:
                return render_template('error.html', current_user='', error_message='Token expired')
            except jwt.InvalidTokenError:
                return render_template('error.html', current_user='', error_message='Invalid token')

            return func(*args, **kwargs)

        return wrapper
    return decorator

###### ROUTE: LOGIN ######

@app.route('/user/login', methods=['GET','POST'])
def user_login():
    if request.method == 'GET':
        # Render the login form HTML
        return render_template('login_form.html')  # Replace with your actual HTML template name
    elif request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        user_type = data.get('user_type')  # Assuming user_type is part of the login request
        
        try:
            # Make a request to the API gateway for user authentication
            auth_response = requests.get(f'{GATEWAY_URL}/user/login', params={'username': username, 'password': password, 'user_type': user_type})

            if auth_response.status_code == 200:
                # Successful login, generate JWT token with user type
                token = jwt.encode({'username': username, 'user_type': user_type}, SECRET_KEY, algorithm='HS256')
                return jsonify({'token': token}), 200
            else:
                # Invalid credentials or other error
                return jsonify({'message': 'Invalid credentials'}), 401
        except requests.RequestException as e:
            # Handle the exception, e.g., log the error
            print(f"Error: {e}")
            return jsonify({'message': 'Service unavailable'}), 503

###### ROUTE: LOGOUT ######
        
@app.route('/user/logout', methods=['GET'])
@requires_auth(user_type=['aluno','docente','tecnico'])
def logout():
    return redirect('/user/login')

###### ROUTE: INDEX ######

@app.route('/', methods=['GET'])
@requires_auth(user_type=['aluno','docente','tecnico'])
def index():
    current_user = request.current_user
    if current_user['user_type'] == 'aluno':
        return redirect('/aluno?token='+request.args.get('token'))
    elif current_user['user_type'] == 'docente':
        return redirect('/docente?token='+request.args.get('token'))
    elif current_user['user_type'] == 'tecnico':
        return redirect('/tecnico?token='+request.args.get('token'))
    
###### ROUTE: VER / EDITAR PERFIL PROPRIO ######

@app.route('/user/<username>', methods=['GET','PUT','DELETE'])
@requires_auth(user_type=['aluno','docente','tecnico'])
def user_profile(username):
    if request.method == 'GET':
        current_user = request.current_user
        if current_user['user_type'] == 'tecnico':
            response=requests.get(f'{GATEWAY_URL}/user/'+username)

            if response.status_code == 200:
                user=response.json()
            else:
                return render_template('error.html', current_user=current_user, error_message=response.json()['message'])

            return render_template('user.html', current_user=current_user, user={'username':'teste'},allow_delete=True)
        else:
            if current_user['username'] == username:
                # response=requests.get(f'{GATEWAY_URL}/user/'+username)

                # if response.status_code == 200:
                #    user=response.json()
                #else:
                #    return render_template('error.html', current_user=current_user, error_message=response.json()['message'])

                return render_template('user.html', current_user=current_user, user={'username':'abc','email':'email@gmail.com'}, allow_delete=False)
            else:
                return render_template('error.html', current_user=current_user, error_message='Unauthorized')
    elif request.method == 'PUT':
        current_user = request.current_user
        if current_user['username'] == username or current_user['user_type'] == 'tecnico':
            data = request.get_json()
            try:
                response=requests.put(f'{GATEWAY_URL}/user/'+username, json=data)
                return response.json(), response.status_code
            except:
                return {'message': 'Could not edit user'}, 500
        else:
            return {'message': 'Unauthorized'}, 401
    elif request.method == 'DELETE':
        current_user = request.current_user
        if current_user['user_type'] == 'tecnico':
            try:
                response=requests.delete(f'{GATEWAY_URL}/user/'+username)
                return response.json(), response.status_code
            except:
                return {'message': 'Could not delete user'}, 500
        else:
            return {'message': 'Unauthorized'}, 401
    

###### ROUTE: INDEX ALUNO ######

@app.route('/aluno', methods=['GET'])
@requires_auth(user_type=['aluno'])
def aluno_index():
    current_user = request.current_user
    todo=requests.get(f'{GATEWAY_URL}/prova/aluno',params={'username': current_user['username']}).json()
    done=requests.get(f'{GATEWAY_URL}/resolucao',params={'username': current_user['username']}).json()
    notifications=requests.get(f'{GATEWAY_URL}/notificacoes',params={'username': current_user['username']}).json()
    print(todo)
    return render_template('aluno.html', current_user=current_user, to_do=todo, done=done, notifications=notifications)

###### ROUTE: INFO DA PROVA ######

# TODO : VISAO DA PROVA POR PARTE DO DOCENTE

@app.route('/prova/<id>/<idversao>', methods=['GET'])
@requires_auth(user_type=['aluno'])
def prova(id,idversao):
    current_user = request.current_user
    response=requests.get(f'{GATEWAY_URL}/prova/'+id+'/'+idversao, params={'username': current_user['username']})
    
    if response.status_code == 200:
        prova=response.json()
    else:
        return render_template('error.html', current_user=current_user, error_message=response.json()['message'])

    # prova['date'] follows the format DD-MM-YYYY and prova['start-time']/prova['finish-time'] follows the format HH:MM
    # if prova['date'] is today and prova['start-time'] is in the present/past and prova['finish-time'] is in the future and prova['done'] is False, then prova is available
    available = False
    date_time = datetime.strptime(prova['data'], '%a, %d %b %Y %H:%M:%S %Z')
    
    # Calculate admission start and finish times
    admission_start_time = date_time 
    admission_finish_time = date_time + timedelta(minutes=prova['tempo_admissao'])
    
    # Current datetime
    current_datetime = datetime.now()
    
    available = False
    
    if date_time.date() == current_datetime.date():
        if admission_start_time <= current_datetime <= admission_finish_time and not prova['done']:
            available = True
    print(prova)
    return render_template('prova_aluno.html', current_user=current_user, prova=prova, available=available)

###### ROUTE: REALIZAR E SUBMETER PROVA ######

# TODO
# NOTA: O aluno faz um pedido get para confirmar que quer realizar a prova e e redirecionado para a rota /realizar/<id>/questao/<id_questao>
#           redirecionar para a primeira questao
#       O aluno faz um pedido post para submeter a prova e e redirecionado para a rota /prova/<id>
#           redirecionar para a pagina da prova
@app.route('/realizar/<id_prova>/<id_versao>', methods=['GET','POST'])
@requires_auth(user_type=['aluno'])
def realizar_prova(id_prova,id_versao):
    current_user = request.current_user
    if request.method == 'GET':
        response = requests.get(f'{GATEWAY_URL}/realizar/{id_prova}',params={'username': current_user['username']})
        if response.status_code == 200:
            return redirect(f'''{id_versao}/questao/{response.json()['questao']}?token='''+request.args.get('token'))
        else:
            return render_template('error.html', current_user=current_user, error_message=response.json()['message'])
    elif request.method == 'POST':  
        #response = requests.post(f'{GATEWAY_URL}/realizar/{id_prova}', params={'username': current_user['username']}, json=request.get_json())
        redirect(f'''/prova/{id_prova}''')
        #if response.status_code == 200:
        #else:
        #    return render_template('error.html', current_user=current_user, error_message=response.json()['message'])
    return render_template('prova_aluno.html', current_user=current_user)
   
###### ROUTE: REALIZAR QUESTAO ######

# TODO
# NOTA: O aluno faz um pedido get para obter a questao 
#       O aluno faz um pedido post para submeter a questao e guardar a resposta
#       O aluno faz um pedido put para atualizar a resposta
@app.route('/realizar/<id_prova>/<id_versao>/questao/<id_questao>', methods=['GET','POST','PUT'])
@requires_auth(user_type=['aluno'])
def realizar_questao(id_prova,id_versao,id_questao):
    current_user = request.current_user
    if request.method == 'GET':
        print(f'{GATEWAY_URL}/realizar/{id_prova}/{id_versao}/questao/{id_questao}')
        response = requests.get(f'{GATEWAY_URL}/realizar/{id_prova}/{id_versao}/questao/{id_questao}',params={'username': current_user['username']})
        if response.status_code == 200:
            data = response.json()
            print(response.json())
            # 0 -> escolha multipla
            # 1 -> verdadeiro / falso
            # 2 -> desenvolvimento
            question_type=0
            question={}
            ids = []
            choices=[]
            for k,v in data.items():
                for val in v:
                    if int(val['id'])==int(id_questao):
                        question=val
                        if k in ['Desen', 'Esp']:
                            question_type=2
                        else:
                            choices=map(lambda x:x[1], val['alineas'])
                    ids.append(int(val['id']))
            route_no_question=f'/realizar/{id_prova}'
            max_questions=len(data['Desen']) + len(data['EM']) + len(data['Esp']) +len(data['VF'])
            return render_template('realizar_questao.html',ids=ids,question_type=question_type,choices=choices,route_no_question=route_no_question,max_questions=max_questions,question=question['descricao'],i_atual=id_questao,id_version=id_versao, current_user=current_user )
        else:
            return render_template('error.html', current_user=current_user, error_message=response.json()['message'])
    elif request.method == 'PUT':
        data = request.get_json()
        response = requests.put(f'{GATEWAY_URL}/realizar/{id_prova}/{id_versao}/questao/{id_questao}',params=data)
        if response.status_code == 200:
            return redirect(f'/realizar/{id_prova}/{id_versao}/questao/{id_questao}') 
        else:
            return render_template('error.html', current_user=current_user, error_message=response.json()['message'])
    elif request.method == 'POST':
        data = {}
        data['resposta'] = request.args.get('resposta')
        data['username']=current_user['username']
        print(data)
        response = requests.post(f'{GATEWAY_URL}/realizar/{id_prova}/{id_versao}/questao/{id_questao}',params=data)
        print(response)
        return response



###### ROUTE: VER RESOLUCAO ######

# TODO : VISAO DA RESOLUCAO POR PARTE DO DOCENTE

@app.route('/resolucao/<id>', methods=['GET'])
@requires_auth(user_type=['aluno'])
def resolucao(id):
    current_user = request.current_user
    response=requests.get(f'{GATEWAY_URL}/resolucao/'+id, params={'username': current_user['username']})
    
    if response.status_code == 200:
        resolucao=response.json()
    else:
        return render_template('error.html', current_user=current_user, error_message=response.json()['message'])

    return render_template('resolucao_aluno.html', current_user=current_user, resolucao=resolucao)

###### ROUTE: NOTIFICACOES ######

@app.route('/notificacoes', methods=['GET'])
@requires_auth(user_type=['aluno'])
def aluno_notifications():
    current_user = request.current_user
    notifications=requests.get(f'{GATEWAY_URL}/notificacoes',params={'username': current_user['username']}).json()
    return render_template('notificacoes.html', current_user=current_user, notifications=notifications)

###### ROUTE: ROTA PARA VER PROVAS POR RESOLVER A QUE O USER TEM ACESSO ######

@app.route('/prova', methods=['GET'])
@requires_auth(user_type=['aluno','docente'])
def aluno_provas():
    current_user = request.current_user
    provas=requests.get(f'{GATEWAY_URL}/prova/aluno',params={'username': current_user['username']}).json()
    print(provas)
    return render_template('user_provas.html', current_user=current_user, provas=provas)

###### ROUTE: ROTA PARA VER PROVAS RESOLVIDAS A QUE O USER TEM ACESSO ######

@app.route('/resolucao', methods=['GET'])
@requires_auth(user_type=['aluno','docente'])
def aluno_resolucoes():
    current_user = request.current_user
    username = current_user['username']
    provas=requests.get(f'{GATEWAY_URL}/corrigidos/{username}').json()
    # Falta o prova.link
    return render_template('user_correcoes.html', current_user=current_user, provas=provas)

###### ROUTE: INDEX DOCENTE ######

@app.route('/docente', methods=['GET'])
@requires_auth(user_type=['docente'])
def docente_index():
    current_user = request.current_user
    provas=requests.get(f'{GATEWAY_URL}/prova/docente',params={'username': current_user['username']}).json()
    por_corrigir=requests.get(f'{GATEWAY_URL}/resolucao',params={'username': current_user['username']}).json()
    return render_template('docente.html', current_user=current_user, available=provas, waiting=por_corrigir)

###### ROUTE: CRIAR PROVA ######

@app.route('/prova/criar', methods=['GET','POST'])
@requires_auth(user_type=['docente'])
def criar_prova():
    current_user = request.current_user
    if request.method == 'GET':
        return render_template('criar_prova.html', current_user=current_user)
    elif request.method == 'POST':
        data = request.get_json()
        (dados,code) = request.post(f'{GATEWAY_URL}/prova',params=data)
        if code == 200:
            return redirect(f'/prova/{dados["id"]}') 
        else:
            return render_template('error.html', current_user=current_user, error_message=dados['message'])
    

###### ROUTE: VER/EDITAR/APAGAR PROVA ######

#################################################### NAO SEI QUAIS TEMPLATES USAR METE SFF

@app.route('/prova/<id_prova>/versao/<id_versao>', methods=['GET','PUT','DELETE'])
@requires_auth(user_type=['docente'])
def info_prova(id_prova,id_versao):
    current_user = request.current_user
    if request.method == 'GET':
        (dados,code) = requests.get(f'{GATEWAY_URL}/prova/{id_prova}/{id_versao}',params={})
        print(dados)
        if code == 200:
            return render_template('view_prova.html', current_user=current_user, exam_data=dados)
        else:
            return render_template('error.html', current_user=current_user, error_message=dados['message'])
    elif request.method == 'PUT':
        data = request.get_json()
        (dados,code) = request.put(f'{GATEWAY_URL}/prova/{id_prova}',params=data)
        if code == 200:
            return redirect(f'/prova/{id_prova}')
        else:
            return render_template('error.html', current_user=current_user, error_message=dados['message']) 
    elif request.method == 'DELETE':
        (dados,code) = request.delete(f'{GATEWAY_URL}/prova/{id_prova}',params={})
        if code == 200:
            return redirect('/prova')
        else:
            return render_template('error.html', current_user=current_user, error_message=dados['message'])
        
###### ROUTE: VER/EDITAR/APAGAR QUESTAO ###### 

@app.route('/prova/<id_prova>/<id_questao>', methods=['GET','PUT','DELETE'])
@requires_auth(user_type=['docente'])
def info_questoes(id_prova,id_questao):
    current_user = request.current_user
    if request.method == 'GET':
        (dados,code) = request.get(f'{GATEWAY_URL}/prova/{id_prova}/questao/{id_questao}',params={})
        if code == 200:
            return render_template('view_questao.html', current_user=current_user, question_data=dados)
        else:
            return render_template('error.html', current_user=current_user, error_message=dados['message'])
    elif request.method == 'PUT':
        data = request.get_json()
        (dados,code) = request.put(f'{GATEWAY_URL}/prova/{id_prova}/questao/{id_questao}',params=data)
        if code == 200:
            return redirect(f'/prova/{id_prova}/questao/{id_questao}')
        else:
            return render_template('error.html', current_user=current_user, error_message=dados['message'])
    elif request.method == 'DELETE':
        (dados,code) = request.delete(f'{GATEWAY_URL}/prova/{id_prova}/questao/{id_questao}',params={})
        if code == 200:
            return 200
        else:
            return render_template('error.html', current_user=current_user, error_message=dados['message'])
        
###### ROUTE: VER PROVA POR CORRIGIR ######

@app.route('/resolucao/<id_prova>', methods=['GET'])
@requires_auth(user_type=['docente'])
def resolucao_prova(id_prova):
    current_user = request.current_user

    # Deve obter uma prova com as respostas dos alunos por corrigir
    response=requests.get(f'{GATEWAY_URL}/resolucao/'+id_prova, params={'username': current_user['username']})
    
    if response.status_code == 200:
        resolucao=response.json()
    else:
        return render_template('error.html', current_user=current_user, error_message=response.json()['message'])

    return render_template('resolucao_docente.html', current_user=current_user, exam_data=resolucao)

###### ROUTE: CORRIGIR PROVA AUTOMATICAMENTE ######

# NOTA: body do pedido tem que ter os parâmetros:
#           - idProva

@app.route('/resolucao/<idprova>/auto', methods=['GET','PUT'])
@requires_auth(user_type=['docente'])
def corrige_automaticamente(idprova):
    current_user = request.current_user
    if request.method == 'GET':
        
        # Deve obter uma prova com a sugestao de correcao automatica
        response=requests.get(f'{GATEWAY_URL}/resolucao/<idprova>/auto', params={'username': current_user['username']})
        if response.status_code == 200:
            return render_template('correcao_auto.html', current_user=current_user, exam_data=response.json())
        else:
            return render_template('error.html', current_user=current_user, error_message=response.json()['message'])
    elif request.method == 'PUT':
        data = request.get_json()

        # Deve postar a correcao de uma prova
        response=requests.put(f'{GATEWAY_URL}/resolucao/<idprova>/auto', params=data)
        if response.status_code == 200:
            return redirect(f'''/resolucao/{idprova}''')
        else:
            return render_template('error.html', current_user=current_user, error_message=response.json()['message'])


###### ROUTE: CORRIGIR PROVA MANUALMENTE ######

# NOTA: body do pedido tem que ter os parâmetros (com estes nomes):
#           - idProva
#           - idQuestao
#           - idAluno
#           - classificacao
@app.route('/resolucao/<idprova>/manual', methods=['PUT'])
@requires_auth(user_type=['docente'])
def corrige_manualmente(idprova):
    current_user = request.current_user

    # Deve postar a correcao de uma prova
    response=requests.put(f'{GATEWAY_URL}/resolucao/<idprova>/manual', params=request.get_json())
    if response.status_code == 200:
        return redirect(f'''/resolucao/{idprova}''')
    else:
        return render_template('error.html', current_user=current_user, error_message=response.json()['message'])

###### ROUTE: PUBLICA AS CLASSIFICACOES DE UMA PROVA MANUALMENTE ######

@app.route('/resolucao/publica/<idprova>', methods=['POST'])
@requires_auth(user_type=['docente'])
def publica_notas(idprova):
    current_user = request.current_user
    response=requests.post(f'{GATEWAY_URL}/resolucao/publica'+idprova, params={'username': current_user['username']})
    if response.status_code == 200:
        return redirect(f'''/resolucao/{idprova}''')
    else:
        return render_template('error.html', current_user=current_user, error_message=response.json()['message'])

###### ROUTE: INDEX TECNICO ######

@app.route('/tecnico', methods=['GET'])
@requires_auth(user_type=['tecnico'])
def tecnico_index():
    current_user = request.current_user
    return jsonify({'message': f'Hello, {current_user["username"]}! This is a protected user route.'})

###### ROUTE: CRIAR ALUNO ######

# TODO

###### ROUTE: CRIAR DOCENTE ######

# TODO

###### ROUTE: VER E PROCURAR UTILIZADORES  ######

# TODO

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
