from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, firstName=instance.username, email=instance.email)

@receiver(pre_delete, sender=User)
def delete_user_profile(sender, instance, **kwargs):
    """
    Deletes the Profile when the User is deleted.
    """
    profile = Profile.objects.filter(user=instance).first()
    if profile:
        profile.delete()