from flask import Blueprint, request
from app.services.Python import PythonService
from app.utils.Middleware import check_token

admin_router = Blueprint('admin_router', __name__)

@admin_router.route('/submit', methods=['POST'])
def user_signup():
    email = request.form.get("email")
    name = request.form.get("name")
    print(email, name)
    try:
        PythonService.create_user(email, name)
        return {"status" : "Success"}, 200
    except Exception as e:
        return {"status" : "Failure", "message": "error"}, 500

@admin_router.route('/login', methods=['POST'])
def user_login():
    email = request.form.get("email")
    password = request.form.get("password")
    uuid = request.form.get("uuid")
    try:
        custom_token = PythonService.authenticate_user(email, password, uuid)
        return {"status" : "Success", "id_token": custom_token.decode()}, 200
    except Exception as e:
        return {"status" : "Failure", "message": "error"}, 500
    
@admin_router.route('/info', methods=['POST'])
@check_token
def user_info():
    user_id = request.user["user_id"]
    try:
        user_info = PythonService.get_user_info(user_id)
        return {"status" : "Success", "info": user_info}, 200
    except Exception as e:
        return {"status" : "Failure", "message": "error"}, 500
    
@admin_router.route('/rename', methods=['POST'])
@check_token
def rename():
    new_name = request.form.get("name")
    user_id = request.user["user_id"]
    try:
        PythonService.rename(user_id, new_name)
        user_info, user_organizations = PythonService.get_user_info(user_id)
        return {"status" : "Success", "info": user_info, "organizations": user_organizations}, 200
    except Exception as e:
        return {"status" : "Failure", "message": f"{e}"}, 500

