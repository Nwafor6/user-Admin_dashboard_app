from django.shortcuts import render
from .models import Trader, Transaction
from .task import generate_data
from threading import Thread
from time import perf_counter

def user_dashboard(request, pk):
    trader = Trader.objects.get(id=pk)  # Assuming the user is identified with ID 1
    transactions = trader.transaction_set.all()  # Retrieve all transactions for the trader

    profit_loss_data = []
    timestamps = []
    thread = Thread(target=generate_data)
    thread.start()
    # thread.join()
    for transaction in transactions:
        profit_loss_data.append(transaction.amount)
        timestamps.append(transaction.timestamp.strftime('%Y-%m-%d %H:%M:%S'))

    context = {
        'trader': trader,
        'profit_loss_data': profit_loss_data,
        'timestamps': timestamps,
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
