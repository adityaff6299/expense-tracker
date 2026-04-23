from django.db import models
from django.contrib.auth.models import User

class Expense(models.Model):
    CATEGORY = [
        ('Food', 'Food'),
        ('Travel', 'Travel'),
        ('Shopping', 'Shopping'),
        ('Housing', 'Housing'),
        ('Healthcare', 'Healthcare'), 
        ('Entertainment', 'Entertainment '), 
        ('Other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    category = models.CharField(max_length=20, choices=CATEGORY)
    date = models.DateField(auto_now_add=True)
    description = models.TextField()

    def __str__(self):
        return self.category
