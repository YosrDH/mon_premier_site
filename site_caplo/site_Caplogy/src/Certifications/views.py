from django.core.paginator import Paginator
from django.db.models import Avg
from django.http import HttpResponseRedirect

from .models import Certification, AutreProduit, catégorie, InformationComplémentaire, Avis, Certif_mieux_notee
from django.shortcuts import render, get_object_or_404, redirect
from .forms import SortForm

def liste_certifications(request):
    certifications=Certification.objects.all()
    autres_produits=AutreProduit.objects.all()
    paginator=Paginator(certifications,5)
    catégories=catégorie.objects.all()

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    form=SortForm(request.GET)

    if form.is_valid():
        tri_critere=form.cleaned_data.get('TriPar')
        if tri_critere == 'prix_asc':
            certifications = certifications.order_by('prix')
        elif tri_critere == 'prix_desc':
            certifications = certifications.order_by('-prix')
        elif tri_critere == 'popularité':
            certifications = certifications.order_by('popularité')
        elif tri_critere == 'note_moyenne':
            certifications = certifications.order_by('note_moyenne')
        elif tri_critere == 'créé_à':
            certifications = certifications.order_by('-créé_à')

    return render(request, 'certifications.html',  {'page_obj': page_obj,'certifications': certifications, 'form':form,
                                                                            'autre_produit':autres_produits,
                                                                             'catégories':catégories})


def certifications_par_ctegorie(request, slug):
    categorie=get_object_or_404(catégorie, slug=slug)
    categorie_button=catégorie.objects.all()
    certifications=Certification.objects.filter(catégories=categorie)
    autre_produit=AutreProduit.objects.all()
    paginator=Paginator(certifications,5)

    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)

    form = SortForm(request.GET)

    if form.is_valid():
        tri_critere = form.cleaned_data.get('TriPar')
        if tri_critere == 'prix_asc':
            certifications = certifications.order_by('prix')
        elif tri_critere == 'prix_desc':
            certifications = certifications.order_by('-prix')
        elif tri_critere == 'popularité':
            certifications = certifications.order_by('popularité')
        elif tri_critere == 'note_moyenne':
            certifications = certifications.order_by('note_moyenne')
        elif tri_critere == 'créé_à':
            certifications = certifications.order_by('-créé_à')

    return render(request, 'certifications_par_categorie.html',{
        'page_obj': page_obj,
        'certifications': certifications,
        'categorie': categorie,
        'categorie_button':categorie_button,
        'form':form,
        'autre_produit':autre_produit
    })

def certification_detail(request, pk):
    certification=get_object_or_404(Certification, pk=pk)
    informations_supplementaires=InformationComplémentaire.objects.filter(certification=certification).first()
    produits_similaires=certification.produits_similaires.all()



    if request.method == 'POST':
        note = request.POST.get('rating')
        commentaire = request.POST.get('commentaire')

        if note and commentaire:
            try:
                note = int(note)
                if 1 <= note <= 5:  # Validation simple de la note
                    Avis.objects.create(
                        certification=certification,
                        note=note,
                        commentaire=commentaire
                    )
                    return HttpResponseRedirect(request.path_info)
                else:

                    pass
            except ValueError:
                # Gérer une note non numérique
                pass

    return render(request, 'certification_detail.html', {'certification':certification,
                                                         'informations_supplementaires': informations_supplementaires,
                                                         'produits_similaires':produits_similaires,
                                                         'avis': Avis.objects.filter(certification=certification),})


def produit_similaire_detail(request, pk):
    produit_similaire=get_object_or_404(AutreProduit, pk=pk)
    if request.method == 'POST':
        note = request.POST.get('rating')
        commentaire = request.POST.get('commentaire')

        if note and commentaire:
            try:
                note = int(note)
                if 1 <= note <= 5:  # Validation simple de la note
                    Avis.objects.create(
                        produit_similaire=produit_similaire,
                        note=note,
                        commentaire=commentaire
                    )
                    return HttpResponseRedirect(request.path_info)
                else:

                    pass
            except ValueError:
                # Gérer une note non numérique
                pass



    return render(request, 'produit_similaire_detail.html', {'produit_similaire':produit_similaire,
                                                             'avis': Avis.objects.filter(produit_similaire=produit_similaire) })

def submit_review(request, pk, type_objet):
    if type_objet == 'certification':
        objet = get_object_or_404(Certification, pk=pk)
    elif type_objet == 'produit_similaire':
        objet = get_object_or_404(AutreProduit, pk=pk)


    note = request.POST.get('note')
    commentaire = request.POST.get('commentaire')

    if note and commentaire:
        try:
            note = int(note)
            if 1 <= note <= 5:
                avis = Avis.objects.create(
                    note=note,
                    commentaire=commentaire,
                    certification=objet if type_objet == 'certification' else None,
                    produit_similaire=objet if type_objet == 'produit_similaire' else None
                )

                # Mettre à jour la note moyenne
                if type_objet == 'certification':
                    moyenne = Avis.objects.filter(certification=objet).aggregate(moyenne=Avg('note'))['moyenne'] or 0
                    objet.note_moyenne = moyenne
                    objet.save()
                elif type_objet == 'produit_similaire':
                    moyenne = Avis.objects.filter(produit_similaire=objet).aggregate(moyenne=Avg('note'))['moyenne'] or 0
                    objet.note_moyenne = moyenne
                    objet.save()

                return redirect('certification_detail', pk=pk) if type_objet == 'certification' else redirect('produit_similaire_detail', pk=pk)
        except ValueError:
            pass  # Gérer une note non numérique

    return redirect('certification_detail', pk=pk) if type_objet == 'certification' else redirect('produit_similaire_detail', pk=pk)

def delete_review(request, pk, type_objet):
    avis = get_object_or_404(Avis, pk=pk)
    if avis.certification:
        certification = avis.certification
        avis.delete()
        # Mettre à jour la note moyenne
        moyenne = Avis.objects.filter(certification=certification).aggregate(moyenne=Avg('note'))['moyenne']
        certification.note_moyenne = moyenne
        certification.save()
        return redirect('certification_detail', pk=certification.pk)
    elif avis.produit_similaire:
        produit_similaire = avis.produit_similaire
        avis.delete()
        # Mettre à jour la note moyenne
        moyenne = Avis.objects.filter(produit_similaire=produit_similaire).aggregate(moyenne=Avg('note'))['moyenne']
        produit_similaire.note_moyenne = moyenne
        produit_similaire.save()
        return redirect('produit_similaire_detail', pk=produit_similaire.pk)


def search_certifications(request):
    certifications = Certification.objects.all()
    autre_produit = AutreProduit.objects.all()


    query=request.GET.get('query')
    results=[]
    if query:
        results=Certification.objects.filter(titre__icontains=query)

    paginator = Paginator(results, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    form = SortForm(request.GET)

    if form.is_valid():
        tri_critere = form.cleaned_data.get('TriPar')
        if tri_critere == 'prix_asc':
            certifications = certifications.order_by('prix')
        elif tri_critere == 'prix_desc':
            certifications = certifications.order_by('-prix')
        elif tri_critere == 'popularité':
            certifications = certifications.order_by('popularité')
        elif tri_critere == 'note_moyenne':
            certifications = certifications.order_by('note_moyenne')
        elif tri_critere == 'créé_à':
            certifications = certifications.order_by('-créé_à')

    return render(request, 'search_results.html', {'results':results, 'query':query,
                                                                        'page_obj': page_obj,
                                                                         'form':form ,
                                                                        'autre_produit':autre_produit} )