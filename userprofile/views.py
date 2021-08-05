from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from userprofile.forms import *


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    fields = ['username', 'email']
    model = User
    template_name = 'registration/new_account.html'

    def get_success_url(self):
        return reverse('app1:watchlist_index')


def signup_view(request):
    if request.method == 'POST':  # request method is POST
        form = NewAccountForm(request.POST)  # create a form instance containing the user's form input
        if form.is_valid():  # validate form contents (username does not already exist, password requirements, email format etc.)
            form.save()  # insert the data into the DB
            return redirect('login')  # redirect user to login page after registration is complete
    else:  # request method is something other than POST (usually GET)
        form = NewAccountForm()

    return render(request, 'registration/new_account.html', {'form': form})


class CreateNewUser(CreateView):
    form_class = NewAccountForm
    # form_class = UserCreationForm
    model = User
    template_name = 'registration/new_account.html'

    def get_success_url(self):
        return reverse('login')
