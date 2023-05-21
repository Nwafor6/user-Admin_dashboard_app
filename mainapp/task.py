import random
from datetime import datetime, timedelta
import os
import django
from django.conf import settings
import pymongo
from pymongo.mongo_client import MongoClient
from datetime import datetime
import time
from mainapp.models import Trader, Transaction
import time
from .db import get_database_connection

def generate_data():
    # Create a datetime object representing the current timestamp
    timestamp = datetime.now()
    timestamp_str = timestamp.strftime('%Y-%m-%d %H:%M:%S')
    db=get_database_connection()
    TradersCollection = db["Traders"]
    TransactionCollection = db["Transactions"]
    traders=TradersCollection.find({})
    for trader in traders:
        # Update the traders balance
        _trader=TradersCollection.find_one({"name":trader["name"]})
        amount = random.uniform(-10, 10)  # Generate a random profit/loss value
        new_balance = _trader["balance"] + amount
        update_query={"$set":{"balance":new_balance}}
        TradersCollection.update_one(_trader, update_query)
        # Sleep for one minute
        # Add to the transaction_collection
        transaction={
            "trader":_trader["_id"],
            "amount":amount,
            "timestamp":timestamp_str
        }
        TransactionCollection.insert_one(transaction)
        time.sleep(1)
    print("New Transcation")

# def generate_data():
#     traders = Trader.objects.all()
#     for trader in traders:
#         for _ in range(3):  # Generate 100 data points
#             amount = random.uniform(-10, 10)  # Generate a random profit/loss value
#             trader.balance += amount
#             trader.save()
#             transaction = Transaction(trader=trader, amount=amount)
#             transaction.save()

#             # Sleep for one minute
#             print(transaction, "New Transcation")
#             time.sleep(1)
            


