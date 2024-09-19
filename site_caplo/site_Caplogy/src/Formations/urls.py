
from django.urls import path

from .views import recherche, liste_formations, detail_formation, payment_process, payment_success, payment_cancelled, \
    payment_error, create_checkout_session, archive_view

urlpatterns = [

    path('', recherche, name='recherche'),
    path('liste/<str:nom_formation>/', liste_formations, name='liste_formations'),
    path('course/<int:id>/', detail_formation, name='detail_formation'),

    path('archive/<int:category_id>/', archive_view, name='archive'),


    path('create-checkout-session/<int:id>/', create_checkout_session, name='create_checkout_session'),
    path('payment_process/<int:id>/', payment_process, name='payment_process'),
    path('payment_success/<int:id>/', payment_success, name='payment_success'),
    path('payment_cancelled/', payment_cancelled, name='payment_cancelled'),
    path('payment_error/', payment_error, name='payment_error'),



]