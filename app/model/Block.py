from dotenv import load_dotenv
from datetime import datetime
from app.config import DevelopmentConfig

load_dotenv()

users_collection_ref = DevelopmentConfig.FIRESTORE_CLIENT.collection(u'users')

class Block:

    """User data structure:

    name: str,
    email: str,
    datecreated: str,
    uuid: str,
    organizations: {},

    Works with Python versions 3.9.
    """

    __id: str =  None
    __user_id: str =  None
    __blocks_collection_ref: str = None

    def __init__(self, id, user_id):
        self.__id = id
        self.__user_id = user_id
        self.__blocks_collection_ref = DevelopmentConfig.FIRESTORE_CLIENT.collection(u'users').document(self.__user_id).collection(u'blockcoding')

    def get_id(self) -> str:
        return self.__id
    
    def create_project(self, file_name):
        check_existing: dict[str,str] = self.__blocks_collection_ref.where("file_name", '==', file_name).get()
        if(len(check_existing))>0:
            message = "Project with this Name already exists. Please try different name."
            raise Exception(message)
        else:
            project_data = {
                "datecreated": datetime.today().strftime('%Y-%m-%d'),
                "file_name": file_name,
            }
            self.__blocks_collection_ref.document(self.__id).set(project_data)

    def submit_project(self, block_code, block_code_xml, file_name):
        # check_existing: dict[str,str] = self.__blocks_collection_ref.document(self.__id).get().to_dict()
        project_data = {
            "block_code": block_code,
            "block_code_xml": block_code_xml,
            "datecreated": datetime.today().strftime('%Y-%m-%d'),
            "file_name": file_name,
        }
        self.__blocks_collection_ref.document(self.__id).update(project_data)
        # if check_existing is None:
        #     project_data = {
        #         "source_code": source_code,
        #         "language": language_id,
        #         "datecreated": datetime.today().strftime('%Y-%m-%d'),
        #         "stdin": stdin,
        #         "result": result,
        #         "error": errors,
        #         "file_name": file_name,
        #     }
        #     self.__blocks_collection_ref.document(self.__id).set(project_data)
        # else:
        #     message = "Organization with this Id already exists. Please Try Again."
            # raise Exception(message)
        
    def update_project(self, source_code, language_id, stdin, result, errors):
        project_data = {
            "source_code": source_code,
            "language": language_id,
            "datecreated": datetime.today().strftime('%Y-%m-%d'),
            "stdin": stdin,
            "result": result,
            "error": errors
        }
        self.__blocks_collection_ref.document(self.__id).update(project_data)

    def get_all_projects(self):
        projects = self.__blocks_collection_ref.get()
        projects = [{"id": project.id, "file_name": project.to_dict()["file_name"]} for project in projects]
        return projects
    
    def get_project_info(self):
        project_dict = self.__blocks_collection_ref.document(self.__id).get().to_dict()
        if project_dict is None: project_dict = {}
        return project_dict