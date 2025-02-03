from pymongo.mongo_client import MongoClient
import os
from dotenv import load_dotenv
from pymongo import IndexModel, ASCENDING

load_dotenv()

username = os.getenv('MONGODB_USERNAME')
password = os.getenv('MONGODB_PASSWORD')
connection = os.getenv('CONNECTION_STRING')

uri = f"mongodb+srv://{username}:{password}@{connection}"

try:
    print(uri)
    client = MongoClient(uri)
    db = client['adcore_db']
    payment_info = db['payment_info']
    client.admin.command('ping')
    print("Connected to MongoDB!")
except Exception as e:
    print(e)
