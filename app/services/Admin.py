from app.model.User import User
from dotenv import load_dotenv
from app.utils.Others import generate_password
from app.config import DevelopmentConfig
from datetime import datetime
from app.services.Block import BlockService
from app.services.Python import PythonService
from app.utils.SendEmail import send_signup_email, send_password_reset_email
from firebase_admin import auth
load_dotenv()

users_collection_ref = DevelopmentConfig.FIRESTORE_CLIENT.collection(u'users')
class AdminService:

    @staticmethod
    def get_verified_users() -> tuple[dict[str,str],list[dict[str,str]]]:
        docs = users_collection_ref.stream()
        users = []
        for doc in docs:
            temp = doc.to_dict()
            data = auth.get_user(doc.id)
            if data.email_verified==True:
                temp['id'] = doc.id
                temp['pythonprojects'] = len(PythonService.get_all_projects(doc.id))
                temp['blockprojects'] = len(BlockService.get_all_projects(doc.id))
                users.append(temp)
        return users
    
    @staticmethod
    def get_unverified_users() -> tuple[dict[str,str],list[dict[str,str]]]:
        page = auth.list_users()
        users=[]
        while page:
            for user in page.users:
                data = auth.get_user(user.uid)
                if data.email_verified==False:
                    temp={}
                    temp['id'] = user.uid
                    temp['email'] = data.email
                    temp['name'] = data.display_name
                    users.append(temp)
            page = page.get_next_page()
        return users
    
    @staticmethod
    def verify_user(verify_user_email) -> tuple[dict[str,str],list[dict[str,str]]]:
        verification_link: str = DevelopmentConfig.AUTH.generate_email_verification_link(verify_user_email)
        return verification_link
    
    # @staticmethod
    # def get_user_info(user_id: str) -> tuple[dict[str,str],list[dict[str,str]]]:
    #     user_object: User = User(user_id)
    #     user_info: dict[str,str] = user_object.get_info()
    #     return {"id": user_id, **user_info}
    
    # @staticmethod
    # def rename(user_id: str, new_name: str) -> None:
    #     user_object: User = User(user_id)
    #     user_object.rename(new_name)

    # @staticmethod
    # def reset_password(email: str) -> None:
    #     return send_password_reset_email(email)
