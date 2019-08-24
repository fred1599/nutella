from django.db import models
from django.contrib.auth.models import User


class Aliment(models.Model):
    users = models.ManyToManyField(
        User,
        verbose_name="liste des utilisateurs",
        related_name="aliment",
    )
    name = models.CharField(max_length=200)
    substitute_of = models.CharField(blank=True, max_length=200)
    url = models.URLField(blank=True)  # lien où se trouve les informations de l'aliment
    url_image = models.URLField(blank=True)  # lien où se trouve l'image
    score = models.CharField(blank=True, max_length=1) # nutrition score

    def __str__(self):
        return self.name
