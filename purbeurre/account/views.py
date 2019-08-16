from django.views.generic.edit import FormView
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.core.mail import send_mail

from .forms import ContactForm, RegisterForm

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

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        try:
            user = User.objects.get(username=username, password=password)
        except User.DoesNotExist:
            logger.warning("L'utilisateur {} n'a pas réussi à se connecter à ".format(username))
            self.success_url = 'error'

        return super().form_valid(form)


class RegisterView(FormView):
    template_name = "account/register.html"
    form_class = RegisterForm
    success_url = 'success'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        mail = form.cleaned_data['email']

        try:
            user = User.objects.get(username=username)
            user = User.objects.get(email=mail)
            self.success_url = 'error'
        except User.DoesNotExist:
            send_mail(
                'Inscription sur le site',
                'Bienvenue sur le site',
                mail,
                recipient_list=[],
                fail_silently=False,
            )
            User.objects.create(username=username, password=password, email=mail)

        return super().form_valid(form)


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
