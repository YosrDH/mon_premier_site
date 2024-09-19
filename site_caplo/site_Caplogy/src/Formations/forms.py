from django import forms


from .models import FormationAVenir, DateFormation


class RechercheFormation(forms.Form):
    nom_formation = forms.ModelChoiceField(FormationAVenir.objects.all(), required=True, label='choisir votre formation')
    formation_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        super(RechercheFormation, self).__init__(*args, **kwargs)
        self.fields['nom_formation'].widget.attrs.update({'class': 'search-bar', 'placeholder': 'Rechercher...'})


class DateFormationForm(forms.ModelForm):
    class Meta:
        model = DateFormation
        fields = ['date', 'lieu', 'inscription_deadline']