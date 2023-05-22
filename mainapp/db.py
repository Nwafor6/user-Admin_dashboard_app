from pymongo.mongo_client import MongoClient
from django.conf import settings
db_connection = None

def get_database_connection():
    global db_connection

    if db_connection is None:
        # Create a new database connection
        client = MongoClient("mongodb+srv://nwaforglory680:Nwafor6.com@cluster0.6ewghef.mongodb.net/?retryWrites=true&w=majority")
        db_connection = client["mydb"]
    
    return db_connection