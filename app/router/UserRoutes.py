from flask import Blueprint, request
# from app.core import limiter
# from app.config import DevelopmentConfig
from app.services.User import UserService
# from app.common.Constants import Constants
from app.utils.Middleware import check_token

user_router = Blueprint('user_router', __name__)
# limiter.limit("1000/day")(user_router)

@user_router.route('/signup', methods=['POST'])
def user_signup():
    email = request.form.get("email")
    name = request.form.get("name")
    print(email, name)
    try:
        UserService.create_user(email, name)
        return {"status" : "Success"}, 200
    except Exception as e:
        return {"status" : "Failure", "message": "error"}, 500

@user_router.route('/login', methods=['POST'])
def user_login():
    email = request.form.get("email")
    password = request.form.get("password")
    uuid = request.form.get("uuid")
    try:
        custom_token = UserService.authenticate_user(email, password, uuid)
        return {"status" : "Success", "id_token": custom_token.decode()}, 200
    except Exception as e:
        return {"status" : "Failure", "message": "error"}, 500
    
@user_router.route('/info', methods=['POST'])
@check_token
def user_info():
    user_id = request.user["user_id"]
    try:
        user_info = UserService.get_user_info(user_id)
        return {"status" : "Success", "info": user_info}, 200
    except Exception as e:
        return {"status" : "Failure", "message": "error"}, 500
    
@user_router.route('/rename', methods=['POST'])
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

