from django.db import models

class Trader(models.Model):
    name = models.CharField(max_length=100)
    balance = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    trader = models.ForeignKey(Trader, on_delete=models.CASCADE)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.trader.name}: {self.amount}"
