from pymongo import MongoClient
import secrets
import json

def connect_to_db():
    try:
        client = MongoClient(f'mongodb+srv://{secrets.DB_USER}:{secrets.DB_PASS}@{secrets.DB_HOST}/{secrets.DB_NAME}')
        print("Database connected successfully")
    except Exception as e:
        print("Error to connect to database: ", e)
    database = client.get_database(secrets.DB_NAME)
    return database
    
def insert_document(db, json_file):
    try:
        properties = db.properties
        properties.insert_one(json_file)
        print("JSON document inserted to DB-Scraping successfully")
    except Exception as e:
        print("Error to insert document: ", e)