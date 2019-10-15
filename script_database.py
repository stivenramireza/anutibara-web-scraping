from pymongo import MongoClient
import secrets
import json

def connect_to_db():
    try: 
        client = MongoClient('mongodb+srv://' + secrets.DB_USER +':' + secrets.DB_PASS + '@' + secrets.DB_HOST + '/' + secrets.DB_NAME) 
        print("Database connected successfully") 
    except:   
        print("Error to connect to database")
    database = client.get_database(secrets.DB_NAME)
    return database
    
def insert_document(db, list_json_files):
    try:
        properties = db.properties
        for json_file in list_json_files:
            with open('./generated_json/' + json_file + ".json") as f:
                file_data = json.load(f)
            properties.insert_one(file_data)
            print("JSON document " + json_file + " inserted successfully")
    except:
        print("Error to insert document")

def main():
    db = connect_to_db()
    list_json_files = ['property_2393445', 'property_4471500', 'property_4471519', 'property_4587456', 'property_4837830', 'property_4979282', 'property_4979293']
    insert_document(db, list_json_files)

if __name__ == "__main__":
    main()