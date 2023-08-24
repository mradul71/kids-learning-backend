from dotenv import load_dotenv
from datetime import datetime
import json
import requests
import os
from app.config import DevelopmentConfig
import firebase_admin

load_dotenv()

users_collection_ref = DevelopmentConfig.FIRESTORE_CLIENT.collection(u'users')

class Python:

    """User data structure:

    name: str,
    email: str,
    datecreated: str,
    uuid: str,
    organizations: {},

    Works with Python versions 3.9.
    """

    __id: str =  None

    def __init__(self, id, user_id):
        self.__id = id
        self.__user_id = user_id
        self.__projects_collection_ref = DevelopmentConfig.FIRESTORE_CLIENT.collection(u'users').document(self.__user_id).collection(u'projects')

    def get_id(self) -> str:
        return self.__id
    
    def create_project(self, source_code, language_id, stdin, result, errors):
        check_existing: dict[str,str] = self.__projects_collection_ref.document(self.__id).get().to_dict()
        if check_existing is None:
            project_data = {
                "source_code": source_code,
                "language": language_id,
                "datecreated": datetime.today().strftime('%Y-%m-%d'),
                "stdin": stdin,
                "result": result,
                "error": errors
            }
            print("data", project_data)
            self.__projects_collection_ref.document(self.__id).set(project_data)
        else:
            message = "Organization with this Id already exists. Please Try Again."
            raise Exception(message)
        
    def create_user_metadata(self, email: str, name: str) -> None:
        check_existing = users_collection_ref.document(self.__id).get().to_dict()
        if check_existing is None:
            user_data: dict[str,str] = {
                "email": email,
                "name": name,
                "datecreated": datetime.today().strftime('%Y-%m-%d')
            }
            users_collection_ref.document(self.__id).set(user_data)
        else:
            raise Exception("Another user with this user id already exists. Please Try Again.")
    
    def get_info(self) -> dict[str,str]:
        user_dict = users_collection_ref.document(self.__id).get().to_dict()
        if user_dict is None: user_dict = {}
        return user_dict
    
    def rename(self, new_name: str) -> None:
        users_collection_ref.document(self.__id).update({"name": new_name})
    
    def check_credentials(self, email, password):
        auth_url: str = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"
        payload: dict[str,str] = json.dumps({
            "email": email,
            "password": password,
            "returnSecureToken": False
        })
        response_data: dict[str,str] = requests.post(auth_url, params={"key": os.environ.get("FIREBASE_API_KEY")}, data=payload)
        response_data = response_data.json()
        if response_data.get("localId"):
            self.__id = response_data["localId"]
        else:
            raise Exception(response_data["error"]["message"])
    
    def get_custom_token(self):
        custom_token: str = DevelopmentConfig.AUTH.create_custom_token(self.__id, {}, app=firebase_admin.get_app())
        return custom_token
    
    def save_uuid(self, uuid: str) -> None:
        users_collection_ref.document(self.__id).update({"uuid": uuid})