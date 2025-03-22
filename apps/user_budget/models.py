from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.http import QueryDict

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="budgets")  # Each budget belongs to a user
    name = models.CharField(max_length=255)  # Name of the budget
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Total budgeted amount
    issued_at = models.DateTimeField(auto_now_add=True)  # Auto-set when created
    updated_at = models.DateTimeField(auto_now=True)  # Auto-update when modified

    class Meta:
            ordering = '-issued_at',
    
    @property
    def amount_used(self):
        expenses: QueryDict = self.expenses_set.all()
        return expenses.aggregate(Sum('amount')).get('amount__sum') or 0
    
    def remaining(self):
        """Dynamically calculate the remaining budget amount."""
        return self.amount - self.amount_used
    
    def __str__(self):
        return f"{self.name} - {self.user.username}"
