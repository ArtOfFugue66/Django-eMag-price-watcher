import random
import string

from django.contrib.auth.models import User
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from userprofile.forms import *


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    fields = ['first_name', 'last_name', 'email']
    model = User
    template_name = 'registration/new_account.html'

    def get_success_url(self):
        return reverse('app1:watchlist_index')


punctuation = '!$%?#@'


class CreateNewUser(CreateView):
    form_class = NewAccountForm
    model = User
    template_name = 'registration/new_account.html'


    def get_success_url(self):
        # psw = ''.join(random.SystemRandom.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits + punctuation) for _ in range(8))
        # try:
        #     user_instance = User.objects.get(id=self.object.id)
        #     user_instance.set_password(psw)
        #     user_instance.save()
        #     content_email = f"Your usename and password: {user_instance.user} {psw}"
        #     msg_html = render_to_string('emails/invite_user.html', {'content_email': str(content_email)})
        # except Exception:
        #     pass
        return reverse('login')
