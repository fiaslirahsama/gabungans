import os
from dotenv import load_dotenv
from os.path import join, dirname, realpath
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists,create_database

load_dotenv()
BASEDIR = os.path.abspath(os.path.dirname(realpath(__file__)))

def validate_database(DATABASE_FILE):
    DB_NAME = os.getenv('DB_NAME')
    engine = create_engine(DATABASE_FILE)
    if not database_exists(engine.url): # Checks for the first time  
        create_database(engine.url)     # Create new DB    
        print(str(DB_NAME)+" Database Created") # Verifies if database is there or not.
    else:
        print("Database "+str(DB_NAME)+" Already Exists")

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DATABASE = os.getenv('DATABASE')
    CSVBUKU = os.getenv('CSVBUKU')
    CSVMEMBER = os.getenv('CSVMEMBER')
    DB_HOST = os.getenv('DB_HOST')
    DB_USERNAME = os.getenv('DB_USERNAME')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_NAME = os.getenv('DB_NAME')
    FOLDER_DATABASE = os.path.join(BASEDIR, DATABASE)
    FOLDER_CSVBUKU = os.path.join(BASEDIR, CSVBUKU)
    FOLDER_CSVMEMBER = os.path.join(BASEDIR, CSVMEMBER)
    # DATABASE_FILE = "sqlite:///{}".format(os.path.join(FOLDER_DATABASE, 'databaseperpustakaan.db'))
    # DATABASE_FILE = 'mysql+pymysql://'+DB_USERNAME+':'+DB_PASSWORD+'@'+DB_HOST+'/'+DB_NAME
    DATABASE_FILE = 'mysql://'+DB_USERNAME+':'+DB_PASSWORD+'@'+DB_HOST+'/'+DB_NAME
    validate_database(DATABASE_FILE)
    SQLALCHEMY_DATABASE_URI = DATABASE_FILE
    CEK_DATABASE = os.path.exists(FOLDER_DATABASE)
    if not CEK_DATABASE:
        os.makedirs(FOLDER_DATABASE)
        print("Folder Database Telah Dibuat.")
        CEK_CSVBUKU = os.path.exists(FOLDER_CSVBUKU)
        if not CEK_CSVBUKU:
            os.makedirs(FOLDER_CSVBUKU)
            print("Folder Upload CSV Buku Telah Dibuat.")
            CEK_CSVMEMBER = os.path.exists(FOLDER_CSVMEMBER)
            if not CEK_CSVMEMBER:
                os.makedirs(FOLDER_CSVMEMBER)
                print("Folder Upload CSV Member Telah Dibuat.")
        else:
            CEK_CSVMEMBER = os.path.exists(FOLDER_CSVMEMBER)
            if not CEK_CSVMEMBER:
                os.makedirs(FOLDER_CSVMEMBER)
                print("Folder Upload CSV Member Telah Dibuat.")
    else:
        CEK_CSVBUKU = os.path.exists(FOLDER_CSVBUKU)
        if not CEK_CSVBUKU:
            os.makedirs(FOLDER_CSVBUKU)
            print("Folder Upload CSV Buku Telah Dibuat.")
            CEK_CSVMEMBER = os.path.exists(FOLDER_CSVMEMBER)
            if not CEK_CSVMEMBER:
                os.makedirs(FOLDER_CSVMEMBER)
                print("Folder Upload CSV Member Telah Dibuat.")
        else:
            CEK_CSVMEMBER = os.path.exists(FOLDER_CSVMEMBER)
            if not CEK_CSVMEMBER:
                os.makedirs(FOLDER_CSVMEMBER)
                print("Folder Upload CSV Member Telah Dibuat.")


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    ENV = os.getenv('FLASK_ENV')
    DEVELOPMENT = True
    SECRET_KEY = os.getenv('SECRET_KEY')
    OAUTHLIB_INSECURE_TRANSPORT = os.getenv('OAUTHLIB_INSECURE_TRANSPORT')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG = os.getenv('DEBUG')


class TestingConfig(Config):
    TESTING = True