from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.fields import DateTimeField
import datetime


class WatchItem(models.Model):
    """
    Class representing an entry in the user's product watchlist
    """
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    url = models.CharField(max_length=300)

    def __str__(self):
        return f"{self.name}: {self.url}"


class Scrape(models.Model):
    """
    Class representing the data scraped for a particular product
    """
    item = models.ForeignKey('WatchItem', on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    dateTime = models.DateTimeField(default=datetime.datetime.now)
    # time = models.TimeField(default=None)

    def __str__(self):
        return f"{self.item} {self.price}: {self.date} {self.time}"
