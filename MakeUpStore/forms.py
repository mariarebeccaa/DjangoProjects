from django import forms

# lab5_Task1
from .models import Marca, Categorie

class ProdusFilterForm(forms.Form):
    nume = forms.CharField(required=False, label="Nume produs", widget=forms.TextInput(attrs={'placeholder': 'Caută după nume'}))
    pret_min = forms.DecimalField(required=False, label="Preț minim", min_value=0, widget=forms.NumberInput(attrs={'placeholder': 'Preț minim'}))
    pret_max = forms.DecimalField(required=False, label="Preț maxim", min_value=0, widget=forms.NumberInput(attrs={'placeholder': 'Preț maxim'}))
    descriere = forms.CharField(required=False, label="Descriere", widget=forms.TextInput(attrs={'placeholder': 'Caută după descriere'}))
    marca = forms.ModelChoiceField(required=False, queryset=Marca.objects.all(), label="Marcă")
    categorie = forms.ModelChoiceField(required=False, queryset=Categorie.objects.all(), label="Categorie")

# lab5_Task2 ----------------------------------------------------------------------------------------------------------------
from django import forms
from datetime import date
import re
# PAS_1: creearea formularului cu validari
def validare_campuri(camp): #pt validari simple folosim validari in campuri
    """Validare comuna pentru nume, prenume, subiect."""
    if camp and not re.match(r'^[A-Z][a-zA-Z\s]*$', camp):
        raise forms.ValidationError("Trebuie sa inceapă cu litera mare si sa contina doar litere si spatii")
    return camp

class ContactForm(forms.Form):
    nume = forms.CharField(max_length=10, required=True, label="Nume", validators=[validare_campuri])
    prenume = forms.CharField(required=False, label="Prenume", validators=[validare_campuri])
    data_nasterii = forms.DateField(label="Data nașterii", widget=forms.DateInput(attrs={'type': 'date'}))
    email = forms.EmailField(required=True, label="E-mail")
    confirmare_email = forms.EmailField(required=True, label="Confirmare E-mail")
    tip_mesaj = forms.ChoiceField(
        choices=[('reclamatie', 'Reclamație'), 
                ('intrebare', 'Întrebare'), 
                ('review', 'Review'), 
                ('cerere', 'Cerere'), 
                ('programare', 'Programare')],
        label="Tip mesaj"
    )
    subiect = forms.CharField(required=True, label="Subiect", validators=[validare_campuri])
    minim_zile_asteptare = forms.IntegerField(required=True, label="Minim zile asteptare", min_value=1, error_messages={"min_value": "Val trb sa fie mai mare decat 0"})
    mesaj = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'placeholder': "Semnează-te la final!"}),
        label="Mesaj (semnează-te la final!)"
    )

    def clean(self): # metoda clean este fololsita pt validari care immplica mai multe campuri sau reguli complexe
        cleaned_data = super().clean() #apeleaza metoda clean din clasa parinte forms.Form
        # super().clean() preia datele validate pt fiecare camp
        email = cleaned_data.get('email')
        confirmare_email = cleaned_data.get('confirmare_email')
        data_nasterii = cleaned_data.get('data_nasterii')
        mesaj = cleaned_data.get('mesaj')
        nume = cleaned_data.get('nume')

        # Validare email
        if email != confirmare_email:
            raise forms.ValidationError("Emailul si confirmarea emailului nu coincid")

        # Validare majoritate
        if data_nasterii:
            today = date.today()
            age_years = today.year - data_nasterii.year
            if today.month < data_nasterii.month or (today.month == data_nasterii.month and today.day < data_nasterii.day):
                age_years -= 1
            if age_years < 18:
                raise forms.ValidationError("Expeditorul trebuie sa fie major")

        # Validare mesaj
        if mesaj:
            # Verificare linkuri
            if any(word.startswith(("http://", "https://")) for word in mesaj.split()):
                raise forms.ValidationError("Mesajul nu poate conține linkuri.")

            # Nr cuvinte
            cuvinte = re.findall(r'\b\w+\b', mesaj)
            if not (5 <= len(cuvinte) <= 100):
                raise forms.ValidationError("Mesajul trebuie sa contină între 5 și 100 de cuvinte.")

            # Verificare semnatura
            if nume and not mesaj.strip().endswith(nume):
                raise forms.ValidationError("Mesajul trebuie să fie semnat cu numele utilizatorului.")

        return cleaned_data
    
# Lab5_Task3
from django import forms
from .models import Produs

