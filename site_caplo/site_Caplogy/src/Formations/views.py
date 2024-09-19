import logging
from calendar import monthcalendar
from datetime import date

import stripe
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse


from .forms import RechercheFormation
from .models import FormationAVenir, ProgrammeFormation, BilletAchat, Avis, Paiement, Categories, DateFormation

import paypalrestsdk

from django.conf import settings
#stripe
stripe.api_key = settings.STRIPE_SECRET_KEY
YOUR_DOMAIN = 'http://http://127.0.0.1:8000'

#Configuration du SDK PayPal
paypalrestsdk.configure({
    "mode":"sandbox",   # Sandbox ou live
    "client_id":settings.PAYPAL_CLIENT_ID,
    "client_secret":settings.PAYPAL_CLIENT_SECRET,
})


def recherche(request):

    if request.method == 'POST':
        form = RechercheFormation(request.POST)
        if form.is_valid():
            nom_formation = form.cleaned_data.get('nom_formation')

            url = reverse('liste_formations', kwargs={'nom_formation': nom_formation})
            return HttpResponseRedirect(url)
    else:
        form=RechercheFormation()

    return render(request, 'recherche.html', {'form':form,})
def liste_formations(request, nom_formation):
    formations = FormationAVenir.objects.filter(titre=nom_formation)
    return render(request, 'liste_formation.html', {'formations': formations, 'nom_formation': nom_formation})








def detail_formation(request, id):
    formation = get_object_or_404(FormationAVenir, id=id)
    programmes = ProgrammeFormation.objects.filter(formation=formation).order_by('jour')
    formateurs = formation.get_formateurs_list()
    billets = BilletAchat.objects.filter(formation=formation)
    categories = formation.categorie.all()

    if request.method == 'POST':
        note = request.POST.get('rating')
        commentaire = request.POST.get('commentaire')

        if note and commentaire:
            try:
                note = int(note)
                if 1 <= note <= 5:  # Validation simple de la note
                    Avis.objects.create(
                        formation=formation,
                        note=note,
                        commentaire=commentaire
                    )
                    return HttpResponseRedirect(request.path_info)
                else:

                    pass
            except ValueError:
                # Gérer une note non numérique
                pass

    context = {
        'formation': formation,
        'programmes': programmes,
        'formateurs': formateurs,
        'billets': billets,
        'avis': Avis.objects.filter(formation=formation),
        'categories': categories,
    }

    return render(request, 'detail_formation.html', context)







def archive_view(request, category_id):
    # Récupérer la catégorie
    categorie = get_object_or_404(Categories, id=category_id)


    # Récupérer les formations expirées pour la catégorie donnée
    formations_expirees = FormationAVenir.objects.filter(
        categorie=categorie,
        date__lt=date.today()
    )

    # Extraire les titres des formations expirées
    noms_formations_expirees = formations_expirees

    context = {
        'noms_formations_expirees': noms_formations_expirees,
        'categorie_nom': categorie.nom,  # Ajouter le nom de la catégorie au contexte

    }

    return render(request, 'archive.html', context)

def payment_process(request, id):
    formation = get_object_or_404(FormationAVenir, id=id)
    prix = formation.prix

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))  # Récupérer la quantité du formulaire
        total_price = prix * quantity

        logging.info(f"Quantity: {quantity}, Total Price: {total_price}")

        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"},
            "redirect_urls": {
                "return_url": request.build_absolute_uri(reverse('payment_success', args=[formation.id])),
                "cancel_url": request.build_absolute_uri(reverse('payment_cancelled'))},
            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": formation.titre,
                        "sku": formation.id,  # Stock Keeping Unit
                        "price": str(prix),
                        "currency": "EUR",
                        "quantity": quantity}]},
                "amount": {
                    "total": str(total_price),
                    "currency": "EUR"},
                "description": f"Payment for {quantity} * {formation.titre}"}]})

        if payment.create():
            for link in payment.links:
                if link.rel == "approval_url":
                    approval_url = str(link.href)
                    return redirect(approval_url)
        else:
            logging.error(payment.error)
            return redirect('payment_error')
    else:
        return redirect('payment_error')

def payment_success(request, id):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    if payment_id and payer_id:
        payment = paypalrestsdk.Payment.find(payment_id)
        if payment.execute({"payer_id": payer_id}):
            # Enregistrer le paiement dans votre modèle
            formation = get_object_or_404(FormationAVenir, id=id)
            montant = float(payment.transactions[0].amount.total)
            Paiement.objects.create(
                formation=formation,
                payer_id=payer_id,
                payment_id=payment_id,
                montant=montant,
                statut=payment.state
            )
            return render(request, 'payment_success.html')
        else:
            logging.error(payment.error)
            return render(request, 'payment_error.html')
    else:
        return redirect('payment_error')


def payment_cancelled(request):
    return render(request, 'payment_cancelled.html')

def payment_error(request):
    return render(request, 'payment_error.html')






def create_checkout_session(request, id):
    formation = get_object_or_404(FormationAVenir, id=id)
    prix = formation.prix * 100  # Convert to cents

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        prix_cents = int(prix) # Multiply by quantity

        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'eur',
                            'product_data': {
                                'name': formation.titre,
                            },
                            'unit_amount': prix_cents,  # Montant total en cents
                        },
                        'quantity': quantity,
                    },
                ],
                mode='payment',
                success_url=request.build_absolute_uri(reverse('payment_success', args=[formation.id])),
                cancel_url=request.build_absolute_uri(reverse('payment_cancelled')),
            )
            return redirect(checkout_session.url)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=403)

def stripe_payment_success(request, id):
    # Handle the success logic here
    formation = get_object_or_404(FormationAVenir, id=id)

    # Assuming you want to save some payment details in your database
    payment_intent_id = request.GET.get('payment_intent')
    if payment_intent_id:
        payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        amount_received = payment_intent.amount_received / 100  # Convert from cents to euros
        currency = payment_intent.currency
        status = payment_intent.status

        # Enregistrer les détails du paiement dans votre modèle
        Paiement.objects.create(
            formation=formation,
            payer_id=payment_intent.charges.data[0].billing_details.name,
            payment_id=payment_intent.id,
            montant=amount_received,
            statut=status
        )

    return render(request, 'payment_success.html', {'formation': formation})

    # Save payment details if necessary
    return render(request, 'payment_success.html')

def payment_cancelled(request):
    return render(request, 'payment_cancelled.html')