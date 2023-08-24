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

# def check_organization_admin(f):
#     @wraps(f)
#     def wrap(*args,**kwargs):
#         user_id = request.user["user_id"]
#         if user_id is not None:
#             try:
#                 user_info = DevelopmentConfig.FIRESTORE_CLIENT.collection(u'users').document(user_id).get().to_dict()
#                 if user_info is None: user_info = {}
#                 if not (check_org_role=="owner" or  check_org_role=="admin"):
#                     return {'status': "Failure", 'message': 'PERMISSION_DENIED: Organization Owner/Admin level access required for this operation.'},403
#                 else:
#                     request.organizationownership = check_org_role
#                     active_sub, sub_error = check_subscription(org_info)
#                     request.activesubscription = active_sub
#                     request.subscriptionerror = sub_error
#                     request.subscriptiontype = org_info.get("currentsubscription", {}).get("type", "freetrial")
#                     db_info = DevelopmentConfig.FIRESTORE_CLIENT.collection(u'databases').document(org_info.get("db",organization_id)).get().to_dict()
#                     if db_info is None: 
#                         raise Exception("DB_NOT_FOUND: Database info not found. Contact Support.")
#                     db_writer = db_info.get("writer")
#                     db_reader = db_info.get("reader")
#                     db_user = db_info.get("user")
#                     db_password = db_info.get("password")
#                     if db_writer and db_reader and db_user and db_password:
#                         def get_mysql_connection_writer(db_name=None):
#                             db_connection = mysql.connector.connect(
#                                 host = db_writer,
#                                 port = 3306,
#                                 user = decrypt(db_user),
#                                 password = decrypt(db_password),
#                                 database = db_name,
#                                 allow_local_infile=True
#                             )
#                             return db_connection
#                         def get_mysql_connection_reader(db_name=None):
#                             db_connection = mysql.connector.connect(
#                                 host = db_reader,
#                                 port = 3306,
#                                 user = decrypt(db_user),
#                                 password = decrypt(db_password),
#                                 database = db_name,
#                                 allow_local_infile=True
#                             )
#                             return db_connection
#                         g.get_mysql_connection_writer = get_mysql_connection_writer
#                         g.get_mysql_connection_reader = get_mysql_connection_reader
#                         g.dbpresent = True
#                     else:
#                         g.dbpresent = False
#             except Exception as e:
#                 return {'status': "Failure", 'message': f"{e}"},500
#         else:
#             return {'status': "Failure", 'message': 'INVALID_DATA: Invalid data recieved.'},400
#         return f(*args, **kwargs)
#     return wrap