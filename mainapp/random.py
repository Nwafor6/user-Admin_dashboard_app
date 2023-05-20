# generate_data.py

import random
from datetime import datetime, timedelta
from .models import Trader, Transaction
import time

def generate_data():
    traders = Trader.objects.all()

    for trader in traders:
        for _ in range(100):  # Generate 100 data points
            amount = random.uniform(-10, 10)  # Generate a random profit/loss value
            trader.balance += amount
            trader.save()
            transaction = Transaction(trader=trader, amount=amount)
            transaction.save()

            # Sleep for one minute
            time.sleep(60)
