from django import forms
from .models import Elev

class ElevForm(forms.ModelForm):
    nume = forms.CharField(label = 'Nume', max_length=30)
    prenume = forms.CharField(label = 'Prenume', max_length=30)
    data_nasterii = forms.DateField(label = 'Data nașterii')
    
    class Meta:
        model = Elev
        fields = ['nume', 'prenume', 'data_nasterii']

    def clean_nume(self):
        nume = self.cleaned_data['nume']
        if not nume[0].isupper() or not nume[1:].islower():
            raise forms.ValidationError("Numele trebuie să înceapă cu literă mare și să fie format doar din litere mici.")
        return nume

    def clean(self):
        cleaned_data = super().clean()
        nume = cleaned_data.get('nume')
        prenume = cleaned_data.get('prenume')

        if nume and prenume and nume == prenume:
            raise forms.ValidationError("Numele și prenumele nu pot fi identice.")

        return cleaned_data