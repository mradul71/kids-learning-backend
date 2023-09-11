from flask import Blueprint, request
from app.services.Admin import AdminService
from app.utils.Middleware import check_token, check_organization_admin

admin_router = Blueprint('admin_router', __name__)
querystring = {"base64_encoded":"true","fields":"*"}

@admin_router.route('/verified-users', methods=['GET'])
@check_token
@check_organization_admin
def get_verified_users():
    try:
        users = AdminService.get_verified_users()
        return {"status" : "Success", "users": users}, 200
    except Exception as e:
        return {"status" : "Failure", "message": str(e)}, 500
    
@admin_router.route('/unverified-users', methods=['GET'])
@check_token
@check_organization_admin
def get_unverified_users():
    try:
        users = AdminService.get_unverified_users()
        return {"status" : "Success", "users": users}, 200
    except Exception as e:
        return {"status" : "Failure", "message": str(e)}, 500
    
@admin_router.route('/verify-user', methods=['POST'])
@check_token
@check_organization_admin
def verify_user():
    try:
        verify_user_email = request.form.get("email")
        verification_link = AdminService.verify_user(verify_user_email)
        return {"status" : "Success", "verification_link": verification_link}, 200
    except Exception as e:
        return {"status" : "Failure", "message": str(e)}, 500