class ProdusForm(forms.ModelForm):
    # campuri aditionale
    discount = forms.DecimalField(
        max_digits=5,
        decimal_places=2,
        required=False,
        label="Discount (%)",
        help_text="Introduceți discountul ca procent între 0 și 100."
    )
    pret_final = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        label="Preț final",
        help_text="Se calculează automat pe baza prețului și discountului."
    )

    class Meta:
        model = Produs # specifica modelul pentru ModelForm
        fields = ['nume', 'pret', 'descriere', 'categorie', 'marci']  # specifica ce campuri sa includa
        labels = {
            'nume': 'Nume produs',
            'pret': 'Preț inițial',
            'descriere': 'Descriere produs',
            'categorie': 'Categorie produs',
            'marci' : 'Marca'
        }
        widgets = {
            'marci': forms.CheckboxSelectMultiple()  # Widget pentru selectarea multipla
        }
        help_texts = {
            'pret': 'Introduceți prețul inițial al produsului (în lei).',
            'descriere': 'Descrierea este opțională.'
        }
        error_messages = {
            'nume': {'max_length': 'Numele produsului nu poate avea mai mult de 100 de caractere.'},
            'pret': {'min_value': 'Prețul trebuie să fie pozitiv.'},
        }

    def clean_discount(self):
        discount = self.cleaned_data.get('discount')
        if discount and (discount < 0 or discount > 100):
            raise forms.ValidationError("Discountul trebuie să fie între 0 și 100%.")
        return discount

    def clean(self):
        cleaned_data = super().clean()
        pret = cleaned_data.get('pret')
        discount = cleaned_data.get('discount')

        # Validare la nivelul intregului formular: Preț final trebuie să fie calculabil
        if pret and discount:
            pret_final_calculat = pret * (1 - discount / 100)
            if pret_final_calculat < 0:
                raise forms.ValidationError("Prețul final nu poate fi negativ.")
            cleaned_data['pret_final'] = pret_final_calculat

        return cleaned_data

    def save(self, commit=True):
        produs = super().save(commit=False)  # Salvam cu `commit=False`
        # calc. campurile aditionale
        discount = self.cleaned_data.get('discount')
        if discount:
            produs.pret = produs.pret * (1 - discount / 100)  # Actualizam pretul cu discount
        if commit:
            produs.save()
        if self.cleaned_data.get('marci'):
            produs.marci.set(self.cleaned_data['marci'])
        return produs
    
    
# lab6
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
# formular de inregistrare
class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(required=True, label="Prenume")
    last_name = forms.CharField(required=True, label="Nume")
    telefon = forms.CharField(required=True, label="Număr de telefon")
    data_nasterii = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Data nașterii"
    )
    oras = forms.CharField(required=True, label="Oraș")
    ocupatie = forms.CharField(required=True, label="Ocupație")
    descriere = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'placeholder': 'Scrie o descriere'}),
        label="Descriere"
    )

    class Meta:
        model = CustomUser
        fields = ("username","first_name", "email", "last_name", "telefon", "data_nasterii", "oras", "ocupatie", "descriere", "password1", "password2")

    def save(self, commit=True):
         # Creeaza userul dar nu-l salveaza inca in baza
        user = super().save(commit=False) 
        user.first_name = self.cleaned_data["first_name"]  # Salvează prenumele
        user.last_name = self.cleaned_data["last_name"]  # Salvează numele
        user.telefon = self.cleaned_data["telefon"]
        user.data_nasterii = self.cleaned_data["data_nasterii"]
        user.oras = self.cleaned_data["oras"]
        user.ocupatie = self.cleaned_data["ocupatie"]
        user.descriere = self.cleaned_data["descriere"]
        # Acum il salvezi manual daca commit=True
        if commit:
            user.save()
        return user
    
    def clean_telefon(self): # metode folosite pt validari personalizate la nivel de camp individual
        telefon = self.cleaned_data['telefon']
        if not telefon.isdigit():
            raise forms.ValidationError("Numărul de telefon trebuie să conțină doar cifre.")
        return telefon

    def clean_data_nasterii(self):
        data_nasterii = self.cleaned_data['data_nasterii']
        if data_nasterii.year > 2005:
            raise forms.ValidationError("Trebuie să aveți cel puțin 18 ani.")
        return data_nasterii
    
    def clean_descriere(self):
        # nr cuvinte
        descriere = self.cleaned_data['descriere']    
        cuvinte = re.findall(r'\b\w+\b', descriere)
        if not (5 <= len(cuvinte) <= 100):
            raise forms.ValidationError("Descrierea trebuie sa contină între 5 și 100 de cuvinte.")
        return descriere
    

from django.contrib.auth.forms import AuthenticationForm
#formular de logare
class CustomAuthenticationForm(AuthenticationForm):
    #adauga un camp nou
    ramane_logat = forms.BooleanField(
        required=False,
        initial=False,
        label='Ramaneti logat'
    )

    def clean(self):        
        cleaned_data = super().clean()
        ramane_logat = self.cleaned_data.get('ramane_logat')
        return cleaned_data
    
from django.contrib.auth.forms import PasswordChangeForm

#formular de schimbare parola
class CustomPasswordChangeForm(PasswordChangeForm):
    def clean_new_password1(self):
        password1 = self.cleaned_data.get('new_password1')
        if len(password1) < 10:
            raise forms.ValidationError("Parola trebuie sa aiba macar 10 caractere.")
        return password1
    
# Lab7_Task2
from django import forms
from django import forms
from .models import Promotie, Categorie

class PromotieForm(forms.ModelForm):
    class Meta:
        model = Promotie
        fields = ['nume', 'data_expirare', 'descriere', 'categorii', 'discount']

    subiect = forms.CharField(max_length=100, label='Subiect', required=True)
    durata = forms.IntegerField(min_value=1, label='Durata (zile)')
    categorii = forms.ModelMultipleChoiceField(queryset=Categorie.objects.all(), label='Categorii', required=True)