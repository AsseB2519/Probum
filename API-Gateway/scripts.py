from tkinter import NO
from flask import jsonify
import requests

def post_dados(target_server_url, data):
    try:
        # Envia os dados para o servidor de destino
        response = requests.post(target_server_url, params=data)

        # Verifica se a criaçao foi bem-sucedida (código de status 200)
        if response.status_code == 200:
            return "Dados enviados com sucesso para o servidor de destino.",response.status_code
        else:
            return f"Falha ao enviar dados. Código de status: {response.status_code}",response.status_code

    except Exception as e:
        return f"Erro ao enviar dados para o microserviço: {str(e)}",500


def post_dados_2(target_server_url, data):
    try:
        # Envia os dados para o servidor de destino
        response = requests.post(target_server_url, json=data)

        # Verifica se a criaçao foi bem-sucedida (código de status 200)
        if response.status_code == 200:
            return "Dados enviados com sucesso para o servidor de destino.",response.status_code
        else:
            return f"Falha ao enviar dados. Código de status: {response.status_code}",response.status_code

    except Exception as e:
        return f"Erro ao enviar dados para o microserviço: {str(e)}",500
    
def get_dados(target_server_url,data=None):
    try:
        # Envia os dados para o servidor de destino
        response = requests.get(target_server_url,params=data)

        # Verifica se a criaçao foi bem-sucedida (código de status 200)
        if response.status_code == 200:
            return response.json(),200
        else:
            return f"Falha na requisiçao dados. Código de status: {response.status_code}",response.status_code

    except Exception as e:
        return f"Erro ao pedir dados do microserviço: {str(e)}",500
    
def delete_dados(target_server_url):
    # URL para a qual você deseja fazer a requisição DELETE

    try:
        # Faz a requisição DELETE para o URL alvo
        response = requests.delete(target_server_url)

        # Verifica se a requisição foi bem-sucedida (código de status 200)
        if response.status_code == 200:
            return "Dados excluídos com sucesso.",200
        else:
            return f"Falha no delete. Código de status: {response.status_code}",response.status_code

    except Exception as e:
        return f"Erro ao eliminar dados no microserviço: {str(e)}",500
    
def put_dados(target_server_url,data):
    try:
        # Faz a requisição PUT para o URL alvo
        response = requests.put(target_server_url,params=data)

        # Verifica se a requisição foi bem-sucedida (código de status 200)
        if response.status_code == 200:
            return "Dados atualizados com sucesso.",200
        else:
            return f"Falha na atualizaçao. Código de status: {response.status_code}",response.status_code

    except Exception as e:
        return f"Erro ao atualizar dados no microserviço: {str(e)}",500