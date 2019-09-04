from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate, login, logout

from .forms import ContactForm, RegisterForm

from .models import Profil
from aliments.models import Aliment

import logging

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
    form_class = ContactForm
    success_url = 'success'
    user = None

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        try:
            self.user = User.objects.get(username=username, password=password)
            login(self.request, self.user)
        except User.DoesNotExist:
            logger.warning("L'utilisateur {} n'a pas réussi à se connecter à ".format(username))
            self.success_url = 'error'

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.user
        return context


class RegisterView(FormView):
    template_name = "account/register.html"
    form_class = RegisterForm
    success_url = 'success'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        mail = form.cleaned_data['email']

        user = authenticate(self.request, username=username, password=password)  # on essaye une authentification, si
        # non authentifié alors user vaut None, si un user existe, alors enregistrement impossible
        if not user:
            
            send_mail(
                'Inscription sur le site',
                'Bienvenue sur le site {}\nVotre mot de passe est: {}'.format(username, password),
                settings.EMAIL_HOST_USER,
                recipient_list=[mail,],
                fail_silently=False,
            ) # envoi du mail

        else:
            self.success_url = 'error' # renvoi vers la page d'erreur de l'enregistrement

        return super().form_valid(form)


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