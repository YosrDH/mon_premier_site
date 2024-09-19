from django.contrib import admin

from .models import Certification, catégorie, AutreProduit, InformationComplémentaire, Avis, Certif_mieux_notee


# Register your models here.
@admin.register(Certification,catégorie,AutreProduit,InformationComplémentaire,Avis,Certif_mieux_notee)

class GenericAdmin(admin.ModelAdmin):
    pass



