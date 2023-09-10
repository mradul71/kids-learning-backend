from flask import Blueprint, request
from app.services.User import UserService
from app.utils.Middleware import check_token
from firebase_admin import auth

admin_router = Blueprint('admin_router', __name__)

@admin_router.route('/all-users', methods=['GET'])
def all_users():
    try:
        allUsers = []
        page = auth.list_users()
        while page:
            userBatch = []
            for user in page.users:
                userData = UserService.get_user_info(user.uid)
                userBatch.append(userData)
            allUsers.append(userBatch)
            page = page.get_next_page()
        return {"status" : "Success", "all_users": allUsers}, 200
    except Exception as e:
        return {"status" : "Failure", "message": "error"}, 500
    
@admin_router.route('/info', methods=['POST'])
@check_token
def user_info():
    user_id = request.user["user_id"]
    try:
        user_info = UserService.get_user_info(user_id)
        return {"status" : "Success", "info": user_info}, 200
    except Exception as e:
        return {"status" : "Failure", "message": "error"}, 500
    
@admin_router.route('/rename', methods=['POST'])
@check_token
def rename():
    new_name = request.form.get("name")
    user_id = request.user["user_id"]
    try:
        UserService.rename(user_id, new_name)
        user_info, user_organizations = UserService.get_user_info(user_id)
        return {"status" : "Success", "info": user_info, "organizations": user_organizations}, 200
    except Exception as e:
        return {"status" : "Failure", "message": f"{e}"}, 500

