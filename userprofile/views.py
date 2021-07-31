import random
import string

from django.contrib.auth.models import User
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm

from userprofile.forms import *


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    fields = ['first_name', 'last_name', 'email']
    model = User
    template_name = 'registration/new_account.html'

    def get_success_url(self):
        return reverse('app1:watchlist_index')


def signup_view(request):
    form = NewAccountForm
    return render(request, 'registration/new_account.html', {'form': form})


class CreateNewUser(CreateView):
    form_class = NewAccountForm
    # form_class = UserCreationForm
    model = User
    template_name = 'registration/new_account.html'

    def get_success_url(self):
        return reverse('login')
