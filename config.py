import os
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

# # Read secret file
# variables = None
# with open('.secrets', 'r') as f:
#    variables = f.read()

  

class Config(object):
    # DB_NAME = variables.split('\n')[0].split('=')[1]
    # DB_USERNAME = variables.split('\n')[1].split('=')[1]
    # DB_PASSWORD = variables.split('\n')[2].split('=')[1]
    DB_USERNAME='root'
    DB_NAME = 'kesandu_db'
    DB_PASSWORD ='!vfhIyH214js9Rf'

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://' + DB_USERNAME + ':''@localhost/'+ DB_NAME 
    # mysql://username:password@host:port/database_name
    
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://' + DB_USERNAME + ':''@localhost/'+ DB_NAME
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://' + DB_USERNAME + ':' + DB_PASSWORD + '@localhost:3306/'+ DB_NAME
    
        
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['bonsoirval@gmail.com']
    LANGUAGES = ['en', 'es']
    MS_TRANSLATOR_KEY = os.environ.get('MS_TRANSLATOR_KEY')
    POSTS_PER_PAGE = 25
    APP_NAME = 'Kesandu'
    EXPLAIN_TEMPLATE_LOADING = True
