from django import forms
from .models import Comanda, Client

class ComandaForm(forms.ModelForm):
    produs = forms.CharField(label='Produs', max_length=100)
    pret = forms.DecimalField(label='Pret')
    client = forms.ModelChoiceField(queryset=Client.objects.all(), label='Client')
    
    class Meta:
        model = Comanda 
        fields = ['produs', 'pret', 'client']

    def clean_pret(self):
        pret = self.cleaned_data['pret']
        if pret <= 0:
            raise forms.ValidationError("Pretul comenzii trebuie sa fie > 0")
        return pret