from .models import Profil


def add_profil(self, user):
    profil = Profil.objects.get_or_create(user)
    return profil
