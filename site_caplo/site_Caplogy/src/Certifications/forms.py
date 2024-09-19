from django import forms
from .models import Certification

class SortForm(forms.Form):
    TriPar = forms.ChoiceField(
        choices=(
            ('', 'Tous'),  # Choix par défaut
            ('prix_asc', 'Tri par tarif croissant'),
            ('prix_desc', 'Tri par tarif décroissant'),
            ('popularité', 'Tri par popularité'),
            ('note_moyenne', 'Tri par note moyenne'),
            ('créé_à', 'Tri du plus récent au plus ancien '),
        ),
        required=False,
        label='Trier par'
    )

    def __init__(self, *args, **kwargs):
        super(SortForm, self).__init__(*args, **kwargs)
        self.fields['TriPar'].widget.attrs.update({'class': 'search-bar'})

