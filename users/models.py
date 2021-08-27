from django.db import models
from django.contrib.auth.models import User
import uuid
import datetime

from django.db.models.signals import post_save, post_delete

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=500, blank=True, null=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user.username)


# create profile when user created
def create_profile(sender, instance, created, **kwwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name,
        )


# delete user when profile deleted
def delete_user(sender, instance, **kwwargs):
    user = instance.user
    user.delete()


post_save.connect(create_profile, sender=User)
post_delete.connect(delete_user, sender=Profile)
