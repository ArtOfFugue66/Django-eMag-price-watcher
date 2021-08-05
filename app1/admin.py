from django.contrib import admin
from app1 import models as app1models

# Register your models here.

admin.site.register(app1models.WatchItem)
admin.site.register(app1models.Scrape)