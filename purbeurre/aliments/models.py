from django.db import models
from django.conf import settings


class Aliment(models.Model):
    """
    Classe Aliment pouvant représenter l'aliment recherché et l'aliment substitut de celui recherché
    Un aliment peut être dans le favoris de plusieurs utilisateurs et un utilisateur
    peut avoir plusieurs aliments favoris
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    url = models.URLField(blank=True)  # lien où se trouve les informations de l'aliment
    url_image = models.URLField(blank=True)  # lien où se trouve l'image
    score = models.CharField(blank=True, max_length=1) # nutrition score

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name
