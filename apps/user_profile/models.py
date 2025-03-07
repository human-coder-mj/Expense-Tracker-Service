from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Profile(models.Model):

    firstName = models.CharField(max_length=200)
    lastName = models.CharField(max_length=200, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=timezone.now())
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self) -> str :
        return f'{self.user.username}'