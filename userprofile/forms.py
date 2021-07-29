from django import forms

# from userprofile.models import UserExtend
from django.contrib.auth.models import User


class NewAccountForm(forms.ModelForm):
    class Meta:
        model = User
        # fields = ['first_name', 'last_name', 'email', 'username', 'password']
        fields = ['first_name', 'last_name', 'email', 'username']