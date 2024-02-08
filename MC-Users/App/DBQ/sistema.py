from DBQ import contactDB
import requests
import json

class User:
    def __init__(self, nome, num, email, password):
        self.nome = nome
        self.num = num
        self.email = email
        self.password = password
        self.user_type = self.determine_user_type()
        
    def determine_user_type(self):
        if self.num.startswith("pg"):
            return "aluno"
        elif self.num.startswith("di"):
            return "docente"
        else:
            return "indefinido"




class Sistema:

    
    def __init__(self, notifications_microservice_url):
        self.notifications_microservice_url = notifications_microservice_url
        self.students_list = []

    def registaAluno(self, nome, num, email):
        aluno = User(nome, num, email, "")
        if aluno.user_type == "aluno":
            contactDB.registaAluno(aluno)

    def registaDocente(self, nome, num, email):
        docente = User(nome, num, email, "")
        if docente.user_type == "docente":
            contactDB.registaDocente(docente)

    def validate_credentials(self, userID, password):
        result = contactDB.validate_credentials(userID, password)
        return bool(result)

    def getPerfil(self, userID, user_type):
        result = contactDB.get_user_profile(userID, user_type)
        if result:
            user_data = result[0]
            return {"numero":user_data[0], "nome": user_data[1], "email": user_data[2]}
        else:
            return None

    def updatePass(self, userID, newPassword):
        clauses = [('1', userID)]
        new_elements = {'password': newPassword}
        contactDB.update_fun('users', clauses, new_elements)

    def updateEmail(self, userID, newEmail):
        clauses = [('1', userID)]
        new_elements = {'email': newEmail}
        contactDB.update_fun('users', clauses, new_elements)
    
    
    
    def publicaClassificacoes(self, alunos):
        # Get the list of emails from the database for the given list of students (alunos)
        student_emails = self.getStudentsEmailsFromDatabase(alunos)
        
        # Relay the list of emails to the notifications microservice
        self.relayToNotificationsMicroservice(student_emails)

    
    def getStudentsEmailsFromDatabase(self, alunos):
        email_list = []
        for aluno in alunos:
            clauses = [('1', aluno.num)]
            result = contactDB.select_fun('users', clauses)
            email_list.extend([user_data[2] for user_data in result] if result else [])
        return email_list

    def relayToNotificationsMicroservice(self, student_emails):
        try:
            # Send an HTTP POST request to the notifications microservice
            response = requests.post(self.notifications_microservice_url, json={"emails": student_emails})
            # Check if the response indicates success (2xx status code)
            response.raise_for_status()
            # Print the response from the notifications microservice
            print("Notification microservice response:", response.text)
            # Return the response object to the caller
            return response
    
        except requests.exceptions.RequestException as e:
            # Handle exceptions that may occur during the request (e.g., network issues)
            print(f"Error connecting to the notifications microservice: {e}")
            # Return None in case of an error
            return None
        
