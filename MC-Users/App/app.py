from flask import Flask, request, jsonify
from DBQ.sistema import Sistema

app = Flask(__name__)

sistema_instance = Sistema("http://endereco-do-servico-de-notificacoes")

@app.route('/receive_alunos_list', methods=['POST'])
def receive_students_list():
    try:
        data = request.get_json()
        students_list = data.get('alunos', [])
        
        # Store the received list of students in the Sistema instance
        sistema_instance.students_list = students_list
        sistema_instance.publicaClassificacoes(students_list)

        return jsonify({'message': 'Students list received successfully'}), 200

    except Exception as e:
        print(f"Error processing students list: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

def validate_username_type(type,username):
    if type=='aluno':
        return username[0:2] == 'PG'
    elif type=='docente':
        return username[0] == 'D'
    elif type=='tecnico':
        return username[0] == 'T'

@app.route('/login', methods=['POST'])
def login():
    try:
        user_id = request.args.get('username')
        password = request.args.get('password')
        user_type = request.args.get('user_type')

        # Validate credentials
        if validate_username_type(user_type,user_id) and sistema_instance.validate_credentials(user_id, password):
            return jsonify({'message': 'Login successful'}), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401

    except Exception as e:
        print(f"Error processing login request: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

    
@app.route('/get_user_info', methods=['GET'])
def get_user_info():
    try:
        user_id = request.args.get('user_id')
        user_type = request.args.get('user_type')

        # Get user information from the Sistema instance
        user_info = sistema_instance.getPerfil(user_id, user_type)

        if user_info:
            return jsonify(user_info), 200
        else:
            return jsonify({'error': 'User not found'}), 404

    except Exception as e:
        print(f"Error processing get_user_info request: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500


# Run the Flask app
if __name__ == '__main__':
    app.run(port=5001,host='0.0.0.0')  # Choose a suitable port for your application