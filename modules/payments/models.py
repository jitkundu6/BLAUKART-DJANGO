from django.db import models

#from django.contrib.auth.models import User
from modules.appcore.accounts.models import CustomUser as User



class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    purpose = models.CharField(max_length=30)
    amount = models.PositiveIntegerField()
    o_id = models.CharField(max_length=30, null=True)
    amount_paid = models.PositiveIntegerField(null=True)
    amount_due = models.PositiveIntegerField(null=True)
    currency = models.CharField(max_length=10, default="INR")
    offer_id = models.IntegerField(default=None, null=True) 
    status = models.CharField(max_length=15, default="initiated")
    attempts = models.PositiveIntegerField(null=True)
    notes = models.TextField(null=True)
    created_at =  models.PositiveIntegerField(null=True)
    date_time = models.DateTimeField(auto_now_add=True)

    #{'id': 'order_H1GPQiRHlPiDQu', 'entity': 'order', 'amount': 100, 'amount_paid': 0, 'amount_due': 100,
    # 'currency': 'USD', 'receipt': None, 'offer_id': None, 'status': 'created', 'attempts':0, 'notes': [], 'created_at': 1618941001}

    #def __str__(self):
    #    return self.user




class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    payments = models.ManyToManyField(Payment)
    purpose = models.CharField(max_length=30)
    amount = models.PositiveIntegerField()
    notes = models.TextField()
    date_time = models.DateTimeField()

    def __str__(self):
        return str(self.user.email) +" : "+ self.purpose +" : "+ str(self.amount)


"""
class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    purpose = models.CharField(max_length=30)
    amount = models.PositiveIntegerField()
    notes = models.TextField()
    status = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user.email) +" : "+ self.purpose +" : "+ str(self.amount)
"""





class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    payments = models.ManyToManyField(Payment)
    balance = models.FloatField(default=0)
    currency = models.CharField(max_length=10, default='INR')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    #def __str__(self):
    #    return self.user
