import logging
import os
import urllib.parse

from django.contrib.auth import authenticate, login, logout, REDIRECT_FIELD_NAME
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.views.generic.list import ListView

from aliments.models import Aliment
from .forms import ContactForm, RegisterForm
from .models import Profil

from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.conf import settings


from django.http import HttpResponseRedirect

logger = logging.getLogger(__name__)

messages = {
    'login': {
        'success': 'Vous êtes connecté',
        'error': "Vous n'êtes pas dans la base de données",
    },

    'register': {
        'success': 'Vous êtes enregistré',
        'error': "Cet utilisateur ou mot de passe",
    }
}


class LoginView(FormView):
    template_name = "account/login.html"
    form_class = AuthenticationForm
    success_url = 'success'
    redirect_field_name = REDIRECT_FIELD_NAME

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super(LoginView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        """
        The user has provided valid credentials (this was checked in AuthenticationForm.is_valid()). So now we
        can log him in.
        """
        login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        if self.success_url:
            redirect_to = self.success_url
        else:
            redirect_to = self.request.REQUEST.get(self.redirect_field_name, '')

        netloc = urllib.parse.urlparse(redirect_to)[1]
        if not redirect_to:
            redirect_to = settings.LOGIN_REDIRECT_URL
        # Security check -- don't allow redirection to a different host.
        elif netloc and netloc != self.request.get_host():
            redirect_to = settings.LOGIN_REDIRECT_URL
        return redirect_to

    def set_test_cookie(self):
        self.request.session.set_test_cookie()

    def check_and_delete_test_cookie(self):
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()
            return True
        return False

    def get(self, request, *args, **kwargs):
        """
        Same as django.views.generic.edit.ProcessFormView.get(), but adds test cookie stuff
        """
        self.set_test_cookie()
        return super(LoginView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Same as django.views.generic.edit.ProcessFormView.post(), but adds test cookie stuff
        """
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            self.check_and_delete_test_cookie()
            return self.form_valid(form)
        else:
            self.set_test_cookie()
            return self.form_invalid(form)


class RegisterView(FormView):
    template_name = "account/register.html"
    form_class = RegisterForm
    success_url = 'success'

    def form_valid(self, form):
        if form.is_valid():
            form.save()
        return redirect('index')


class ProfilView(ListView):
    template_name = 'account/profil.html'
    model = Profil

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['aliments'] = Aliment.objects.filter(user_set=context['user'])
        return context


def get_success_login(request):
    message = messages['login']['success']
    return render(request, 'account/success.html', {'message': message})


def get_error_login(request):
    message = messages['login']['error']
    title = "Vous n'êtes pas dans la base"
    return render(request, 'account/error.html', {'message': message, 'title': title})


def get_success_register(request):
    message = messages['register']['success']
    title = "Vous êtes bien enregistré"
    return render(request, 'account/success.html', {'message': message, 'title': title})


def get_error_register(request):
    message = messages['register']['error']
    title = "Vous n'êtes pas enregistré"
    return render(request, 'account/error.html', {'message': message, 'title': title})


def disconnect(request):
    logout(request)
    return redirect('index')
