from django.db import models
from django.contrib.auth.models import User
from aliments.models import Aliment


class Profil(models.Model):
    """
    Modèle regroupant les informations du profil utilisateur
    - Infos générales de l'utilisateur (username, password)
    - Ses aliments favoris
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    aliments = models.ManyToManyField(Aliment, related_name='profil_set', blank=True)

    def __str__(self):
        return 'Profil n°{}'.format(self.user.pk)

    class Meta:
        ordering = ('pk',)
