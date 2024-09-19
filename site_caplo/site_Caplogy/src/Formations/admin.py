from django.contrib import admin

from . import forms
from .models import Categories, FormationAVenir, ProgrammeFormation, Module, Formateur, Avis, BilletAchat, Paiement, \
    DateFormation


# Register your models here.
@admin.register(Categories,FormationAVenir,ProgrammeFormation,Module,Formateur,Avis,BilletAchat,Paiement,DateFormation
                )

class GenericAdmin(admin.ModelAdmin):
    pass


