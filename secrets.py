import os
from dotenv import load_dotenv

class Secrets:

    if os.environ.get('ENV') == 'production':
        dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    else:
        dotenv_path = os.path.join(os.path.dirname(__file__), '.env.dev')
    load_dotenv(dotenv_path)
    
    PATH_JSON = os.environ.get('PATH_JSON')

    DB_HOST = os.environ.get('DB_HOST')
    DB_NAME = os.environ.get('DB_NAME')
    DB_USER = os.environ.get('DB_USER')
    DB_PASS = os.environ.get('DB_PASS')