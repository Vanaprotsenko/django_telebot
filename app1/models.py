from django.db import models

class Expense(models.Model):
    income = models.IntegerField()
    expense = models.IntegerField()
    date = models.DateField(auto_now_add=True,blank=True,null=True)



    