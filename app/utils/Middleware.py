from functools import wraps
from flask import request
import pandas as pd
import firebase_admin
from app.config import DevelopmentConfig

def check_token(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        bearer_token = request.headers.get('Authorization')
        if not bearer_token:
            return {'status': "Failure", 'message': 'AUTHORIZATION_HEADER_MISSING: No Authorization token provided'},401
        bearer_token = bearer_token.strip().split(' ')
        if len(bearer_token) > 0 and bearer_token[0].lower() != "bearer":
            return {'status': "Failure", 'message': 'INVALID_HEADER: Authorization header must start with `Bearer`'},401
        elif len(bearer_token) <= 1:
            return {'status': "Failure", 'message': 'INVALID_HEADER: Authorization Token not found'},401
        elif len(bearer_token) > 2:
            return {'status': "Failure", 'message': 'INVALID_HEADER: Authorization header must be `Bearer Token'},401
        token = bearer_token[1]
        try:
            user = DevelopmentConfig.AUTH.verify_id_token(token, app=firebase_admin.get_app(), check_revoked=True)
            request.user = user
        except:
            return {'message':'INVALID_TOKEN: Invalid token provided.'},401
        return f(*args, **kwargs)
    return wrap

def check_organization_admin(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        user_id = request.user["user_id"]
        if user_id is not None:
            try:
                user_info = DevelopmentConfig.FIRESTORE_CLIENT.collection(u'users').document(user_id).get().to_dict()
                if user_info is None: user_info = {}
                if user_info.get("isAdmin") == None:
                    return {'status': "Failure", 'message': 'PERMISSION_DENIED: Organization Owner/Admin level access required for this operation.'},403
            except Exception as e:
                return {'status': "Failure", 'message': f"{e}"},500
        else:
            return {'status': "Failure", 'message': 'INVALID_DATA: Invalid data recieved.'},400
        return f(*args, **kwargs)
    return wrap