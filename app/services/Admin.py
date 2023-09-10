from app.model.User import User
from dotenv import load_dotenv
from app.utils.Others import generate_password
from app.config import DevelopmentConfig
from datetime import datetime

load_dotenv()

users_collection_ref = DevelopmentConfig.FIRESTORE_CLIENT.collection(u'admins')

class UserService:

    @staticmethod
    def create_user(email: str, name: str) -> tuple[str,str]:
        if email and name:
            print("hello")
            password = generate_password()
            user_obj: User = User(None)
            user_obj.create_user(email, name, password)
            user_obj.create_user_metadata(email, name)
            user_id = user_obj.get_id()
            # send_signup_email(email, password)
            return user_id
        else:
            raise Exception("INVALID_DATA: Please provide a valid email and name.")
        
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
        
    @staticmethod
    def authenticate_user(email: str, password: str, uuid: str) -> str:
        user_obj: User = User(None)
        user_obj.check_credentials(email, password)
        user_obj.save_uuid(uuid)
        return user_obj.get_custom_token()
    
    @staticmethod
    def get_user_info(user_id: str) -> tuple[dict[str,str],list[dict[str,str]]]:
        user_object: User = User(user_id)
        user_info: dict[str,str] = user_object.get_info()
        return {"id": user_id, **user_info}
    
    @staticmethod
    def rename(user_id: str, new_name: str) -> None:
        user_object: User = User(user_id)
        user_object.rename(new_name)
