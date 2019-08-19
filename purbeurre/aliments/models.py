from django.db import models
from django.contrib.auth.models import User


class Aliment(models.Model):
    users = models.ManyToManyField(
        User,
        verbose_name="liste des utilisateurs",
        related_name="aliment",
    )
    name = models.CharField()
    substitute_of = models.CharField(blank=True)
    url = models.URLField(blank=True)  # lien où se trouve les informations de l'aliment
    url_image = models.URLField(blank=True)  # lien où se trouve l'image

    def __str__(self):
        return self.name
