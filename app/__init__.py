from flask import Flask, request, g
from flask_cors import CORS, cross_origin
from time import strftime, time

# from app.core import limiter
# from app.config import TestingConfig, DevelopmentConfig, ProductionConfig
# from app.errors.handlers import errors
# from app.router.HealthRoutes import health_router
from app.router.UserRoutes import user_router
from app.router.PythonProjectRoutes import python_project_router
from app.router.BlockRoutes import block_project_router
from app.router.AdminRoutes import admin_router
# from app.router.OrganizationRoutes import organization_router
# from app.router.ProjectRoutes import project_router
# from app.router.ModelRoutes import model_router
# from app.router.PaymentRoutes import payment_router

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

cors = CORS(
    app, 
    resources={r'/*': {
        'origins': ["http://localhost:3000","http://localhost"], 
        'methods': ["GET","POST","PUT","DELETE"]
    }}
)
# app.config['CORS_HEADERS'] = 'Content-Type'

# # limiter.init_app(app)

# app.config.from_object(DevelopmentConfig)

# app.register_blueprint(errors)
# app.register_blueprint(health_router)
app.register_blueprint(user_router, url_prefix="/user")
app.register_blueprint(python_project_router, url_prefix="/python-compiler")
app.register_blueprint(block_project_router, url_prefix="/block-coding")
app.register_blueprint(admin_router, url_prefix="/admin")
# app.register_blueprint(organization_router, url_prefix="/organization")
# app.register_blueprint(project_router, url_prefix="/project")
# app.register_blueprint(model_router, url_prefix="/model")
# app.register_blueprint(payment_router, url_prefix="/payment")

@app.before_request
def before_request():
    request.start_time = time()

@app.after_request
def after_request(response):
    timestamp = strftime('[%Y-%m-%d %H:%M:%S]')
    protocol = request.environ.get('SERVER_PROTOCOL')
    duration = (time() - request.start_time)
    print(f'{request.remote_addr} - - {timestamp} "{request.method} {request.path} {protocol}" {response.status_code} {response.content_length} {duration}', flush=True)
    return response

# @app.teardown_request
# def teardown_request(exception=None):
#     mysql_reader = g.pop("mysql_reader", None)
#     if mysql_reader is not None: mysql_reader.close()
