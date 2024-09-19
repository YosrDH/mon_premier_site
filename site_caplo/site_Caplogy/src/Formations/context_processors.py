
from datetime import datetime


from .models import FormationAVenir


def formations_avenir(request):
    formations_avenir = FormationAVenir.objects.all()[:4]


    return {'formations_avenir': formations_avenir}


def liste_event(request):
    today=datetime.today().date()
    evenements=FormationAVenir.objects.filter(date__gte=today).order_by('date')
    categories=FormationAVenir.objects.values_list('categorie__nom', flat=True).distinct()
    formations_a_venir=FormationAVenir.objects.all()

    selected_date=request.GET.get('date')  # Utilisez request.GET.get('date')
    selected_category=request.GET.get('categorie')  # Utilisez request.GET.get('categorie')

    if selected_date:
        evenements=evenements.filter(date=selected_date)
    if selected_category:
        evenements=evenements.filter(categorie=selected_category)

    return  {'evenements':evenements,
             'categories':categories,
             'selected_date':selected_date,
             'selected_category':selected_category,
             'formations_a_venir':formations_a_venir}



