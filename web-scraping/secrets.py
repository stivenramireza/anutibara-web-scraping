from dotenv import load_dotenv
import os

if os.environ.get('ENV') == 'production':
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
else:
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env.dev')
load_dotenv(dotenv_path)

DB_HOST = os.environ.get('DB_HOST')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')

MAIN_PAGE_URL_BUY = os.environ.get('MAIN_PAGE_URL_BUY')
MAIN_PAGE_URL_RENT = os.environ.get('MAIN_PAGE_URL_RENT')
MAIN_PAGE_SHORT_URL_BUY = os.environ.get('MAIN_PAGE_SHORT_URL_BUY')
MAIN_PAGE_SHORT_URL_RENT = os.environ.get('MAIN_PAGE_SHORT_URL_RENT')
MAIN_URL = os.environ.get('MAIN_URL')