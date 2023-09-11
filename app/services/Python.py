from app.model.Python import Python
from dotenv import load_dotenv
from app.utils.Others import generate_password
from app.config import DevelopmentConfig
from datetime import datetime
from app.utils.Others import generate_random_id
# from app.utils.SendEmail import send_signup_email, send_verification_email, send_password_reset_email, send_invitation_email, send_invitation_acceptance_email, send_invitation_rejection_email
load_dotenv()

users_collection_ref = DevelopmentConfig.FIRESTORE_CLIENT.collection(u'users')
invitations_collection_ref = DevelopmentConfig.FIRESTORE_CLIENT.collection(u'invitations')
class PythonService:

    @staticmethod
    def create_project(user_id, file_name):
        file_id = generate_random_id(25)
        project_obj: Python = Python(file_id, user_id)
        return project_obj.create_project(file_name)

    @staticmethod
    def submit_project(user_id, source_code, language_id, stdin, result, errors, file_name, file_id):
        if source_code and language_id:
            if file_id == "null":
                file_id = generate_random_id(25)
            project_obj: Python = Python(file_id, user_id)
            project_obj.submit_project(source_code, language_id, stdin, result, errors, file_name)
        else:
            raise Exception("An error occurred")
        
    @staticmethod
    def update_project(project_id, user_id, source_code, language_id, stdin, result, errors):
        if project_id and source_code and language_id:
            project_obj: Python = Python(project_id, user_id)
            project_obj.update_project(source_code, language_id, stdin, result, errors)
        else:
            raise Exception("An error occurred")
        
    @staticmethod
    def get_all_projects(user_id):
        if user_id:
            project_obj: Python = Python(None, user_id)
            return project_obj.get_all_projects()
        else:
            raise Exception("An error occurred")
        
    @staticmethod
    def get_project_info(project_id, user_id):
        if user_id:
            project_obj: Python = Python(project_id, user_id)
            return project_obj.get_project_info()
        else:
            raise Exception("An error occurred")
