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
db = client['your_database_name']
payee_collection = db['payee_info']

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Connected to MongoDB!")
except Exception as e:
    print(e)

# Create indexes
try:
    # Create a unique index on email
    email_index = IndexModel([("payee_email", ASCENDING)], unique=True)
    payee_collection.create_indexes([email_index])
    
    # Validate the schema
    db.command({
        'collMod': 'payee_info',
        'validator': {
            '$jsonSchema': {
                'bsonType': 'object',
                'required': [
                    'payee_first_name',
                    'payee_last_name',
                    'payee_added_date_utc',
                    'payee_address_line_1',
                    'payee_city',
                    'payee_country',
                    'payee_postal_code',
                    'payee_phone_number',
                    'payee_email'
                ],
                'properties': {
                    'payee_first_name': {'bsonType': 'string'},
                    'payee_last_name': {'bsonType': 'string'},
                    'payee_added_date_utc': {'bsonType': 'date'},
                    'payee_address_line_1': {'bsonType': 'string'},
                    'payee_address_line_2': {'bsonType': 'string'},
                    'payee_city': {'bsonType': 'string'},
                    'payee_country': {'bsonType': 'string', 'pattern': '^[A-Z]{2}$'},
                    'payee_province_or_state': {'bsonType': 'string'},
                    'payee_postal_code': {'bsonType': 'string'},
                    'payee_phone_number': {'bsonType': 'string', 'pattern': '^\+[1-9]\d{1,14}$'},
                    'payee_email': {'bsonType': 'string', 'pattern': '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'}
                }
            }
        }
    })
    print("Collection and indexes created successfully!")
except Exception as e:
    print(f"An error occurred: {e}")