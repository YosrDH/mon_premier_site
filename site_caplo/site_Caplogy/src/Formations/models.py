from datetime import datetime

from django.db import models
from django.urls import reverse


# Create your models here.


class Categories(models.Model):
    nom=models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class Formateur(models.Model):
    nom = models.CharField(max_length=100)
    specialite = models.CharField(max_length=200)
    image = models.ImageField(upload_to='fichiers/')
    linkedin = models.URLField(blank=True)
    article=models.URLField(blank=True)

    def __str__(self):
        return self.nom



class FormationAVenir(models.Model):
    titre = models.CharField(max_length=200)
    lieu = models.CharField(max_length=200)
    date = models.DateField(null=True, blank=True)
    heure_debut = models.TimeField(default='00:00:00')
    heure_fin = models.TimeField(default='00:00:00')
    image = models.ImageField(upload_to='fichiers/')
    categorie = models.ManyToManyField(Categories)
    description = models.TextField(default='')
    prix=models.DecimalField(max_digits=10, decimal_places=2)
    inscri_deadline = models.DateField(null=True, blank=True)
    heure_deadline=models.TimeField(default='00:00:00')
    organisateurs=models.CharField(max_length=200, default='')
    email = models.EmailField(max_length=254, blank=True, null=True)
    linkedin = models.URLField(blank=True)
    google_agenda = models.URLField(blank=True)
    yahoo = models.URLField(blank=True)
    outlook = models.URLField(blank=True)
    objectifs= models.TextField(default='')
    public_visé=models.TextField(default='')
    Positionnement=models.TextField(default='')
    organisation=models.TextField(default='')
    methode=models.TextField(default='')
    validation=models.TextField(default='')
    sanction=models.TextField(default='')
    prérequis=models.TextField(default='')
    formateurs = models.ManyToManyField(Formateur)
    dates_et_lieu_description=models.TextField(default='')
    informations_pratiques=models.TextField(default='')
    Formations_formationavenir_formations_connexes=models.ManyToManyField('self', blank=True, related_name='formations_connexes_set')

    def __str__(self):
        return self.titre
    def get_formateurs_list(self):
        return list(self.formateurs.all())


class DateFormation(models.Model):
    formation = models.ForeignKey(FormationAVenir, on_delete=models.CASCADE, related_name='dates')
    date = models.DateField()
    heure_debut = models.TimeField(default='00:00:00')
    heure_fin = models.TimeField(default='00:00:00')
    lieu = models.CharField(max_length=200)
    inscription_deadline = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.date} - {self.lieu}"

    def get_detail_repetee_url(self):
        return reverse('detail_formation_repetee', args=[self.id])


class Paiement(models.Model):
    formation = models.ForeignKey(FormationAVenir, on_delete=models.CASCADE)
    payer_id = models.CharField(max_length=255)
    payment_id = models.CharField(max_length=255)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    statut = models.CharField(max_length=50)
    date_paiement = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Paiement {self.payment_id} pour {self.formation.titre}"




class ProgrammeFormation(models.Model):
    formation = models.ForeignKey(FormationAVenir, on_delete=models.CASCADE)
    jour = models.DateField()
    titre_jour = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.formation.titre} -  {self.titre_jour}"

class Module(models.Model):
    programme = models.ForeignKey(ProgrammeFormation, on_delete=models.CASCADE)
    titre = models.CharField(max_length=200)
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()
    description = models.TextField()

    def __str__(self):
        return self.titre






    def __str__(self):
        return self.titre

    def get_absolute_url(self):
        return reverse('formations:detail_formation', args=[str(self.id)])






class Avis(models.Model):
    formation= models.ForeignKey(FormationAVenir, on_delete=models.CASCADE)
    commentaire=models.TextField(default='')
    note=models.IntegerField(default=0)

    def __str__(self):
        return f"Avis_sur -  {self.formation}"





class BilletAchat(models.Model):
    formation = models.ForeignKey(FormationAVenir, on_delete=models.CASCADE)
    titre=models.CharField(max_length=200, default='')
    quantité= models.PositiveIntegerField()
    additional_option = models.BooleanField(default=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    date_achat= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"billet d'achat pour {self.formation.titre} - {self.quantité} tickets"