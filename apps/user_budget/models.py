from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.http import QueryDict
from django.core.exceptions import ValidationError

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
        return expenses.aggregate(models.Sum('expense_amount')).get('expense_amount__sum') or 0
    
    @property
    def remaining(self):
        """Dynamically calculate the remaining budget amount."""
        return self.amount - self.amount_used
    
    def __str__(self):
        return f"{self.name} - {self.user.username}"

class Goal(models.Model):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("achieved", "Achieved"),
        ("expired", "Expired"),
    ]

    title = models.CharField(max_length=100)
    desc = models.CharField(max_length=255, blank=True)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    deadline = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def progress(self):
        if self.target_amount == 0:
            return 0
        return round((self.current_amount / self.target_amount) * 100, 2)

    def clean(self):
        if self.current_amount > self.target_amount:
            raise ValidationError("Current amount cannot exceed the target amount.")
        if self.deadline and self.deadline < timezone.now():
            self.status = "expired"

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def update_status(self):
        if self.current_amount >= self.target_amount:
            self.status = "achieved"
        elif self.deadline and self.deadline < timezone.now():
            self.status = "expired"
        else:
            self.status = "active"
        self.save()