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
        print(name,"name of the user")
        db=get_database_connection()
        TradersCollection = db["Traders"]
        TransactionCollection = db["Transactions"]
        trader= TradersCollection.find_one({
            "name":str(name),
        })
        print(trader)
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

# Function that makes transactions for the stock traders
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
            "balance":100,
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
