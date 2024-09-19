from django.db import models
from django.utils.text import slugify

class catégorie(models.Model):
    titre = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titre)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titre


class AutreProduit(models.Model):
    titre = models.CharField(max_length=100)
    prix = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    image = models.ImageField(upload_to='fichiers/', default='')
    description = models.TextField(default='')
    catégories = models.ManyToManyField(catégorie)
    desc_detaille=models.TextField(default='')
    note_moyenne=models.FloatField(default=0.0, null=True, blank=True)

    def __str__(self):
        return self.titre


class Certification(models.Model):
    titre = models.CharField(max_length=200)
    image = models.ImageField(upload_to='fichiers/', default='')
    desc_produit = models.TextField(default='')
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    popularité = models.CharField(max_length=100)
    note_moyenne = models.FloatField(default=0.0, null=True,blank=True)
    créé_à = models.DateTimeField(auto_now_add=True)
    catégories = models.ManyToManyField(catégorie)
    produits_similaires = models.ManyToManyField(AutreProduit)

    def __str__(self):
        return self.titre


class Certif_mieux_notee(models.Model):
    titre=models.ManyToManyField(Certification)

    def __str__(self):
        return f'Certifications mieux notées'
class InformationComplémentaire(models.Model):
    certification=models.ForeignKey(Certification, on_delete=models.CASCADE)

    localiser_un_centre_de_test = models.TextField(default='',blank=True)
    créer_un_compte = models.TextField(default='', blank=True)
    attribuer_un_bon_à_votre_compte = models.TextField(default='', blank=True)
    echanger_votre_bon_examen = models.TextField(default='', blank=True)
    echanger_votre_test_pratique_via_GMetrix = models.TextField(default='', blank=True)
    utiliser_le_bon = models.TextField(default='', blank=True)
    domaines_objectifs = models.URLField(max_length=300, default='', blank=True)
    fournisseur = models.CharField(max_length=200, default='', blank=True)


    def __str__(self):
        return f"{self.certification.titre}"


class Avis(models.Model):
    certification = models.ForeignKey(Certification, on_delete=models.CASCADE, null=True, blank=True)
    produit_similaire=models.ForeignKey(AutreProduit, on_delete=models.CASCADE, null=True, blank=True)
    note = models.IntegerField()
    commentaire = models.TextField()
    créé_à = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.certification:
            return f"{self.certification.titre}"
        else:
            return f"{self.produit_similaire.titre}"




