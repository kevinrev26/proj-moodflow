from pymongo import MongoClient
from config.settings import MONGO_CONFIG

def get_database():
    client = MongoClient(MONGO_CONFIG['HOST'], MONGO_CONFIG['PORT'])
    db = client[MONGO_CONFIG['DB_NAME']]
    return db