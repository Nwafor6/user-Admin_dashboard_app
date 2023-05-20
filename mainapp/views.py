from django.shortcuts import render
from .models import Trader, Transaction

def user_dashboard(request):
    trader = Trader.objects.get(id=1)  # Assuming the user is identified with ID 1
    transactions = trader.transaction_set.all()  # Retrieve all transactions for the trader

    profit_loss_data = []
    timestamps = []

    for transaction in transactions:
        profit_loss_data.append(transaction.amount)
        timestamps.append(transaction.timestamp.strftime('%Y-%m-%d %H:%M:%S'))

    context = {
        'trader': trader,
        'profit_loss_data': profit_loss_data,
        'timestamps': timestamps,
    }

    return render(request, 'user_dashboard.html', context)

def admin_dashboard(request):
    traders = Trader.objects.all()
    profit_loss_data = []
    timestamps = []

    for trader in traders:
        transactions = trader.transaction_set.all()

        # Calculate the average profit/loss for the trader
        avg_profit_loss = sum(transaction.amount for transaction in transactions) / len(transactions)

        profit_loss_data.append(avg_profit_loss)
        timestamps.append(transactions[0].timestamp.strftime('%Y-%m-%d %H:%M:%S'))

    context = {
        'traders': traders,
        'profit_loss_data': profit_loss_data,
        'timestamps': timestamps,
    }

    return render(request, 'admin_dashboard.html', context)
