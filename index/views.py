from django.shortcuts import render


def index(request):
    user = request.user
    return render(request, 'index/accueil.html', {'user': user})


def mentions(request):
    return render(request, 'index/mentions.html', )