import os
from dotenv import load_dotenv
import string
import firebase_admin
from firebase_admin import credentials,db,auth, firestore
import logging
from datetime import datetime

load_dotenv()
cred = credentials.Certificate(os.environ.get("FIREBASE_CREDENTIAL_FILENAME"))
firebase_admin.initialize_app(cred,{
    'databaseURL':os.environ.get("FIREBASE_DATABASE_URL"),
    'authDomain':os.environ.get("FIREBASE_AUTH_DOMAIN")
})

letters = string.ascii_letters

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
def setup_logger(name, log_file, level=logging.INFO):
    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger

# current_date = datetime.today().strftime('%Y-%m-%d')
# create_folder(f'logs/{current_date}/')
# info_logger = setup_logger('info_logger', f'logs/{current_date}/Info.log')
# error_logger = setup_logger('error_logger', f'logs/{current_date}/Error.log')

class BaseConfig(object):
    """base config"""
    SECRET_KEY = os.environ.get("secret_key", os.environ.get("APP_SECRET"))


# class TestingConfig(BaseConfig):
#     """testing config"""
#     TESTING = True
#     DEBUG = True


class DevelopmentConfig(BaseConfig):
    """dev config"""
    DEBUG = True
    AUTH = auth
    FIREBASE_DATABASE_REF = db.reference('/')
    FIRESTORE_CLIENT = firestore.client()
    STORAGE_REF = ""
    # INFO_LOGGER = info_logger
    # ERROR_LOGGER = error_logger


# class ProductionConfig(BaseConfig):
#     """production config"""
#     DATABASE_URI = ""
