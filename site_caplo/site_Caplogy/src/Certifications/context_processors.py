from .models import Certif_mieux_notee


def best_certifications(request):
    # Assurez-vous qu'il y a au moins un objet Certif_mieux_notee
    certif_mieux_notee = Certif_mieux_notee.objects.first()

    if certif_mieux_notee:
        best_certifications = certif_mieux_notee.titre.all()  # Récupérez les certifications associées


    return {
        'best_certifications': best_certifications
    }