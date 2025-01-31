from pymongo.mongo_client import MongoClient
import os
from dotenv import load_dotenv
from pymongo import IndexModel, ASCENDING

load_dotenv()
# Get MongoDB credentials from environment variables
username = os.getenv('MONGODB_USERNAME')
password = os.getenv('MONGODB_PASSWORD')

# Construct the URI using the environment variables
uri = f"mongodb+srv://{username}:{password}@cluster0.0k3wn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri)
db = client['adcore_db']

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Connected to MongoDB!")
except Exception as e:
    print(e)
