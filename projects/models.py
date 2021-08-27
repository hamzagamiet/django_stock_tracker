from django.db import models
import uuid
import datetime
from users.models import Profile

# Create your models here.
class Watchlist(models.Model):
    watcher = models.CharField(max_length=50, null=True, blank=True)
    ticker = models.CharField(max_length=10, blank=True, null=True)
