from django.urls import path

from .views import liste_certifications, certifications_par_ctegorie, certification_detail, search_certifications, \
    submit_review, produit_similaire_detail

urlpatterns = [


    path('', liste_certifications, name='liste_certifications'),
    path('categorie/<slug:slug>/', certifications_par_ctegorie, name='certifications_par_categorie'),
    path('detail_certification/<int:pk>/', certification_detail, name='certification_detail'),
    path('detail_produit_similaire/<int:pk>/', produit_similaire_detail, name='produit_similaire_detail'),
    path('search/', search_certifications, name='search_certifications'),
    path('submit_review/<int:pk>/<str:type_objet>/', submit_review, name='submit_review'),


]