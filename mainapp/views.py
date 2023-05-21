from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Trader, Transaction
from .task import generate_data
from threading import Thread
from time import perf_counter
from pymongo.mongo_client import MongoClient
from datetime import datetime
from django.contrib import messages
from .db import get_database_connection
from django.http import JsonResponse
import time
import random


timestamp = datetime.now()
timestamp_str = timestamp.strftime('%Y-%m-%d %H:%M:%S')

# Function for users to access their dashboard
def user_login(request): 
    if request.method =="POST":
        name=request.POST["name"]
        db=get_database_connection()
        TradersCollection = db["Traders"]
        TransactionCollection = db["Transactions"]
        trader= TradersCollection.find_one({
            "name":name,
        })
        if trader:
            print(trader["_id"], "Hello my ")
            return redirect("user_dashboard", trader["name"])
    messages.warning(request, 'Invalid user !!')
    return render(request, 'mainapp/login.html')

# Fetch trader's details including transcation details
def user_dashboard(request,user_name):
    db=get_database_connection() 
    TradersCollection = db["Traders"]
    TransactionCollection = db["Transactions"]
    trader=TradersCollection.find_one({
        "name":user_name,
    })
    
    context = {
        "user":user_name,
        'name': trader["name"],
        'balance': trader["balance"],
        'id': trader["_id"],
    }
    user_dash_plot(request, user_name)
    return render(request, 'partials/base.html', context)

def user_dash_plot(request,user_name):
    db=get_database_connection() 
    TradersCollection = db["Traders"]
    TransactionCollection = db["Transactions"]
    trader=TradersCollection.find_one({
        "name":user_name,
    })
    transactions=TransactionCollection.find({"trader":trader["_id"]})
    print({"Trader":trader}, "Hello word")
    profit_loss_data=[]
    timestamps=[]
    for transaction in transactions:
    # Access the transaction data
        profit_loss_data.append(transaction["amount"])
        timestamps.append(transaction["timestamp"])
    context = {
        'name': trader["name"],
        'profit_loss_data': profit_loss_data,
        'timestamps': timestamps,
    }
    thread=Thread(target=bgTransaction(request))
    thread.start()
    return render(request, "partials/index.html", context)

# Function that makes trasactions for the stick trader
def bgTransaction(request):
    thread=Thread(target=generate_data)
    thread.start()
    print("Tranfered request")
    return JsonResponse({"detail":"Requested added to queue"})

def admin_dashboard(request):
    db=get_database_connection() 
    TransactionCollection = db["Transactions"]
    transactions=TransactionCollection.find({})
    profit_loss_data = [transaction["amount"] for transaction in transactions]
    avg_profit_loss = sum(profit_loss_data) / len(profit_loss_data)
    context = {
        "avg_profit_loss":avg_profit_loss,
    }
    if request.method =="POST":
        name=request.POST["name"]
        TradersCollection = db["Traders"]
        newTrader={
            "name":name,
            "amount":100,
            "timestamp":timestamp_str
        }
        TradersCollection.insert_one(newTrader)

    return render(request, 'partials/admin2.html', context)

def admin_dash_plot(request):
    db=get_database_connection() 
    TradersCollection = db["Traders"]
    TransactionCollection = db["Transactions"]
    traders=TradersCollection.find({})
    transactions=TransactionCollection.find({})
    profit_loss_data = [transaction["amount"] for transaction in transactions]
    traders_name = [trader["name"] for trader in traders]
    
    avg_profit_loss = sum(profit_loss_data) / len(profit_loss_data)
    context = {
        'traders': traders_name,
        'profit_loss_data': profit_loss_data,
        "avg_profit_loss":avg_profit_loss,
    }

    return render(request, 'partials/admin3.html', context)





# def user_dashboard(request, pk):
    
#     trader = Trader.objects.get(id=pk)  # Assuming the user is identified with ID 1
#     transactions = trader.transaction_set.all()  # Retrieve all transactions for the trader

#     profit_loss_data = []
#     timestamps = []
#     thread = Thread(target=generate_data)
#     thread.start()
#     # thread.join()
#     for transaction in transactions:
#         profit_loss_data.append(transaction.amount)
#         timestamps.append(transaction.timestamp.strftime('%Y-%m-%d %H:%M:%S'))

#     context = {
#         'trader': trader,
#         'profit_loss_data': profit_loss_data,
#         'timestamps': timestamps,
#     }

#     return render(request, 'mainapp/index.html', context)

# def admin_dashboard(request):
#     traders = Trader.objects.all()
#     profit_loss_data = []
#     timestamps = []
#     traders_=[]

#     for trader in traders:
#         transactions = trader.transaction_set.all()

#         # Calculate the average profit/loss for the trader
#         avg_profit_loss = sum(transaction.amount for transaction in transactions) / len(transactions)

#         profit_loss_data.append(avg_profit_loss)
#         timestamps.append(transactions[0].timestamp.strftime('%Y-%m-%d %H:%M:%S'))
#         traders_.append(trader.name)

#     context = {
#         'traders': traders_,
#         'profit_loss_data': profit_loss_data,
#         'timestamps': timestamps,
#     }

#     return render(request, 'mainapp/admin.html', context)
# def bgTransaction(request):
#     # Create a datetime object representing the current timestamp
#     timestamp = datetime.now()
#     timestamp_str = timestamp.strftime('%Y-%m-%d %H:%M:%S')
#     print(request.method)
#     uri = "mongodb+srv://nwaforglory680:Nwafor6.com@cluster0.6ewghef.mongodb.net/?retryWrites=true&w=majority"
#     # Create a new client and connect to the server
#     client = MongoClient(uri)
#     dbname = client['mydb']
#     collection_name = dbname["Traders"]
#     names=["Trader B","Trader C", "Trader D","Trader E","Trader F","Trader G","Trader H"]
#     Traders =[]
#     for i in names:
#        Traders.append({
#             "name": i,
#             "balance":100.0,
#             "timestamp": timestamp_str,
#         })
#     collection_name.insert_many(Traders)
#     return HttpResponse("Trader Added successfully")