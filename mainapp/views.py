from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Trader, Transaction
from .task import generate_data
from threading import Thread
from time import perf_counter
from pymongo.mongo_client import MongoClient
from datetime import datetime
import time
import random
# import datetime


timestamp = datetime.now()
timestamp_str = timestamp.strftime('%Y-%m-%d %H:%M:%S')


# Function for users to access their dashboard
def user_login(request): 
    if request.method =="POST":
        name=request.POST["name"]
        uri = "mongodb+srv://nwaforglory680:Nwafor6.com@cluster0.6ewghef.mongodb.net/?retryWrites=true&w=majority"
        client = MongoClient(uri)
        dbname = client['mydb']
        TradersCollection = dbname["Traders"]
        TransactionCollection = dbname["Transactions"]
        trader= TradersCollection.find_one({
            "name":name,
        })
        if trader:
            print(trader["_id"], "Hello my ")
            return redirect("user_dashboard", trader["name"])
    
    return render(request, 'mainapp/login.html')

# Fetch trader's details including transcation details
def user_dashboard(request, user_name): 
    uri = "mongodb+srv://nwaforglory680:Nwafor6.com@cluster0.6ewghef.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(uri)
    dbname = client['mydb']
    TradersCollection = dbname["Traders"]
    TransactionCollection = dbname["Transactions"]
    trader=TradersCollection.find_one({
        "name":user_name,
    })
    transaction=TransactionCollection.find({"trader":trader["_id"]})
    print({"Trader":trader,"transaction":transaction,}, "Hello word")
    


    context = {
        'name': trader,
        'balance': trader["balance"],
        # 'profit_loss_data': profit_loss_data,
        # 'timestamps': timestamps,
    }

    return render(request, 'mainapp/index.html', context)

def admin_dashboard(request):
    traders = Trader.objects.all()
    profit_loss_data = []
    timestamps = []
    traders_=[]

    for trader in traders:
        transactions = trader.transaction_set.all()

        # Calculate the average profit/loss for the trader
        avg_profit_loss = sum(transaction.amount for transaction in transactions) / len(transactions)

        profit_loss_data.append(avg_profit_loss)
        timestamps.append(transactions[0].timestamp.strftime('%Y-%m-%d %H:%M:%S'))
        traders_.append(trader.name)

    context = {
        'traders': traders_,
        'profit_loss_data': profit_loss_data,
        'timestamps': timestamps,
    }

    return render(request, 'mainapp/admin.html', context)


# Function that makes trasactions for the stick trader
def bgTransaction(request):
    thread=Thread(target=generate_data)
    thread.start()
    return HttpResponse("Requested added to queue")

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