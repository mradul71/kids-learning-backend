from app.model.Block import Block
from app.model.Block import Block
from dotenv import load_dotenv
from app.utils.Others import generate_password
from app.config import DevelopmentConfig
from datetime import datetime
from app.utils.Others import generate_random_id

load_dotenv()

users_collection_ref = DevelopmentConfig.FIRESTORE_CLIENT.collection(u'users')
invitations_collection_ref = DevelopmentConfig.FIRESTORE_CLIENT.collection(u'invitations')
class BlockService:

    @staticmethod
    def create_project(user_id, file_name):
        file_id = generate_random_id(25)
        project_obj: Block = Block(file_id, user_id)
        project_obj.create_project(file_name)

    @staticmethod
    def submit_project(user_id, block_code, block_code_xml, file_name, file_id):
        if block_code:
            if file_id == "null":
                file_id = generate_random_id(25)
            project_obj: Block = Block(file_id, user_id)
            project_obj.submit_project(block_code, block_code_xml, file_name)
        else:
            raise Exception("An error occurred")
        
    @staticmethod
    def update_project(project_id, user_id, source_code, language_id, stdin, result, errors):
        if project_id and source_code and language_id:
            project_obj: Block = Block(project_id, user_id)
            project_obj.update_project(source_code, language_id, stdin, result, errors)
        else:
            raise Exception("An error occurred")
        
    @staticmethod
    def get_all_projects(user_id):
        if user_id:
            project_obj: Block = Block(None, user_id)
            return project_obj.get_all_projects()
        else:
            raise Exception("An error occurred")
        
    @staticmethod
    def get_project_info(project_id, user_id):
        if user_id:
            project_obj: Block = Block(project_id, user_id)
            return project_obj.get_project_info()
        else:
            raise Exception("An error occurred")
