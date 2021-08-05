from django import forms
from . import models

class AddItemForm(forms.ModelForm):
    class Meta:
        model = models.WatchItem
        fields = ['name', 'url']
