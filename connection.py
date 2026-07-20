import os
from pymongo import MongoClient


def get_db():
    client = MongoClient(os.environ["MONGO_URI"])
    return client[os.environ.get("MONGO_DB_NAME", "Bengkel")]
