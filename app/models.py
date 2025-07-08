import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

client = None
db = None

def connect_to_mongo():
    global client, db
    uri = os.getenv("MONGO_URI")
    client = MongoClient(uri)
    db = client.reparaciones

def get_collection():
    return db.documentos
