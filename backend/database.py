from pymongo import MongoClient
from config import config

db_client = MongoClient(config.MONGO_URI)
db = db_client.get_database()

def init_db():
    try:
        # Example of initializing collections
        if 'stocks' not in db.list_collection_names():
            db.create_collection('stocks')
        if 'users' not in db.list_collection_names():
            db.create_collection('users')
        
        print("Database connected and collections initialized successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")

def close_db():
    db_client.close()
    print("Database connection closed.")