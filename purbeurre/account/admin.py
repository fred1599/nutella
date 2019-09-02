from django.contrib import admin

from .models import Profil


@admin.register(Profil)
class AlimentAdmin(admin.ModelAdmin):
    pass
