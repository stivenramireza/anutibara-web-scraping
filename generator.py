import secrets
import json
import script_database as database

def create_json(json_data):
    json_file = json.loads(json.dumps(json_data, indent = 4, ensure_ascii = False))
    db = database.connect_to_db()
    database.insert_document(db, json_file)