from django.db import models
from django.contrib.auth.models import User
from user_budget.models import Budget


class Category(models.Model):
    title = models.CharField(max_length=50)
    desc = models.CharField(max_length=250, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False) #This allows recovery and prevents accidental data loss.

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['title', 'user'], name='unique_category_per_user')
        ]

    def __str__(self):
        return f"{self.title} ({self.user.username})"


class Expenses(models.Model):
    title = models.CharField(max_length=50)
    desc = models.CharField(max_length=250, blank=True)
    expense_amount = models.DecimalField(max_digits=10 ,decimal_places=2, blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, blank=True)
    budget = models.ForeignKey(Budget, null=False, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-added_at',)

    def __str__(self):
        return self.title
