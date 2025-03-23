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

