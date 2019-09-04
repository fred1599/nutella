from django.contrib import admin

from .models import Aliment


@admin.register(Aliment)
class AlimentAdmin(admin.ModelAdmin):
    pass
