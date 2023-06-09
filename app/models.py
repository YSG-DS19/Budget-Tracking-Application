from django.db import models
from django.contrib.auth.models import User

TYPE=(
    ('Positive','Positive'),
    ('Negative','Negative')
)

class Profile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    income = models.FloatField()
    balance = models.FloatField()
    expenses = models.FloatField(default=0)
   

    def __str__(self):
        return str(self.user)

class Expense(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=122)
    amount = models.FloatField(null=True)
    expense_type = models.CharField(max_length=122, choices=TYPE)

    def __str__(self):
        return self.name